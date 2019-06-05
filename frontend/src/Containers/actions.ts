import {CarPos} from "../RootType";

export enum ActionsEnum {
    feedData= "addData",
    saveSeries= "SaveSeries",
    cleanSeries = "CleanSeries"
}

export const  ActAddData= (data:CarPos)=>({
    data,
    type:  ActionsEnum.feedData
})

export  const ActSave=   ()=>({
    type: ActionsEnum.saveSeries,
})

export  const ActClean=   ()=>({
    type: ActionsEnum.cleanSeries,
})


export type ActionType=any | ReturnType <typeof  ActAddData>
