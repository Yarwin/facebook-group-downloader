#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

su -m coneser -c "celery worker -A fbdownloader"
