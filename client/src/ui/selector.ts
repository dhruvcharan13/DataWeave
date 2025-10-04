import { createSelector } from "@reduxjs/toolkit";
import { useSelector } from "react-redux";
import { AppState } from "../store/appState";
import { LoadingThunks } from "./loadingThunks";

export const getLoadingFlagOfTarget = createSelector(
  (state: AppState) => state.uiState.loadingFlags,
  (state: AppState, target) => target,
  (loadingFlags, target: LoadingThunks): boolean => {
    return loadingFlags[target] === true;
  }
);

export const useIsLoading = (target: LoadingThunks) => {
  return useSelector((state: AppState) =>
    getLoadingFlagOfTarget(state, target)
  );
};
