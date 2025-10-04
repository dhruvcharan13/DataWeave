from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pandas as pd
import json
import os
import uuid
from datetime import datetime
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
import google.generativeai as genai
from sqlalchemy import create_engine, text, MetaData, Table, Column, String, Integer, Float, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
import psycopg2
from psycopg2.extras import RealDictCursor
from schema_analyzer import SchemaAnalyzer

app = FastAPI(title="EY Data Integration API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# PostgreSQL connection for direct database operations
# Note: For Supabase, we'll use the Supabase client instead of direct PostgreSQL connection
# This avoids connection string issues and uses the proper Supabase API
engine = None  # We'll use Supabase client for database operations

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here"))
model = genai.GenerativeModel('gemini-pro')

# Pydantic models
class FileUploadResponse(BaseModel):
    file_id: str
    file_name: str
    file_type: str
    columns: List[str]
    row_count: int
    sample_data: List[Dict[str, Any]]

class RelationshipSuggestion(BaseModel):
    file_a: str
    column_a: str
    file_b: str
    column_b: str
    confidence_score: float
    relationship_type: str

class SchemaAnalysis(BaseModel):
    table_name: str
    columns: List[Dict[str, Any]]
    row_count: int
    relationships: List[Dict[str, Any]]
    data_quality: Dict[str, Any]

class CrossBankMapping(BaseModel):
    bank1_table: str
    bank1_column: str
    bank2_table: str
    bank2_column: str
    confidence_score: float
    mapping_type: str
    transformation_needed: bool

# Utility functions
def analyze_file_schema(file_path: str, file_type: str) -> Dict[str, Any]:
    """Analyze file and extract schema information"""
    try:
        if file_type == 'csv':
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        schema = {
            'columns': df.columns.tolist(),
            'row_count': len(df),
            'data_types': df.dtypes.to_dict(),
            'null_counts': df.isnull().sum().to_dict(),
            'unique_counts': df.nunique().to_dict(),
            'sample_data': df.head(5).to_dict('records')
        }

        return schema
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error analyzing file: {str(e)}")

def create_postgresql_table(df: pd.DataFrame, table_name: str, file_id: str) -> str:
    """Create PostgreSQL table from DataFrame with proper schema using Supabase"""
    try:
        # Clean table name
        clean_table_name = f"bank_data_{file_id}_{table_name.lower().replace(' ', '_').replace('/', '_')}"
        
        # Convert DataFrame to records for Supabase insertion
        records = df.to_dict('records')
        
        # Add metadata to each record
        for record in records:
            record['file_id'] = file_id
            record['created_at'] = datetime.now().isoformat()
        
        # Insert data into Supabase (this will create the table automatically)
        result = supabase.table(clean_table_name).insert(records).execute()
        
        return clean_table_name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating PostgreSQL table: {str(e)}")

def analyze_postgresql_schema(table_name: str) -> Dict[str, Any]:
    """Analyze PostgreSQL table schema and relationships using Supabase"""
    try:
        # Get sample data from Supabase
        result = supabase.table(table_name).select("*").limit(5).execute()
        sample_data = result.data if result.data else []
        
        # Get row count
        count_result = supabase.table(table_name).select("*", count="exact").execute()
        row_count = count_result.count if count_result.count else 0
        
        # Analyze columns from sample data
        columns = []
        if sample_data:
            for key in sample_data[0].keys():
                # Determine data type from sample values
                sample_value = sample_data[0][key]
                if isinstance(sample_value, str):
                    data_type = "text"
                elif isinstance(sample_value, (int, float)):
                    data_type = "numeric"
                elif isinstance(sample_value, bool):
                    data_type = "boolean"
                else:
                    data_type = "text"
                
                columns.append({
                    'column_name': key,
                    'data_type': data_type,
                    'is_nullable': True,
                    'column_default': None
                })
        
        return {
            'table_name': table_name,
            'columns': columns,
            'foreign_keys': [],  # Will be determined by AI analysis
            'row_count': row_count,
            'sample_data': sample_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing PostgreSQL schema: {str(e)}")

def get_ai_schema_analysis(schema_data: Dict[str, Any]) -> Dict[str, Any]:
    """Use Gemini AI to analyze schema and suggest relationships"""
    try:
        prompt = f"""
        Analyze this banking database schema and provide insights:
        
        Table: {schema_data['table_name']}
        Columns: {schema_data['columns']}
        Row Count: {schema_data['row_count']}
        Sample Data: {schema_data['sample_data'][:3]}
        
        Please provide:
        1. Primary key identification
        2. Foreign key relationships
        3. Data quality issues
        4. Business logic insights
        5. Potential relationships with other banking tables
        
        Respond in JSON format with the following structure:
        {{
            "primary_key": "column_name",
            "foreign_keys": [{{"column": "col_name", "references": "table.column"}}],
            "data_quality": {{"issues": [], "recommendations": []}},
            "business_insights": ["insight1", "insight2"],
            "potential_relationships": [{{"column": "col_name", "relationship_type": "type"}}]
        }}
        """
        
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        return {"error": f"AI analysis failed: {str(e)}"}

def get_cross_bank_mapping_analysis(bank1_schemas: List[Dict], bank2_schemas: List[Dict]) -> Dict[str, Any]:
    """Use Gemini AI to suggest cross-bank field mappings"""
    try:
        prompt = f"""
        Analyze these two banking schemas and suggest field mappings for data integration:
        
        BANK 1 SCHEMAS:
        {json.dumps(bank1_schemas, indent=2)}
        
        BANK 2 SCHEMAS:
        {json.dumps(bank2_schemas, indent=2)}
        
        Please provide cross-bank field mappings with confidence scores:
        
        Respond in JSON format:
        {{
            "customer_mappings": [
                {{"bank1_table": "table", "bank1_field": "field", "bank2_table": "table", "bank2_field": "field", "confidence": 0.95, "transformation": "direct"}}
            ],
            "account_mappings": [...],
            "transaction_mappings": [...],
            "merge_strategy": "recommended approach",
            "data_quality_considerations": ["consideration1", "consideration2"]
        }}
        """
        
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        return {"error": f"Cross-bank mapping analysis failed: {str(e)}"}

# API Endpoints
@app.get("/")
async def root():
    return {"message": "EY Data Integration API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload and analyze CSV/Excel files with PostgreSQL processing"""
    try:
        uploaded_files = []
        postgresql_tables = []

        for file in files:
            # Save file temporarily
            file_id = str(uuid.uuid4())
            file_path = f"temp/{file_id}_{file.filename}"
            os.makedirs("temp", exist_ok=True)

            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)

            # Analyze file
            file_type = 'csv' if file.filename.endswith('.csv') else 'excel'
            schema = analyze_file_schema(file_path, file_type)

            # Load data into DataFrame
            if file_type == 'csv':
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)

            # Create PostgreSQL table
            table_name = file.filename.replace('.csv', '').replace('.xlsx', '').replace('.xls', '')
            postgresql_table = create_postgresql_table(df, table_name, file_id)
            postgresql_tables.append(postgresql_table)

            # Analyze PostgreSQL schema
            pg_schema = analyze_postgresql_schema(postgresql_table)

            # Get AI analysis
            ai_analysis = get_ai_schema_analysis(pg_schema)

            # Store in Supabase
            file_record = {
                'id': file_id,
                'file_name': file.filename,
                'file_type': file_type,
                'file_size': len(content),
                'postgresql_table': postgresql_table,
                'uploaded_at': datetime.now().isoformat()
            }

            # Insert file record
            supabase.table('files').insert(file_record).execute()

            # Insert schema records with AI insights
            schema_records = []
            for col in schema['columns']:
                schema_records.append({
                    'file_id': file_id,
                    'column_name': col,
                    'data_type': str(schema['data_types'][col]),
                    'sample_values': schema['sample_data'][:3],
                    'null_count': schema['null_counts'][col],
                    'unique_count': schema['unique_counts'][col],
                    'ai_analysis': ai_analysis.get('potential_relationships', [])
                })

            supabase.table('schemas').insert(schema_records).execute()

            uploaded_files.append(FileUploadResponse(
                file_id=file_id,
                file_name=file.filename,
                file_type=file_type,
                columns=schema['columns'],
                row_count=schema['row_count'],
                sample_data=schema['sample_data']
            ))

            # Clean up temp file
            os.remove(file_path)

        return {
            "files": uploaded_files,
            "postgresql_tables": postgresql_tables,
            "message": "Files uploaded and processed into PostgreSQL successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files")
async def get_files():
    """Get all uploaded files"""
    try:
        result = supabase.table('files').select('*').execute()
        return {"files": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-bank-schemas")
async def analyze_bank_schemas():
    """Analyze Bank 1 and Bank 2 schemas for relationships and mappings"""
    try:
        # Load the analysis results
        with open('bank_schema_analysis.json', 'r') as f:
            analysis = json.load(f)
        
        # Store relationships in Supabase
        for rel in analysis['relationships']:
            supabase.table('relationships').insert({
                'file_a': rel['source_table'],
                'column_a': rel['source_column'],
                'file_b': rel['target_table'],
                'column_b': rel['target_column'],
                'confidence_score': 0.9,  # High confidence for internal relationships
                'relationship_type': rel['relationship_type'],
                'status': 'suggested'
            }).execute()
        
        # Store mappings in Supabase
        for mapping in analysis['cross_bank_mappings']:
            supabase.table('mappings').insert({
                'source_file': mapping['bank1_table'],
                'source_column': mapping['bank1_column'],
                'target_file': mapping['bank2_table'],
                'target_column': mapping['bank2_column'],
                'transformation': 'direct',
                'approved': False
            }).execute()
        
        return {
            "message": "Bank schema analysis completed",
            "relationships_found": len(analysis['relationships']),
            "mappings_found": len(analysis['cross_bank_mappings']),
            "analysis": analysis
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bank-analysis")
async def get_bank_analysis():
    """Get bank schema analysis results"""
    try:
        with open('bank_schema_analysis.json', 'r') as f:
            analysis = json.load(f)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-cross-bank-mapping")
async def analyze_cross_bank_mapping():
    """Analyze cross-bank field mappings using AI"""
    try:
        # Get all uploaded files
        files_result = supabase.table('files').select('*').execute()
        files = files_result.data

        # Separate Bank 1 and Bank 2 files
        bank1_files = [f for f in files if 'Bank1' in f['file_name']]
        bank2_files = [f for f in files if 'Bank2' in f['file_name']]

        if not bank1_files or not bank2_files:
            raise HTTPException(status_code=400, detail="Both Bank 1 and Bank 2 files are required")

        # Get schemas for each bank
        bank1_schemas = []
        bank2_schemas = []

        for file in bank1_files:
            if file.get('postgresql_table'):
                schema = analyze_postgresql_schema(file['postgresql_table'])
                bank1_schemas.append(schema)

        for file in bank2_files:
            if file.get('postgresql_table'):
                schema = analyze_postgresql_schema(file['postgresql_table'])
                bank2_schemas.append(schema)

        # Get AI-powered cross-bank mapping analysis
        ai_mapping = get_cross_bank_mapping_analysis(bank1_schemas, bank2_schemas)

        # Store mapping suggestions in Supabase
        if 'customer_mappings' in ai_mapping:
            for mapping in ai_mapping['customer_mappings']:
                supabase.table('mappings').insert({
                    'source_file': mapping['bank1_table'],
                    'source_column': mapping['bank1_field'],
                    'target_file': mapping['bank2_table'],
                    'target_column': mapping['bank2_field'],
                    'transformation': mapping.get('transformation', 'direct'),
                    'confidence_score': mapping.get('confidence', 0.8),
                    'approved': False
                }).execute()

        return {
            "message": "Cross-bank mapping analysis completed",
            "bank1_schemas": len(bank1_schemas),
            "bank2_schemas": len(bank2_schemas),
            "ai_mapping_analysis": ai_mapping
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/postgresql-tables")
async def get_postgresql_tables():
    """Get all PostgreSQL tables created from uploaded files"""
    try:
        # Get all files with PostgreSQL tables
        files_result = supabase.table('files').select('*').execute()
        files = files_result.data
        
        tables = []
        for file in files:
            if file.get('postgresql_table'):
                # Get basic info about the table
                table_name = file['postgresql_table']
                try:
                    # Get a sample to determine column count
                    sample_result = supabase.table(table_name).select("*").limit(1).execute()
                    if sample_result.data:
                        column_count = len(sample_result.data[0].keys())
                    else:
                        column_count = 0
                    
                    tables.append({
                        "table_name": table_name,
                        "file_name": file['file_name'],
                        "column_count": column_count,
                        "created_at": file['uploaded_at']
                    })
                except:
                    # Table might not exist yet
                    continue
            
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/table-schema/{table_name}")
async def get_table_schema(table_name: str):
    """Get detailed schema information for a specific PostgreSQL table"""
    try:
        schema_info = analyze_postgresql_schema(table_name)
        ai_analysis = get_ai_schema_analysis(schema_info)
        
        return {
            "table_name": table_name,
            "schema": schema_info,
            "ai_analysis": ai_analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/merge-datasets")
async def merge_datasets(merge_config: Dict[str, Any]):
    """Merge datasets based on AI-suggested mappings"""
    try:
        # This would implement the actual data merging logic
        # For now, return a placeholder response
        return {
            "message": "Dataset merging functionality will be implemented",
            "merge_config": merge_config,
            "status": "pending"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/comprehensive-analysis")
async def run_comprehensive_analysis():
    """Run comprehensive bank schema analysis and get AI recommendations"""
    try:
        # Initialize schema analyzer
        analyzer = SchemaAnalyzer()
        
        # Run full analysis
        analysis_results = analyzer.run_full_analysis()
        
        # Get Gemini AI analysis if API key is available
        gemini_analysis = None
        if os.getenv("GEMINI_API_KEY") and os.getenv("GEMINI_API_KEY") != "your_gemini_api_key_here":
            try:
                response = model.generate_content(analysis_results['gemini_prompt'])
                gemini_analysis = json.loads(response.text)
            except Exception as e:
                gemini_analysis = {"error": f"Gemini analysis failed: {str(e)}"}
        
        return {
            "message": "Comprehensive analysis completed",
            "analysis_results": analysis_results,
            "gemini_analysis": gemini_analysis,
            "summary": {
                "bank1_tables": analysis_results['bank1']['summary']['total_tables'],
                "bank1_fields": analysis_results['bank1']['summary']['total_fields'],
                "bank2_tables": analysis_results['bank2']['summary']['total_tables'],
                "bank2_fields": analysis_results['bank2']['summary']['total_fields'],
                "total_relationships": len(analysis_results['bank1']['relationships']) + len(analysis_results['bank2']['relationships'])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analysis-results")
async def get_analysis_results():
    """Get the latest comprehensive analysis results"""
    try:
        if os.path.exists('comprehensive_bank_analysis.json'):
            with open('comprehensive_bank_analysis.json', 'r') as f:
                results = json.load(f)
            return results
        else:
            return {"message": "No analysis results found. Run /comprehensive-analysis first."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
