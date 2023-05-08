# Define image to use
FROM python:3.11.0-alpine

#define workdir
WORKDIR /app

# Copy requirements for installation
COPY ./requirements.txt ./

# Install dependencies
RUN /usr/local/bin/python -m pip install --upgrade pip 
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt

RUN mkdir notification_service
COPY ./notification_service/ ./notification_service

# Define volume to sync changes automatically
VOLUME /notification_service

EXPOSE 8082

# Run app
ENTRYPOINT uvicorn notification_service.main:app --port 8082 --host 0.0.0.0 --reload
