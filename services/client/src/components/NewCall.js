import React from 'react';
import Axios from 'axios';

import AddCall from './AddCall';
import NewCallsDataGrid from './NewCallDataGrid';
import { Button } from 'react-bootstrap';
import { getData, sendPost } from './apiCalls';

class NewCall extends React.Component {
  state = {
    new_date: '',
    new_capital: 0,
    new_investment_name: '',
    rule: 'fifo',
    committments: [],
    rows: [],
    filters: {},
    calc_button_clicked: false,
    toDashboard: false,
  };

  formIsChanging = () => this.setState({ calc_button_clicked: false });

  onFiltersChange = filters => this.setState({ filters });

  onRowsChange = rows => this.setState({ rows });

  onCalculate = ({ date, name, capital, rule }, calc_button_clicked = true) => {
    this.setState({ calc_button_clicked });
    this.setState(
      { new_date: date, new_capital: capital, new_investment_name: name, rule: rule },
      () => {
        let cs = this.state.committments;
        let unfilled_capital = this.state.new_capital;
        cs = cs.map(c => {
          c.undrawn_committment_before_drawdown = c.amount;
          for (let inv of c.investments) {
            c.undrawn_committment_before_drawdown -= inv.investment;
          }
          return c;
        });
        cs = cs.map(c => {
          c.total_drawdown_notice =
            unfilled_capital >= c.undrawn_committment_before_drawdown
              ? c.undrawn_committment_before_drawdown
              : unfilled_capital;
          unfilled_capital -= c.total_drawdown_notice;
          c.undrawn_committment_after_drawdown =
            c.undrawn_committment_before_drawdown - c.total_drawdown_notice;
          return c;
        });
        this.onRowsChange(cs);
      },
    );
  };

  getCommittments = async () => {
    return getData('committments')
      .then(res => res.committments)
      .then(cs => {
        return Axios.all([...cs.map(c => getData(`funds/${c.fund_id}`))]).then(res => {
          const funds = res.map(r => r.name);
          return cs.map(c => {
            c.fund_name = funds[c.fund_id - 1];
            c.total_drawdown_notice = 0;
            c.undrawn_committment_after_drawdown = 0;
            c.undrawn_committment_before_drawdown = 0;
            return c;
          });
        });
      })
      .then(committments => this.setState({ committments }))
      .catch(err => console.log(err));
  };

  addToDB = evt => {
    evt.preventDefault();
    sendPost('capitalcalls', {
      name: this.state.new_investment_name,
      capital: this.state.new_capital,
      date: this.state.new_date,
      rule: this.state.rule,
    })
      .then(res => res.data)
      .then(call => {
        console.log(call);
        return sendPost('investments', {
          call_id: call.id,
          rule: this.state.rule,
        });
      })
      .then(data => {
        alert(data.message);
        this.props.changeView('dashboard');
      })
      .catch(err => console.log(err));
  };

  componentDidMount() {
    this.getCommittments().then(res =>
      this.onCalculate(
        {
          name: this.state.new_investment_name,
          date: this.state.newdate,
          capital: this.state.new_capital,
          rule: this.state.rule,
        },
        false,
      ),
    );
  }

  render() {
    return (
      <>
        <AddCall
          onDateChange={this.onDateChange}
          onCalculate={this.onCalculate}
          capital={this.state.new_capital}
          onFormChange={this.onFormChange}
          formIsChanging={this.formIsChanging}
        />
        {this.state.calc_button_clicked === true ? (
          <>
            <NewCallsDataGrid
              className="mb-5"
              rows={this.state.rows}
              filters={this.state.filters}
              onFiltersChange={this.onFiltersChange}
              onRowsChange={this.onRowsChange}
            />
            <div className="mb-5 pb-5">
              <Button className="mb-5" type="submit" onClick={this.addToDB}>
                Add to DB
              </Button>
            </div>
          </>
        ) : (
          <p>Click button above</p>
        )}
      </>
    );
  }
}

export default NewCall;
