export enum LoadingThunks {
  DATA_LOAD, // sample
}

export type loadingFlags = {
  [allLoadingThunks in keyof LoadingThunks]?: boolean;
};
