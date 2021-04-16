#!/bin/sh

SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")
echo $SCRIPTPATH


#curl -H 'Cache-Control: no-cache' http://localhost:8000/api/
#echo
#curl -H 'Cache-Control: no-cache' http://localhost:8000/api/users/
#echo
#echo "--------------------------------"

for i in {001..021}
do
  r1=$(curl -X POST -H 'Cache-Control: no-cache' -s -F "file_uploaded=@${SCRIPTPATH}/fish${i}.sb3" http://localhost:8000/api/upload/)
  r2=$(echo $r1 | jq -r '.')
  a=$(echo $r2 | jq -r '.Abstraction')
  p=$(echo $r2 | jq -r '.Parallelization')
  l=$(echo $r2 | jq -r '.Logic')
  s=$(echo $r2 | jq -r '.Synchronization')
  f=$(echo $r2 | jq -r '.FlowControl')
  u=$(echo $r2 | jq -r '.UserInteractivity')
  d=$(echo $r2 | jq -r '.DataRepresentation')

  s=`expr $a + $p + $l + $s + $f + $u + $d`

  printf "fish${i}.sb3 "
  printf "%02d " $s
  echo $r2

done
