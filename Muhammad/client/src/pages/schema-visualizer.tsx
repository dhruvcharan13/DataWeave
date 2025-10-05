import Box from "@mui/material/Box";
import CssBaseline from "@mui/material/CssBaseline";
import DatasetSidebar from "../components/DatasetSidebar";
import SchemaGraph from "../components/SchemaGraph";
import { useState } from "react";

export default function SchemaVisualizer() {
  const [selectedDataset, setSelectedDataset] = useState("Bank1");

  return (
    <>
      <CssBaseline />
      <Box
        sx={{
          display: "flex",
          width: "100vw",
          height: "100vh",
          overflow: "hidden",
          bgcolor: "background.default",
        }}
      >
        {/* Sidebar */}
        <DatasetSidebar
          selected={selectedDataset}
          onSelect={setSelectedDataset}
        />

        {/* Graph */}
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            height: "100%",
            overflow: "hidden",
            p: 0,
            m: 0,
          }}
        >
          <SchemaGraph selectedDataset={selectedDataset} />
        </Box>
      </Box>
    </>
  );
}
