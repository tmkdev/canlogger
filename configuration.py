import os
import csv
import logging

configs={
    'scriptpath': '~/canlogger',
    'configpath': '~/canlogger/configs',
    'logdir': '~/logs',
    'poweroff_timer': 10,
    'nocan_timeout': 30,
    'kcd': '~/canlogger/configs/gm_global_a_hs.kcd',
    'canbus': 'can0',
    'mqtt_enable': 0,
    'nbp_enable': 0,
    #'serial': '/dev/rfcomm0'
    'ip': '192.168.4.1',
    'port': 35000,
}

nbp_kpis = {
    'tcs_active': None,
    'transmission_commanded_gear': None,
    'vehicle_dynamics_yaw_rate': 'Deg',
    'vdcs_over_understeer': None,
    'vdcs_active': None,
    'abs_active': None,
    'vehicle_stability_lateral_acceleration': 'g',
    'steering_wheel_angle': 'Deg',
    'accelerator_actual_position': '%',
    'boost_pressure_indication': '%',
    'platform_brake_position': '%',
    'engine_speed': 'RPM',
    }

transmission_gear_map = {
    0: -2,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    12: 1,
    13: 0,
    14: -1,
    15: 0,
}

for name in configs:
    if  name in os.environ:
        configs[name] = os.getenv(name)

logging.warning(configs)
