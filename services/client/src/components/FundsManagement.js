import React from 'react';
import { Container, Row } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import * as Icons from '@fortawesome/free-solid-svg-icons';
import NavBar from './NavBar';
import FundsDataGrid from './FundsDataGrid';
import CommittmentsDataGrid from './CommittmentsDataGrid';

class FundsManagementApp extends React.Component {
  state = {
    view: 'funds',
  };

  onChangeView = view => {
    this.setState({ view });
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
  render() {
    return (
      <div className="App">
        <NavBar menuItems={this.navBarMenuItems} onMenuItemClicked={this.onChangeView} />
        <Container className="AppContainer">
          <Row>{this.state.view === 'funds' ? <FundsDataGrid /> : <CommittmentsDataGrid />}</Row>
        </Container>
      </div>
    );
  }
}

export default FundsManagementApp;
