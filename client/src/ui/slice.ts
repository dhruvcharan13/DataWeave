import {
  ActionReducerMapBuilder,
  AsyncThunk,
  createSlice,
} from '@reduxjs/toolkit';
import { UIState } from '../store/appState';
import { defaultAppState } from '../store/defaultState';
import { LoadingThunks } from './loadingThunks';

export type ThemeMode = 'light' | 'dark';

export const UISlice = createSlice({
  name: 'ui',
  initialState: {
    ...(defaultAppState.uiState as UIState),
  },
  reducers: {
    setThemeMode: (state, action) => {
      const themeMode: ThemeMode = action.payload;
      state.themeMode = themeMode;
    },
  },
  extraReducers: (builder) => {
    // bindLoadingThunks(builder, someThunk, LoadingThunks.DATA_LOAD);
  },
});

export const uiActions = {
  setThemeMode: UISlice.actions.setThemeMode,
};

const bindLoadingThunks = (
  builder: ActionReducerMapBuilder<UIState>,
  thunks: AsyncThunk<any, any, any>,
  targetLoadingFlag: LoadingThunks
) => {
  builder.addCase(thunks.pending, (state) => {
    state.loadingFlags[targetLoadingFlag] = true;
  });
  builder.addCase(thunks.fulfilled, (state) => {
    state.loadingFlags[targetLoadingFlag] = false;
  });
  builder.addCase(thunks.rejected, (state) => {
    state.loadingFlags[targetLoadingFlag] = false;
  });
};
export default UISlice.reducer;
