import { loadingFlags } from '../ui/loadingThunks';
import { ThemeMode } from '../ui/slice';

export type UIState = {
  themeMode: ThemeMode;
  loadingFlags: loadingFlags;
  isUserLoggedIn: boolean;
};
export type UserState = {
  userId: string | null;
  isAdmin: boolean;
};

export type AppState = {
  uiState: UIState;
  userState: UserState;
};
