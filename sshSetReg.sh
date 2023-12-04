#!/bin/bash
#
ssh pi@192.168.71.159 "sudo i2cset -r -y 1 0x09 $1 $2 w"
# ssh pi@192.168.71.159 "sudo i2cget -y 1 0x09 $1 w"


