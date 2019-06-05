import React from 'react';
import './App.css';
import PageRoot from "./Containers";
import {Provider} from "react-redux";
import {createStore} from "redux";
import {RootReducers} from "./Reducers";
import 'antd/dist/antd.css'; // or 'antd/dist/antd.less'


const store = createStore(RootReducers)

const App: React.FC = () => {
    return (
        <div className="App">
            <Provider store={store}>
                <PageRoot/>
            </Provider>
        </div>
    );
}

export default App;
