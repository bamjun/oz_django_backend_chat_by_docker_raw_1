#!/bin/sh
set -e

echo "'django' service is up - executing command"
# envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
envsubst '\$STATIC_DIR' < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'
