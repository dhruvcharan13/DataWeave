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

# API Endpoints
@app.get("/")
async def root():
    return {"message": "EY Data Integration API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload and analyze CSV/Excel files"""
    try:
        uploaded_files = []
        
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
            
            # Store in Supabase
            file_record = {
                'id': file_id,
                'file_name': file.filename,
                'file_type': file_type,
                'file_size': len(content),
                'file_url': file_path,
                'uploaded_at': datetime.now().isoformat()
            }
            
            # Insert file record
            supabase.table('files').insert(file_record).execute()
            
            # Insert schema records
            schema_records = []
            for col in schema['columns']:
                schema_records.append({
                    'file_id': file_id,
                    'column_name': col,
                    'data_type': str(schema['data_types'][col]),
                    'sample_values': schema['sample_data'][:3],
                    'null_count': schema['null_counts'][col],
                    'unique_count': schema['unique_counts'][col]
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
        
        return {"files": uploaded_files}
    
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
