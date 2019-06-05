import {ICarTrackReducer} from "./Containers/reducers";

export interface IRootStore {
    Car: ICarTrackReducer
}

export type CarFSM = "IDLE" | "LOCKING" | "RIN" | "ROUT"

export interface CarPos {
    angel: number
    FSM: CarFSM
    time: Date
}

export type LSData = Array<{
    k: Date,
    v: number
}>

export  interface ILSItem {
    time:Date
    data:LSData
}