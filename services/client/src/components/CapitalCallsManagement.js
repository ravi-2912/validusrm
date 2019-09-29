import React from 'react';
import Axios from 'axios';
import PropTypes from 'prop-types';
import { Container, Row } from 'react-bootstrap';

import NavBar from './NavBar';
import NewCall from './NewCall';
import CapitalCallsDataGrid from './CapitalCallsDataGrid';
import { calcs_for_funds_invested_committed } from './helper';

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
    return Axios.get('http://localhost:5000/funds')
      .then(res => {
        const data = res.data;
        if (data.status === 'success') {
          return data.data.funds;
        }
      })
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
    return Axios.get('http://localhost:5000/investments')
      .then(res => {
        const data = res.data;
        if (data.status === 'success') {
          return data.data.fundinvestments;
        }
      })
      .then(invs => this.setState({ fundinvestments: invs }))
      .catch(err => console.log(err));
  };

  getCalls = async () => {
    return Axios.get('http://localhost:5000/capitalcalls')
      .then(res => {
        const data = res.data;
        if (data.status === 'success') {
          return data.data.capitalcalls;
        }
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
      let url = `http://localhost:5000/capitalcalls/${this.state.calls[index].id}`;

      Axios.put(url, {
        ...updated,
      })
        .then(res => {
          const data = res.data;
          if (data.status === 'success') {
            return data.data;
          }
        })
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
      let status = (Array.isArray(res) ? res : [res]).map(r => r.data.status === 'success');
      if (status) {
        this.getCalls();
        this.getFundInvestments();
      }
    };

    Axios.delete(`http://localhost:5000/capitalcalls/${id}`)
      .then(res =>
        Axios.all(
          invesetments_id.map(inv_id => {
            return Axios.delete(`http://localhost:5000/investments/${inv_id}`);
          }),
        ),
      )
      .then(res => {
        onDeleteCheckSuccess(res);
      })
      .catch(err => console.log(err));
  };

  render() {
    return (
      <div className="App">
        <NavBar
          activeItem={this.state.view === 'dashboard' ? 1 : 2}
          menuItems={navBarMenuItems}
          onMenuItemClicked={view => {
            this.getFundInvestments();
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
              <NewCall committments={this.state.committments} />
            )}
          </Row>
        </Container>
      </div>
    );
  }
}

export default CapitalCallsManagement;
