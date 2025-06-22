# docker build -t no-nc . && docker run -p 127.0.0.1:1337:1337 -t no-nc
FROM debian:12 AS build

RUN apt-get update -y && apt-get install libc6-dev gcc -y --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY nc.c nc.c

ARG FLAG=GPNCTF{fake_flag}
RUN gcc nc.c -o /nc -DRAW_FLAG="$FLAG"

FROM debian:12

RUN apt-get update -y && apt-get install socat -y --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY --from=build /nc nc
EXPOSE 1337

ENTRYPOINT [ "socat", "tcp-l:1337,reuseaddr,fork", "EXEC:./nc,stderr" ]
