import { createTheme } from "@mui/material/styles";

export const getTheme = (mode: "light" | "dark") =>
  createTheme({
    palette: {
      mode,
      primary: {
        main: '#6366f1', // Modern indigo blue
        light: '#818cf8',
        dark: '#4f46e5',
      },
      secondary: {
        main: '#ec4899', // Pink accent
        light: '#f472b6',
        dark: '#db2777',
      },
      background: {
        default: mode === 'light' ? '#fafafa' : '#0f172a',
        paper: mode === 'light' ? '#ffffff' : '#1e293b',
      },
    },
    typography: {
      fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Helvetica Neue", Arial, "Noto Sans", sans-serif',
    },
    shape: {
      borderRadius: 12,
    },
  });
