#! /bin/bash

trap ctrl_c SIGINT

function ctrl_c() {
	echo "Cat fed"
	sleep 1
	echo "0=70%" > /dev/servoblaster
	sleep 1
	killall servod
	exit 0
}

if [ -z "$1" ]; then
	echo "Usage: ./feed.sh <angle>"
	exit 1
fi

echo "Feeding the cat"
./servod --p1pins=8 &> /dev/null

while true
do
	echo "0=$((50-$1))%" > /dev/servoblaster
	sleep 1
	echo "0=$((50+$1))%" > /dev/servoblaster
	sleep 1
done
