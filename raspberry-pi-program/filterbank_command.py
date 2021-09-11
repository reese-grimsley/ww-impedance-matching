import time
import RPi.GPIO as GPIO
import smbus #sudo apt-get install i2c-tools, python-smbus. Also enable i2c in raspi-config

MUX_0_PIN = 11 #GPIO 17, but pin 11 on the header. LED attached; will be on when pin is high
MUX_1_PIN = 13 #GPIO 27, but pin 13 on the header. LED attached; will be on when pin is high

I2C_BUS_ID = 1
CAP_I2C_ADDR = 0x60

def i2c_setup(bus_id=I2C_BUS_ID):

    bus = smbus.SMBus(bus_id)
    time.sleep(.5)
    return bus

def i2c_read_cap(bus, address=CAP_I2C_ADDR):
    reg_addr = 0 #datashet says we don't need a register address..
    read_bytes = bus.read_byte_data(address, reg_addr)
    return read_bytes

def i2c_write_cap_value_volatile(bus, value, address=CAP_I2C_ADDR):
    assert value >=0 and value < 0x200 #9 bit value, unsigned
    byte_1 = 0 | ((value & 0x100) >> 8) # first config byte. LSbit is most signicant of 9-bit value
    byte_2 = value & 0xFF #second config byte; lower 8 bits of cap value
    bus.write_byte_data(address, byte_1, byte_2)

def i2c_write_cap_value_nonvolatile(*args, **kwargs):
    raise NotImplementedError()


def setup_gpio_pins(m0_pin=MUX_0_PIN, m1_pin=MUX_1_PIN):
    GPIO.setwarnings(False) # this is probably a bad idea...
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(m0_pin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(m1_pin, GPIO.OUT, initial=GPIO.HIGH)

def enable_matching_circuit(circuit_num, m0_pin=MUX_0_PIN, m1_pin=MUX_1_PIN):
    '''
    circuit number should be within 0,3. We'll use modulo 4 anyway
    '''
    assert circuit_num >=0, 'use a positive number (integer) between 0 and 3'

    m0_value = GPIO.HIGH if circuit_num & 0x1 == 0x1 else GPIO.LOW
    m1_value = GPIO.HIGH if circuit_num & 0x2 == 0x2 else GPIO.LOW

    GPIO.output(m0_pin, m0_value)
    GPIO.output(m1_pin, m1_value)

if __name__ == "__main__":
    setup_gpio_pins()
    bus = i2c_setup()

    #do a startup sequence to show all the options
    enable_matching_circuit(3)
    time.sleep(.5)
    enable_matching_circuit(2)
    time.sleep(.5)
    enable_matching_circuit(1)
    time.sleep(.5)
    enable_matching_circuit(0)

    while True:
        print('CLI:')
        print('  - "z (integer)" will activate matching circuit')
        print('  - "c (integer)" will set a value for the digitally tuned capacitor (value space TBD)')
        print('  - "r" will display information about the current configuation')
        input_str = input('Input matching circuit to configure (an integer)\n')
        print()
        try:
            if input_str[0] == 'z':
                matching_circuit_num = int(input_str[1:])
                enable_matching_circuit(matching_circuit_num)
            elif input_str[0] =='c':
                cap_value = int(input_str[1:])
                i2c_write_cap_value_volatile(bus, cap_value)
        except ValueError as e:
            print('Invalid value; try an integer between 0 and 3')
            print(e)
