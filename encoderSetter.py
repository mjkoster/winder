import board
import digitalio
import rotaryio
import TM1637
import time

class valueEncoder():
    def __init__ (self, clk, dio, enca, encb, butt, minValue=0, maxValue=100, precision=1, ratio=1 ,pratio=0, vinit=None):
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
            self._value = vinit
        else:
            self._value = self.minValue
        self.lastPosition = 0
        self.display.write(self.display.encode_string("8.8.8.8."))
        time.sleep(1)
        self.display.write(self.display.encode_string("{:{w}.{p}f}".format(self._value, w = self.width, p = self.precision)))

    def poll(self):
        self.position = self.encoder.position
        if self.position != self.lastPosition:
            if self.button._value:
                self._value += (self.position - self.lastPosition) * 10**-self.precision * 10**self.ratio
            else:
                self._value += (self.position - self.lastPosition) * 10**-self.precision * 10**self.pratio
            self._value = min(self._value, self.maxValue)
            self._value = max(self._value, self.minValue)
            self._value = round(self._value,self.precision)
            self.display.write(self.display.encode_string("{:{w}.{p}f}".format(self._value, w = self.width, p = self.precision)))
            self.lastPosition = self.position
            return True
        return False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, setValue):
        self._value = setValue


if __name__ == '__main__':
    clockPin = board.D51
    dioPin = board.D53
    encoderaPin = board.D25
    encoderbPin = board.D26
    encoderButtonPin = board.D27
    testSetter = valueEncoder(clockPin, dioPin, encoderaPin, encoderbPin, encoderButtonPin)

    while True:
        if testSetter.poll():
            print(testSetter.value())
        time.sleep(0.1)
