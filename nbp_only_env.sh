#!/bin/bash
export pythonenv=$HOME/candy

export scriptpath=$HOME/canlogger
export configpath=$HOME/canlogger/configs

export logdir=$HOME/logs
export kcd=${configpath}/gm_global_a_hs.kcd
export canbus=can0

#Enable mqtt output
export mqtt_enable=0

#Enable nbp output
export nbp_enable=1
export serial=/dev/rfcomm0
