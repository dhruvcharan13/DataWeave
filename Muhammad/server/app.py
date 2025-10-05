from schema_json import extract_schema_from_dir
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import uvicorn
from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
import uuid
from fastapi import Form
import pandas as pd
import sys
from pathlib import Path
from gemini_service import generate_text
from schema_detector import process_directory
import uuid
from fastapi import Form
import re
import json

from prompts import generate_relationship_prompt, generate_mapping_prompt
from starlette.concurrency import run_in_threadpool
from newscript import BankDataMerger
# Add the server directory to the Python path
sys.path.append(str(Path(__file__).parent))

# Initialize FastAPI
app = FastAPI()

UPLOAD_BASE_DIR = "user_uploads"
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    try:
        response = await generate_text("Tell me a joke about AI")
    except Exception as e:
        return {"message": str(e)}
    return {"message": response}

# Create base upload directory if it doesn't exist
os.makedirs(UPLOAD_BASE_DIR, exist_ok=True)

@app.post("/api/upload-files")
async def upload_files(
    source_files: list[UploadFile] = File(default=[]),
    target_files: list[UploadFile] = File(default=[]),
    user_id: str = Form(None)
):
    
    try:
        if not user_id or not user_id.strip():
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "User ID is required"}
            )
            
        # Create user directories
        user_dir = os.path.join(UPLOAD_BASE_DIR, user_id)
        source_dir = os.path.join(user_dir, "source")
        target_dir = os.path.join(user_dir, "target")

        # if os.path.exists(user_dir):
        #     import shutil
        #     shutil.rmtree(user_dir)
        
        # Remove existing directories if they exist
        if os.path.exists(user_dir):
            import shutil
            shutil.rmtree(user_dir)
            
        # Create fresh directories
        os.makedirs(source_dir, exist_ok=True)
        os.makedirs(target_dir, exist_ok=True)
        
        # Track errors
        errors = []
        
        # Save source files
        for file in source_files:
            if not file.filename or not file.filename.strip():
                continue
                
            file_path = os.path.join(source_dir, os.path.basename(file.filename))
            
            try:
                contents = await file.read()
                if not contents:
                    raise ValueError("File is empty")
                    
                if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                    with open(file_path, "wb") as buffer:
                        buffer.write(contents)
            except Exception as e:
                error_msg = f"Error processing source file {file.filename}: {str(e)}"
                print(error_msg)
                errors.append(error_msg)
        
        # Save target files
        for file in target_files:
            if not file.filename or not file.filename.strip():
                continue
                
            file_path = os.path.join(target_dir, os.path.basename(file.filename))
            
            try:
                contents = await file.read()
                if not contents:
                    raise ValueError("File is empty")
                    
                if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                    with open(file_path, "wb") as buffer:
                        buffer.write(contents)
            except Exception as e:
                error_msg = f"Error processing target file {file.filename}: {str(e)}"
                print(error_msg)
                errors.append(error_msg)
        
        # If there were any errors, return them immediately
        if errors:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"errors": errors}
            )
        
        # Process directories to get schema info
        try:
            source_info = extract_schema_from_dir(source_dir)
            target_info = extract_schema_from_dir(target_dir)
            
            schema_prompt = generate_relationship_prompt(source_info, target_info)
            # Generate schema analysis
            schema_analysis = await generate_text(schema_prompt)
            
            # Extract JSON from response
            json_match = re.search(r'```(?:json)?\s*({[\s\S]*?})\s*```', schema_analysis)
            if json_match:
                schema_analysis = json.loads(json_match.group(1))
            else:
                try:
                    schema_analysis = json.loads(schema_analysis)
                except json.JSONDecodeError:
                    raise ValueError("Failed to parse schema analysis")
            
            return {"schema_analysis": schema_analysis}
            
        except Exception as e:
            print(f"Error during schema analysis: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": f"Schema analysis failed: {str(e)}"}
            )
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"An unexpected error occurred: {str(e)}"}
        )


@app.post("/api/generate-suggested-mapping")
async def generate_suggested_mapping(schema_analysis: dict):
    try:
        source_database = schema_analysis["source"]
        target_database = schema_analysis["target"]

        mapping_prompt = generate_mapping_prompt(source_database, target_database)

        mapping_response = await generate_text(mapping_prompt)

        json_match = re.search(r'```(?:json)?\s*({[\s\S]*?})\s*```', mapping_response)
        if json_match:
            mapping_response = json.loads(json_match.group(1))
        else:
            try:
                mapping_response = json.loads(mapping_response)
            except json.JSONDecodeError:
                raise ValueError("Failed to parse mapping response")
        
        return {"mapping_response": mapping_response}
    except Exception as e:
        print(f"Error during suggested mapping generation: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Suggested mapping generation failed: {str(e)}"}
        )
        
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

# New endpoint to run the merge process and save outputs under DataWeave/output
@app.post("/api/run-merge")
async def run_merge(mapping_path: str | None = None):
    try:
        # Determine repository root: .../DataWeave
        repo_root = Path(__file__).resolve().parents[2]

        # Default directories
        bank1_dir = str(repo_root / "Bank 1 Data")
        bank2_dir = str(repo_root / "Bank 2 Data")
        output_dir = str(repo_root / "output")

        os.makedirs(output_dir, exist_ok=True)

        # Determine mapping file path
        candidate_paths = []
        if mapping_path:
            candidate_paths.append(Path(mapping_path))
        # Workspace root mapping_output.json (commonly used during development)
        candidate_paths.append(Path("/Users/dhruvcharan/Downloads/Archive/mapping_output.json"))
        # Server-local mapping.json fallback
        candidate_paths.append(Path(__file__).parent / "mapping.json")

        mapping_file = None
        for p in candidate_paths:
            if p and p.exists():
                mapping_file = str(p)
                break

        if not mapping_file:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "No mapping file found. Provide mapping_path or place mapping.json next to server."}
            )

        merger = BankDataMerger(mapping_file, bank1_dir, bank2_dir, output_dir)
        await run_in_threadpool(merger.run_merge)

        # List generated files
        files = sorted(os.listdir(output_dir)) if os.path.isdir(output_dir) else []
        return {"output_dir": output_dir, "files": files}

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Merge failed: {str(e)}"}
        )