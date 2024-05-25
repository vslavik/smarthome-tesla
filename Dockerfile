FROM --platform=$BUILDPLATFORM golang:latest AS gotools
WORKDIR /app

COPY vehicle-command/ ./
ARG TARGETOS
ARG TARGETARCH
RUN GOOS=$TARGETOS GOARCH=$TARGETARCH GOBIN=/usr/local/bin \
    go get ./... && go build ./... && go install ./cmd/...


FROM python:3.12-slim-bookworm AS pyapp
WORKDIR /app

RUN apt-get update && apt-get -y install bluez

RUN pip3 install poetry
RUN poetry config virtualenvs.create false

COPY --from=gotools /usr/local/bin/* /usr/local/bin/

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY main.py ./

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
