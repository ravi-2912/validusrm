import React from "react";
import ReactDOM from "react-dom";
import axios from "axios";
import "./index.css";
import UsersList from "./components/UsersList";
import * as serviceWorker from "./serviceWorker";
import AddUser from "./components/AddUser";
//import App from "./App";

class App extends React.Component {
  REACT_APP_USERS_SERVICE_URL = "http://localhost:5000"; //process.env.REACT_APP_USERS_SERVICE_URL;
  state = {
    users: [],
    username: "",
    email: ""
  };

  getUsers = () => {
    axios
      .get(`${this.REACT_APP_USERS_SERVICE_URL}/users`)
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

  addUser = event => {
    event.preventDefault();
    const data = {
      username: this.state.username,
      email: this.state.email
    };
    axios
      .post(`${this.REACT_APP_USERS_SERVICE_URL}/users`, data)
      .then(res => {
        this.getUsers();
        this.setState({ username: "", email: "" });
      })
      .catch(err => {
        console.log(err);
      });
  };

  handleChange = event => {
    event.preventDefault();
    const obj = {
      [event.target.name]: event.target.value
    };
    this.setState(obj);
  };

  render() {
    return (
      <section className="section">
        <div className="container">
          <div className="columns">
            <div className="column is-half">
              <br />
              <h1 className="title is-1">ll Users</h1>
              <hr />
              <br />
              <AddUser
                addUser={this.addUser}
                username={this.state.username}
                email={this.state.email}
                handleChange={this.handleChange}
              />
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
