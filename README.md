# Agentic RAG Pipeline with custom vectorstore in MongoDB

This is an MVP of an agentic RAG pipeline with a custom vectorstore in MongoDB.
It is built using FastAPI and MongoDB, as well as Docker.
It uses custom indexing, retrieval, and generation pipelines, as well as an agentic framework to query the knowledge base.
The RAG agent supports answering complex questions that require multiple steps to answer.


## Installation and running the app

### Running the app
1. Install docker in your machine. In Mac you should install docker desktop: https://www.docker.com/products/docker-desktop/
2. Clone the repo
3. Run `make up` on your terminal to run the app. What this does is:
    - Starts a MongoDB docker container in your local port 27018. This container will be used as the vector database. It has persistent storage in your machine, so it will keep the data even after the container is stopped.
    - Starts the FastAPI docker container, which runs the app on port 8000.
The MongoDB container will not contain any database by default. When uploading a document, you should provide the name of the database to use. This will create the database if it does not exist.
The structure of the MongoDB database is explained in the [MongoDB structure](#mongodb-structure) section.

### Usage
The app provides three endpoints:

1. **Upload endpoint.** This endpoint allows you to upload a PDF file to the app. It will automatically index the document and store the chunks in the vector database.
The input is a Pydantic object with two fields:
    - `file`: the PDF file to upload.
    - `db_name`: the name of the database to use. Here you can customize your database name, which in production would be the name of the tenant. This allows you to have multiple databases in the same MongoDB instance.
The output is a Pydantic object with the following fields:
    - `parent_document_id`: the id of the document in the `documents` collection.
    Example:
    ```python
    import requests
    with open("tests/routes/test.pdf", "rb") as file:
        response = requests.post(
            "http://0.0.0.0:8000/upload/",
            files={"file": ("test.pdf", file, "application/pdf")},
            params={"db_name": "tenant1"})
    ```

2. **Delete endpoint.** This endpoint allows you to delete a document from the app. It will delete the document from the `documents` and `vectors` collections of the `tenant1` database.
The input is a Pydantic object with two fields:
    - `document_id`: the id of the document to delete.
    - `db_name`: the name of the database to use.
You should provide the `document_id` of the document to delete. This is the id of the document in the `documents` collection. The vector embeddings associated with the document are also deleted automatically.
The output is a Pydantic object with the following fields:
    - `message`: the message of the response.
    Example:
    ```python
    import requests
    response = requests.delete(
        "http://0.0.0.0:8000/delete/",
        json={"document_id": "1234567890", "db_name": "tenant1"})
    ```

3. **Generate endpoint.** This endpoint allows you to query the app with a natural language question. It will use the RAG agent to answer the question.
The input is a Pydantic object with two fields:
    - `query`: the question to query the app with.
    - `db_name`: the name of the database to use.
The output is a Pydantic object with the following fields:
    - `response`: the answer to the question.
    - `queries`: the queries made to the knowledge base to answer the question. This is also a Pydantic object with the following fields:
        - `query`: the question made to the knowledge base.
        - `retrieved_ids`: the ids of the documents retrieved from the knowledge base.
        This field is useful to understand how the answer was retrieved, and to provide citations if needed in the frontend.
    Example:
    ```python
    import requests
    response = requests.post(
        "http://0.0.0.0:8000/generate/",
        json={"query": "What were the R&D costs?", "db_name": "tenant1"})
    ``` 
Alternatively, use the FASTAPI UI by going to `http://0.0.0.0:8000/docs` and clicking on `Try it out` under the various endpoints.

### Running tests
The code is highly modularized and designed to be extended to support more features. To this end, each module of the code is also fully tested using pytest.
When adding new features, such as new sparse retrievers, or parsing of new file types, you should also add tests for the new functionality.

To run the tests, first create a Python virtual environment and install the dependencies with `make install`.
You can run the tests with `make test`.

## Design and documentation

### Code Structure
[TODO]: add code structure diagram

### Development pipeline
[TODO]: add explanation of the development pipeline, testing, etc.


### MongoDB structure
Within each database, there are two collections: `documents` and `vectors`.
- `documents` contains the original documents uploaded to the app. This is kept for referencing and also in case the documents should be re-indexed if the indexing strategy changes. Currently re-indexing is not supported, but it would be easy to add another endpoint for this purpose. Specifically, it contains the following fields:
    - `document_id`: the id of the document.
    - `text`: the text of the document.
    - `metadata`: the metadata of the document.
    - `_id`: the id of the MongoDB object (generated by MongoDB)
- `vectors` contains the vector embeddings of the document chunks. Specifically, it contains the following fields:
    - `parent_document_id`: the id of the document that the vector belongs to.
    - `vector_embedding`: the vector embedding.
    - `vector_id`: the id of the vector.
    - `metadata`: the metadata of the vector.
    - `_id`: the id of the MongoDB object (generated by MongoDB)
- The `metadata` object, which is present in both `documents` and `vectors` collections, contains the metadata of the document. Specifically, it contains the following fields:
    - `title`: the title of the document.
    - `author`: the author of the document.
    - `description`: the description of the document.
    - `keywords`: the keywords of the document.
    - `created_at`: the date the document was created.


### Indexing pipeline
[TODO]: add indexing pipeline diagram

1. Upload a PDF document through the `/upload` endpoint.
2. The document is parsed and the metadata is extracted by the `DocumentParser` class.
3. The document is chunked into smaller chunks with an overlap of 128 words by the `Chunker` class.
4. Each chunk is embedded into a vector embedding by the `Embedder` class.
5. The document metadata and the vector embeddings are stored in the `documents` and `vectors` collections of the `tenant1` database.


### Retrieval pipeline
[TODO]: add retrieval pipeline diagram

### Retrieval
1. Query the app through the `/query` endpoint.
2. The query is embedded into a vector embedding by the `Embedder` class.
3. The query vector embedding is used to find the most similar vector embeddings in the `vectors` collection of the `tenant1` database. This is handled by the `DenseRetriever` class.
The indices of the top k most similar vectors are retrieved.
4. The text from the `documents` collection is retrieved using the indices of the top k most similar vectors.


#### Nearest neighbor search with MongoDB
The nearest neighbor search is implemented using MongoDB's aggregation framework. This is done by taking the vector embedding and the query embedding and an aggregation pipeline to compute the cosine similarity. An aggregation pipeline is a specific flow of operations that processes, transforms, and returns results. In this case, the pipeline is used to compute the cosine similarity between the vector embedding and the query embedding.

This ensures that the nearest neighbor search is efficient and scalable.



### Generation pipeline: Agentic RAG
[TODO]: add generation pipeline diagram

