FROM python:3.9-slim-buster

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install --no-cache-dir  -r requirements.txt

EXPOSE 5000
CMD ["python", "/app/noa-web-app.py"]