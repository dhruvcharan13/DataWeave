import React, { useEffect, useState } from "react";
import { Box, Typography, CircularProgress, Alert, Button } from "@mui/material";
import MappingGrid from "../components/MappingGrid";

interface Mapping {
  id: string | number;
  domain: string;
  source: { table: string; column: string };
  target: { table: string; column: string };
  confidence: number;
  transform: { type: string; params: Record<string, unknown> };
  rationale: string;
}

const SuggestedMapping = () => {
  const [mappings, setMappings] = useState<Mapping[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isMerging, setIsMerging] = useState(false);

  useEffect(() => {
    try {
      const suggestedMapping = localStorage.getItem("suggestedMapping");
      if (!suggestedMapping) {
        throw new Error("No mapping data found. Please generate mappings first.");
      }

      const parsed = JSON.parse(suggestedMapping);
      const mappingData = parsed?.mapping_response?.mappings || [];
      
      if (!Array.isArray(mappingData)) {
        throw new Error("Invalid mapping data format");
      }

      // Ensure each mapping has a unique ID
      const mappedData = mappingData.map((item: any, index: number) => ({
        ...item,
        id: item.id || index,
      }));

      setMappings(mappedData);
      setError(null);
    } catch (err) {
      console.error("Error loading mappings:", err);
      setError(err instanceof Error ? err.message : "Failed to load mappings");
    } finally {
      setLoading(false);
    }
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ margin: "1rem" }}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  const handleMap = async () => {
    try {
      setIsMerging(true);
      const res = await fetch("http://localhost:8000/api/run-merge", {
        method: "POST",
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body?.error || `Merge failed with status ${res.status}`);
      }
      // eslint-disable-next-line no-alert
      alert("Dataset merged and downloaded");
    } catch (e: any) {
      // eslint-disable-next-line no-alert
      alert(e?.message || "Failed to run merge");
    } finally {
      setIsMerging(false);
    }
  };

  return (
    <Box sx={{ margin: "1rem" }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h4" gutterBottom>
          Suggested Mapping
        </Typography>
        <Button variant="contained" onClick={handleMap} disabled={isMerging}>
          {isMerging ? "Mapping..." : "Map"}
        </Button>
      </Box>
      <MappingGrid data={mappings} />
    </Box>
  );
};

export default SuggestedMapping;
