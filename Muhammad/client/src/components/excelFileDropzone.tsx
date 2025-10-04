import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import {
  Box,
  Typography,
  IconButton,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from "@mui/material";
import {
  TableChart as TableChartIcon,
  Close as CloseIcon,
  Schema as SchemaIcon,
} from "@mui/icons-material";

export interface FileWithPreview extends File {
  preview: string;
  id: string;
}

interface ExcelFileDropzoneProps {
  title: string;
  onFilesChange: (files: FileWithPreview[]) => void;
  files: FileWithPreview[];
  allFiles: FileWithPreview[];
}

export const ExcelFileDropzone: React.FC<ExcelFileDropzoneProps> = ({
  title,
  onFilesChange,
  files,
  allFiles,
}) => {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      // Get array of current file names for comparison
      const existingFileNames = allFiles.map((file) => file.name.toLowerCase());

      const newFiles = acceptedFiles.reduce((acc: FileWithPreview[], file) => {
        // Check if file with same name already exists
        if (!existingFileNames.includes(file.name.toLowerCase())) {
          // Create a new object that preserves all File properties
          const fileWithPreview: FileWithPreview = Object.assign(
            new File([file], file.name, { type: file.type }),
            {
              preview: URL.createObjectURL(file),
              id: Math.random().toString(36).substr(2, 9),
            }
          );
          acc.push(fileWithPreview);
        } else {
          console.warn(
            `File '${file.name}' was not added because it already exists.`
          );
        }
        return acc;
      }, []);

      if (newFiles.length > 0) {
        onFilesChange([...files, ...newFiles]);
      }
    },
    [files, onFilesChange]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
        ".xlsx",
      ],
      "application/vnd.ms-excel": [".xls"],
      "text/csv": [".csv"],
    },
    multiple: true,
  });

  const removeFile = (fileId: string) => {
    const updatedFiles = files.filter((file) => file.id !== fileId);
    onFilesChange(updatedFiles);
  };

  return (
    <Paper
      variant="outlined"
      sx={{
        p: 2,
        flex: 1,
        minHeight: "300px",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <Box sx={{ textAlign: "center", mb: 2 }}>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {files.length > 0
            ? `${files.length} table${files.length > 1 ? "s" : ""} loaded`
            : "No tables loaded"}
        </Typography>
      </Box>

      <Box
        {...getRootProps()}
        sx={{
          flex: 1,
          border: "2px dashed",
          borderColor: "divider",
          borderRadius: 1,
          p: 3,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          cursor: "pointer",
          backgroundColor: isDragActive ? "action.hover" : "background.paper",
          "&:hover": {
            backgroundColor: "action.hover",
          },
          mb: 2,
        }}
      >
        <input {...getInputProps()} />
        <SchemaIcon color="action" sx={{ fontSize: 48, mb: 1 }} />
        <Typography color="textSecondary" align="center" gutterBottom>
          {isDragActive
            ? `Drop database tables here`
            : `Drag & drop database files here`}
        </Typography>
        <Typography
          variant="body2"
          color="text.secondary"
          align="center"
          sx={{ mb: 1 }}
        >
          or click to browse files
        </Typography>
        <Typography
          variant="caption"
          color="text.secondary"
          align="center"
          sx={{
            display: "inline-block",
            bgcolor: "action.hover",
            px: 1,
            py: 0.5,
            borderRadius: 1,
            fontSize: "0.7rem",
          }}
        >
          Supports: XLSX, XLS, CSV
        </Typography>
      </Box>

      {files.length > 0 && (
        <Box sx={{ mt: 2, maxHeight: "200px", overflow: "auto" }}>
          <List dense>
            {files.map((file) => (
              <ListItem
                key={file.id}
                secondaryAction={
                  <IconButton
                    edge="end"
                    aria-label="remove"
                    onClick={(e) => {
                      e.stopPropagation();
                      removeFile(file.id);
                    }}
                  >
                    <CloseIcon />
                  </IconButton>
                }
                sx={{
                  "&:hover": {
                    backgroundColor: "action.hover",
                  },
                }}
              >
                <ListItemIcon>
                  <TableChartIcon />
                </ListItemIcon>
                <ListItemText
                  primary={file.name}
                  secondary={`${(file.size / 1024).toFixed(2)} KB`}
                  sx={{
                    "& .MuiListItemText-primary": {
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                      maxWidth: "200px",
                    },
                  }}
                />
              </ListItem>
            ))}
          </List>
        </Box>
      )}
    </Paper>
  );
};

export default ExcelFileDropzone;
