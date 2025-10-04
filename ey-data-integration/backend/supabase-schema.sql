-- EY Data Integration Challenge - Supabase Schema
-- Uploaded files and metadata
CREATE TABLE files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  file_name TEXT,
  file_type TEXT,
  file_size BIGINT,
  file_url TEXT,
  uploaded_at TIMESTAMP DEFAULT NOW()
);

-- Column schemas of each uploaded file
CREATE TABLE schemas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  file_id UUID REFERENCES files(id) ON DELETE CASCADE,
  column_name TEXT,
  data_type TEXT,
  sample_values JSONB,
  null_count INTEGER DEFAULT 0,
  unique_count INTEGER DEFAULT 0
);

-- Detected/suggested relationships between tables
CREATE TABLE relationships (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  file_a UUID REFERENCES files(id) ON DELETE CASCADE,
  column_a TEXT,
  file_b UUID REFERENCES files(id) ON DELETE CASCADE,
  column_b TEXT,
  confidence_score FLOAT,
  relationship_type TEXT, -- 'one_to_one', 'one_to_many', 'many_to_many'
  status TEXT CHECK (status IN ('suggested', 'approved', 'rejected')) DEFAULT 'suggested'
);

-- Mappings between dataset A & B
CREATE TABLE mappings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_file UUID REFERENCES files(id),
  source_column TEXT,
  target_file UUID REFERENCES files(id),
  target_column TEXT,
  transformation TEXT,
  approved BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Data cleaning suggestions
CREATE TABLE cleaning_suggestions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  file_id UUID REFERENCES files(id),
  column_name TEXT,
  suggestion TEXT,
  pandas_code TEXT,
  approved BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Export jobs
CREATE TABLE exports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  schema_file_url TEXT,   -- schema definition file
  folder_url TEXT,        -- folder of exported tables
  status TEXT CHECK (status IN ('pending','ready','failed')) DEFAULT 'pending'
);

-- Track which tables belong to an export
CREATE TABLE export_tables (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  export_id UUID REFERENCES exports(id) ON DELETE CASCADE,
  table_name TEXT,
  file_url TEXT
);

-- Enable Row Level Security
ALTER TABLE files ENABLE ROW LEVEL SECURITY;
ALTER TABLE schemas ENABLE ROW LEVEL SECURITY;
ALTER TABLE relationships ENABLE ROW LEVEL SECURITY;
ALTER TABLE mappings ENABLE ROW LEVEL SECURITY;
ALTER TABLE cleaning_suggestions ENABLE ROW LEVEL SECURITY;
ALTER TABLE exports ENABLE ROW LEVEL SECURITY;
ALTER TABLE export_tables ENABLE ROW LEVEL SECURITY;

-- Create policies for user data isolation
CREATE POLICY "Users can view own files" ON files FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own files" ON files FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own files" ON files FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own files" ON files FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own schemas" ON schemas FOR SELECT USING (
  EXISTS (SELECT 1 FROM files WHERE files.id = schemas.file_id AND files.user_id = auth.uid())
);

CREATE POLICY "Users can view own relationships" ON relationships FOR SELECT USING (
  EXISTS (SELECT 1 FROM files WHERE files.id = relationships.file_a AND files.user_id = auth.uid())
);

CREATE POLICY "Users can view own mappings" ON mappings FOR SELECT USING (
  EXISTS (SELECT 1 FROM files WHERE files.id = mappings.source_file AND files.user_id = auth.uid())
);

CREATE POLICY "Users can view own cleaning suggestions" ON cleaning_suggestions FOR SELECT USING (
  EXISTS (SELECT 1 FROM files WHERE files.id = cleaning_suggestions.file_id AND files.user_id = auth.uid())
);

CREATE POLICY "Users can view own exports" ON exports FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own exports" ON exports FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own exports" ON exports FOR UPDATE USING (auth.uid() = user_id);
