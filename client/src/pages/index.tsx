import React, { useState } from "react";
import { Box, Typography, Container, Grid, Button } from "@mui/material";
import ExcelFileDropzone, {
  FileWithPreview,
} from "../components/excelFileDropzone";
import router from "next/router";

export default function Home() {
  const [sourceDb, setSourceDb] = useState<FileWithPreview[]>([]);
  const [targetDb, setTargetDb] = useState<FileWithPreview[]>([]);

  const isConfirmDisabled = sourceDb.length === 0 || targetDb.length === 0;

  React.useEffect(() => {
    console.log(sourceDb, targetDb);
  }, [sourceDb, targetDb]);

  return (
    <div>
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
        <Typography variant="body2" color="text.secondary">
          Drop your database files above to begin mapping and merging
        </Typography>
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
                    {file.name}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {(file.size / 1024).toFixed(2)} KB
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
                    {file.name}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {(file.size / 1024).toFixed(2)} KB
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
        onClick={() => router.push("/confirm")}
        disabled={isConfirmDisabled}
        color="success"
      >
        Visualize the Schemas
      </Button>
    </div>
  );
}
