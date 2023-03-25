FROM python:3.8-slim-buster
WORKDIR /app
VOLUME /classsifier-volume
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src/. . 
CMD [ "uvicorn", "api:app"]