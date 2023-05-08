from fastapi.testclient import TestClient
from fastapi import status
from test import config
from notification_service.app import app

session = config.init_postg_db(app)

client = TestClient(app)



def test_when_registering_a_new_device_it_registers_correctly():
    device_token = "ExponentPushToken[yEMHoKK54im4ig2FbyU1Rm]"
    response = client.post("/notifications/new_user", json={'user_id': 1, 'token': device_token})
    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    data = data["message"]

    expected = {
        "user_id": 1,
        "token": device_token,
    }
    assert data["user_id"] == expected["user_id"]
    assert data["token"] == expected["token"] 