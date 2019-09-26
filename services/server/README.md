# Capital Calls API

The API server is built using [Flask](https://flask.palletsprojects.com/en/1.1.x/) using [Python 3.7](https://docs.python.org/3/). A REST API is developed with the help of [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/).

The server access a [SQLite3](https://docs.python.org/3/library/sqlite3.html?highlight=sqlite#) database when running on Windows Hosts whereas a [PostgreSQL](https://www.postgresql.org/) when running in a [Docker](https://www.docker.com/) Container. The API queries the database thorugh Object Relational Mapping (ORM) using [SQLAlchemy](https://www.sqlalchemy.org/).

The API development follow a Test Driven Development (TDD) approach. Test are written using [`unittest`](https://docs.python.org/3/library/unittest.html) module avaialble within Python. This approach helps in design first and code later approach. Key specifications for the API were determined and then individual test were written. The actual code were then written for the test to pass.

## 5. Running

The API server can run either on a Windows Host having Python 3.7 or higher or on a [Docker container](https://docs.docker.com/get-started/part2/) using [Docker Compose](https://docs.docker.com/compose/) file.

In either case the API server depends on some environment variables that need to be set prior to running the server, these are explained further.

### 5.1. On Windows Host

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
$ (services/server)> python main.py run
```

To run tests or code coverage provide `test` or `cov` as argument to `main.py` instead of run.

```bash
$ (services/server)> python main.py test
$ (services/server)> python main.py cov
```

#### 5.1.1. What is `main.py`?

`main.py` is a Command Line Interface (CLI) wrapper around `manage.py` (another CLI) that creates some environemnt variables essentiallt to run the server on [localhost:5000](http://localhost:5000).

#### 5.1.2. What is `manage.py`?

`manage.py` is the file to configure the Flask CLI and manage the app from the command line. 

### 5.2. Docker Compose

**Note:** Docker `volumes` keyword

### 5.2.1. On Docker Containers

#### 5.2.3. PostgreSQL Server

#### 5.2.2. What is `Entrypoint.sh`?


## 1. API Endpoints

Using the RESTfull best practice alongwith TDD, the following routes are available in the API.

| Endpoint          | HTTP Method | CRUD Method| Result                  |
|-------------------|-------------|------------|-------------------------|
| /funds            | POST        | Create     | Add one fund            |
| /funds            | GET         | Read       | Get all funds           |
| /funds/:id        | GET         | Read       | Get one fund            |
| /funds/:id        | PUT         | Update     | Update one fund         |
| /funds/:id        | DELETE      | Delete     | Delete one fund         |
| /committments     | POST        | Create     | Add one committment     |
| /committments     | GET         | Read       | Get all committments    |
| /committments/:id | GET         | Read       | Get one committment     |
| /committments/:id | PUT         | Update     | Update one committment  |
| /committments/:id | DELETE      | Delete     | Delete one committment  |
| /capitalcalls     | POST        | Create     | Add one capital call    |
| /capitalcalls     | GET         | Read       | Get all capital calls   |
| /capitalcalls/:id | GET         | Read       | Get one capital call    |
| /capitalcalls/:id | PUT         | Update     | Update one capital call |
| /capitalcalls/:id | DELETE      | Delete     | Delete one capital call |
| /investments      | POST        | Create     | Add one investment      |
| /investments      | GET         | Read       | Get all investments     |
| /investments/:id  | GET         | Read       | Get one investment      |
| /investments/:id  | PUT         | Update     | Update one investment   |
| /investments/:id  | DELETE      | Delete     | Delete one investment   |



## 2. API Requests and Responses

API requests can be mad using [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) or more conveniently and easily using [Axios](https://www.npmjs.com/package/axios). Some basic requests are shown below.

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

* POST request to /capitalcalls

    ```javascript
    Axios.post(`${SERVER_URL}/capitalcalls`, {
        name: 'investment_1',
        capital: 1000000.0
        rule: 'fifo'
    }).then(res => res.json())
      .then(data => res.data)
      .catch(err => console.log(err))
    ```

* PUT request to /committments/:id

    ```javascript
    Axios.put(`${SERVER_URL}/committments/${id}`, {
        fund_id: 7
    }).then(res => res.json())
      .then(data => res.data)
      .catch(err => console.log(err))
    ```

* PUT request to /capitallcalls/:id

    ```javascript
    Axios.put(`${SERVER_URL}/committments/${id}`, {
        name: 'invesment_xyz'
    }).then(res => res.json())
      .then(data => res.data)
      .catch(err => console.log(err))
    ```

* DELETE request to /committments:id

    ```javascript
    Axios.deletet(`${SERVER_URL}/committments/${id}`)
        .then(res => res.json())
        .then(data => res.data)
        .catch(err => console.log(err))
    ```

Assuming the API server is running on localhost, the SERVER_URL =  ["http://localhost:5000"](http://localhost:5000).


The response from API requests follows a standardized output of key-value pair objects. Every response will have three keys - `status`, `message` and `data`. The `status` key will contain values either `success` or `fail`. The `data` key will have values that are either object (recieved for POST, GET and PUT request) or list of objects (for GET request). The `data` key will be empty object for DELETE request.

**Standard response structure**

```json
{
    status: 'success', // or 'fail'
    message: 'API response message',
    data: [{
        'key': value
    }]
}
```

**Response in `data` key**

* POST/PUT request to /funds

* GET response from /funds

    ```json
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


## 3. Code Structure

## 4. Dependencies

## 6. Development Strategy

### 6.1. Tests

### 6.2. Code Coverage

## Model

### Tables

### Relationships

### FIFO logic

### Known issues

## Further Developments

**Note**

* *Authentications*

  ddd

* *Deployment*

## References

1. Testdrivenio
2. flask book
3. docker
