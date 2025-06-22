FROM gcc:15.1.0 as build

WORKDIR /
COPY lib.c main.c /
RUN gcc lib.c main.c -o chall -fno-stack-protector -fno-pie -no-pie

FROM ubuntu:25.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update --fix-missing && apt-get upgrade -y
RUN apt-get install -y adduser socat

ARG FLAG=FLAG{Congrats_on_solving_now_do_on_remote}
RUN echo "$FLAG" > /flag

RUN adduser --comment "CTF user" ctf

WORKDIR /home/ctf/

COPY --from=build chall .

EXPOSE 8443
USER ctf

ENTRYPOINT ["socat", "-v", "TCP-LISTEN:8443,fork,reuseaddr", "EXEC:./chall"]
