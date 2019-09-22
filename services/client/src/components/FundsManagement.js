import React from 'react';
import { Container, Row } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import * as Icons from '@fortawesome/free-solid-svg-icons';
import Axios from 'axios';
import NavBar from './NavBar';
import FundsDataGrid from './FundsDataGrid';
import CommittmentsDataGrid from './CommittmentsDataGrid';

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
    buttonText: 'Add Fund',
  },
  {
    name: 'Committments',
    route: '/committments',
    desc: 'List all committments.',
    buttonText: 'Add Committment',
  },
];

const calcs = committments => {
  let totalCommitted = 0;
  let totalInvested = 0;
  for (let c of committments) {
    totalCommitted += c.amount;
    for (let i of c.investments) {
      totalInvested += i.investment;
    }
  }
  // added this for progressbar values
  const invested_committed = {
    value: totalCommitted === 0 ? 0 : (100 * totalInvested) / totalCommitted,
    totalCommitted: totalCommitted,
    totalInvested: totalInvested,
  };
  return invested_committed;
};

class FundsManagement extends React.Component {
  state = {
    view: '',
    funds: [],
    newFund: {},
    committments: [],
    filters: {},
  };

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
          // added this for progressbar values
          fund.invested_committed = calcs(fund.committments);
          return fund;
        });
        this.setState({ funds: updateFunds });
      })
      .catch(err => console.log(err));
  };

  getCommittments = () => {
    Axios.get('http://localhost:5000/committments')
      .then(res => {
        const data = res.data;
        if (data.status === 'success') {
          return data.data.committments;
        }
      })
      .then(committments => {
        const updateCommittments = committments.map(committment => {
          // added this for progressbar values
          committment.invested_committed = calcs([committment]);

          return committment;
        });
        this.setState({ committments: updateCommittments });
      })
      .catch(err => console.log(err));
  };

  componentDidMount() {
    const view = window.location.pathname.slice(1);
    this.setState({ view });
    this.getfunds();
    this.getCommittments();
  }

  onFiltersChange = filters => this.setState({ filters });

  onRowsChange = (rows, index = undefined, updated = undefined) => {
    if (index !== undefined && updated) {
      let url = `http://localhost:5000/${this.state.view}/`;
      if (this.state.view === 'funds') {
        url += `${this.state.funds[index].id}`;
      } else {
        console.log(this.state.committments[index]);
        url += `${this.state.committments[index].id}`;
      }
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
          if (this.state.view === 'funds') {
            const fund = obj;
            const funds = this.state.funds;
            fund.invested_committed = calcs(fund.committments);
            funds[fund.id - 1] = fund;
            this.setState({ funds });
          } else {
            const committment = obj;
            const committments = this.state.committments;
            committment.invested_committed = calcs([committment]);
            committments[committment.id - 1] = committment;
            this.setState({ committment });
          }
        })
        .catch(err => console.log(err));
    }
  };

  onRowDelete = id => {
    let obj = {};
    let len = 0;
    if (this.state.view === 'funds') {
      obj = this.state.funds[id - 1];
      len = obj.committments.length;
    } else {
      obj = this.state.committments[id - 1];
      len = obj.investments.length;
    }
    if (len > 0) {
      alert(`First delete dependents for ${this.state.view} ID ${obj.id} .`);
    } else {
      Axios.delete(`http://localhost:5000/${this.state.view}/${id}`)
        .then(res => {
          const data = res.data;
          if (data.status === 'success') {
            this.getfunds();
            this.getCommittments();
          }
        })
        .catch(err => console.log(err));
    }
  };

  addFundToDB = name => {
    Axios.post('http://localhost:5000/funds', {
      name,
    })
      .then(res => res.data)
      .then(res => {
        if (res.status === 'success') {
          this.getfunds();
        }
      })
      .catch(err => console.log(err));
  };

  addCommittmentToDB = data => {
    Axios.post('http://localhost:5000/committments', {
      ...data,
    })
      .then(res => res.data)
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
            this.getfunds();
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
