import Box from "@mui/material/Box";
import CssBaseline from "@mui/material/CssBaseline";
import DatasetSidebar from "../components/DatasetSidebar";
import SchemaGraph from "../components/SchemaGraph";
import { useEffect, useState } from "react";
import { keyframes } from "@emotion/react";
import { Backdrop, CircularProgress, Fade } from "@mui/material";

export default function SchemaVisualizer() {
  const [loading, setLoading] = useState(false);
  const [selectedDataset, setSelectedDataset] = useState<string>("");


  const setIsLoading = (isLoading: boolean) => {
    setLoading(isLoading);
  };
  useEffect(() => {
    const stored = localStorage.getItem("schemaAnalysis");
    if (stored) {
      const parsed = JSON.parse(stored);
      //  Automatically default to first available dataset (Source or Target)
      const defaultDataset =
        parsed.source?.database || parsed.target?.database || "";
      setSelectedDataset(defaultDataset);
    }
  }, []);

  // Animation for the backdrop
  const fadeIn = keyframes`
    from { opacity: 0; }
    to { opacity: 1; }
  `;

  return (
    <Box sx={{ position: 'relative', minHeight: '100vh' }}>
      <Backdrop
        sx={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          zIndex: 1400,
          backgroundColor: 'rgba(0, 0, 0, 0.7)',
          backdropFilter: 'blur(4px)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          animation: `${fadeIn} 0.3s ease-in-out`,
          '&.MuiBackdrop-invisible': {
            opacity: 0,
            pointerEvents: 'none',
            transition: 'opacity 0.3s ease-in-out',
          },
        }}
        open={loading}
        transitionDuration={300}
      >
        <Fade in={loading} timeout={300}>
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 2,
              p: 4,
              borderRadius: 2,
              backgroundColor: 'rgba(255, 255, 255, 0.1)',
              backdropFilter: 'blur(8px)',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
              border: '1px solid rgba(255, 255, 255, 0.1)',
            }}
          >
            <CircularProgress 
              size={60} 
              thickness={4}
              sx={{
                color: 'primary.main',
                animationDuration: '1.5s',
                '& .MuiCircularProgress-circle': {
                  strokeLinecap: 'round',
                },
              }}
            />
            <Box sx={{ 
              color: 'common.white', 
              fontWeight: 'medium',
              fontSize: '1.1rem',
              textAlign: 'center',
              maxWidth: 300,
              textShadow: '0 2px 4px rgba(0,0,0,0.2)'
            }}>
              Analyzing schemas and generating mappings...
            </Box>
          </Box>
        </Fade>
      </Backdrop>
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
          setIsLoading={setIsLoading}
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
    </Box>
  );
}
