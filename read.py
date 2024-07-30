from machine import Pin
import time

# 赤外線受信機のピンを指定
pin_receiver = Pin(16, Pin.IN, Pin.PULL_UP)

# 信号データを保持する変数
signal_data = []
start_time = 0
recording = False


# ピンの状態変化を記録するハンドラ
def record_pulses(pin):
    global signal_data, start_time, recording
    current_time = time.ticks_us()
    if not recording:
        if pin.value() == 0:
            recording = True
            start_time = current_time
    else:
        duration = time.ticks_diff(current_time, start_time)
        if len(signal_data) % 2 == 1:
            signal_data.append(-duration)  # HIGH持続時間を負の値として記録
        else:
            signal_data.append(duration)  # LOW持続時間を正の値として記録
        start_time = current_time


# 割り込みを設定
pin_receiver.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=record_pulses)


# 信号を受信する関数
def receive_signal(timeout=1000):
    global signal_data, recording
    signal_data = []
    recording = False
    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < timeout:
        pass  # 指定した時間待つ
    return signal_data


# メインプログラム
print("version 1")
while True:
    # print("Waiting for IR signal...")
    signal = receive_signal()
    if signal:
        print("Signal received:", signal)
        print("Signal length:", len(signal))
