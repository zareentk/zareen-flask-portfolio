#!/bin/bash

NAME="Zareen"
EMAIL="zareenk@outlook.com"
NUM=$RANDOM
url=http://localhost:5000/api/timeline_post

#echo "$NUM"
options='--fail --connect-timeout 3 --retry 0 -s -o /dev/null -w %{http_code}'
last_req="$(curl $options -X POST ${url} -d "name="$NAME"&email="$EMAIL"&content=This is a random timeline post, with a random number:"$NUM"")"
retVal=$?

if [ $last_req == 200 ]; then
	echo "The post was added successfully"
else
	echo "It was unsuccessful"
fi
response=$(curl -s -w "\n%{http_code}" ${url})

var="$(curl -s -X GET ${url} | jq '.timeline_post[0]')"

echo "$var"
