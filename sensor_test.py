from machine import Pin, ADC
from utime import sleep

# センサーが接続されているADCピン
ir_read_adc = ADC(Pin(26))
ir_read = Pin(16, Pin.IN)

# GP25ピンを出力に設定
led = Pin(15, Pin.OUT)


def read_sensor_adc():
    value = ir_read_adc.read_u16()  # 0から65535の範囲の値
    return value


def level(value):
    if value > 50000:
        return 1
    if value > 20000:
        return 2
    if value > 10000:
        return 3
    if value > 8000:
        return 4
    if value > 5000:
        return 5
    if value > 2000:
        return 7
    if value > 500:
        return 8
    return 9


while True:
    value = read_sensor_adc()
    l = level(value)
    print("-" * level(value), value)

    led.value(ir_read.value())
    sleep(0.1)
