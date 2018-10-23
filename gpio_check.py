import RPi.GPIO as GPIO
jumper=21

GPIO.setmode(GPIO.BCM)

GPIO.setup(jumper, GPIO.IN, pull_up_down=GPIO.PUD_UP)
exit(GPIO.input(jumper))
