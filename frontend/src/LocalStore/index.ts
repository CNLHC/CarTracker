import {LSData} from "../RootType";

export const getItemCounter = () => {
    const s = localStorage.getItem("CarTrackerCount")
    const CurrentCount: number = parseInt(s !== null ? s : "0");
    if (s === null) {
        localStorage.setItem("CarTrackerCount", "0")

    }
    return CurrentCount
}
export const saveSeries= (data:LSData)=>{
    const CurrentCount = getItemCounter()
    localStorage.setItem("CarTrackerCount", (CurrentCount + 1).toString())
    localStorage.setItem(`CTCItem${CurrentCount}`, JSON.stringify({
        time: new Date(),
        data: data
    }))

}

