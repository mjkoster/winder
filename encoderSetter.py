import board
import digitalio
import rotaryio
import TM1637
import time

class valueSetter():
    def __init__ (self, clk, dio, enca, encb, butt, minValue=0, maxValue=100, precision=1, ratio=1 ,pratio=0, vinit=None, ):

        self.display = TM1637.TM1637Decimal(clk, dio)
        self.encoder = rotaryio.IncrementalEncoder(enca, encb)
        self.button = digitalio.DigitalInOut(butt)
        self.button.direction = digitalio.Direction.INPUT

        self.minValue = minValue
        self.maxValue = maxValue
        self.precision = precision
        self.ratio = ratio
        self.pratio = pratio

        if self.precision == 0:
            self.width = 4
        else:
            self.width = 5

        if vinit != None:
            self.value = vinit
        else:
            self.value = self.minValue

        self.lastPosition = 0

        self.display.write(self.display.encode_string("8.8.8.8."))
        time.sleep(1)
        self.display.write(self.display.encode_string("{:0{w}.{p}f}".format(self.value, w = self.width, p = self.precision)))

    def poll(self):
        self.position = self.encoder.position
        if self.position != self.lastPosition:
            if self.button.value:
                self.value += (self.position - self.lastPosition) * 10**-self.precision * 10**self.ratio
            else:
                self.value += (self.position - self.lastPosition) * 10**-self.precision * 10**self.pratio

            self.value = min(self.value, self.maxValue)
            self.value = max(self.value, self.minValue)
            self.value = round(self.value,self.precision)

            self.display.write(self.display.encode_string("{:0{w}.{p}f}".format(self.value, w = self.width, p = self.precision)))
            self.lastPosition = self.position
            return True
        return False

    def currentValue(self):
        return self.value

if __name__ == '__main__':

    clockPin = board.D51
    dioPin = board.D53
    encoderaPin = board.D25
    encoderbPin = board.D26
    encoderButtonPin = board.D27

    minValue = 0
    maxValue = 100
    precision = 1
    ratio = 0
    pushedRatio = 1
    initialValue = minValue

    testSetter = valueSetter(clockPin, dioPin, encoderaPin, encoderbPin, encoderButtonPin, minValue, maxValue, precision, ratio, pushedRatio)
    while True:
        if testSetter.poll():
            print(testSetter.currentValue())
        time.sleep(0.1)
