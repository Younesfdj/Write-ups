# docker build -t nasa . && docker run -p 127.0.0.1:1337:1337 -t nasa
FROM ubuntu:latest@sha256:b59d21599a2b151e23eea5f6602f4af4d7d31c4e236d22bf0b62b86d2e386b8f

RUN apt-get update -y && apt-get install socat libasan8 gdb -y --no-install-recommends \
&& apt-get clean && rm -rf /var/lib/apt/lists/*

COPY nasa nasa

ARG FLAG=GPNCTF{fake_flag}
RUN echo "$FLAG" > /flag

EXPOSE 1337

ENTRYPOINT [ "socat", "tcp-l:1337,reuseaddr,fork", "EXEC:./nasa,stderr" ]
