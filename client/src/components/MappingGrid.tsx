import React, { useState, useMemo } from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { Box, Typography, Chip, Select, MenuItem } from "@mui/material";

export default function MappingGrid({ data = [] }) {
  const [rows, setRows] = useState(
    data.map((row, index) => ({ ...row, id: row.id || index }))
  );

  // Unique dropdown options from target attributes
  const targetOptions = useMemo(() => {
    const uniqueTargets = new Set(
      data
        .filter((r) => r.target?.table && r.target?.column)
        .map((r) => `${r.target.table}.${r.target.column}`)
    );
    return Array.from(uniqueTargets);
  }, [data]);

  const handleTargetChange = (id: number, newTarget: string) => {
    const [table, column] = newTarget.split(".");
    setRows((prev) =>
      prev.map((row) =>
        row.id === id ? { ...row, target: { table, column } } : row
      )
    );
  };

  const columns: GridColDef[] = [
    {
      field: "domain",
      headerName: "Domain",
      width: 120,
      headerAlign: "center",
      align: "center",
    },
    {
      field: "source",
      headerName: "Source (Table.Column)",
      width: 250,
      headerAlign: "center",
      align: "left",
      renderCell: (params) => {
        const table = params.value?.table || "";
        const column = params.value?.column || "";
        return (
          <Box
            sx={{ display: "flex", flexDirection: "column", lineHeight: 1.2 }}
          >
            <Typography variant="body2" sx={{ fontWeight: 600 }}>
              {table}
            </Typography>
            <Typography
              variant="caption"
              sx={{ color: "text.secondary", fontSize: "0.75rem" }}
            >
              {column}
            </Typography>
          </Box>
        );
      },
    },

    {
      field: "target",
      headerName: "Target (Table.Column)",
      width: 300,
      headerAlign: "center",
      align: "left",
      renderCell: (params) => {
        const current =
          params.value?.table && params.value?.column
            ? `${params.value.table}.${params.value.column}`
            : "";
        return (
          <Select
            value={current}
            size="small"
            variant="outlined"
            onChange={(e) => handleTargetChange(params.row.id, e.target.value)}
            displayEmpty
            MenuProps={{
              PaperProps: {
                sx: {
                  bgcolor: "background.paper",
                  maxHeight: 320,
                  border: "1px solid",
                  borderColor: "divider",
                  borderRadius: 2,
                  "& .MuiMenuItem-root": {
                    py: 1,
                    px: 2,
                    fontSize: "0.9rem",
                    transition: "all 0.2s ease",
                  },
                  "& .MuiMenuItem-root:hover": {
                    bgcolor: "action.hover",
                  },
                  "& .MuiMenuItem-root.Mui-selected": {
                    bgcolor: "primary.main",
                    color: "#fff",
                    fontWeight: 600,
                    "&:hover": {
                      bgcolor: "primary.dark",
                    },
                  },
                },
              },
            }}
            sx={{
              width: "100%",
              fontSize: "0.9rem",
              fontWeight: 500,
              bgcolor: current ? "background.paper" : "error.dark",
              borderRadius: 1.5,
              "& .MuiOutlinedInput-notchedOutline": {
                borderColor: current ? "divider" : "error.light",
              },
              "&:hover .MuiOutlinedInput-notchedOutline": {
                borderColor: current ? "action.active" : "error.main",
              },
              "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
                borderColor: "primary.main",
              },
            }}
          >
            <MenuItem value="" sx={{ color: "text.disabled", fontStyle: "italic" }}>
              Unmapped
            </MenuItem>
            {targetOptions.map((opt) => (
              <MenuItem key={opt} value={opt}>
                <Box
                  sx={{
                    display: "flex",
                    flexDirection: "column",
                    lineHeight: 1.2,
                  }}
                >
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    {opt.split(".")[0]}
                  </Typography>
                  <Typography
                    variant="caption"
                    sx={{ color: "text.secondary", fontSize: "0.75rem" }}
                  >
                    {opt.split(".")[1]}
                  </Typography>
                </Box>
              </MenuItem>
            ))}
          </Select>
        );
      },
    },
    {
      field: "confidence",
      headerName: "Confidence",
      width: 130,
      headerAlign: "center",
      align: "center",
      renderCell: (params) => (
        <Chip
          label={params.value ? `${(params.value * 100).toFixed(0)}%` : "—"}
          color={
            !params.value
              ? "error"
              : params.value > 0.9
              ? "success"
              : params.value > 0.7
              ? "warning"
              : "error"
          }
          size="small"
          sx={{ width: 80, justifyContent: "center" }}
        />
      ),
    },
    {
      field: "transform",
      headerName: "Transform",
      width: 450,
      headerAlign: "center",
      align: "left",
      renderCell: (params) => {
        if (!params.value) return "—";
        const value = params.value;
        const paramsStr =
          Object.keys(value.params || {}).length > 0
            ? ` (${JSON.stringify(value.params)})`
            : "";
        return `${value.type}${paramsStr}`;
      },
    },
    {
      field: "rationale",
      headerName: "Rationale",
      minWidth: 650,
      flex: 1,
      headerAlign: "center",
      align: "left",
      renderCell: (params) => (
        <div
          style={{
            whiteSpace: "normal",
            lineHeight: "1.5",
            padding: "8px 0",
            width: "100%",
          }}
        >
          {params.value || "—"}
        </div>
      ),
    },
  ];

  // Highlight unmapped rows
  const getRowClassName = (params) => {
    const unmapped =
      !params.row.source?.table ||
      !params.row.source?.column ||
      !params.row.target?.table ||
      !params.row.target?.column;
    return unmapped ? "row-unmapped" : "";
  };

  return (
    <Box>
      <Box sx={{ height: "80vh", width: "100%", overflow: "auto" }}>
        <Box sx={{ minWidth: "fit-content", width: "100%" }}>
          <DataGrid
            rows={rows}
            columns={columns}
            getRowClassName={getRowClassName}
            checkboxSelection
            disableColumnMenu
            disableRowSelectionOnClick
            getRowHeight={() => "auto"} // 🔹 Let rows expand to fit content
            rowHeight={64} // (optional fallback) slightly taller baseline
            sx={{
              border: "none",
              "& .MuiDataGrid-columnHeaders": {
                bgcolor: "background.default",
                fontWeight: "bold",
                position: "sticky",
                top: 0,
                zIndex: 1,
              },
              "& .row-unmapped": {
                bgcolor: "error.dark !important",
              },
              "& .MuiDataGrid-cell": {
                whiteSpace: "normal",
                padding: "8px",
                display: "flex",
                alignItems: "center",
                lineHeight: 1.3,
              },
            }}
          />
        </Box>
      </Box>
    </Box>
  );
}
