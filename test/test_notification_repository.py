from fastapi.testclient import TestClient
from fastapi import status
from test import config
from notification_service.database.notification_schema import DeviceBase, RegisterDevice
from notification_service.database.notification_repository import get_device_token, register_device

session = config.init_postg_db()

def test_when_registering_a_new_device_it_returns_the_token_correctly():
    device_token = "ExponentPushToken[yEMHoKK54im4ig2FbyU1Rm]"
    register_device(session, 1, device_token)

    expected = {
        "user_id": 1,
        "device_token": device_token,
    }
    returned_token = get_device_token(session, 1)
    assert returned_token == device_token 