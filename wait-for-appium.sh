#!/bin/bash
# wait-for-appium.sh

set -e
cmd="pytest ${PYTEST_PARAM}"
until curl appium-server:4723; do
  >&2 echo "Appium is unavailable - sleeping"
  sleep 1
done

>&2 echo "Appium is up - executing command"

exec $cmd
