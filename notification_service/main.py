import uvicorn
from notification_service.app import app
from notification_service.triggers.notification_trigger import send_notifications_previous_day
from notification_service.database.database import init_database
from apscheduler.schedulers.background import BackgroundScheduler
import logging

engine = init_database() 
logging.basicConfig(level=logging.INFO)

scheduler = BackgroundScheduler()
scheduler.add_job(func=send_notifications_previous_day, args=[engine], trigger='interval', seconds=30)
#scheduler.add_job(func=send_notifications_previous_day, trigger='cron', hour=7, minute=00)

scheduler.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)