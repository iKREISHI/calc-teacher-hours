FROM python:3.13-slim-bookworm

WORKDIR /app

# Установка русской локали
ENV LANG=ru_RU.UTF-8 \
    LANGUAGE=ru_RU.UTF-8 \
    LC_ALL=ru_RU.UTF-8 \
    TZ=Asia/Yekaterinburg

RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    tzdata \
    && echo "ru_RU.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen ru_RU.UTF-8 \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    cron \
    libpq-dev \
    dos2unix \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./*.toml ./*.lock ./.python-version ./
RUN uv sync
COPY ./src /app

COPY docker/django/entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh
RUN chmod +x /entrypoint.sh