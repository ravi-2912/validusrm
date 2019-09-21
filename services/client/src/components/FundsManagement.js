import React from 'react';
import { Container, Row } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import * as Icons from '@fortawesome/free-solid-svg-icons';
import Axios from 'axios';
import NavBar from './NavBar';
import FundsDataGrid from './FundsDataGrid';
import CommittmentsDataGrid from './CommittmentsDataGrid';

class FundsManagement extends React.Component {
  state = {
    view: 'funds',
    funds: [],
    newFund: {},
    committments: [],
    filters: {},
    rows: [],
  };

  onFiltersChange = filters => this.setState({ filters });
  onRowsChange = rows => this.setState({ rows });
  onAddRow = index => {
    console.log(index, this.state.rows.length);
  };

  navBarMenuItems = [
    {
      name: 'Home',
      route: '/',
      desc: 'Go to home page.',
      buttonText: 'Home',
    },
    {
      name: 'Funds',
      route: '',
      desc: 'List all funds',
      buttonText: 'Add Fund',
    },
    {
      name: 'Committments',
      route: '',
      desc: 'List all committments.',
      buttonText: 'Add Committment',
    },
  ];

  getfunds = () => {
    Axios.get('http://localhost:5000/funds')
      .then(res => {
        const data = res.data;
        if (data.status === 'success') {
          return data.data.funds;
        }
      })
      .then(funds => {
        const updateFunds = funds.map(fund => {
          let totalCommitted = 0;
          let totalInvested = 0;
          for (let c of fund.committments) {
            totalCommitted += c.amount;
            for (let i of c.investments) {
              totalInvested += i.investment;
            }
          }
          // added this for progressbar values
          fund.invested_committed = {
            value: totalCommitted === 0 ? 0 : (100 * totalInvested) / totalCommitted,
            totalCommitted: totalCommitted,
            totalInvested: totalInvested,
          };
          return fund;
        });
        this.setState({ funds: updateFunds });
        this.setState({ rows: updateFunds });
      })
      .catch(err => console.log(err));
  };

  getCommittments = () => {
    Axios.get('http://localhost:5000/committments')
      .then(res => {
        const data = res.data;
        if (data.status === 'success') {
          this.setState({ committments: data.data.committments });
        }
      })
      .catch(err => console.log(err));
  };

  componentDidMount() {
    this.getfunds();
  }

  render() {
    return (
      <div className="App">
        <NavBar
          menuItems={this.navBarMenuItems}
          onMenuItemClicked={view => this.setState({ view })}
        />
        <Container className="AppContainer">
          <Row>
            {this.state.view === 'committments' ? (
              <CommittmentsDataGrid />
            ) : (
              <FundsDataGrid
                rows={this.state.rows}
                filters={this.state.filters}
                onFiltersChange={this.onFiltersChange}
                onRowsChange={this.onRowsChange}
                onAddRow={this.onAddRow}
              />
            )}
          </Row>
        </Container>
      </div>
    );
  }
}

export default FundsManagement;
