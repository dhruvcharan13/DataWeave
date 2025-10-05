**DataWeave**

AI-Assisted Data Integration Platform
Seamlessly merge, clean, and validate complex datasets — with transparency, control, and intelligence.

**Inspiration**

DataWeave was born out of a frustration that every data engineer, analyst, or consultant has faced — dealing with messy, inconsistent, and disconnected data sources.

While companies invest heavily in ETL tools and warehouses, the human-in-the-loop experience — where analysts can see, understand, and guide AI-driven transformations — is often missing.
We wanted to build something that feels as intuitive as Notion or PowerApps, powered by Gemini + OpenAI intelligence, with Supabase and cloud storage flexibility.

**What It Does**

DataWeave is an AI-assisted data integration platform that helps organizations merge, clean, and validate messy datasets — without losing control or transparency.

Upload: Users upload folders containing Excel/CSV files and schema definitions.

Infer Relationships: DataWeave automatically identifies table relationships (primary/foreign keys) and generates schema visualizations.

AI-Assisted Mapping: It then maps two different databases or schemas, even when structures differ.

Human Control: Users can validate, adjust, and approve AI mappings and transformations.

Output: Produces clean, unified CSVs/Excels and a new schema file describing the merged data model.

How We Built It

Frontend:

Built with Next.js (React + TailwindCSS + MUI)
Intuitive drag-and-drop uploads, schema visualizer (React Flow), and column mapping interface inspired by PowerApps

Backend:

FastAPI + Pandas for dataset parsing, normalization, and merge operations

AI Layer:

Gemini API (LLM) for semantic schema understanding, column mapping, and data relationship inference

Output:

Merged structured datasets and a new schema definition describing inferred relationships and mappings

Workflow Overview

Upload two databases (source & target) > 
Backend reads and summarizes schema & table metadata > 
LLM infers relationships between tables within each dataset > 
LLM performs cross-database mapping (source → target) > 
User reviews & edits mappings via intuitive UI > 
System merges and exports clean unified CSVs/Excels > 

Screenshots

Upload Datasets		
<img width="1860" height="871" alt="image" src="https://github.com/user-attachments/assets/4447c4ab-3486-4ad4-9b37-0998dd291fe7" />

Schema Visualization
<img width="1848" height="892" alt="image" src="https://github.com/user-attachments/assets/ca2dc1ae-1d6f-4fa3-8b8f-2e9babb78945" />

AI-Assisted Mapping
<img width="1845" height="851" alt="image" src="https://github.com/user-attachments/assets/76744e68-5a04-4616-8d86-00d499cb74f1" />


	
	
