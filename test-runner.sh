#!/bin/bash -e
# script to connect to the OpenSTF farm and run automated Appium tests
# you can pass a serial number of a device if you already know it ahead of time

# only count the last command that failed
set -e
set -u
set -o pipefail

# cleanup function
function cleanup {
    if [[ -z "${SERIAL:-}" ]];
    then
        echo "==============================================="
        echo "              Stopping containers              "
        echo "==============================================="
        docker stop $PYSLIM
        docker-compose down
        docker volume rm app
    else
        echo "==============================================="
        echo "              Stopping Appium                  "
        echo "==============================================="
        docker-compose down
        echo "==============================================="
        echo "              Stopping remote ADB              "
        echo "==============================================="
        docker exec $PYSLIM python /app/utilities/openstf_connection.py --disconnect $SERIAL
        docker stop $PYSLIM
        echo "==============================================="
        echo "              Removing volume                  "
        echo "==============================================="
        docker volume rm app

    fi
}
trap cleanup EXIT

while getopts 's:p:h:' OPTION; do
    case "$OPTION" in
        s)
            DEVICE_SERIAL="$OPTARG"
            ;;
        p)
            PYTEST_PARAM="$OPTARG"
            ;;
        h)
            HOCKEY_PARAM="$OPTARG"
            ;;
        ?)
            echo "script usage: [-s deviceserial] [-p ""pytest params""] [-h ""--store||--rc --version (optional)""] "
            exit 1
            ;;
    esac
done

echo "==============================================="
echo "              Creating volume                  "
echo "==============================================="
docker volume create --name app

echo "==============================================="
echo "              Starting pyslim                  "
echo "==============================================="
docker-compose build pyslim
PYSLIM=$(docker run -dt -v app:/app/app --rm pyslim)

# Getting a device from OpenSTF
if [[ -z "${DEVICE_SERIAL:-}" ]];
then
    SERIAL=$(docker exec $PYSLIM python /app/utilities/openstf_connection.py --serial)
    echo "checked out $SERIAL"
else
    SERIAL=$DEVICE_SERIAL
fi

# get the device URL
DEVICE_URL=$(docker exec $PYSLIM python utilities/openstf_connection.py --connect $SERIAL)
export DEVICE_URL

# build the containers for appium & python
echo "==============================================="
echo "              Starting Appium                  "
echo "==============================================="
APPIUMSERVER=$(docker-compose run -v app:/root/app -d appium-server)

# download apk from HockeyApp
echo "==============================================="
echo "              Downloading app                  "
echo "==============================================="
if [[ -z "${HOCKEY_PARAM:-}" ]];
then
    docker exec $PYSLIM python /app/utilities/hockey.py --store
else
    docker exec $PYSLIM python /app/utilities/hockey.py $HOCKEY_PARAM
fi
echo "Done"

# build the containers for appium & python
echo "==============================================="
echo "              Installing app                   "
echo "==============================================="
docker exec $APPIUMSERVER adb devices
INSTALLED=$(docker exec $APPIUMSERVER adb shell pm list packages | grep INSERT.ANDROID.APPNAME)
if [[ -z $INSTALLED ]];
then
    docker exec $APPIUMSERVER adb install /root/app/app.apk
else
    docker exec $APPIUMSERVER adb uninstall INSERT.ANDROID.APPNAME && docker exec $APPIUMSERVER adb install /root/app/app.apk
fi

# build the containers for appium & python
echo "==============================================="
echo "              Starting tests                   "
echo "==============================================="
if [[ -z "${PYTEST_PARAM:-}" ]];
then
    docker-compose run pyslim
else
    docker-compose run -e "PYTEST_PARAM=$PYTEST_PARAM" pyslim
fi
