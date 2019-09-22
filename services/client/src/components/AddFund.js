import React, { useState } from 'react';
import { Button, Modal, Form } from 'react-bootstrap';

class AddFund extends React.Component {
  state = {
    show: false,
    name: '',
  };

  handleClose = evt => {
    evt.preventDefault();
    if (evt) {
      if (evt.target.id === 'addToDB') {
        if (!this.state.name) {
          alert('Enter a valid fund name.');
        } else {
          this.props.addToDB(this.state.name);
        }
      }
    }
    this.setState({ show: false, name: '' });
  };

  handleShow = () => this.setState({ show: true });

  onChange = evt => {
    evt.preventDefault();
    this.setState({ name: evt.target.value });
  };

  render() {
    return (
      <>
        <Button variant="primary" onClick={this.handleShow}>
          Add Fund
        </Button>

        <Modal show={this.state.show} onHide={this.handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>Add New Fund</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form.Group controlId="formFundName">
              <Form.Label>Fund Name</Form.Label>
              <Form.Control
                required
                value={this.state.name}
                type="text"
                placeholder="Enter a fund name"
                onChange={this.onChange}
              />
              <Form.Text className="text-muted">Enter a unique fund name.</Form.Text>
            </Form.Group>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={this.handleClose}>
              Close
            </Button>
            <Button id="addToDB" variant="primary" onClick={evt => this.handleClose(evt)}>
              Add to DB
            </Button>
          </Modal.Footer>
        </Modal>
      </>
    );
  }
}

export default AddFund;
