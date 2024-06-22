FROM --platform=$BUILDPLATFORM golang:latest AS gotools
WORKDIR /app

COPY vehicle-command/ ./
ARG TARGETOS
ARG TARGETARCH
ENV GOOS=$TARGETOS
ENV GOARCH=$TARGETARCH
RUN go get ./... && go build ./... && go install ./cmd/...


FROM python:3.12-slim-bookworm AS pyapp

RUN mkdir /data
ENV TESLA_HOME=/data

WORKDIR /app

RUN apt-get update && apt-get -y install bluez

RUN pip3 install poetry
RUN poetry config virtualenvs.create false

COPY --from=gotools /go/bin/* /usr/local/bin/

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY teslabox teslabox/

EXPOSE 8000
CMD ["uvicorn", "teslabox.main:app", "--host", "0.0.0.0", "--port", "8000"]
