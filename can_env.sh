#!/bin/bash
export pythonenv=$HOME/candy

export scriptpath=$HOME/canlogger
export configpath=$HOME/canlogger/configs

export logdir=$HOME/logs
export poweroff_timer=30
export nocan_timeout=30
export kcd=$configpath/gm_global_a_hs.kcd
export canbus=can0

#Enable mqtt output
export mqtt=1

#Enable nbp output
export nbp=1
export nbp_csv=$configpath/gmlan_hs_nbp.nbp_csv
export serial=/dev/rfcomm0
