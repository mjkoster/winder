import board
import digitalio
import rotaryio
import TM1637
import time

clockPin = board.D51
dioPin = board.D53
encoderaPin = board.D25
encoderbPin = board.D26
encoderButtonPin = board.D27

minValue = 88
maxValue = 108
precision = 1
initialValue = minValue
ratio = 0
pushedRatio = 1

button = digitalio.DigitalInOut(encoderButtonPin)
button.direction = digitalio.Direction.INPUT
encoder = rotaryio.IncrementalEncoder(encoderaPin, encoderbPin)
display = TM1637.TM1637Decimal(clockPin, dioPin)

if precision == 0:
    width = 4
else:
    width = 5

lastPosition = 0
value = initialValue

display.write(display.encode_string("8.8.8.8."))
time.sleep(1)
display.write(display.encode_string("{:0{w}.{p}f}".format(value, w = width, p = precision)))

while True:
    position = encoder.position
    if position != lastPosition:
        if button.value:
            value += (position - lastPosition) * 10**-precision * 10**ratio
        else:
            value += (position - lastPosition) * 10**-precision * 10**pushedRatio

        value = min(value, maxValue)
        value = max(value, minValue)

        display.write(display.encode_string("{:0{w}.{p}f}".format(value, w = width, p = precision)))
        lastPosition = position
    time.sleep(0.1)
