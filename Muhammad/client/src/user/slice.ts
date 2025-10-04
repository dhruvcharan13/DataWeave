import { createSlice } from '@reduxjs/toolkit';
import { UserState } from '../store/appState';
import { defaultAppState } from '../store/defaultState';

export const userSlice = createSlice({
  name: 'user',
  initialState: {
    ...(defaultAppState.userState as UserState),
  },
  reducers: {
    loginUser: (state, action) => {
      const { userId, isAdmin } = action.payload;
      state.userId = userId;
      state.isAdmin = isAdmin;
    },
    logoutUser: (state) => {
      state.userId = null;
      state.isAdmin = false;
    },
  },
});

export const userActions = {
  loginUser: userSlice.actions.loginUser,
  logoutUser: userSlice.actions.logoutUser,
};

export default userSlice.reducer;
