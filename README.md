# 🏆 DataWeave — Winner of the EY Data Integration Challenge

**An AI-powered data integration and lineage engine for auditable, explainable, and compliant ETL workflows.**

DataWeave redefines how organizations merge heterogeneous datasets by combining **LLM reasoning**, **human-in-the-loop validation**, and **enterprise-grade auditability**.  
Built during the **EY Data Integration Challenge** @ Hack The Valley X, the system demonstrates what next-generation ETL should look like — transparent, traceable, and intelligent.

---

## Overview

DataWeave allows users to:

- Upload and analyze heterogeneous financial datasets  
- Automatically align relational databases across sources using Gemini-assisted metadata reasoning  
- Visually map and merge records with confidence scoring, human review, and full lineage tracking  
- Export clean, API-ready datasets and audit reports  

The platform consists of three core modules:
1. **Upload Page** — Upload and validate source datasets

   <img width="1440" height="811" alt="Screenshot 2025-10-27 at 12 51 42 AM" src="https://github.com/user-attachments/assets/b4fe509d-a1e2-4abe-a340-245a0bd631ba" />
2. **Schema Visualizer** — Inspect structure, compare schemas, and correct mismatched relationships

   <img width="1440" height="811" alt="Screenshot 2025-10-27 at 12 56 36 AM" src="https://github.com/user-attachments/assets/edec24c3-5aa9-43d2-ae76-b4548c3cc019" />
3. **Mapping Page** — Approve or edit AI-suggested mappings and export clean merges
   
   <img width="1440" height="811" alt="Screenshot 2025-10-27 at 1 08 43 AM" src="https://github.com/user-attachments/assets/58d4c95a-edb5-4eb9-9d27-648ddc5025c5" />

---

## Key Features

### 1. Data Lineage & Traceability  
> “Can we prove where every merged value came from?”

Every change made to the data in DataWeave is fully traceable:

- Shows **source dataset**, **applied transformation**, **confidence score**, and **final output field**  

---

## 2. Human-in-the-Loop Review System  
> “The AI suggests, the analyst approves.”

- Analysts can check and **edit** AI-generated mappings
- Every action updates the mapping JSON and informs future model suggestions
- All approvals and overrides are logged.

---

## 3. Secure Data Cleaning
> “Clean the data without letting sensitive data leak.”

- Automatically standardizes formats using **regex + LLM classification** (emails, SSNs, account numbers)  
- Uses secure algorithms to clean data without sending important financial data to external LLMs

---

## 4. Automated Mapping Explanation (via AI)  
> “Explain why you matched these fields.”

- Uses **Gemini** to generate rationales for every mapping:
  > “These columns share similar naming, type, and refer to the same concept (Customer ID).”  
- Displays **confidence scores** and **plain-English reasoning** alongside each mapping  

---

## 5. Reconciliation Report  
> “What changed after merging?”

Automatically generates an **detailed report** after every merge, including:

- Number of rows merged  
- **% matched / unmatched**  
- **Confidence distributions**  
- **Validation summaries**

---

## Tech Stack
Frontend:	React, TypeScript, Next, MUI
Backend:	FastAPI, Python, Supabase, PostgreSQL
AI & Data Processing:	Gemini API, Pandas

## Setup Instructions

Clone the repo
- git clone https://github.com/yourusername/dataweave.git
- cd dataweave

Backend setup
- cd server
- pip install -r requirements.txt
- python app.py

Frontend setup
- cd client
- npm install
- npm run dev
