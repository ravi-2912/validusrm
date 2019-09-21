import React from 'react';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import * as Icons from '@fortawesome/free-solid-svg-icons';
import '../css/NavBar.css';

class NavBar extends React.Component {
  render() {
    const menuItems = this.props.menuItems;
    const onMenuItemClicked = this.props.onMenuItemClicked;
    return (
      <Navbar collapseOnSelect expand="lg" bg="light" variant="light" fixed="top">
        <Navbar.Brand href="#home">
          <img src="res/logo.png" alt="logo" height="50px" />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="mr-auto">
            {menuItems.map((item, ind) => (
              <Nav.Link href={item.route} key={ind} onSelect={this.onMenuItemClicked(item.route)}>
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
