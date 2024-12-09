from machine import Pin, Timer
import time

# 赤外線受信機のピンを指定
ir_pin = Pin(15, Pin.IN)

# タイマーの初期化
timer = Timer()

# 信号データを保持する変数
signal_data = []


# タイマー割り込みハンドラ
def timer_handler(timer):
    global signal_data
    signal_data.append(ir_pin.value())


# 信号を受信する関数
def receive_signal():
    global signal_data
    signal_data = []
    timer.init(period=1, mode=Timer.PERIODIC, callback=timer_handler)

    # ピンへの入力がLOWになるまで待機し、LOWになった時刻を記録
    # ピンへの入力がHIGHになるまで待機し、HIGHになった時刻を記録
    # ピンへの入力がLOWであった時間が1000µs以上であれば、リーダー部の検出として信号受信を開始

    # 最大1秒間信号を受信（リーダー部の検出まで続ける）
    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < 1000:
        if len(signal_data) > 2 and signal_data[-1] == 0:
            high_duration = sum(1 for val in signal_data if val == 1)
            if high_duration > 1000:  # 1ms以上HIGH状態が続いた場合
                break
    timer.deinit()
    return signal_data


# パルス幅をデコードする関数
def decode_pulses(signal):
    pulses = []
    last_val = signal[0]
    count = 0
    for val in signal:
        if val == last_val:
            count += 1
        else:
            pulses.append(count)
            count = 1
            last_val = val
    pulses.append(count)
    return pulses


# NECフォーマットのデコード関数
def decode_nec(pulses):
    if len(pulses) < 68:
        return None
    data = 0
    for i in range(2, 66, 2):
        data <<= 1
        if pulses[i] > pulses[i + 1]:
            data |= 1
    return data


# Sonyフォーマットのデコード関数
def decode_sony(pulses):
    if len(pulses) < 24:
        return None
    data = 0
    for i in range(1, 24, 2):
        data <<= 1
        if pulses[i] > pulses[i + 1]:
            data |= 1
    return data


# RC5フォーマットのデコード関数
def decode_rc5(pulses):
    if len(pulses) < 26:
        return None
    data = 0
    for i in range(1, 26, 2):
        data <<= 1
        if pulses[i] > pulses[i + 1]:
            data |= 1
    return data


# RC6フォーマットのデコード関数
def decode_rc6(pulses):
    if len(pulses) < 36:
        return None
    data = 0
    for i in range(1, 36, 2):
        data <<= 1
        if pulses[i] > pulses[i + 1]:
            data |= 1
    return data


# メインプログラム
while True:
    print("Waiting for IR signal...", end="")
    while True:
        signal = receive_signal()
        pulses = decode_pulses(signal)

        nec_data = decode_nec(pulses)
        if nec_data is not None:
            print("\nNEC format detected:", hex(nec_data))
            break
        sony_data = decode_sony(pulses)
        if sony_data is not None:
            print("\nSony format detected:", hex(sony_data))
            break
        rc5_data = decode_rc5(pulses)
        if rc5_data is not None:
            print("\nRC5 format detected:", hex(rc5_data))
            break
        rc6_data = decode_rc6(pulses)
        if rc6_data is not None:
            print("\nRC6 format detected:", hex(rc6_data))
            break

        print(".", end="")

    print()




