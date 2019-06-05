import {ActionsEnum, ActionType} from './actions'
import produce from "immer"
import {CarFSM} from "../RootType";
import {saveSeries} from "../LocalStore";


export interface ICarTrackReducer {
    carFSM: CarFSM
    DateSeries: Date[]
    DataSeries: number[]
    HistorySeries: Array<{
        Date: Date[]
        Data: number[]
    }>
}


const InitState: ICarTrackReducer = {
    carFSM: "IDLE",
    DateSeries: [],
    DataSeries: [],
    HistorySeries: []
};


const CarTrackReducers = (state: ICarTrackReducer = InitState, action: ActionType) => produce<ICarTrackReducer>(state, draft => {
    switch (action.type) {
        case ActionsEnum.feedData:
            if(action.data.angel>0){
                draft.DataSeries = [...state.DataSeries, action.data.angel]
                draft.DateSeries = [...state.DateSeries, action.data.time]
            }

            if (state.DateSeries.length > 200) {
                draft.DataSeries.shift()
                draft.DateSeries.shift()
            }

            draft.carFSM = action.data.FSM

            return
        case ActionsEnum.cleanSeries:
            draft.DataSeries = []
            draft.DateSeries = []
            return;
        case ActionsEnum.saveSeries:
            const currentData = state.DataSeries.map(((value, index) => ({
                k: state.DateSeries[index],
                v: value
            })))
            saveSeries(currentData)
    }
})

export default CarTrackReducers;
