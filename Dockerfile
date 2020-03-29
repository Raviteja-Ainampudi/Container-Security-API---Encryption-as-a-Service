FROM python:3.7

# Create app directory
RUN mkdir /app
WORKDIR /app

# Install app dependencies
COPY ./requirements.txt ./

RUN pip install -r requirements.txt
RUN export FLASK_APP=/app/app.py

COPY . /app

EXPOSE 5000/tcp

CMD ["python3", "/app/app.py"]

