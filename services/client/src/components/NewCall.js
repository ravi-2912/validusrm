import React from 'react';
import { Button, Form, Container, Row, Col } from 'react-bootstrap';

class NewCall extends React.Component {
  render() {
    return (
      <Col className="text-left">
        <Form>
          <Form.Group controlId="formDate">
            <Form.Label>Select Date</Form.Label>
            <Form.Control type="text" placeholder="Enter a date" />
            <Form.Text className="text-muted">Date when the call is made.</Form.Text>
          </Form.Group>

          <Form.Group controlId="exampleForm.ControlSelect1">
            <Form.Label>Example select</Form.Label>
            <Form.Control as="select">
              <option>1</option>
              <option>2</option>
              <option>3</option>
              <option>4</option>
              <option>5</option>
            </Form.Control>
          </Form.Group>

          <Button variant="primary" type="submit">
            Submit
          </Button>
        </Form>
      </Col>
    );
  }
}

export default NewCall;
