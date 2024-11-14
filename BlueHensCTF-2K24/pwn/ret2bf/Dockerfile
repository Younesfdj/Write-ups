FROM ubuntu:22.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install socat gcc make gcc gcc-multilib g++-multilib mono-mcs socat patchelf && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /pwn
COPY entry.sh /entry.sh
COPY pwnme /pwn/pwnme
COPY flag.txt /pwn/flag.txt

RUN groupadd ctf

RUN useradd -G ctf --home=/pwn pwnuser
RUN useradd -G ctf --home=/pwn pwnflag

RUN chmod 444 /pwn/flag.txt

EXPOSE 34347
CMD ["./entry.sh"]
