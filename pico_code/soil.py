# Reads soil moisture using a capactivie soil moisture sensor
# ADC is connected to Pin(26) which is GPIO pin 26
# Connect VCC to 3V3(OUT)

import utime
import machine
from machine import ADC, Pin

def get_soil_moisture():

    # Retrives the analog signal from GP Pin 26
    soil = ADC(Pin(26))

    # Calibration numbers for the sensor, last calibrated 7/8/2023
    cal_min = 45087.13
    cal_max = 18101.6
    cal_range = cal_min - cal_max 

    # Configuration parameters
    read_Delay = 0.5
    buffer_size = 10
    moisture_buffer = [0] * buffer_size
    buffer_index = 0

    # read moisture value and convert to percentage
    moisture = (cal_min - soil.read_u16()) * 100 / cal_range
    # print(str(moisture))
    
    # add the current reading to the buffer and increment the buffer
    moisture_buffer[buffer_index] = moisture
    
    # increment the buffer index, wrapping around if necessary
    buffer_index = (buffer_index + 1) % buffer_size
    # print(str(buffer_index))
    
    # calcuate the average moisture from the buffer
    average_moisture = sum(moisture_buffer) / buffer_size
    
    if average_moisture < 0:
        reading = 0.0
    elif average_moisture > 100:
        reading = 100.0
    else:
        reading = round(average_moisture, 1)
    
    utime.sleep(read_Delay)
    
    return reading

# For testing purposes, not needed for release
# while True:
#     print(get_soil_moisture())
#     utime.sleep(1)
    

