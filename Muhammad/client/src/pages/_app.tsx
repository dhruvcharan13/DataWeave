// pages/_app.tsx
import { CssBaseline, Theme, ThemeProvider } from "@mui/material";
import type { AppProps } from "next/app";
import { Provider, useSelector } from "react-redux";
import ResponsiveAppBar from "../components/appBar";
import { AppState } from "../store/appState";
import "../styles/globals.css";
import { ThemeMode } from "../ui/slice";
import { getTheme } from "../ui/theme";
import { store, persistor } from "../store/store";
import { PersistGate } from "redux-persist/integration/react";
import { Container } from "@mui/material";
import "../components/graphStyles.css";


function ThemedApp({ Component, pageProps }: AppProps) {
  const themeMode: ThemeMode = useSelector(
    (state: AppState) => state.uiState.themeMode
  );
  const theme: Theme = getTheme(themeMode);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ResponsiveAppBar />
      <Container maxWidth="lg" sx={{ my: 2 }}>
        <Component {...pageProps} />
      </Container>
    </ThemeProvider>
  );
}

export default function MyApp(props: AppProps) {
  return (
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <ThemedApp {...props} />
      </PersistGate>
    </Provider>
  );
}
