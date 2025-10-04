// store/store.ts
import { combineReducers, configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage'; // defaults to localStorage for web
import createRootReducer from './rootReducer';

const persistConfig = {
  key: 'root',
  storage,
  whitelist: ['uiState', 'userState'],
};

const persistedReducer = persistReducer(
  persistConfig,
  combineReducers(createRootReducer())
);

const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
});

const persistor = persistStore(store);

export { store, persistor };
