from notification_service.app import app
from notification_service.database import database, models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def init_postg_db(app=None):
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, echo=False, connect_args={"check_same_thread": False}
    )

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    if app is not None: 
        app.dependency_overrides[database.get_postg_db] = override_get_db
    return TestingSessionLocal()

def get_amount_devices(session):
    return session.query(models.Device).count()