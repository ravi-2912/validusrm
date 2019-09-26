import React from 'react';
import { Form, Button, Col } from 'react-bootstrap';
import DatePicker from 'react-date-picker';

class AddCall extends React.Component {
  state = {
    date: new Date(),
  };
  onChange = date => this.setState({ date });
  render() {
    return (
      <Col className="text-left" lg={6}>
        <Form>
          <Form.Group controlId="formDate">
            <Form.Label>Select a Call Date</Form.Label>
            <DatePicker onChange={this.onChange} value={this.state.date} className="form-control" />
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
            <Form.Control type="text" placeholder="Investment #" />
            <Form.Text className="text-muted">Name of the investment.</Form.Text>
          </Form.Group>

          <Form.Group controlId="formCapitalRequired">
            <Form.Label>Enter Capital Required for Investment</Form.Label>
            <Form.Control type="text" placeholder="12345" />
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
