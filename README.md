# Capital Calls Web App

The Web App is made using a [Python](https://docs.python.org/3/) API server and [React](https://reactjs.org/) client. [Bootstrap](https://getbootstrap.com/) is primarily used for within React components and the grid/table view is made using [React Data Grid](https://adazzle.github.io/react-data-grid/) from Adazzle.

The API server is built using [Flask](https://flask.palletsprojects.com/en/1.1.x/) using [Python 3.7](https://docs.python.org/3/). A REST API is developed with the help of [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/).

The server access a [SQLite3](https://docs.python.org/3/library/sqlite3.html?highlight=sqlite#) database when running on Windows Hosts whereas a [PostgreSQL](https://www.postgresql.org/) when running in a [Docker](https://www.docker.com/) Container. The API queries the database thorugh Object Relational Mapping (ORM) using [SQLAlchemy](https://www.sqlalchemy.org/).

The API development follow a Test Driven Development (TDD) approach. Test are written using [`unittest`](https://docs.python.org/3/library/unittest.html) module avaialble within Python. This approach helps in design first and code later approach. Key specifications for the API were determined and then individual test were written. The actual code were then written for the test to pass.

## 5. Running

The API server can run either on a Windows Host having Python 3.7 or higher or on a [Docker container](https://docs.docker.com/get-started/part2/) using [Docker Compose](https://docs.docker.com/compose/) file.

In either case the API server depends on some environment variables that need to be set prior to running the server, these are explained further.

### 5.1. On Windows Host


#### 5.1.1. Run the server
Python 3.7 should be installed on the Windows host and added to PATH environment variable. This can be checked in command as follows:

```bash
$> python -V
#  Python 3.7.3
$> pip -V
# pip 19.1.1 from C:\Users\<UserName>\AppData\Local\Continuum\anaconda3\lib\site-packages\pip (python 3.7)
```

To run the server, navigate to the `./services/server` folder and run `main.py` as shown below. This will run the server on ['http://localhost:5000'](http://localhost:5000). Test by opening it and trying [/funds](http://localhost:5000/funds), [/committments](http://localhost:5000/committments), [/capitalcalls](http://localhost:5000/capitalcalls) or [/investments](http://localhost:5000/investments) on the browser.

```bash
$> cd services/server
$ (services/server)> python -m venv env
$ (services/server)> env/Scripts/activate
$(env) (services/server)> pip install -r requirements
$(env) (services/server)> python main.py run
```

To run tests or code coverage provide `test` or `cov` as argument to `main.py` instead of run.

```bash
$> (services/server)> python main.py test
$> (services/server)> python main.py cov
```

#### 5.1.2. Run the client

[NodeJS v10.16](https://nodejs.org/en/) and NPM v6.9 should be installed on the host machine. This can be checked with following commands.

```bash
$> node --version
# v10.16.3
$> npm --version
# 6.9.0
```

To run the ReactJS client navigate to the `./services/client` folder and run `npm run local` to run on localhost. This will start the development server and will set environment vaiable for server i.e. to localhost, assuming API server is runnning as per 5.1.1. above.

```bash
$> cd services/client
$ (services/client)> npm install
$ (services/client)> npm rum local
```

After this navigate to ['http://localhoat:3000'](http://localhoat:3000) to access the ReactJS client.

Note that `npm start` or `npm run build` commands will not get access to API server for localhost.

### 5.2. Docker

Dockerfiles and Docker compose files are provided in `services/server` and parent folder. Docker compose is build up of three containers: 
* Python Alpine to run the Flask API server
* Postres Alpine to run the PostgreSQL databse server
* Node Alpine to run the ReactJS client server

To run the web app in Docker container execute the following commands.

```bash
$> docker-compose up --build
```

The above will build the all the service containers provided in thhe `docker-compose.yml` file. To run as daemon add `-d` flag to above command.

Once the services are running navigate to [http://192.168.99.100:3007](http://192.168.99.100:3007) to access the react-client.

**Important**
Note, the Docker services will run depending on what version of Docker is available on host machine i.e. Legacy Docker Toolbox or the new Docker for Windows, etc. Depending on the Docker, [`REACT_APP_USERS_SERVICE_URL`](https://github.com/ravi-2912/validusrm/blob/master/docker-compose.yml#L41) environment variable needs to amended in the docker.

The address [http://192.168.99.100](http://192.168.99.100) is what I obtsained from Legacy Docker Toolbox.

#### PORTS

It is important to note the ports where the web app runs specially in a Docker container. Ports list are given in table below

| Run Environment  | Client         | Server         |
| ---------------- | -------------- | -------------- |
| Windows Host     | localhost:3000 | localhost:5000 |
| Docker Container | localhost:3007 | localhost:5001 |


## 1. API Endpoints

Using the RESTfull best practice alongwith TDD, the following routes are available in the API.

| Endpoint          | HTTP Method | CRUD Method | Result                  |
| ----------------- | ----------- | ----------- | ----------------------- |
| /funds            | POST        | Create      | Add one fund            |
| /funds            | GET         | Read        | Get all funds           |
| /funds/:id        | GET         | Read        | Get one fund            |
| /funds/:id        | PUT         | Update      | Update one fund         |
| /funds/:id        | DELETE      | Delete      | Delete one fund         |
| /committments     | POST        | Create      | Add one committment     |
| /committments     | GET         | Read        | Get all committments    |
| /committments/:id | GET         | Read        | Get one committment     |
| /committments/:id | PUT         | Update      | Update one committment  |
| /committments/:id | DELETE      | Delete      | Delete one committment  |
| /capitalcalls     | POST        | Create      | Add one capital call    |
| /capitalcalls     | GET         | Read        | Get all capital calls   |
| /capitalcalls/:id | GET         | Read        | Get one capital call    |
| /capitalcalls/:id | PUT         | Update      | Update one capital call |
| /capitalcalls/:id | DELETE      | Delete      | Delete one capital call |
| /investments      | POST        | Create      | Add one investment      |
| /investments      | GET         | Read        | Get all investments     |
| /investments/:id  | GET         | Read        | Get one investment      |
| /investments/:id  | PUT         | Update      | Update one investment   |
| /investments/:id  | DELETE      | Delete      | Delete one investment   |



## 2. API Requests and Responses

API requests can be mad using [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) or more conveniently and easily using [Axios](https://www.npmjs.com/package/axios). Some basic requests examples are shown below.

* GET requests to /funds

    ```javascript
    Axios.get(`${SERVER_URL}/funds`)
        .then(res => res.json())
        .then(data => res.data)
        .catch(err => console.log(err))
    ```

* GET requests to /committment/:id

    ```javascript
    Axios.get(`${SERVER_URL}/committments/${id}`)
        .then(res => res.json())
        .then(data => res.data)
        .catch(err => console.log(err))
    ```


Assuming the API server is running on localhost, the SERVER_URL =  ["http://localhost:5000"](http://localhost:5000).


The response from API requests follows a standardized output of key-value pair objects. Every response will have three keys - `status`, `message` and `data`. The `status` key will contain values either `success` or `fail`. The `data` key will have values that are either object (recieved for POST, GET and PUT request) or list of objects (for GET request). The `data` key will be empty object for DELETE request.

**Standard response structure**

```javascript
{
    status: 'success', // or 'fail'
    message: 'API response message',
    data: [{
        'key': value
    }]
}
```

**Example Response in `data` key**

* GET response from /funds

    ```javascript
    {
        status: 'success',
        message: 'API response message',
        data: [
            {
                'id': (number),
                'name: (string)
            },{
                'id': (number),
                'name: (string)
            }, ...
        ]
    }
    ```

### Known issues

1. API Server does not take querry commands such as filtering within URL. As a result API calls could be expensive when large data is there.
2. Flash messaging or form validation is not present for good user experience.
3. Post querries specially for posting capital investment is not task-queue based, as a result when multiples users are using the app, the app FIFO logic could break.
4. Manage states, routes and components more appropriately in the React application.
5. Small numbe of API test fail due to code changes, this does not impact code functionality.

## References

1. [Testdriven.io](http://testdriven.io/)
2. Daniel Gaspar and Jack Stouffer, ***[Mastering Flask Development](https://www.packtpub.com/gb/web-development/mastering-flask-web-development-second-edition)***, PacktPublishing Ltd., Oct 2018.
3. [Docker](https://www.docker.com/)