import {connect} from 'mqtt';


export const MQTTClient = connect("mqtt://ali.cnworkshop.xyz", {port: 20010})


MQTTClient.on('connect', function () {
    console.log("subscribe to openmv/data")
    MQTTClient.subscribe('openmv/data', function (err:any) {
    })
})


