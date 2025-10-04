import { UISlice } from '../ui/slice';
import { userSlice } from '../user/slice';

const createRootReducer = () => {
  return {
    uiState: UISlice.reducer,
    userState: userSlice.reducer,
  };
};

export default createRootReducer;
