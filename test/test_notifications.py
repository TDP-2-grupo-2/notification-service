from fastapi.testclient import TestClient
from fastapi import status
from notification_service.utils.jwt_handler import create_access_token
from test import config
from notification_service.app import app

session = config.init_postg_db(app)

client = TestClient(app)

def test_when_registering_a_new_device_it_registers_correctly():
    device_token = "ExponentPushToken[yEMHoKK54im4ig2FbyU1Rm]"
    user_token = create_access_token("1", 'attendee')
    response = client.post("/notifications/new_user", headers={"Authorization": f"Bearer {user_token}"}, json={'device_token': device_token})
    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    data = data["message"]

    expected = {
        "user_id": 1,
        "token": device_token,
    }
    assert data["user_id"] == expected["user_id"]
    assert data["token"] == expected["token"] 

def test_when_registering_twice_a_new_device_with_the_same_token_it_returns_the_same_device():
    device_token = "ExponentPushToken[yEMHoKK54im4ig2FbyU1Rm]"
    user_token = create_access_token("1", 'attendee')
    client.post("/notifications/new_user", headers={"Authorization": f"Bearer {user_token}"}, json={'device_token': device_token})
    response = client.post("/notifications/new_user", headers={"Authorization": f"Bearer {user_token}"}, json={'device_token': device_token})
    data = response.json()
    data = data["message"]

    expected = {
        "user_id": 1,
        "token": device_token,
    }
    assert data["user_id"] == expected["user_id"]
    assert data["token"] == expected["token"] 
    assert config.get_amount_devices(session) == 1


def test_when_registering_twice_a_new_device_but_with_the_different_tokens_it_returns_the_last_device():
    device_token = "ExponentPushToken[yEMHoKK54im4ig2FbyU1Rm]"
    new_device_token = "ExponentPushToken[KLMJoKK54im5ig2FbyU1PK]"

    user_token = create_access_token("1", 'attendee')
    client.post("/notifications/new_user", headers={"Authorization": f"Bearer {user_token}"}, json={'device_token': device_token})
    response = client.post("/notifications/new_user", headers={"Authorization": f"Bearer {user_token}"}, json={'device_token':new_device_token})
    data = response.json()
    data = data["message"]

    expected = {
        "user_id": 1,
        "token": new_device_token,
    }
    assert data["user_id"] == expected["user_id"]
    assert data["token"] == expected["token"] 
    assert config.get_amount_devices(session) == 1