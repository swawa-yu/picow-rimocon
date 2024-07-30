from machine import Pin, ADC
from utime import sleep

# センサーが接続されているADCピン
adc = ADC(Pin(26))

# GP25ピンを出力に設定
led = Pin(15, Pin.OUT)


def read_sensor():
    # センサーの値を読み取る
    value = adc.read_u16()  # 0から65535の範囲の値
    # voltage = value * 3.3 / 65535  # 電圧に変換 (Picoは3.3V基準)
    voltage = value * 3.0 / 65535  # 電圧に変換 (Picoは3.3V基準)
    distance = 27.86 / (voltage - 0.42)  # 距離に変換（センサーの特性に基づく計算）
    return value, voltage, distance


while True:
    value, voltage, distance = read_sensor()
    led.toggle()
    print("Raw Value:", value, "Voltage:", voltage, "Distance (cm):", distance)
    sleep(0.1)
