from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='inepromodbus2mqtt',
   version='1.0',
   description='Python script to read out measurements by the Inepro N380CT over modbus and share them via MQTT',
   license="gpl-3.0",
   long_description=long_description,
   author='TheGroundZero',
   author_email='2406013+TheGroundZero@users.noreply.github.com',
   url="https://sequr.be/",
   packages=['inepromodbus2mqtt'],
   install_requires=['minimalmodbus', 'paho-mqtt']
)