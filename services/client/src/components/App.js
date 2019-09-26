import React from 'react';
import NavBar from './NavBar';
import { Container, Row, CardColumns, Card, Button } from 'react-bootstrap';
import '../css/App.css';

class App extends React.Component {
  menuItems = [
    {
      name: 'Capital Calls',
      route: '/dashboard',
      desc: 'Create  and confirm investments from available funds.',
      buttonText: 'Make Investments',
    },
    {
      name: 'Funds Management',
      route: '/funds',
      desc: 'Create and make committments into funds.',
      buttonText: 'Manage Funds',
    },
  ];
  render() {
    return (
      <div className="App">
        <NavBar menuItems={this.menuItems} />
        <Container className="AppContainer">
          <Row>
            <CardColumns>
              {this.menuItems.map((item, ind) => {
                return (
                  <Card style={{ width: '18rem' }} className="cool-blue" key={ind}>
                    <Card.Body>
                      <Card.Title>{item.name}</Card.Title>
                      <Card.Text>{item.desc}</Card.Text>
                      <Button variant="dark" href={item.route}>
                        {item.buttonText}
                      </Button>
                    </Card.Body>
                  </Card>
                );
              })}
            </CardColumns>
          </Row>
        </Container>
      </div>
    );
  }
}

export default App;
