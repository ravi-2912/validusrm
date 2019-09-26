import React from 'react';
import AddCall from './AddCall';
import AddFund from './AddFund';

class NewCall extends React.Component {
  state = {
    date: new Date(),
    name: '',
    capital: 0,
    rule: 'fifo',
  };

  onDateChange = date => this.setState({ date });

  onAddToDB = () => {};

  render() {
    return <AddCall date={this.state.date} onDateChange={this.onDateChange} />;
  }
}

export default NewCall;
