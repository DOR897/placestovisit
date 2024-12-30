
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(abspath(__file__))))


 
from main import app


client = TestClient(app)


@pytest.fixture
def db():
    from main import engine
    from sqlalchemy.orm import Session

    # Create a new SQLite in-memory database for testing
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()




def test_create_location():
    # Test creating a new location
    data = {
        "name": "Test Location",
        "description": "Test description"
    }
    response = client.post("/locations", json=data)
    assert response.status_code == 200
    location = response.json()
    assert location["name"] == data["name"]
    assert location["description"] == data["description"]

def test_get_location():
    # Test retrieving a location
    location_id = 1  # Assuming there is a location with ID 1 in the database
    response = client.get(f"/locations/{location_id}")
    assert response.status_code == 200
    location = response.json()
    assert location["id"] == location_id

def test_update_location():
    # Test updating a location
    location_id = 1  # Assuming there is a location with ID 1 in the database
    data = {
        "name": "Updated Location",
        "description": "Updated description"
    }
    response = client.put(f"/locations/{location_id}", json=data)
    assert response.status_code == 200
    location = response.json()
    assert location["name"] == data["name"]
    assert location["description"] == data["description"]

def test_delete_location():
    # Test deleting a location
    location_id = 1  # Assuming there is a location with ID 1 in the database
    response = client.delete(f"/locations/{location_id}")
    assert response.status_code == 200
    result = response.json()
    assert result["message"] == "Location deleted successfully."

