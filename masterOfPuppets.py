import smbus
from time import sleep
from struct import unpack
import sqlite3 as lite

bus = smbus.SMBus(1)
address = 0x03

con = None
con = lite.connect('db.sqlite3')

def sendToDB():
    cur = con.cursor()
    data = read()
    cur.execute("update main_app_sensors set value=%s where id=0" %data[0])
    cur.execute("update main_app_sensors set value=%s where id=1" %data[1])
    cur.execute("update main_app_sensors set value=%s where id=2" %data[2])
    cur.execute("update main_app_sensors set value=%s where id=3" %data[3])
    cur.execute("update main_app_buttons set state=%s where id=1" %1 if data[5] == True else 0)
    cur.execute("update main_app_buttons set state=%s where id=2" %1 if data[6] == True else 0)
    con.commit()

def getFromDB():
    cur = con.cursor()
    data = []
    for val in (4,5,6):
        cur.execute("select value from main_app_sensors where id=%s" % val)
        data.append(cur.fetchone()[0])
    cur.execute("select state from main_app_buttons where id=0")
    data.append(True if cur.fetchone()[0] == 1 else False)
    send(data)


debugSendPacket = [15,20,1, True]

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
    # packet description
    # DS18B20 temp C, DHT temp C, DHT humidity %, soil moisture %, IN1 state (LED), IN2 state (PUMP), IN3 state (HEAT), wanted temperature, wanted soil moisture, temp offset
    I2CPacket = []
    I2CPacket =  bus.read_i2c_block_data(address, 0, 19)
    hexdata = ''.join([chr(item) for item in I2CPacket])
    return unpack('fffb???bbb',hexdata)

while 1:
    try:
        getFromDB()
        sendToDB()
        print "ding"
        sleep(2)
    except KeyboardInterrupt:
        con.close()
        break
    except:
        print "Zjebalo sie"
        sleep(2)
        continue
