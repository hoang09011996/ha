ARG IMAGE_TAG=latest
FROM kestra/kestra:$IMAGE_TAG

RUN mkdir -p /app/plugins && \
  apt-get update -y && \
  apt-get install -y --no-install-recommends golang && \
  apt-get install -y pip && \
  pip install pandas==2.0.3 requests==2.31.0


RUN /app/kestra plugins install \
  io.kestra.plugin:plugin-notifications:LATEST \
  io.kestra.storage:storage-gcs:LATEST \
  io.kestra.plugin:plugin-gcp:LATEST
