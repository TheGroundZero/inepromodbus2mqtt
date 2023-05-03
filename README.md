# IneproModbus2MQTT

Python script to read out measurements by the Inepro N380CT over modbus and share them via MQTT.

## Intro

My EV charger has a loadbalancing feature that ensures the total power draw of my charger + the rest of my household doesn't exceed a safe level.
Should there be a high energy demand in the house, the EV charger will decrease the charge output to keep everything balanced.
To do this, current measuring clamps around the house's grid feed are connected to the Inepro N380CT and it communicates over modbus to the charger.

Using this script, I can get a copy of the data being sent to the charger, which I can then import in e.g. Home Assistant or Grafana for visualisation.

TODO:

- Provide a `write` function that allows me change the config of the N380CT.
  Completing the feature set the device supports.
- Add a feature to send out spoofed modbus data.
  E.g. to make the charger _think_ my energy consumption is high and have it slow down charging.

For more info, check the linked [blog post][blog].

## Installation

I am using a Raspberry Pi Zero W with a [RS485 Pi HAT][pihat].

Following the [user manual][n380ct_manual] for the Inepro N380CT I hooked up the A, B and GND connections from the HAT
to terminals 22, 23, and 21 respectively.
5V power was initially provided via a USB charger connected to a nearby socket, but I later switched to a DIN-mounted 5V constant voltage driver.
Alternatively, you could use a 12V to 5V buck converter and hook it up to the existing 12V power supply powering the N380CT.

Check which serial path the device has received on your system and pass it to the script via the `--device` parameter.
In my case (and I set it as default) this was `/dev/serial0`.

## MQTT setup

Create a MQTT user for your system and pass the information to the script using the `--user`, `--pass`, and `--client` parameters.

```bash
mosquitto_passwd /mosquitto/config/mqttuser mqtt_n380ct
# Password:
# Reenter password:
```

Don't forget to also pass the (IP) address and (optionally) the port of your MQTT broker using the `--broker` and `--port` params respectively.

## Usage

```bash
python3 inepromodbus2mqtt/inepromodbus2mqtt.py -h

usage: inepromodbus2mqtt.py [-h] [-b BROKER] [-p PORT] [-u MQTTUSER] [-s MQTTPASS]
                            [-c CLIENT_ID] [-d DEVICE]

optional arguments:
  -h, --help            show this help message and exit
  -b BROKER, --broker BROKER
                        Address of MQTT broker
  -p PORT, --port PORT  Port of MQTT broker
  -u MQTTUSER, --user MQTTUSER
                        User to connect to MQTT broker
  -s MQTTPASS, --pass MQTTPASS
                        Password to connect to MQTT broker
  -c CLIENT_ID, --client CLIENT_ID
                        Client ID to identify to MQTT broker
  -d DEVICE, --device DEVICE
                        Path to serial modbus device
```

[blog]: https://sequr.be "Sequr.be"
[pihat]: https://www.kiwi-electronics.nl/rs-485-pi "RS485 HAT for Raspberry Pi"
[n380ct_manual]: docs/https://ineprometering.com/wp-content/uploads/2023/04/N380-CT-0516-short-user-manual-V1.14-3.pdf "N380-CT-0516 short user manual"
