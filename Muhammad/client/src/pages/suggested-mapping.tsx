import React, { useEffect, useState } from "react";
import { Box, Typography, CircularProgress, Alert } from "@mui/material";
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

  return (
    <Box sx={{ margin: "1rem" }}>
      <Typography variant="h4" gutterBottom>
        Suggested Mapping
      </Typography>
      <MappingGrid data={mappings} />
    </Box>
  );
};

export default SuggestedMapping;
