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


# Add the server directory to the Python path
sys.path.append(str(Path(__file__).parent))

# Initialize FastAPI
app = FastAPI()

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

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


import uuid
from fastapi import Form

UPLOAD_BASE_DIR = "user_uploads"

# Create base upload directory if it doesn't exist
os.makedirs(UPLOAD_BASE_DIR, exist_ok=True)

@app.post("/api/upload-files")
async def upload_files(
    source_files: list[UploadFile] = File(default=[]),
    target_files: list[UploadFile] = File(default=[]),
    user_id: str = Form(None)
):
    try:
        print(f"Received upload request with {len(source_files)} source files and {len(target_files)} target files")
        
        # Generate a user ID if not provided
        if not user_id or not user_id.strip():
            # return 404
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": "User ID is required"}
            )
            
        # Create user directories
        user_dir = os.path.join(UPLOAD_BASE_DIR, user_id)
        source_dir = os.path.join(user_dir, "source")
        target_dir = os.path.join(user_dir, "target")
        
        os.makedirs(source_dir, exist_ok=True)
        os.makedirs(target_dir, exist_ok=True)
        
        saved_files = {"source_files": [], "target_files": [], "user_id": user_id}
        
        # Save source files
        for file in source_files:
            if not file.filename or not file.filename.strip():
                continue
                
            file_path = os.path.join(source_dir, os.path.basename(file.filename))
            
            # Skip if file already exists and has content
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                saved_files["source_files"].append({
                    "filename": os.path.basename(file.filename),
                    "status": "skipped",
                    "reason": "File already exists",
                    "path": file_path,
                    "size": os.path.getsize(file_path)
                })
                continue
                
            try:
                # Read file content once
                contents = await file.read()
                if not contents:
                    raise ValueError("File is empty")
                    
                # Write to file
                with open(file_path, "wb") as buffer:
                    buffer.write(contents)
                    
                saved_files["source_files"].append({
                    "filename": os.path.basename(file.filename),
                    "status": "uploaded",
                    "path": file_path,
                    "size": len(contents)
                })
            except Exception as e:
                print(f"Error processing {file.filename}: {str(e)}")
                saved_files["source_files"].append({
                    "filename": os.path.basename(file.filename) if file.filename else "unknown",
                    "status": "error",
                    "reason": str(e)
                })
            
        # Save target files
        for file in target_files:
            if not file.filename or not file.filename.strip():
                continue
                
            file_path = os.path.join(target_dir, os.path.basename(file.filename))
            
            # Skip if file already exists and has content
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                saved_files["target_files"].append({
                    "filename": os.path.basename(file.filename),
                    "status": "skipped",
                    "reason": "File already exists",
                    "path": file_path,
                    "size": os.path.getsize(file_path)
                })
                continue
                
            try:
                # Read file content once
                contents = await file.read()
                if not contents:
                    raise ValueError("File is empty")
                    
                # Write to file
                with open(file_path, "wb") as buffer:
                    buffer.write(contents)
                    
                saved_files["target_files"].append({
                    "filename": os.path.basename(file.filename),
                    "status": "uploaded",
                    "path": file_path,
                "size": len(contents)
            })
            except Exception as e:
                print(f"Error processing {file.filename}: {str(e)}")
                saved_files["target_files"].append({
                    "filename": os.path.basename(file.filename) if file.filename else "unknown",
                    "status": "error",
                    "reason": str(e)
                })
            
        from schema_detector import process_directory
        
        # Process source and target directories
        source_dir = os.path.join(user_dir, "source")
        target_dir = os.path.join(user_dir, "target")
        
        # Get schema and file information
        source_info = process_directory(source_dir)
        target_info = process_directory(target_dir)
        
        # Add schema and file info to the response
        saved_files['schema_info'] = {
            'source': source_info,
            'target': target_info
        }
        
        return saved_files
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Failed to process files: {str(e)}"}
        )
    

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)