import React from 'react';
import PropTypes from 'prop-types';
import { Container, Row } from 'react-bootstrap';

import NavBar from './NavBar';
import FundsDataGrid from './FundsDataGrid';
import CommittmentsDataGrid from './CommittmentsDataGrid';
import { calcs_for_funds_invested_committed } from './helper';
import { getFunds, getCommittments, sendUpdates, sendDelete, sendPost } from './apiCalls';

const navBarMenuItems = [
  {
    name: 'Home',
    route: '/',
    desc: 'Go to home page.',
    buttonText: 'Home',
  },
  {
    name: 'Funds',
    route: '/funds',
    desc: 'List all funds',
    buttonText: 'List Funds',
  },
  {
    name: 'Committments',
    route: '/committments',
    desc: 'List all committments.',
    buttonText: 'List Committments',
  },
];

class FundsManagement extends React.Component {
  state = {
    view: '',
    funds: [],
    newFund: {},
    committments: [],
    filters: {},
  };

  static propTypes = {
    location: PropTypes.object.isRequired,
  };

  getFunds = () => {
    getFunds()
      .then(funds => {
        const updateFunds = funds.map(fund => {
          // added this for progressbar values
          fund.invested_committed = calcs_for_funds_invested_committed(fund.committments);
          return fund;
        });
        this.setState({ funds: updateFunds });
      })
      .catch(err => console.log(err));
  };

  getCommittments = () => {
    getCommittments()
      .then(committments => {
        const updateCommittments = committments.map(committment => {
          // added this for progressbar values
          committment.invested_committed = calcs_for_funds_invested_committed([committment]);

          return committment;
        });
        this.setState({ committments: updateCommittments });
      })
      .catch(err => console.log(err));
  };

  componentDidMount() {
    const view = this.props.location.pathname.slice(1);
    this.setState({ view });
    this.getFunds();
    this.getCommittments();
  }

  onFiltersChange = filters => this.setState({ filters });

  onRowsChange = (rows, index = undefined, updated = undefined) => {
    if (index !== undefined && updated) {
      let id = `${this.state.view}/`;
      if (this.state.view === 'funds') {
        id += `${this.state.funds[index].id}`;
      } else {
        id += `${this.state.committments[index].id}`;
      }
      sendUpdates(id, updated)
        .then(obj => {
          if (this.state.view === 'funds') {
            const fund = obj;
            const funds = this.state.funds;
            fund.invested_committed = calcs_for_funds_invested_committed(fund.committments);
            funds[fund.id - 1] = fund;
            this.setState({ funds });
          } else {
            const committment = obj;
            const committments = this.state.committments;
            committment.invested_committed = calcs_for_funds_invested_committed([committment]);
            committments[committment.id - 1] = committment;
            this.setState({ committment });
          }
        })
        .catch(err => console.log(err));
    }
    if (this.state.view === 'funds') {
      this.setState({ funds: rows });
    } else {
      this.setState({ committments: rows });
    }
  };

  onRowDelete = id => {
    let obj = {};
    let len = 0;
    if (this.state.view === 'funds') {
      obj = this.state.funds.filter(fund => fund.id === id)[0];
      len = obj.committments.length;
    } else {
      obj = this.state.committments.filter(c => c.id === id)[0];
      len = obj.investments.length;
    }
    if (len > 0) {
      alert(`First delete dependents for ${this.state.view} ID ${obj.id} .`);
    } else {
      let idToDelete = `${this.state.view}/${id}`;
      sendDelete(idToDelete)
        .then(res => {
          if (res) {
            this.getFunds();
            this.getCommittments();
          }
        })
        .catch(err => console.log(err));
    }
  };

  addFundToDB = data => {
    sendPost('funds', data)
      .then(res => {
        if (res.status === 'success') {
          this.getFunds();
        }
      })
      .catch(err => console.log(err));
  };

  addCommittmentToDB = data => {
    sendPost('committments', data)
      .then(res => {
        if (res.status === 'success') {
          this.getCommittments();
        }
      })
      .catch(err => console.log(err));
  };

  render() {
    return (
      <div className="App">
        <NavBar
          activeItem={this.state.view === 'funds' ? 1 : 2}
          menuItems={navBarMenuItems}
          onMenuItemClicked={view => {
            this.getFunds();
            if (view === 'committments') {
              this.getCommittments();
            }
            this.setState({ view });
          }}
        />
        <Container className="AppContainer">
          <Row>
            {this.state.view === 'committments' ? (
              <CommittmentsDataGrid
                rows={this.state.committments}
                filters={this.state.filters}
                onFiltersChange={this.onFiltersChange}
                onRowsChange={this.onRowsChange}
                onRowDelete={this.onRowDelete}
                addCommittmentToDB={this.addCommittmentToDB}
                funds={this.state.funds}
              />
            ) : (
              <FundsDataGrid
                rows={this.state.funds}
                filters={this.state.filters}
                onFiltersChange={this.onFiltersChange}
                onRowsChange={this.onRowsChange}
                onRowDelete={this.onRowDelete}
                addFundToDB={this.addFundToDB}
              />
            )}
          </Row>
        </Container>
      </div>
    );
  }
}

export default FundsManagement;
