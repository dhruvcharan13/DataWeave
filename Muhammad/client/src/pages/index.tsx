import React, { useState } from "react";
import { Box, Typography, Button, CircularProgress, Container } from "@mui/material";
import ExcelFileDropzone, {
  FileWithPreview,
} from "../components/excelFileDropzone";
import router from "next/router";
import { uploadFiles } from "../utils/api";

export default function Home() {
  const [sourceDb, setSourceDb] = useState<FileWithPreview[]>([]);
  const [targetDb, setTargetDb] = useState<FileWithPreview[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const isConfirmDisabled = sourceDb.length === 0 || targetDb.length === 0 || isUploading;

  React.useEffect(() => {
    console.log(sourceDb, targetDb);
  }, [sourceDb, targetDb]);

  return (
    <Container maxWidth="lg" sx={{ my: 2 }}>
      <Box sx={{ textAlign: "center", mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Database Merger
        </Typography>
        <Typography
          variant="subtitle1"
          color="text.secondary"
          maxWidth="md"
          mx="auto"
        >
          Upload and merge database tables from multiple sources. Map fields
          between schemas to combine your data seamlessly.
        </Typography>

        <Typography
          variant="subtitle1"
          color="text.secondary"
          maxWidth="md"
          mx="auto"
        >
          You can change the Target Database later as well
        </Typography>
      </Box>

      <Box
        sx={{
          display: "flex",
          gap: 3,
          mt: 2,
          flexDirection: { xs: "column", md: "row" },
        }}
      >
        <Box sx={{ flex: 1 }}>
          <ExcelFileDropzone
            title="Source Database"
            files={sourceDb}
            onFilesChange={setSourceDb}
            allFiles={sourceDb.concat(targetDb)}
          />
        </Box>

        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "text.secondary",
            "& svg": { fontSize: 24 },
          }}
        >
          <Box
            sx={{
              transform: "rotate(90deg)",
              display: { xs: "block", md: "none" },
            }}
          >
            →
          </Box>
          <Box sx={{ display: { xs: "none", md: "block" } }}>→</Box>
        </Box>

        <Box sx={{ flex: 1 }}>
          <ExcelFileDropzone
            title="Target Database"
            files={targetDb}
            onFilesChange={setTargetDb}
            allFiles={sourceDb.concat(targetDb)}
          />
        </Box>
      </Box>

      <Box sx={{ mt: 4, textAlign: "center" }}>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
          Drop your database files above to begin mapping and merging
        </Typography>
        {uploadError && (
          <Typography color="error" variant="body2" sx={{ mt: 1 }}>
            {uploadError}
          </Typography>
        )}
      </Box>

      {/* Debug section - can be removed in production */}
      <Box
        sx={{
          mt: 4,
          p: 2,
          bgcolor: "background.paper",
          borderRadius: 1,
          display: "none",
        }}
      >
        <Typography variant="h6" gutterBottom>
          Debug Info
        </Typography>
        <Box sx={{ display: "flex", gap: 2 }}>
          <Box sx={{ flex: 1 }}>
            <Typography variant="subtitle1" gutterBottom>
              Source Database Files:
            </Typography>
            <Box
              sx={{
                maxHeight: "200px",
                overflow: "auto",
                bgcolor: "background.paper",
                p: 1,
                borderRadius: 1,
              }}
            >
              {sourceDb.map((file) => (
                <Box
                  key={file.id}
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    mb: 1,
                  }}
                >
                  <Typography variant="body2" noWrap sx={{ maxWidth: "70%" }}>
                    {file.file.name}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {(file.file.size / 1024).toFixed(2)} KB
                  </Typography>
                </Box>
              ))}
            </Box>
          </Box>
          <Box sx={{ flex: 1 }}>
            <Typography variant="subtitle1" gutterBottom>
              Target Database Files:
            </Typography>
            <Box
              sx={{
                maxHeight: "200px",
                overflow: "auto",
                bgcolor: "background.paper",
                p: 1,
                borderRadius: 1,
              }}
            >
              {targetDb.map((file) => (
                <Box
                  key={file.id}
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    mb: 1,
                  }}
                >
                  <Typography variant="body2" noWrap sx={{ maxWidth: "70%" }}>
                    {file.file.name}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {(file.file.size / 1024).toFixed(2)} KB
                  </Typography>
                </Box>
              ))}
            </Box>
          </Box>
        </Box>
      </Box>
      <Button
        variant="contained"
        fullWidth
        sx={{ mt: 2 }}
        // onClick={async () => {
        //   try {
        //     setUploadError(null);
        //     setIsUploading(true);
            
        //     // Upload source and target files
        //     const response = await uploadFiles(
        //       sourceDb.map(f => f.file),
        //       targetDb.map(f => f.file)
        //     );
            
        //     console.log('Upload response:', response);
            
        //     // Handle schema analysis response
        //     if (response.schema_analysis) {
        //       const { source, target } = response.schema_analysis;
              
        //       // Store the schema analysis in localStorage for the next page
        //       localStorage.setItem('schemaAnalysis', JSON.stringify({
        //         source: {
        //           database: source?.database || 'source',
        //           tables: source?.tables || []
        //         },
        //         target: {
        //           database: target?.database || 'target',
        //           tables: target?.tables || []
        //         }
        //       }));
              
        //       // Navigate to confirmation page with schema data
        //       router.push({
        //         pathname: '/confirm',
        //         query: { 
        //           sourceDb: source?.database || 'source',
        //           targetDb: target?.database || 'target'
        //         }
        //       });
        //     } else {
        //       // Fallback for older response format
        //       console.warn('Unexpected response format. Falling back to legacy handling.');
              
        //       // Store user ID for future requests if available
        //       if (response.user_id) {
        //         localStorage.setItem('userId', response.user_id);
        //       }
              
        //       // Navigate to confirmation page with minimal data
        //       // router.push({
        //       //   pathname: '/confirm',
        //       //   query: { 
        //       //     sourceDb: 'source',
        //       //     targetDb: 'target'
        //       //   }
        //       // });
        //       router.push('/schema-visualizer');             
        //     }
            
        //   } catch (error) {
        //     console.error('Upload failed:', error);
        //     setUploadError(error instanceof Error ? error.message : 'Failed to upload files. Please try again.');
        //   } finally {
        //     setIsUploading(false);
        //   }
        // }}
        onClick={async () => {
          try {
            setUploadError(null);
            setIsUploading(true);
        
            // Upload source and target files
            const response = await uploadFiles(
              sourceDb.map((f) => f.file),
              targetDb.map((f) => f.file)
            );
        
            console.log("Upload response:", response);
        
            // ✅ Handle new schema analysis format from backend
            if (response.schema_analysis) {
              const { source, target } = response.schema_analysis;
        
              // Save entire backend structure directly — no need to rebuild manually
              localStorage.setItem(
                "schemaAnalysis",
                JSON.stringify({ source, target })
              );
        
              // Go to the visualizer
              router.push("/schema-visualizer");
            } else {
              console.warn("Unexpected response format — no schema_analysis found");
              setUploadError("No schema analysis returned from backend.");
            }
          } catch (error) {
            console.error("Upload failed:", error);
            setUploadError(
              error instanceof Error
                ? error.message
                : "Failed to upload files. Please try again."
            );
          } finally {
            setIsUploading(false);
          }
        }}        
        disabled={isConfirmDisabled}
        color="success"
        startIcon={isUploading ? <CircularProgress size={20} color="inherit" /> : null}
      >
        {isUploading ? 'Uploading...' : 'Visualize the Schemas'}
      </Button>
    </Container>
  );
}
