from machine import Pin
import time

# 赤外線受信機のピンを指定
pin_receiver = Pin(16, Pin.IN, Pin.PULL_UP)

HIGH = 1
LOW = 0

# PWM
def is_receiving():
    return not pin_receiver.value()


# 信号を受信する関数
"""
timeout: タイムアウト時間(us)
"""
def receive_signal(timeout=20000):
    signal_data = []

    # 信号の開始を待つ
    while not is_receiving():
        pass

    # 
    current_value = True
    start_time = time.ticks_us()

    while True:
        if current_value == HIGH:
            while is_receiving():
                pass
            t = time.ticks_us()
            signal_data.append(time.ticks_diff(t, start_time))
            current_value = False
            start_time = t

        else:
            while not is_receiving():
                if time.ticks_diff(time.ticks_us(), start_time) > timeout:
                    return signal_data
                pass
            t = time.ticks_us()
            signal_data.append(-time.ticks_diff(t, start_time))
            current_value = True
            start_time = t


# メインプログラム
print("version 1")
while True:
    # print("Waiting for IR signal...")
    signal = receive_signal()
    if signal:
        print("Signal received:", signal)
        print("Signal length:", len(signal))
