#!/bin/bash
export pythonenv=$HOME/candy

export scriptpath=$HOME/canlogger
export configpath=$HOME/canlogger/configs

export logdir=$HOME/logs
export kcd=${configpath}/gm_global_a_hs.kcd
export canbus=can0

#Enable mqtt output
export mqtt_enable=1

#Enable nbp output
export nbp_enable=1
#export serial=/dev/rfcomm0
export ip=192.168.4.1
export port=35000
