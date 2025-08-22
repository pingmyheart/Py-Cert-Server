FROM python:3-alpine

#Build Args
ARG SERVICE_VERSION
ARG SERVICE_NAME

# Service env variable
ENV ARTIFACT_NAME=$SERVICE_NAME
ENV ARTIFACT_VERSION=$SERVICE_VERSION

RUN mkdir -p /opt/$ARTIFACT_NAME

WORKDIR /opt/$ARTIFACT_NAME

COPY . .
RUN pip install -r requirements.txt &&  \
    pip install gunicorn

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]