
# Core API and Celery layered image file

FROM python:3.10 AS base
ENV PYTHONUNBUFFERED=1

RUN set -ex \
    \
    && apt-get update \
    && apt-get install postgis -y --no-install-recommends \
    && apt-get install gdal-bin -y --no-install-recommends \
    && apt-get install -y --no-install-recommends \
        ca-certificates curl netbase wget \
        git openssh-client \
        libcurl4-openssl-dev libpq-dev libjpeg-dev libpng-dev libsqlite3-dev libxml2-dev libyaml-dev \
        libtool libssl-dev build-essential python3-dev python3-virtualenv python3-cffi python3-pip libcairo2 \
        libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev \
        shared-mime-info \
    && apt-get install ffmpeg libsm6 libxext6  -y

COPY src/requirements.txt /app/

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY src /app

WORKDIR /app


FROM base AS api

COPY scripts/entrypoint.sh /entrypoint.sh
COPY scripts/wait.sh /wait.sh

EXPOSE 8000

RUN chmod +x /wait.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]

CMD gunicorn -c /app/config/gunicorn_config.py --log-level=${DJANGO_LOGLEVEL} --name ${SERVICE_VARIANT} --max-requests=1000 --timeout=100000000 --access-logfile - --error-logfile - --bind=0.0.0.0:8000 core.${WSGI_NAME}:application


FROM base AS celery

COPY scripts/wait.sh /wait.sh
COPY scripts/entrypoint-celery.sh /entrypoint-celery.sh

RUN chmod +x /wait.sh
RUN chmod +x /entrypoint-celery.sh

ENTRYPOINT [ "/entrypoint-celery.sh" ]

EXPOSE 8000
