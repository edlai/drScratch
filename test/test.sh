#!/bin/sh

curl -H 'Cache-Control: no-cache' http://localhost:8000/api/
echo ""
curl -H 'Cache-Control: no-cache' http://localhost:8000/api/users/
echo ""
