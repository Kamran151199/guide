#!/bin/sh

# Entry point for the Celery Worker container.

echo "Waiting for database to be ready..."
/wait.sh -t 10 -h ${POSTGRESQL_HOST} -p ${POSTGRESQL_PORT} -- echo "postgresql is up" &&
  /wait.sh -t 10 -h ${REDIS_HOST} -p ${REDIS_PORT} -- echo "redis is up" &&
  exec "$@"
