FROM golang:1.24 as builder
COPY . /app
WORKDIR /app
RUN go build -o tidyQuic

FROM ubuntu:latest
COPY --from=builder /app/tidyQuic /app/tidyQuic
COPY server.crt /app/server.crt
COPY server.key /app/server.key
WORKDIR /app
RUN chmod +x tidyQuic

ENTRYPOINT ./tidyQuic