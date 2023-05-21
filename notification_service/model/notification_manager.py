import datetime
import logging
from fastapi import status
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

db_users = Depends(get_postg_db)
logging.warning(db_users)

def send_push_notification(token, title, message, data):
    logging.warning('llega biennnnnnnn!!!!!!!!!!!!!!!111111')
    try:
        pushMessage = PushMessage(to=token,title=title, body=message, data=data, priority='high',display_in_foreground=False)
        response = PushClient().publish(pushMessage)
        response.validate_response()
        return token
    except PushServerError as exc:
        logging.warning("There was an error sending a reminder of event: ", str(exc))
        return None
    except (ConnectionError, HTTPError) as exc:
        logging.warning("There was an error sending a reminder of event: ", str(exc))
        return None
    except Exception as exc:
        logging.warning("There was an error validating the response to notification reminder: ", str(exc))
        return None



def notify_users_about_modifications(db, users_to_notify, modifications):
    notified_users = []
    for user in users_to_notify:
        user_device_token = get_device_token(db, user)
        if user_device_token is None:
            logging.warning("User " + user + " has no registered device.")
        else:
            logging.warning('EL USER LO ENCUENTRA')
            data = {"notification_type": "modifications", "event_id": modifications['event_id'], "modifications": modifications['modifications']}
            result = send_push_notification(user_device_token, modifications['event_name'], modifications['message'], data)
            if result is not None:
                notified_users.append(user)



def notify_users(users_to_notify: list,  db: Session = Depends(get_postg_db)):
    logging.warning('lño que devuelve db', type(db))
    for user in users_to_notify:
        user_device_token = get_device_token(db, user['user_id'])
        if user_device_token is None:
            logging.warning("User " + user['user_id'] + " has no registered device.")
        else: 
            title = user['event_name']
            body = "Recordá que comienza mañana " + user['event_date'] + " a las " + user['event_start_time']
            logging.warning(user)
            logging.warning(user['event_id'])
            data = {"notification_type": "reminder", "event_id": user['event_id']}

            send_push_notification('user_device_token', title, body, data)



def notify_modifications(modifications: dict, db):
    # request para obtener usuarios a notificar
    response = requests.get(f"https://event-service-solfonte.cloud.okteto.net/events/reservations/event/{modifications['event_id']}/attendees")

    if response.status_code == status.HTTP_200_OK:
        users_to_notify = response.json()['message']
        logging.warning('NOTIFICAR', users_to_notify)
        notify_users_about_modifications(db, users_to_notify, modifications)
    else:
        logging.error('received response status', response.status_code)