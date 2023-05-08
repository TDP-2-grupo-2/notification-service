from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

notification_router = APIRouter()

""" @notification_router.post("/", status_code=status.HTTP_201_CREATED)
def  """