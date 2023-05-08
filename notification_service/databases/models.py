from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Device(Base):
    __tablename__ = "tokens"

    user_id = Column("user_id", Integer, nullable=False,primary_key=True)
    token = Column("token", String, nullable=False)
    
