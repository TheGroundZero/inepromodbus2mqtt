#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Read modbus data from Inepro N380CT
# https://ineprometering.com/wp-content/uploads/2023/04/N380-CT-0516-short-user-manual-V1.14-3.pdf
#
# https://sequr.be
#

import argparse
import logging
import minimalmodbus
#import paho.mqtt.client as mqtt
import serial
import sys
import time

parser = argparse.ArgumentParser()
# parser.add_argument("-b", "--broker", dest="broker",
#                     type=str,
#                     default="localhost",
#                     help="Address of MQTT broker")
# parser.add_argument("-p", "--port", dest="port",
#                     type=int,
#                     default=1883,
#                     help="Port of MQTT broker")
# parser.add_argument("-u", "--user", dest="mqttuser",
#                     type=str,
#                     default="mqttuser",
#                     help="User to connect to MQTT broker")
# parser.add_argument("-s", "--pass", dest="mqttpass",
#                     type=str,
#                     default="",
#                     help="Password to connect to MQTT broker")
# parser.add_argument("-c", "--client", dest="client_id",
#                     type=str,
#                     default="",
#                     help="Client ID to identify to MQTT broker")
parser.add_argument("-d", "--device", dest="device",
                    type=str,
                    default="/dev/serial0",
                    help="Path to serial modbus device")
args = parser.parse_args()

# broker = args.broker
# port = args.port
# mqttuser = args.mqttuser
# mqttpass = args.mqttpass
# client_id = args.client_id
device = args.device

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# def mqtt_connect(broker, port, mqttuser, mqttpass, client_id):
#   # callback for mqtt
#   def on_connect(client, userdata, flags, rc):
#     logging.debug("MQTT connected with result code {}".format(rc))

#   def on_disconnect(client, userdata, rc):
#     logging.debug("MQTT disconnected with result code {}".format(rc))
#     client.loop_stop()

#   client = mqtt.Client(client_id)
#   client.username_pw_set(mqttuser, mqttpass)
#   client.on_connect = on_connect
#   client.on_disconnect = on_disconnect
#   client.connect_async(broker, port, 60)
#   return client

# def mqtt_subscribe(client):
#   def on_message(client, userdata, msg):
#     logging.debug("[ {} ({})] {}".format(msg.topic, msg.qos, msg.payload))

#   client.subscribe("meters/inepro/command", 2)
#   client.on_message = on_message

# def mqtt_publish(client, data):
#   def on_publish(client, userdata, mid):
#     logging.debug("[{}] published ({})".format(mid, userdata))

#   def send(client, topic, payload="", qos=2, retain=False):
#     res = client.publish(topic, payload, qos, retain)
#     res.wait_for_publish()
#     logging.debug("[{}] status: {} - {}".format(res.mid, res.rc, "Published" if res.is_published() else "Failed"))
#     time.sleep(0.5)

#   client.on_publish = on_publish
#   for k, v in data.items():
#     send(client, "meters/inepro/{}".format(k), v)

def modbus_connect(device):
  instrument = minimalmodbus.Instrument(port=device, slaveaddress=1) # Set to inverter's address
  instrument.serial.baudrate = 9600
  instrument.serial.parity   = serial.PARITY_EVEN
  #instrument.serial.bytesize = 8
  #instrument.serial.stopbits = 1
  #instrument.serial.timeout  = 3
  instrument.debug = True
  return instrument

