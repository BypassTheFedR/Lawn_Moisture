# Version 1.0
# main.py is what the controller will run when it powers on (this is default for micropython firmware)
# Sends soil moisture and temperatue data to a server

import network
from time import sleep
from picozero import pico_temp_sensor
import machine
from soil import get_soil_moisture
import urequests

ssid = 'Ministry_Of_Magic'
password = '#G0blet_F!re'
frequency = 60

def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def send_data(temperature, soil_moisture):
    # Sends data to the server
    # This is my laptops address for development purposes
    url = "http://192.168.50.31:8000/data/"
    data = {
        "temperature": temperature,
        "soil_moisture": soil_moisture
    }

    headers = {'Content-Type': 'application/json'}
    response = urequests.post(url, json=data, headers=headers)
    print(response.text)

def main():
    try:
        connect()
        while True:
            # Reads the temperature and convert to Fahrenheit
            temperature = pico_temp_sensor.temp
            temperature = round((temperature * (9 / 5) + 32), 1)

            # Read the soil moisture
            soil_moisture = get_soil_moisture()

            # Send data to the server
            send_data(temperature, soil_moisture)

            # Wait before sending next data
            sleep(frequency)
    except KeyboardInterrupt:
        machine.reset()

main()