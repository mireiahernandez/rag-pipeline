# test service response
import requests
import pytest

@pytest.mark.asyncio
async def test_service_up():
    response = requests.get("http://0.0.0.0:8000/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

