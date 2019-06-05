import * as React from 'react';
import {connect} from "react-redux"
import {CarPos, IRootStore} from "../RootType";
import ReactEcharts from "echarts-for-react";
import {MQTTClient} from "../Connectors/MQTT.js";
import {ActAddData, ActClean} from "./actions";
import {Button, Icon} from "antd";


const mapStateToProps = (state: IRootStore) => ({
    RTDate: state.Car.DateSeries,
    RTData: state.Car.DataSeries,
    RTFSM: state.Car.carFSM
});
const mapDispatchToProps = (dispatch: any) => ({
    onFeedData: (data: CarPos) => dispatch(ActAddData(data)),
    onClearData: () => dispatch(ActClean())
});


type IStateProps = ReturnType<typeof mapStateToProps>
type IDispatchProps = ReturnType<typeof mapDispatchToProps>

interface IOwnProps {
}

type IPageProps = IStateProps & IDispatchProps & IOwnProps


export class UnconnectedPageRoot extends React.Component<IPageProps> {
    componentDidMount(): void {
        MQTTClient.on('message', (topic: any, message: any) => {
            const data: CarPos = {
                FSM: message.toString().split(",")[0],
                angel: message.toString().split(",")[1],
                time: new Date()
            }
            this.props.onFeedData(data)
        })
    }


    private getOptions() {
        const Data = this.props.RTData
        const Date = this.props.RTDate
        return ({
            title: {
                text: '车辆追踪实时数据'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    animation: false
                }
            },
            xAxis: {
                type: 'time',
                splitLine: {
                    show: false
                }
            },
            yAxis: {
                min: 0,
                max: 180,
                type: 'value',
                scale: true,
                splitLine: {
                    show: false
                }
            },
            series: [{
                name: '角度数据',
                type: 'line',
                showSymbol: true,
                markPoint: {
                    symbol: 'diamond'

                },
                animation:true,
                hoverAnimation: false,
                animationDurationUpdate:200,
                data: Data.map(((v, index) => ({
                    name: Date[index].toDateString(),
                    value: [Date[index], v],
                })))
            }]
        })
    }

    render() {
        const LabeledIcon = (Text: string, iconType: string) => <div
        style={{
            "fontSize":"32pt",


        }}>
            <Icon type={iconType}/>
            <span>{Text}</span>
        </div>

        const stateICO = this.props.RTFSM === "IDLE" ? LabeledIcon("未锁定", "unlock") :
            this.props.RTFSM === "RIN" ? LabeledIcon("确认锁定", "loading") :
                this.props.RTFSM === "LOCKING" ? LabeledIcon("已锁定", "lock") :
                    this.props.RTFSM === "ROUT" ? LabeledIcon("确认失锁", "loading") : null


        return (
            <div>
                <ReactEcharts
                    option={this.getOptions()}
                    style={{
                        "height": "400px",
                        "width": "80%",
                        "margin": "0 auto"
                    }}
                />
                <div>
                    {stateICO}


                </div>

                <Button onClick={this.props.onClearData}>清除数据</Button>
            </div>
        )
    }
}

const PageRoot = connect(mapStateToProps, mapDispatchToProps)(UnconnectedPageRoot);

export default PageRoot
