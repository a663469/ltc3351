#!/bin/bash
#
tmp=$(date +%j-%H-%M-%S)".txt"

ssh pi@192.168.71.159 "sudo i2cdump -y 1 0x09 w" > $tmp

cat $tmp
echo $tmp

python2 ./start.py $tmp > description_$tmp
cat description_$tmp

mkdir ./dumps/$(date +%j-%H-%M-%S)
mv ./*.txt ./dumps/$(date +%j-%H-%M-%S)/
