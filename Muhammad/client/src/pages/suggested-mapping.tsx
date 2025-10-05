import React from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { Box, Typography, Chip } from "@mui/material";
import { mock_suggested_mapping } from "../mockData";


  
const SuggestedMapping = () => {
    console.log(mock_suggested_mapping.mappings)
    return (
        <div style={{ margin: "1rem"}}>
            <h1>Suggested Mapping</h1>
            <MappingGrid data={mock_suggested_mapping.mappings} />
        </div>
    );
};

export default SuggestedMapping;




const columns: GridColDef[] = [
  { 
    field: "domain", 
    headerName: "Domain", 
    width: 120,
    headerAlign: 'center',
    align: 'center',
    renderCell: (params) => params.value as string
  },
  {
    field: "source",
    headerName: "Source (Table.Column)",
    width: 250,
    headerAlign: 'center',
    align: 'left',
    renderCell: (params) => `${(params.value as any).table}.${(params.value as any).column}`
  },
  {
    field: "target",
    headerName: "Target (Table.Column)",
    width: 250,
    headerAlign: 'center',
    align: 'left',
    renderCell: (params) => `${(params.value as any).table}.${(params.value as any).column}`
  },
  {
    field: "confidence",
    headerName: "Confidence",
    width: 130,
    headerAlign: 'center',
    align: 'center',
    renderCell: (params) => (
      <Chip
        label={`${((params.value as number) * 100).toFixed(0)}%`}
        color={
          (params.value as number) > 0.9
            ? "success"
            : (params.value as number) > 0.7
            ? "warning"
            : "error"
        }
        size="small"
        sx={{ width: 80, justifyContent: 'center' }}
      />
    ),
  },
  {
    field: "transform",
    headerName: "Transform",
    width: 550,
    headerAlign: 'center',
    align: 'left',
    renderCell: (params) => {
      const value = params.value as { type: string; params: Record<string, unknown> };
      const paramsStr = Object.keys(value.params).length > 0 
        ? ` (${JSON.stringify(value.params)})` 
        : "";
      return `${value.type}${paramsStr}`;
    },
  },
  {
    field: "rationale",
    headerName: "Rationale",
    minWidth: 700,
    flex: 1,
    headerAlign: 'center',
    align: 'left',
    renderCell: (params) => (
      <div style={{ 
        whiteSpace: 'normal',
        lineHeight: '1.5',
        padding: '8px 0',
        width: '100%'
      }}>
        {params.value as string}
      </div>
    ),
  },
];

function MappingGrid({ data }) {
  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Data Mapping Overview
      </Typography>
      <Box sx={{ height: '80vh', width: '100%', overflow: 'auto' }}>
        <Box sx={{ minWidth: 'fit-content', width: '100%' }}>
          <DataGrid
            rows={data.map((row, index) => ({ ...row, id: row.id || index }))}
            columns={columns}
            getRowId={(row) => row.id}
            checkboxSelection
            sx={{
              border: "none",
              minWidth: '100%',
              width: 'max-content',
              "& .MuiDataGrid-columnHeaders": {
                backgroundColor: "#f5f5f5",
                fontWeight: "bold",
                position: 'sticky',
                top: 0,
                zIndex: 1,
              },
              "& .MuiDataGrid-row": {
                minWidth: '100%',
                width: 'max-content',
              },
              "& .MuiDataGrid-cell": {
                whiteSpace: 'normal !important',
                padding: '8px',
                display: 'flex',
                alignItems: 'center',
                '& > div': {
                  maxWidth: '100%',
                  wordBreak: 'break-word',
                }
              },
              "& .MuiDataGrid-cell--withRenderer": {
                padding: '8px',
              },
              "& .MuiDataGrid-main": {
                overflow: 'visible',
              },
              "& .MuiDataGrid-virtualScroller": {
                overflowX: 'auto',
                overflowY: 'auto',
              },
            }}
          />
        </Box>
      </Box>
    </Box>
  );
}
