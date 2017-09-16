import smbus
from time import sleep
from struct import unpack

bus = smbus.SMBus(1)
address = 0x03

debug = [20,17,19, False]

def send(data):
    """
    simple send function to send a list of values over I2c
    """
    # packet description
    # wanted temp, wanted soil moisture %, wanted temp range, LED power
    bus.write_i2c_block_data(address, 0, data)

def read():
    """
    this function receives packed data about all sensors, buttons and local variables
    """
    I2CPacket = []
    I2CPacket =  bus.read_i2c_block_data(address, 0, 19)
    hexdata = ''.join([chr(item) for item in I2CPacket])
#    print I2CPacket
    return unpack('fffb???bbb',hexdata)

def parse(packet):
    """
    method parses received data and assigns them to proper variables
    For debug purposes
    """

    # packet description
    # DS18B20 temp C, DHT temp C, DHT humidity %, soil moisture %, IN1 state (LED), IN2 state (PUMP), IN3 state (HEAT), wanted temperature, wanted soil moisture, temp offset
    DS18B20_temp = packet[0]
    DHT_temp = packet[1]
    DHT_hum = packet[2]
    soil_moist = packet[3]
    in1_state = packet[4]
    in2_state = packet[5]
    in3_state = packet[6]
    wanted_temp = packet[7]
    wanted_soil = packet[8]
    temp_offset = packet[9]

    print "External temperature: " + str(DS18B20_temp) + "C"
    print "Internal\ntemperature: {}C humidity: {}% soil moisture: {}%".format(DHT_temp, DHT_hum, soil_moist)
    print "LED: {} PUMP: {} HEAT: {}".format(in1_state, in2_state, in3_state)
    print "Set temperature: {}C Set moisture: {}% set temperature range: {}C".format(wanted_temp, wanted_soil, temp_offset)
