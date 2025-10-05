import Box from "@mui/material/Box";
import CssBaseline from "@mui/material/CssBaseline";
import DatasetSidebar from "../components/DatasetSidebar";
import SchemaGraph from "../components/SchemaGraph";
import { useEffect, useState } from "react";

export default function SchemaVisualizer() {
  // const [selectedDataset, setSelectedDataset] = useState("Bank1");
  //const [selectedDataset, setSelectedDataset] = useState("Source");
  const [selectedDataset, setSelectedDataset] = useState<string>("");

  
  useEffect(() => {
    const stored = localStorage.getItem("schemaAnalysis");
    if (stored) {
      const parsed = JSON.parse(stored);
      //  Automatically default to first available dataset (Source or Target)
      const defaultDataset = parsed.source?.database || parsed.target?.database || "";
      setSelectedDataset(defaultDataset);
    }
  }, []);
  

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
    sx={{
      flexGrow: 1,
      height: "100%",
      overflow: "hidden",
      bgcolor: "background.default",
      position: "relative",
    }}
  >
    <SchemaGraph selectedDataset={selectedDataset} />
  </Box>
</Box>

    </>
  );
}