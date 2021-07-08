# Regex rules - parquet file

_An application using python and django framework to manage regex rules which are applied on a parquet type of file._
_The API is built by using the django rest framework library._

### How to setup

Install the requirements  
`pip install -r requirements.txt`

Run the migrations  
`python manage.py migrate`

Create a superuser  
`python manage.py createsuperuser`

The parquet file with name UK_outlet_meal.parquet.gzip must be in the same folder where the project exists.

### How to run

`python manage.py runserver`

### How to run with Docker

A sample Dockerfile is provided that will run the application in an isolated environment. The user can create a virtual environment before building the image. 

Build the image  
`docker build -t myproject .`

Run the image  
`docker run -it -p 8000:8000 <image_id>`

Create a superuser (inside the docker container)  
`docker exec -it <container name> bash`  
`python manage.py createsuperuser`

### How to run tests

`python manage.py test`

### Usage

The application consists of an API which can be accessed for CRUD operations concerning the regex patterns. Regex rules can be assigned to brands (At least one brand must exist in order to create a new rule). The second part consists of an application that can be used from a browser in order to search for results in the parquet file depending on regex patterns. 

### API Endpoints

_/api/brands/_  
Allowed methods:  
- GET  
Lists all brands from database
- POST  
Creates a new brand  
Required fields:   
    - _name_ (charfield)  

_/api/brands/id/_  
Allowed methods:
- PUT  
Updates a single brand  
Required value in the query string:  
    - _id_ (int)  
- DELETE  
Deletes a single brand  
Required value in the query string:  
    - _id_ (int)  

_/api/rules/_  
Allowed methods:  
- GET  
Lists all rules from database
- POST  
Creates a new rule  
Required fields:   
    - _description_ (charfield),  
    - _type\_of\_search_ (choices: _contains_, _match\_in_, _match\_out_),  
    - _pattern_ (charfield),  
    - _column_ (charfield),  
    - _brands_ (list with brand ids)    

_/api/rules/id/_  
Allowed methods:
- PUT  
Updates a single rule  
Required value in the query string:  
    - _id_ (int)  
- DELETE  
Deletes a single rule  
Required value in the query string:  
    - _id_ (int)  

### Web Application Endpoint and usage  

_/regex-patterns/_  
Allowed methods: GET, POST  
The web page for applying the regex rules to the data.  
Required fields:  
- _type of search_ (Default finds results that contain the input text, In and Out search for a whole word returning the results which have this word (In) or the results that don't have it(Out))  
- _column_ (provide the column on which the regex pattern will be applied to)  
- _pattern_ (the regex pattern)  
  
In the current page the user can choose the type of search (first dropdown menu field), the column of the parquet file in which the regex pattern will be applied to and the third field of the form is for defining the regex pattern to be used.  