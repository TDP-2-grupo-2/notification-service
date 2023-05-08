import uvicorn
from notification_service.app import app
from notification_service.database import notifications_database


notifications_database.init_database()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)