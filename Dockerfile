FROM python:3.7

RUN apt-get update && apt-get dist-upgrade && apt-get auto-remove

# Create app directory
RUN mkdir /app
WORKDIR /app

# Install app dependencies
COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000/tcp

CMD ["python3", "/app/app.py"]

