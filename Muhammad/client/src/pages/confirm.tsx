import React, { useState, useEffect } from "react";
import { Box, Typography, Container, Button, CircularProgress, Alert, Paper } from "@mui/material";
import { useRouter } from "next/router";
import { getFiles } from "../store/fileStore";

interface SchemaPrompt {
  bank_name: string;
  prompt: string;
}

export default function Confirm() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [prompts, setPrompts] = useState<SchemaPrompt[]>([]);
  const [uploadStatus, setUploadStatus] = useState<string>("");
  const [sourceFiles, setSourceFiles] = useState<File[]>([]);
  const [targetFiles, setTargetFiles] = useState<File[]>([]);

  const handleSchemaAnalysis = async () => {
    setLoading(true);
    setError(null);
    setUploadStatus("Starting schema analysis...");

    try {
      // Test basic connectivity first
      setUploadStatus("Testing backend connection...");
      console.log('Testing backend connection...');
      
      try {
        const testResponse = await fetch('http://localhost:8000/test');
        const testResult = await testResponse.json();
        console.log('Backend test successful:', testResult);
      } catch (testError) {
        console.error('Backend test failed:', testError);
        throw new Error(`Backend connection failed: ${testError.message}`);
      }
      
      // Step 1: Upload files to backend
      setUploadStatus("Uploading files to Supabase...");
      
      // Check if we have files
      if (sourceFiles.length === 0 && targetFiles.length === 0) {
        throw new Error('No files found. Please upload files first.');
      }
      
      // Create FormData with all files
      const formData = new FormData();
      
      console.log('Source files:', sourceFiles);
      console.log('Target files:', targetFiles);
      console.log('Source files length:', sourceFiles.length);
      console.log('Target files length:', targetFiles.length);
      
      // Add source files
      sourceFiles.forEach((file, index) => {
        console.log('Adding source file:', file.name, file);
        formData.append('files', file, file.name);
      });
      
      // Add target files
      targetFiles.forEach((file, index) => {
        console.log('Adding target file:', file.name, file);
        formData.append('files', file, file.name);
      });

      console.log('Sending upload request to backend...');
      console.log('FormData entries:');
      for (let [key, value] of formData.entries()) {
        console.log(key, value);
      }
      
              const uploadResponse = await fetch('http://localhost:8000/upload-files', {
                method: 'POST',
                body: formData
              });

      console.log('Upload response status:', uploadResponse.status);
      console.log('Upload response ok:', uploadResponse.ok);

      if (!uploadResponse.ok) {
        const errorText = await uploadResponse.text();
        console.error('Upload failed:', errorText);
        throw new Error(`Failed to upload files: ${uploadResponse.status} - ${errorText}`);
      }

      const uploadResult = await uploadResponse.json();
      console.log('Upload result:', uploadResult);
      setUploadStatus(`Files uploaded: ${uploadResult.message}`);

      // Step 2: Generate schema prompts
      setUploadStatus("Generating schema prompts...");
      console.log('Sending prompt generation request...');
      const promptResponse = await fetch('http://localhost:8000/generate-schema-prompts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          schema_files: uploadResult.schema_files || []
        })
      });

      console.log('Prompt response status:', promptResponse.status);
      console.log('Prompt response ok:', promptResponse.ok);

      if (!promptResponse.ok) {
        const errorText = await promptResponse.text();
        console.error('Prompt generation failed:', errorText);
        throw new Error(`Failed to generate prompts: ${promptResponse.status} - ${errorText}`);
      }

      const promptResult = await promptResponse.json();
      console.log('Prompt result:', promptResult);
      setPrompts(promptResult.prompts);
      setUploadStatus("Schema analysis complete!");

    } catch (err) {
      console.error('Error in handleSchemaAnalysis:', err);
      setError(err instanceof Error ? err.message : 'An error occurred');
      setUploadStatus("");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Get files from file store
    const { sourceFiles: storedSourceFiles, targetFiles: storedTargetFiles } = getFiles();
    console.log('Retrieved files from store:', { storedSourceFiles, storedTargetFiles });
    setSourceFiles(storedSourceFiles);
    setTargetFiles(storedTargetFiles);
  }, []);

  useEffect(() => {
    // Auto-start the process when files are loaded
    if (sourceFiles.length > 0 || targetFiles.length > 0) {
      handleSchemaAnalysis();
    }
  }, [sourceFiles, targetFiles]);

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Box sx={{ textAlign: "center", mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Schema Analysis
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Analyzing uploaded database schemas and generating AI prompts
        </Typography>
      </Box>

      {loading && (
        <Box sx={{ textAlign: "center", my: 4 }}>
          <CircularProgress />
          <Typography variant="body1" sx={{ mt: 2 }}>
            {uploadStatus}
          </Typography>
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {prompts.length > 0 && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" gutterBottom>
            Generated Schema Prompts
          </Typography>
          {prompts.map((prompt, index) => (
            <Paper key={index} sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                {prompt.bank_name} Schema Prompt
              </Typography>
              <Box
                sx={{
                  bgcolor: "background.paper",
                  p: 2,
                  borderRadius: 1,
                  border: "1px solid",
                  borderColor: "divider",
                  maxHeight: "400px",
                  overflow: "auto",
                  fontFamily: "monospace",
                  fontSize: "0.875rem",
                  whiteSpace: "pre-wrap"
                }}
              >
                {prompt.prompt}
              </Box>
            </Paper>
          ))}
        </Box>
      )}

      <Box sx={{ mt: 4, textAlign: "center" }}>
        <Button
          variant="outlined"
          onClick={() => router.push("/")}
          sx={{ mr: 2 }}
        >
          Back to Upload
        </Button>
        {prompts.length > 0 && (
          <Button
            variant="contained"
            onClick={() => {
              // Next step: Send prompts to Gemini
              console.log("Next: Send prompts to Gemini for analysis");
            }}
          >
            Analyze with AI
          </Button>
        )}
      </Box>
    </Container>
  );
}