def modbus_read(instrument):
  timestamp = time.time()
  ####################################################################################################
  # 0x4000
  serialno = instrument.read_long(16384, functioncode=3, signed=True)
  logging.info("{:<25s}{:15n}".format("Serial No.", serialno))
  # 0x4002
  metercode = instrument.read_register(16386, number_of_decimals=0, functioncode=3, signed=True)
  logging.info("{:<25s}{:15n}".format("Meter code", metercode))
  # 0x4003
  meterid = instrument.read_register(16387, number_of_decimals=0, functioncode=3, signed=True)
  logging.info("{:<25s}{:15n}".format("Meter ID", meterid))
  # 0x4004
  baudrate = instrument.read_register(16388, number_of_decimals=0, functioncode=3, signed=True)
  logging.info("{:<25s}{:15n}".format("Baud rate", baudrate))
  # 0x4005
  protoversion = instrument.read_float(16389, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n}".format("Protocol version", protoversion))
  # 0x4007
  softversion = instrument.read_float(16391, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n}".format("Software version", softversion))
  # 0x4009
  hardversion = instrument.read_float(16393, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n}".format("Software version", hardversion))
  # 0x400B
  meteramps = instrument.read_long(16395, functioncode=3, signed=True)
  logging.info("{:<25s}{:15n} A".format("Meter Amps", meteramps))
  # 0x4011
  parity = instrument.read_register(16401, number_of_decimals=0, functioncode=3, signed=True)
  logging.info("{:<25s}{:15n}".format("Parity Settings", parity))
  # 0x401B
  softversioncrc = instrument.read_long(16411, functioncode=3, signed=True)
  logging.info("{:<25s}{:15n}".format("Software version CRC", softversioncrc))
  # 0x400F
  combination = instrument.read_register(16399, number_of_decimals=0, functioncode=3, signed=True)
  logging.info("{:<25s}{:15n}".format("Combination Code", combination))
  ####################################################################################################
  # 0x5000
  voltage = instrument.read_float(20480, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} V".format("Voltage", voltage))
  # 0x5002
  l1voltage = instrument.read_float(20482, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} V".format("L1 Voltage", l1voltage))
  # 0x5004
  l2voltage = instrument.read_float(20484, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} V".format("L2 Voltage", l2voltage))
  # 0x5006
  l3voltage = instrument.read_float(20486, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} V".format("L3 Voltage", l3voltage))
  # 0x5008
  gridfreq = instrument.read_float(20488, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} Hz".format("Grid Frequency", gridfreq))
  # 0x500A
  current = instrument.read_float(20490, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} A".format("Current", current))
  # 0x500C
  l1current = instrument.read_float(20492, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} A".format("L1 Current", l1current))
  # 0x500E
  l2current = instrument.read_float(20494, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} A".format("L2 Current", l2current))
  # 0x5010
  l3current = instrument.read_float(20496, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} A".format("L3 Current", l3current))
  # 0x5012
  activepower = instrument.read_float(20498, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kW".format("Active Power", activepower))
  # 0x5014
  l1activepower = instrument.read_float(20500, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kW".format("L1 Active Power", l1activepower))
  # 0x5016
  l2activepower = instrument.read_float(20502, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kW".format("L2 Active Power", l2activepower))
  # 0x5018
  l3activepower = instrument.read_float(20504, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kW".format("L3 Active Power", l3activepower))
  # 0x501A
  reactivepower = instrument.read_float(20506, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kVa".format("Reactive Power", reactivepower))
  # 0x501C
  l1reactivepower = instrument.read_float(20508, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kVa".format("L1 Reactive Power", l1reactivepower))
  # 0x501E
  l2reactivepower = instrument.read_float(20510, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kVa".format("L2 Reactive Power", l2reactivepower))
  # 0x5020
  l3reactivepower = instrument.read_float(20512, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kVa".format("L3 Reactive Power", l3reactivepower))
  # 0x5022
  apparentpower = instrument.read_float(20514, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} KVa".format("Apparent Power", apparentpower))
  # 0x5024
  l1apparentpower = instrument.read_float(20516, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} KVa".format("L1 Apparent Power", l1apparentpower))
  # 0x5026
  l2apparentpower = instrument.read_float(20518, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} KVa".format("L2 Apparent Power", l2apparentpower))
  # 0x5028
  l3apparentpower = instrument.read_float(20520, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} KVa".format("L3 Apparent Power", l3apparentpower))
  # 0x502A
  powerfactor = instrument.read_float(20522, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n}".format("Power Factor", powerfactor))
  # 0x502C
  l1powerfactor = instrument.read_float(20524, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n}".format("L1 Power Factor", l1powerfactor))
  # 0x502E
  l2powerfactor = instrument.read_float(20526, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n}".format("L2 Power Factor", l2powerfactor))
  # 0x5030
  l3powerfactor = instrument.read_float(20528, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n}".format("L3 Power Factor", l3powerfactor))
  ####################################################################################################
  # 0x6000
  activeenergy = instrument.read_float(24576, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kWh".format("Active Energy", activeenergy))
  # 0x6006
  l1activeenergy = instrument.read_float(24582, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kWh".format("L1 Active Energy", l1activeenergy))
  # 0x6008?
  l2activeenergy = instrument.read_float(24584, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kWh".format("L2 Active Energy", l2activeenergy))
  # 0x600A ?
  l3activeenergy = instrument.read_float(24586, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kWh".format("L3 Active Energy", l3activeenergy))
  # 0x600C
  forwactiveenergy = instrument.read_float(24588, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kWh".format("Forward Active Energy", forwactiveenergy))
  # 0x600E ?
  l1forwactiveenergy = instrument.read_float(24590, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kWh".format("L1 Forward Active Energy", l1forwactiveenergy))
  # 0x6010 ?
  l2forwactiveenergy = instrument.read_float(24592, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kWh".format("L2 Forward Active Energy", l2forwactiveenergy))
  # 0x6012 ?
  l3forwactiveenergy = instrument.read_float(24594, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kWh".format("L3 Forward Active Energy", l3forwactiveenergy))
  # 0x6018
  revactiveenergy = instrument.read_float(24600, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kWh".format("Reverse Active Energy", revactiveenergy))
  # 0x601A ?
  l1revactiveenergy = instrument.read_float(24602, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kWh".format("L1 Reverse Active Energy", l1revactiveenergy))
  # 0x601C ?
  l2revactiveenergy = instrument.read_float(24604, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kWh".format("L2 Reverse Active Energy", l2revactiveenergy))
  # 0x601E ?
  l3revactiveenergy = instrument.read_float(24606, number_of_registers=2, functioncode=3)
  logging.info("{:<25s}{:15n} kWh".format("L3 Reverse Active Energy", l3revactiveenergy))

  data = {
    'online': timestamp,
    'serialno': serialno,
    'metercode': metercode,
    'meterid': meterid,
    'baudrate': baudrate,
    'protoversion': protoversion,
    'softversion': softversion,
    'hardversion': hardversion,
    'meteramps': meteramps,
    'parity': parity,
    'softversioncrc': softversioncrc,
    'combination': combination,
    'voltage': voltage,
    'l1voltage': l1voltage,
    'l2voltage': l2voltage,
    'l3voltage': l3voltage,
    'gridfreq': gridfreq,
    'current': current,
    'l1current': l1current,
    'l2current': l2current,
    'l3current': l3current,
    'activepower': activepower,
    'l1activepower': l1activepower,
    'l2activepower': l2activepower,
    'l3activepower': l3activepower,
    'reactivepower': reactivepower,
    'l1reactivepower': l1reactivepower,
    'l2reactivepower': l2reactivepower,
    'l3reactivepower': l3reactivepower,
    'apparentpower': apparentpower,
    'l1apparentpower': l1apparentpower,
    'l2apparentpower': l2apparentpower,
    'l3apparentpower': l3apparentpower,
    'powerfactor': powerfactor,
    'l1powerfactor': l1powerfactor,
    'l2powerfactor': l2powerfactor,
    'l3powerfactor': l3powerfactor,
    'activeenergy': activeenergy,
    'l1activeenergy': l1activeenergy,
    'l2activeenergy': l2activeenergy,
    'l3activeenergy': l3activeenergy,
    'forwactiveenergy': forwactiveenergy,
    'l1forwactiveenergy': l1forwactiveenergy,
    'l2forwactiveenergy': l2forwactiveenergy,
    'l3forwactiveenergy': l3forwactiveenergy,
    'revactiveenergy': revactiveenergy,
    'l1revactiveenergy': l1revactiveenergy,
    'l2revactiveenergy': l2revactiveenergy,
    'l3revactiveenergy': l3revactiveenergy
  }

  return data

def main():
  try:
    print(minimalmodbus._get_diagnostic_string())
    #mqttc = mqtt_connect(broker, port, mqttuser, mqttpass, client_id)
    #mqtt_subscribe(mqttc)
    #mqttc.loop_start()
    modc = modbus_connect(device)
    data = modbus_read(modc)
    print(data)
    #time.sleep(2)
    #mqtt_publish(mqttc, data)
    #time.sleep(2)
    #mqttc.loop_stop()
    #mqttc.disconnect()

  except TypeError as err:
    logging.error("TypeError:\n{}".format(err))

  except ValueError as err:
    logging.error("ValueError:\n{}".format(err))

  except minimalmodbus.NoResponseError as err:
    logging.error("Modbus no response:\n{}".format(err))

  except serial.SerialException as err:
    logging.error("SerialException:\n{}".format(err))

  except Exception as err:
    logging.error("Exception:\n{}".format(err))

if __name__ == "__main__":
  main()
