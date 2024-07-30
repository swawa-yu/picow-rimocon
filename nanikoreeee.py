# durasionsにappendされていない......??
# global周辺が問題？

from machine import Pin, Timer
import time

# 赤外線受信機のピンを指定
ir_pin = Pin(15, Pin.IN)

# 信号データを保持する変数
signal_data = []
start_time = 0
recording = False
durations_hogehoge = []


# LOWからHIGHへの変化を記録するハンドラ
def rising_edge(pin):
    global durations_hogehoge, signal_data, start_time
    current_time = time.ticks_us()
    if recording:
        duration = time.ticks_diff(current_time, start_time)
        durations_hogehoge.append(1)
        signal_data.append(duration)
        start_time = current_time


# HIGHからLOWへの変化を記録するハンドラ
def falling_edge(pin):
    global signal_data, durations_hogehoge, start_time, recording
    current_time = time.ticks_us()
    if not recording:
        recording = True
        start_time = current_time
    else:
        duration = time.ticks_diff(current_time, start_time)
        signal_data.append(-duration)
        durations_hogehoge.append(duration)
        start_time = current_time


# 割り込みを設定
ir_pin.irq(trigger=Pin.IRQ_RISING, handler=rising_edge)
ir_pin.irq(trigger=Pin.IRQ_FALLING, handler=falling_edge)


# 信号を受信する関数
def receive_signal(timeout=1000):
    global signal_data, recording, durations_hogehoge
    signal_data = []
    durations_hogehoge = []
    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < timeout:
        pass  # 指定した時間待つ
    recording = False
    print("hogehoge:", signal_data, durations_hogehoge)
    return signal_data, durations_hogehoge


# メインプログラム
while True:
    print("Waiting for IR signal...")
    signal, duration = receive_signal()
    if signal:
        print("Signal received:", signal)
        print("TIME(us): ", sum(abs(x) for x in signal))
        print("LENGTH: ", len(signal))
        print(duration)
        print(durations_hogehoge)
