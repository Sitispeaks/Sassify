# docker/web/Dockerfile
FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade Pillow
RUN pip install -r requirements.txt
COPY . /app
RUN chmod +x /app/entrypoint.sh
