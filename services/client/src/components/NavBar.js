import React from 'react';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import * as Icons from '@fortawesome/free-solid-svg-icons';
import '../css/NavBar.css';

class NavBar extends React.Component {
  handleSelect = eventKey => {
    const menuItems = this.props.menuItems;
    const clicked = menuItems[eventKey].name.toLowerCase();
    this.props.onMenuItemClicked(clicked);
  };

  render() {
    const menuItems = this.props.menuItems;
    return (
      <Navbar collapseOnSelect expand="lg" bg="light" variant="light" fixed="top">
        <Navbar.Brand href="#home">
          <img src="res/logo.png" alt="logo" height="50px" />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="mr-auto" onSelect={this.handleSelect}>
            {menuItems.map((item, ind) => (
              <Nav.Link href={item.route} eventKey={ind} key={ind}>
                {item.name}
              </Nav.Link>
            ))}
          </Nav>
          <Nav>
            <Nav.Link href="#deets">
              <FontAwesomeIcon icon={Icons.faUser} />
            </Nav.Link>
            <Nav.Link eventKey={2} href="#memes">
              <FontAwesomeIcon icon={Icons.faSignOutAlt} />
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    );
  }
}

export default NavBar;
