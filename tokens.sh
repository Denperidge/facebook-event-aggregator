#!/bin/bash

# A script that gets & saves facebook tokens locally

function prompt {
    if [ -f "$1" ]; then
    
}

echo "[0]"
echo "[1]"
read -p "Select token: " token

case $token in

  1)
    prompt userid
    prompt useraccesstoken
    url="https://graph.facebook.com/{your-user-id}/accounts?access_token={user-access-token}"
    ;;
esac

curl -i -X GET 