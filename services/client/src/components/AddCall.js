import React from 'react';
import { Form, Button, Col } from 'react-bootstrap';
import DatePicker from 'react-date-picker';

class AddCall extends React.Component {
  state = {
    date: new Date(),
    name: '',
    capital: 0,
    rule: 'fifo',
  };

  handleSubmit = evt => {
    evt.preventDefault();
    this.props.onCalculate(this.state);
  };

  onDateChange = date => this.setState({ date });

  onChange = evt => {
    evt.preventDefault();
    this.setState({
      ...this.state,
      [evt.currentTarget.name]: evt.currentTarget.value,
    });
  };

  render() {
    return (
      <Col className="text-left" lg={6}>
        <Form onSubmit={this.handleSubmit}>
          <Form.Group controlId="formDate">
            <Form.Label>Select a Call Date</Form.Label>
            <DatePicker
              onChange={this.onDateChange}
              value={this.state.date}
              className="form-control"
            />
            <Form.Text className="text-muted">Date when the call is made.</Form.Text>
          </Form.Group>

          <Form.Group controlId="formRule">
            <Form.Label>Select Investment Rule</Form.Label>
            <Form.Control as="select">
              <option>First-In-First-Out (FIFO)</option>
            </Form.Control>
          </Form.Group>

          <Form.Group controlId="formInvestmentName">
            <Form.Label>Enter Investment Name</Form.Label>
            <Form.Control
              type="text"
              placeholder="Investment #"
              name="name"
              required
              value={this.state.name}
              onChange={this.onChange}
            />
            <Form.Text className="text-muted">Name of the investment.</Form.Text>
          </Form.Group>

          <Form.Group controlId="formCapitalRequired">
            <Form.Label>Enter Capital Required for Investment</Form.Label>
            <Form.Control
              name="capital"
              type="text"
              required
              placeholder="12345"
              value={this.state.capital}
              onChange={this.onChange}
            />
            <Form.Text className="text-muted">How much capital to be invested in USD.</Form.Text>
          </Form.Group>

          <Button variant="primary" type="submit">
            Calculate Investments
          </Button>
        </Form>
      </Col>
    );
  }
}

export default AddCall;
