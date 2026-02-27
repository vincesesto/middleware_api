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
curl http://0.0.0.0:8000/xml/1
```
