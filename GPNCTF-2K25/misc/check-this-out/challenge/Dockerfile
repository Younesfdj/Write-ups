FROM ghcr.io/astral-sh/uv:debian

COPY flag /flag

RUN useradd -m user
USER user
WORKDIR /home/user/app

COPY src/ /home/user/app

EXPOSE 1337

ENTRYPOINT ["uv", "run", "uvicorn", "main:app", "--port", "1337", "--host", "0.0.0.0"]
