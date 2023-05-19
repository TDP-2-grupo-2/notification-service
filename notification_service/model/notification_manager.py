import datetime
import logging
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
import os
import requests
from requests.exceptions import ConnectionError, HTTPError
from sqlalchemy.orm import Session
from notification_service.database.notification_repository import get_device_token

from fastapi import Depends
from notification_service.database.database import get_postg_db

"""
{
    user_id
    user_name
    event_name
    event_date
    event_start_time
}
"""


def send_push_notification(token, title, message, event_id):
    try:
        token1 = "ExponentPushToken[_cSmg9FAJ7hMlQisW4YBn6]"
        data = {"notification_type": "reminder", "event_id": event_id}
        pushMessage = PushMessage(to=token1,title=title, body=message, data=data, priority='high',display_in_foreground=False)
        response = PushClient().publish(pushMessage)
        response.validate_response()
    except PushServerError as exc:
        logging.warning("There was an error sending a reminder of event: ", str(exc))
    except (ConnectionError, HTTPError) as exc:
        logging.warning("There was an error sending a reminder of event: ", str(exc))
    except Exception as exc:
        logging.warning("There was an error validating the response to notification reminder: ", str(exc))



def notify_users(users_to_notify: list,  db: Session = Depends(get_postg_db)):
    for user in users_to_notify:
        user_device_token = get_device_token(db, user['user_id'])
        if user_device_token is None:
            logging.warning("User " + user['user_id'] + " has no registered device.")
        else: 
            title = user['event_name']
            body = "Recordá que comienza mañana " + user['event_date'] + " a las " + user['event_start_time']
            logging.warning(user)
            logging.warning(user['event_id'])
            send_push_notification('user_device_token', title, body, user['event_id'])
