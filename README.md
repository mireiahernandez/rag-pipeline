# rag_pipeline

## Running the app

1. Install docker in your machine
2. Run `make up` to run the app

## Endpoints

1. Root endpoint. Python query to test if the app is running: 
```python
    import requests
    response = requests.get("http://0.0.0.0:8000/")
    print(response.json())
```

## Running tests
1. Run `make install` to install the dependencies in the local environment
2. Run `make test` to run the tests (`make test` also runs `make install`)
