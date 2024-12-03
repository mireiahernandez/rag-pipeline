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


## MongoDB structure
- `make up`automatically sets up a MongoDB instance with docker compose.
- The MongoDB instance has two databases: `test` and `tenant1`.
- `test` is used for testing purposes.
- `tenant1` is used for the main application. In the future, this should be extended to support multiple tenants.

Within each database, there are two collections: `documents` and `vectors`.
- `documents` contains the document metadata and the document chunks. Specifically, it contains the following fields:
    - `document_id`: the id of the document.
    - `text`: the text of the document.
    - `metadata`: the metadata of the document.
- `vectors` contains the vector embeddings of the document chunks. Specifically, it contains the following fields:
    - `parent_document_id`: the id of the document that the vector belongs to.
    - `vector_embedding`: the vector embedding.
    - `vector_id`: the id of the vector.
    - `metadata`: the metadata of the vector.
- The `metadata` object, which is present in both `documents` and `vectors` collections, contains the metadata of the document. Specifically, it contains the following fields:
    - `title`: the title of the document.
    - `author`: the author of the document.
    - `subject`: the subject of the document.
    - `keywords`: the keywords of the document.
    - `created_at`: the date the document was created.

## Document indexing pipeline
1. Upload a PDF document through the `/upload` endpoint.
2. The document is parsed and the metadata is extracted by the `DocumentParser` class.
3. The document is chunked into smaller chunks with an overlap of 128 words by the `Chunker` class.
4. Each chunk is embedded into a vector embedding by the `Embedder` class.
5. The document metadata and the vector embeddings are stored in the `documents` and `vectors` collections of the `tenant1` database.

## Document deletion pipeline
1. Delete a document through the `/delete` endpoint.
2. The document is deleted from the `documents` and `vectors` collections of the `tenant1` database.


## Query pipeline
### Retrieval
1. Query the app through the `/query` endpoint.
2. The query is embedded into a vector embedding by the `Embedder` class.
3. The query vector embedding is used to find the most similar vector embeddings in the `vectors` collection of the `tenant1` database. This is handled by the `DenseRetriever` class.
The indices of the top k most similar vectors are retrieved.
4. The text from the `documents` collection is retrieved using the indices of the top k most similar vectors.


### Nearest neighbor search with MongoDB
The nearest neighbor search is implemented using MongoDB's aggregation framework. This is done by taking the vector embedding and the query embedding and an aggregation pipeline to compute the cosine similarity. An aggregation pipeline is a specific flow of operations that processes, transforms, and returns results. In this case, the pipeline is used to compute the cosine similarity between the vector embedding and the query embedding.

This ensures that the nearest neighbor search is efficient and scalable.



## Generation pipeline
1. The query and the retrieved text are passed to the `Generator` class.
2. The `Generator` class generates a response using the query and the retrieved text.
