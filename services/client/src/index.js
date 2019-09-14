import React from "react";
import ReactDOM from "react-dom";
import axios from "axios";
import "./index.css";
import UsersList from "./components/UsersList";
import * as serviceWorker from "./serviceWorker";
import AddUser from "./components/AddUser";
//import App from "./App";

class App extends React.Component {
  state = {
    users: []
  };

  getUsers = () => {
    let REACT_APP_USERS_SERVICE_URL = "http://localhost:5000";
    axios
      .get(`${REACT_APP_USERS_SERVICE_URL}/users`)
      .then(res => {
        let users = res.data.data.users;
        this.setState({ users });
      })
      .catch(err => {
        console.log(err);
      });
  };

  componentDidMount() {
    this.getUsers();
  }

  render() {
    return (
      <section className="section">
        <div className="container">
          <div className="columns">
            <div className="column is-half">
              <br />
              <h1 className="title is-1">All Users</h1>
              <hr />
              <br />
              <AddUser />
              <br />
              <br />
              <UsersList users={this.state.users} />
            </div>
          </div>
        </div>
      </section>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("root"));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
