# test service response
import requests
import pytest


@pytest.mark.asyncio
async def test_upload_endpoint_multiple_files() -> None:
    # load pdf files
    pdf_paths = [
        "examples/pdfs/ACME_Earnings.pdf",
        "examples/pdfs/hr_manual.pdf"  # Add another PDF for testing
    ]
    files = []
    for pdf_path in pdf_paths:
        files.append(
            (
                "files",
                (pdf_path.split("/")[-1], open(pdf_path, "rb"), "application/pdf")  # noqa: E501
            )
        )

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
    assert len(response.json()) == len(pdf_paths)


@pytest.mark.asyncio
async def test_upload_endpoint_single_file() -> None:
    # load pdf files
    pdf_path = "examples/pdfs/ACME_Earnings.pdf"
    files = [
        (
            "files",
            (pdf_path.split("/")[-1], open(pdf_path, "rb"), "application/pdf")
        )
    ]
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
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_delete_endpoint() -> None:
    response = requests.delete(
        "http://0.0.0.0:8000/delete/",
        json={"document_id": "666666666666666666666666", "db_name": "test"}
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_generate_endpoint() -> None:
    response = requests.post(
        "http://0.0.0.0:8000/generate/",
        json={"query": "What is the capital of France?", "db_name": "test"}
    )
    assert response.status_code == 200
    assert "paris" in response.json()["response"].lower()
    print(response.json())
