import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import App from './App';
import NotFound from './NotFound';
import DataGrid from './DataGrid';
import NavBar from './NavBar';
import FundsManagement from './FundsManagement';
import CapitalCallsManagement from './CapitalCallsManagement';

const Router = () => (
  <BrowserRouter>
    <Switch>
      <Route exact path="/grid" component={DataGrid} />
      <Route exact path="/nav" component={NavBar} />
      <Route exact path="/:direction(funds|committments)" component={FundsManagement} />
      <Route exact path="/:direction(dashboard|newcall)" component={CapitalCallsManagement} />
      <Route exact path="/" component={App} />
      <Route component={NotFound} />
    </Switch>
  </BrowserRouter>
);

export default Router;
