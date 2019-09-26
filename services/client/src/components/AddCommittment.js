import React from 'react';
import { Button, Modal, Form } from 'react-bootstrap';

class AddCommittment extends React.Component {
  state = {
    show: false,
    fund_id: null,
    amount: 0,
  };

  handleClose = evt => {
    evt.preventDefault();
    if (evt) {
      if (evt.target.id === 'addToDB') {
        if (!parseFloat(this.state.amount)) {
          alert('Enter a valid committment amount.');
        } else {
          this.props.addToDB({ amount: this.state.amount, fund_id: this.state.fund_id });
        }
      }
    }
    this.setState({ show: false, fund_id: null, amount: 0 });
  };

  handleShow = () => this.setState({ show: true });

  onChange = evt => {
    evt.preventDefault();
    this.setState({
      ...this.state,
      [evt.currentTarget.name]: evt.currentTarget.value,
    });
  };

  render() {
    return (
      <>
        <Button variant="primary" onClick={this.handleShow}>
          Add Committment
        </Button>

        <Modal show={this.state.show} onHide={this.handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>Add New Committment</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form.Group controlId="formCommittmentAmount">
              <Form.Label>Committment Amount</Form.Label>
              <Form.Control
                name="amount"
                required
                value={this.state.amount}
                type="text"
                placeholder="Enter a committment amount"
                onChange={this.onChange}
              />
              <Form.Text className="text-muted">
                Enter a committment amout for the specified fund.
              </Form.Text>
            </Form.Group>
            <Form.Group controlId="formCommittmentFundID">
              <Form.Label>Select Fund </Form.Label>
              <Form.Control as="select" onChange={this.onChange} name="fund_id">
                {this.props.funds.map(fund => {
                  return (
                    <option key={fund.id} value={fund.id}>
                      {fund.id} - {fund.name}
                    </option>
                  );
                })}
              </Form.Control>
              <Form.Text className="text-muted">
                Select a a fund for committing the amount.
              </Form.Text>
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

export default AddCommittment;
