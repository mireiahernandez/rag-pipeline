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
2. Uplaod endpoint. Upload a PDF file to the app, there are two ways to do this:
    - Upload through request:
    ```python
    import requests
    response = requests.post("http://0.0.0.0:8000/upload/", files={"file": ("test.pdf", open("tests/routes/test.pdf", "rb"), "application/pdf")})
    print(response.json())
    ```
    - Upload through UI:
        - Go to `http://0.0.0.0:8000/docs`
        - Click on `Try it out` under `upload_pdf`
        - Upload the file `tests/routes/test.pdf`
        - Click on `Execute`
        - See the response
## Running tests
1. Run `make install` to install the dependencies in the local environment
2. Run `make test` to run the tests (`make test` also runs `make install`)
