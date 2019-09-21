import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import App from './App';
import NotFound from './NotFound';
import DataGrid from './DataGrid';

const Router = () => (
    <BrowserRouter>
        <Switch>
            <Route exact path="/grid" component={DataGrid} />
            <Route exact path="/" component={App} />
            <Route component={NotFound} />
        </Switch>
    </BrowserRouter>
);

export default Router;
