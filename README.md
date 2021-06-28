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

A sample Dockerfile is provided that will run the application in an isolated environment 

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

The application consists of an API which can be accessed for CRUD operations concerning the regex patterns. Regex rules can be assigned to brands. The second part consists of an application that can be used from a browser in order to test regex patterns on the parquet file. 

### Endpoints

_/api/brands/_  
Allowed methods:  
- GET  
Lists all brands from database
- POST  
Creates a brand  

_/api/brands/id/_  
Allowed methods:
- PUT  
Updates a single brand  
- DELETE  
Deletes a single brand  

_/api/rules/_  
Allowed methods:  
- GET  
Lists all rules from database
- POST  
Creates a rule  

_/api/rules/id/_  
Allowed methods:
- PUT  
Updates a single rule  
- DELETE  
Deletes a single rule

_/regex-patterns/_  
Allowed methods: GET, POST  
The web page for applying the regex rules to the data.  
Required fields:  
- type of search (Default uses _contains_ from pandas, In and Out use _match_ for a whole word)  
- column (provide the column on which the regex pattern will be applied)  
- pattern (the regex pattern)