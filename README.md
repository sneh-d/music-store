# Music Store

[Hosted on Heroku at : https://music-store-97.herokuapp.com](https://music-store-97.herokuapp.com)

The motivation for this project is to create my capstone project for Udacity's Fullstack Nanodegree program.
It models a store that is responsible for keeping record of music albums and various music artists.
The assumption is that I am the Manager of the store and want to create a system to simplify and streamline my work.

## Project dependencies

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Working within a virtual environment is recommended.

#### PIP Dependencies

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

- you may need to change the database url in setup.sh after which you can run
```bash
source setup.sh
```

- Start server by running
```bash
flask run
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.


#### Authentication

Authentication is implemented using Auth0, it uses RBAC to assign permissions using roles, these are tokens you could use to access the endpoints.
Note: The tokens expires in 24 hours you can create your own tokens at [Auth0](https://auth0.com/). You would need to reflect this in auth.py
```py
AUTH0_DOMAIN = '<your auth domain>'
ALGORITHMS = ['RS256']
API_AUDIENCE = '<your api audience>'
```

## Database Setup
As the project uses Postgresql as its database, you would need to create one locally and add configuration details in setup.sh.
To update the database and add data to the tables run the following :
```bash
python manage.py db upgrade
python manage.py seed
```


## Testing
Ensure a test database is created and configured in setup.sh.
To start tests, run
```
source test.sh
```


## Documentation
The Endpoints were documented using postman collections
- open `music-store-Heroku.postman_collection.json` in postman to test with live url on heroku
- open `music-store-Heroku.postman_collection.json` and change host to localhost in postman to test with Localhost

Note: The tokens would expire in 24hrs, use updated token as described in the Athentication section.

### Error Handling

- 401 errors due to RBAC are returned as

```json
    {
      "code": "unauthorized",
      "description": "Permission not found."
    }
```


Other Errors are returned in the following json format:

```json
      {
        "success": "False",
        "error": 422,
        "message": "Unprocessable entity",
      }
```

The error codes currently returned are:

* 400 – bad request
* 401 – unauthorized
* 404 – resource not found
* 422 – unprocessable
* 500 – internal server error



### Endpoints

#### GET /albums

- General:
  - Returns all the albums.
  - Roles authorized : Customer and Manager.

- Sample:  `curl http://127.0.0.1:5000/albums`

```json
{
  "albums": [
    {
      "artist": "The Beatles",
      "id": 1,
      "title": "Abbey Road",
      "year": 1969
    },
    {
      "artist": "Pink Floyd",
      "id": 2,
      "title": "Dark Side of the Moon",
      "year": 1973
    }
  ],
  "success": true
}
```

#### GET /albums/\<int:id\>

- General:
  - Route for getting a specific album.
  - Roles authorized : Customer and Manager.

- Sample:  `curl http://127.0.0.1:5000/albums/1`

```json
{
  "album": {
    "artist": "The Beatles",
    "id": 1,
    "title": "Abbey Road",
    "year": 1969
  },
  "success": true
}
```

#### POST /albums

- General:
  - Creates a new album based on a payload.
  - Roles authorized : Manager.

- Sample: `curl http://127.0.0.1:5000/albums -X POST -H "Content-Type: application/json" -d '{
	"title": "Evolve",
	"year": "2017",
	"artist": "Imagine Dragons"
}'`

```json
{
  "album": {
    "artist": "Imagine Dragons",
    "id": 3,
    "title": "Evolve",
    "year": 2017
  },
  "success": true
}
```

#### PATCH /albums/\<int:id\>

- General:
  - Patches an album based on a payload.
  - Roles authorized : Manager.

- Sample: `curl http://127.0.0.1:5000/albums/2 -X POST -H "Content-Type: application/json" -d '{
	"year": "2006"
}'`

```json
{
  "album": {
    "artist": "Pink Floyd",
    "id": 2,
    "title": "Dark Side of the Moon",
    "year": 2006
  },
  "success": true
}
```


#### DELETE /albums/<int:id\>


- General:
  - Deletes an album by id given as the url parameter.
  - Roles authorized : Manager.

- Sample: `curl http://127.0.0.1:5000/albums/2 -X DELETE`

```json
{
    "deleted": 2,
    "success": true
}
```

#### GET /artists

- General:
  - Returns all the artists.
  - Roles authorized : Customer and Manager.

- Sample:  `curl http://127.0.0.1:5000/artists`

```json
{
  "artists": [
    {
      "id": 1,
      "name": "The Beatles"
    },
    {
      "id": 2,
      "name": "Pink Floyd"
    }
  ],
  "success": true
}
```

#### GET /artists/\<int:id\>

- General:
  - Route for getting a specific artist.
  - Roles authorized : Customer and Manager.

- Sample:  `curl http://127.0.0.1:5000/artists/1`

```json
{
  "artist": {
    "id": 1,
    "name": "The Beatles"
  },
  "success": true
}
```

#### POST /artists

- General:
  - Creates a new artist based on a payload.
  - Roles authorized : Manager.

- Sample: `curl http://127.0.0.1:5000/artists -X POST -H "Content-Type: application/json" -d '{
	"name": "Adele"
}
'`

```json
{
  "artist": {
    "id": 3,
    "name": "Adele"
  },
  "success": true
}
```

#### PATCH /artists/\<int:id\>

- General:
  - Patches an artist based on a payload.
  - Roles authorized : Manager.

- Sample: `curl http://127.0.0.1:5000/artists/3 -X POST -H "Content-Type: application/json" -d '{
	"name": "John Lenon"
}'`

```json
{
  "artist": {
    "id": 3,
    "name": "John Lenon"
  },
  "success": true
}
```


#### DELETE /artists/<int:id\>


- General:
  - Deletes an artist by id form the url parameter.
  - Roles authorized : Manager.

- Sample: `curl http://127.0.0.1:5000/artists/3 -X DELETE`

```json
{
    "deleted": 3,
    "success": true
}
```

## Authors
- Udacity provided setup details.
- Snehil Dahiya worked on the application.