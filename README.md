## Notes - Release v1.0.0

# How I worked through this
1. Created a basic app that responds to a health check endpoint
2. Set up pipenv for dependency management
3. Set up pipenv to also run the app with a dev command
4. Created a Dockerfile to build the app into a container
5. Create a simple endpoint that returns the xml data from the middleware xml-api


## Testing the app
# How to run the app from the command line
```
pipenv run ivicorn app.main:app --reload --host 0.0.0.0 --port 8000
pipenv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
# Clone the repo and run
```
pip install --user pipenv
pipenv sync
pipenv run dev
```
# Or build the docker image
```
docker build -t middle-api:local .
```
# And then run
```
docker run --rm -p 8000:8000 middle-api:local
```
# Testing the endpoints with curl
```
curl http://0.0.0.0:8000/health
curl http://0.0.0.0:8000/xml/1
curl http://0.0.0.0:8000/xml/2

# Output
# curl http://0.0.0.0:8000/xml/1
#<?xml version="1.0" encoding="UTF-8"?>
#<Data>
#	<id>1</id>
#	<name>MWNZ</name>
#	<description>..is awesome</description>
#</Data>

```

## Notes - Release v2.0.0

# How I worked through this
1. Investigate how to read the OpenAPI spec from the middleware xml-api and understand the structure of the URL request and the response needed
2. Workout what needs to be returned as part of the JSON response and how to use Python to simplify this
3. Investigate using xmltodict module to convert the XML response into a Python dictionary
4. Update the app to return the JSON response with the relevant data from the XML response

## Testing the app
Testing the app is the same as before, but now we need to use a new url and is provided with a new response structure. The endpoints to test are:
```
curl http://0.0.0.0:8000/health
{"ok":true}

curl http://0.0.0.0:8000/v1/companies/1
{"id":1,"name":"MWNZ","description":"..is awesome"}

curl http://0.0.0.0:8000/v1/companies/2
{"id":2,"name":"Other","description":"....is not"}

curl http://0.0.0.0:8000/v1/companies/99
{"error":"not_found","error_description":"Not found"}
```
