import { CssBaseline, ThemeProvider } from "@mui/material";
import type { AppProps } from "next/app";
import { useSelector } from "react-redux";
import { AppState } from "../store/appState";
import { getTheme } from "./theme";
import ResponsiveAppBar from "../components/appBar";

export default function ThemedApp({ Component, pageProps }: AppProps) {
  const themeMode = useSelector((state: AppState) => state.uiState.themeMode);
  const theme = getTheme(themeMode);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ResponsiveAppBar />
      <Component {...pageProps} />
    </ThemeProvider>
  );
}
