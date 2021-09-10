import time
import RPi.GPIO as GPIO
import smbus #sudo apt-get install i2c-tools, python-smbus. Also enable i2c in raspi-config

MUX_0_PIN = 17 #GPIO 17, but pin 11 on the header. LED attached; will be on when pin is high
MUX_1_PIN = 27 #GPIO 27, but pin 13 on the header. LED attached; will be on when pin is high

I2C_BUS_ID = 1
CAP_I2C_ADDR = 0x60

def i2c_setup(bus_id=I2C_BUS_ID):

    bus = smbus.SMBus(bus_id)
    return bus

def i2c_read_cap(bus, address=CAP_I2C_ADDR):


def setup_gpio_pins(m0_pin=MUX_0_PIN, m1_pin=MUX_1_PIN):
    GPIO.setup(m0_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(m1_pin, GPIO.OUT, initial=GPIO.LOW)

def enable_matching_circuit(circuit_num, m0_pin=MUX_0_PIN, m1_pin=MUX_1_PIN):
    '''
    circuit number should be within 0,3. We'll use modulo 4 anyway
    '''

    assert circuit_num >0, 'use a positive number (integer) between 0 and 3'

    m0_value = GPIO.HIGH if circuit_num & 0x1 == 1 else GPIO.LOW
    m1_value = GPIO.HIGH if circuit_num & 0x2 == 1 else GPIO.LOW

    GPIO.output(m0_pin, m0_value)
    GPIO.output(m1_pin, m1_value)



if __name__ == "__main__":
    setup_gpio_pins()
    i2c_setup()

    #do a startup sequence to show all the options
    enable_matching_circuit(3)
    time.sleep(.5)
    enable_matching_circuit(2)
    time.sleep(.5)
    enable_matching_circuit(1)
    time.sleep(.5)
    enable_matching_circuit(0)

    while True:
        input_str = input('Input matching circuit to configure (an integer)')
        try:
            matching_circuit_num = int(input(input_str))
            enable_matching_circuit(matching_circuit_num)
        except ValueError:
            print('Invalid matching circuit; try an integer between 0 and 3')
