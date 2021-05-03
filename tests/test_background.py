from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from main import app

client = TestClient(app)


def test_save_crawled_data():
    response = client.get("/background/saveCrawledUnsavedValue/")
    assert response.status_code == 200
    assert response.json() == "Reception completed"

