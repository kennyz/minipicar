import RPi.GPIO as gpio

## 12 16 18 22
outPinNum = 12

gpio.setmode(gpio.BOARD)
gpio.setup(outPinNum, gpio.OUT)
gpio.output(outPinNum, gpio.LOW)

gpio.cleanup()
