import React from 'react';
import Axios from 'axios';
import PropTypes from 'prop-types';
import { Container, Row } from 'react-bootstrap';

import NavBar from './NavBar';
import NewCall from './NewCall';
import CapitalCallsDataGrid from './CapitalCallsDataGrid';
import { calcs_for_funds_invested_committed } from './helper';
import { getData, sendUpdates, sendDelete } from './apiCalls';

const navBarMenuItems = [
  {
    name: 'Home',
    route: '/',
    desc: 'Go to home page.',
    buttonText: 'Home',
  },
  {
    name: 'Dashboard',
    route: '/dashboard',
    desc: 'List all capital calls.',
    buttonText: 'Show Calls',
  },
  {
    name: 'New Call',
    route: '/newcall',
    desc: 'Add new call.',
    buttonText: 'New Call',
  },
];

class CapitalCallsManagement extends React.Component {
  state = {
    view: '',
    calls: [],
    fundinvestments: [],
    funds: [],
    committments: [],
    filters: {},
  };

  static propTypes = {
    location: PropTypes.object.isRequired,
  };

  getFunds = async () => {
    return getData('funds')
      .then(res => res.funds)
      .then(funds => {
        const updateFunds = funds.map(fund => {
          // added this for progressbar values
          fund.invested_committed = calcs_for_funds_invested_committed(fund.committments, fund);
          return fund;
        });
        this.setState({ funds: updateFunds });
      })
      .catch(err => console.log(err));
  };

  getFundInvestments = async () => {
    return getData('investments')
      .then(res => res.fundinvestments)
      .then(invs => this.setState({ fundinvestments: invs }))
      .catch(err => console.log(err));
  };

  getCalls = async () => {
    return getData('capitalcalls')
      .then(res => {
        setTimeout(() => {}, 5000);
        return res.capitalcalls;
      })
      .then(calls => {
        // Quite complex manipulation to create a table for dashboard
        const invs = this.state.fundinvestments;
        const funds = this.state.funds;
        return calls.map(call => {
          let call_invs = call.investments;
          for (const [ind, i] of call_invs.entries()) {
            for (let inv of invs) {
              if (i.id === inv.fundinvestment_id) {
                call.investments[ind].fund_name = funds.filter(f => f.id === inv.fund_id)[0].name;
                call.investments[ind].fund_id = funds.filter(f => f.id === inv.fund_id)[0].id;
              }
            }
          }
          return call;
        });
      })
      .then(calls => this.setState({ calls }))
      .catch(err => console.log(err));
  };

  componentDidMount() {
    const view = this.props.location.pathname.slice(1);
    this.setState({ view });
    this.getFunds()
      .then(res => this.getFundInvestments())
      .then(res => this.getCalls());
  }

  onFiltersChange = filters => this.setState({ filters });

  onRowsChange = (rows, index = undefined, updated = undefined) => {
    if (index !== undefined && updated) {
      const id = `capitalcalls/${this.state.calls[index].id}`;
      sendUpdates(id, updated)
        .then(obj => {
          const call = obj;
          const calls = this.state.calls;
          calls[call.id - 1] = call;
          this.setState({ calls });
        })
        .catch(err => console.log(err));
    }
    this.setState({ calls: rows });
  };

  onRowDelete = id => {
    let call = this.state.calls.filter(call => call.id === id)[0];
    let invesetments_id = call.investments === [] ? [] : call.investments.map(inv => inv.id);

    const onDeleteCheckSuccess = res => {
      let status = (Array.isArray(res) ? res : [res]).map(r => r === true);
      if (status) {
        this.getCalls();
        this.getFundInvestments();
      }
    };
    const idToDelete = `capitalcalls/${id}`;
    sendDelete(idToDelete)
      .then(res => Axios.all(invesetments_id.map(inv_id => sendDelete(`investments/${inv_id}`))))
      .then(res => {
        onDeleteCheckSuccess(res);
      })
      .catch(err => console.log(err));
  };

  changeView = view => {
    this.getFunds()
      .then(res => this.getFundInvestments())
      .then(res => this.getCalls());
    this.setState({ view });
  };

  render() {
    return (
      <div className="App">
        <NavBar
          activeItem={this.state.view === 'dashboard' ? 1 : 2}
          menuItems={navBarMenuItems}
          onMenuItemClicked={view => {
            this.getFunds()
              .then(res => this.getFundInvestments())
              .then(res => this.getCalls());
            this.setState({ view });
          }}
        />
        <Container className="AppContainer">
          <Row>
            {this.state.view === 'dashboard' ? (
              <CapitalCallsDataGrid
                rows={this.state.calls}
                filters={this.state.filters}
                onFiltersChange={this.onFiltersChange}
                onRowsChange={this.onRowsChange}
                onRowDelete={this.onRowDelete}
              />
            ) : (
              <NewCall committments={this.state.committments} changeView={this.changeView} />
            )}
          </Row>
        </Container>
      </div>
    );
  }
}

export default CapitalCallsManagement;
