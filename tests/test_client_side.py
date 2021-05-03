from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from main import app

client = TestClient(app)


def test_get_recent_data():
    response = client.get("/mostRecentData/")
    assert response.status_code == 200

