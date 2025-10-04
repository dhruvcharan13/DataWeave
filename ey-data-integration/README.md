# EY Data Integration MVP

A hackathon MVP for the EY Data Integration Challenge at Hack the Valley.

## Project Structure

```
ey-data-integration/
├── frontend/          # Next.js React app
├── backend/           # FastAPI Python backend
│   ├── main.py        # FastAPI application
│   ├── config.py      # Configuration
│   ├── requirements.txt
│   ├── supabase-schema.sql
│   └── setup.py       # Setup script
└── README.md
```

## Quick Start

### 1. Backend Setup (FastAPI + Supabase)
```bash
cd backend
python setup.py
# Update .env file with your Supabase credentials
# Run supabase-schema.sql in your Supabase dashboard
python main.py
```
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### 2. Frontend Setup (Next.js)
```bash
cd frontend
npm run dev
```
- App: http://localhost:3002

## Backend Features

- ✅ **File Upload**: CSV/Excel file processing with Pandas
- ✅ **Schema Analysis**: Automatic column detection and data type inference
- ✅ **Supabase Integration**: Database storage for files, schemas, relationships
- ✅ **API Endpoints**: RESTful API for frontend communication

## Database Schema

The backend uses Supabase with the following tables:
- `files` - Uploaded file metadata
- `schemas` - Column schemas for each file
- `relationships` - Detected relationships between tables
- `mappings` - User-defined data mappings
- `cleaning_suggestions` - AI-suggested data cleaning
- `exports` - Export job tracking

## Development Approach

We'll build this step by step:

1. ✅ **Foundation**: Basic Next.js + FastAPI setup
2. ✅ **Backend**: FastAPI + Supabase + file processing
3. 🔄 **Step 1**: File upload component
4. 🔄 **Step 2**: Schema analysis UI
5. 🔄 **Step 3**: Relationship detection
6. 🔄 **Step 4**: Mapping interface
7. 🔄 **Step 5**: Export functionality

## Current Status

- ✅ Basic project structure
- ✅ Frontend foundation (Next.js + Tailwind)
- ✅ Backend with Supabase integration
- ✅ File upload and schema analysis API
- 🔄 Ready for frontend integration
