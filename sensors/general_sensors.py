from sensors.sensors_utils import AbstractSensor
# code adapted for TybeeHive, got from https://gist.github.com/But2ene/a6ebbb1fbcf1dd11f0aec9cf649c97af

import RPi.GPIO as GPIO


def createBoolList(size=8):
    ret = []
    for i in range(size):
        ret.append(False)
    return ret

def initialize_power_pins(pin_vcc, pin_gnd):
    GPIO.setmode(GPIO.BOARD)
    # initializaion of VVC and GND pin
    GPIO.output(pin_vcc, GPIO.HIGH)
    GPIO.output(pin_gnd, GPIO.LOW)


class HX711:
    def __init__(self, dout, pd_sck, gain=128):
        # set the pins for clock (SCK) and data (DOUT)
        self.PD_SCK = pd_sck
        self.DOUT = dout

        # set the state of the pins
        GPIO.setup(self.PD_SCK, GPIO.OUT)
        GPIO.setup(self.DOUT, GPIO.IN)

        # set default charasteristics
        self.GAIN = 0
        self.OFFSET = 0
        self.SCALE = 1
        self.lastVal = 0

        # set gain
        self.set_gain(gain)

    def is_ready(self):
        return GPIO.input(self.DOUT) == 0

    def set_gain(self, gain):
        if gain is 128:
            self.GAIN = 1
        elif gain is 64:
            self.GAIN = 3
        elif gain is 32:
            self.GAIN = 2

        GPIO.output(self.PD_SCK, False)
        self.read()

    def read(self):
        while not self.is_ready():
            # print("WAITING")
            pass

        dataBits = [createBoolList(), createBoolList(), createBoolList()]

        for j in range(2, -1, -1):
            for i in range(7, -1, -1):
                GPIO.output(self.PD_SCK, True)
                dataBits[j][i] = GPIO.input(self.DOUT)
                GPIO.output(self.PD_SCK, False)

        # set channel and gain factor for next reading
        # for i in range(self.GAIN):
        GPIO.output(self.PD_SCK, True)
        GPIO.output(self.PD_SCK, False)

        # check for all 1
        if all(item == True for item in dataBits[0]):
            return self.lastVal

        bits = []
        for i in range(2, -1, -1):
            bits += dataBits[i]

        self.lastVal = int(''.join(map(str, bits)), 2)
        return self.lastVal

    def read_average(self, times=3):
        sum = 0
        for i in range(times):
            sum += self.read()

        return sum / times

    def get_value(self, times=3):
        return self.read_average(times) - self.OFFSET

    def get_units(self, times=3):
        """
        :param times: number of measure to calculate the mean on
        :return: value measured, after scale and tare
        """
        return self.get_value(times) / self.SCALE

    def tare(self, times=15):
        sum = self.read_average(times)
        self.set_offset(sum)

    def set_scale(self, scale):
        self.SCALE = scale

    def set_offset(self, offset):
        self.OFFSET = offset

    def power_down(self):
        GPIO.output(self.PD_SCK, False)
        GPIO.output(self.PD_SCK, True)

    def power_up(self):
        GPIO.output(self.PD_SCK, False)

############# EXAMPLE


# #pins
# pin_data = 13
# pin_sck = 12
#
# # set values (do not change)
# gain = 128 # gain of the sensor, must be either 128, 64 or 32
#
# # calibrated values
# scale = 1 # set it beforehand to get the result in the right unit
# offset = 0 # TODO : find a proper solution to save calibrated values to sensor_enabled.py
# n_repetition = 3 # number of times the sensor does the measure to get an average value, useful for accuracy and denoising



class TemperatureSensor(AbstractSensor):
    def __init__(self, sensor_id, pin,
                 pin_vcc, pin_gnd,
                 name=''):
        import Adafruit_Pyhon_DHT
        super(TemperatureSensor, self).__init__(sensor_id, name)
        self.sensor_type = Adafruit_Pyhon_DHT.DHT22
        self.pin = pin
        # initialization of power pins
        initialize_power_pins(pin_vcc, pin_gnd)

    def callback(self):
        moisture, temperature = Adafruit_Python_DHT.read(self.sensor_type, self.pin)
        if temperature is None:
            return 0
        return temperature


class MoistureSensor(AbstractSensor):
    def __init__(self, sensor_id, pin,
                 pin_vcc, pin_gnd,
                 name=''):
        import Adafruit_Pyhon_DHT
        super(MoistureSensor, self).__init__(sensor_id, name)
        self.sensor_type = Adafruit_Pyhon_DHT.DHT22
        self.pin = pin
        # initialization of power pins
        initialize_power_pins(pin_vcc, pin_gnd)

    def callback(self):
        moisture, temperature = Adafruit_Python_DHT.read(self.sensor_type, self.pin)
        if moisture is None:
            return 0
        return moisture


class WeightSensor(AbstractSensor):
    def __init__(self, sensor_id,
                 pin_data, pin_sck, pin_vcc, pin_gnd,
                 gain=128, n_repetition=3, scale=1, offset=0,
                 name=''):
        super(WeightSensor, self).__init__(sensor_id, name)
        # initialization of power pins
        initialize_power_pins(pin_vcc, pin_gnd)
        # initialization of interface with load cell amplifier HX711
        self.weight_sensor = HX711(dout=pin_data, pd_sck=pin_sck, gain=gain)
        self.weight_sensor.set_scale(scale=scale)
        self.weight_sensor.set_offset(offset=offset)
        self.n_repetition = n_repetition


        # hardware start
        self.weight_sensor.power_down()
        self.weight_sensor.power_up()

    def callback(self):
        return self.weight_sensor.get_units(self.n_repetition)
