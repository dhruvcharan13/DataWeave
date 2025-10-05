import { AppState } from './appState';

export const defaultAppState: AppState = {
  uiState: {
    themeMode: 'dark',
    loadingFlags: {},
    isUserLoggedIn: false,
  },
  userState: {
    userId: null,
    isAdmin: false,
  },
};
