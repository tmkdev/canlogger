# canlogger
Pi canbus logger with file, mqtt and numeric broadcast protocol (Track Addict nbp) outputs

Needed to complete:

Pi - with Wifi and or bluetooth. (I usxze a pi zero W)

RS485 CAN Hat or other MCP2515 based CANBUS adapters. Or even USB ones would work if you set them up for CAN0. 

GPS or RTC for setting dates without internet. GPS logs if you run the full logger.

12V->5V power supply. A good 2A phone charger would work.

A OBD connector to connect the CANBUS shield to you car. 

The KCD supplied works for GM Global A architectures (Works on my 2009 Cadillac. Your experince will be different). Won't work for any others. You can use one you find or hack/make and adjust the configuration.py to export parameters you want. 

I take ( 0 | none | no ) responsibilty if you blow up your car or your car's computer. Be careful. You have been warned! 

Layout:

Car -> CANBUS -> CANHAT -> Pi -> NPB Protocol over Bluetooth or Wifi -> Track Addict
                              -> MQTT over Wifi -> Phone app for MQTT
                              -> Raw candump logs
