# test service response
import requests
import pytest


@pytest.mark.asyncio
async def test_service_up() -> None:
    response = requests.get("http://0.0.0.0:8000/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_upload_file_real() -> None:
    # load a pdf file
    pdf_path = "tests/routes/test.pdf"
    with open(pdf_path, "rb") as file:
        # Create the files dictionary as FastAPI expects
        files = {
            "file": ("new_hr_policy.pdf", file, "application/pdf")
        }
        # Add db_name as a parameter
        params = {
            "db_name": "test"  # Using test database for testing
        }
        response = requests.post(
            "http://0.0.0.0:8000/upload/",
            files=files,
            params=params
        )
    print(response.json())
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_file_real() -> None:
    response = requests.delete(
        "http://0.0.0.0:8000/delete/",
        json={"document_id": "666666666666666666666666", "db_name": "test"}
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_generate_answer() -> None:
    response = requests.post(
        "http://0.0.0.0:8000/generate/",
        json={"query": "What is the capital of France?", "db_name": "test"}
    )
    assert response.status_code == 200
    assert "paris" in response.json()["response"].lower()
    print(response.json())
