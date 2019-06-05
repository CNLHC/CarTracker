import {combineReducers} from "redux";
import CarTrackReducers from "./Containers/reducers";

export const RootReducers = combineReducers({
    Car:CarTrackReducers

})