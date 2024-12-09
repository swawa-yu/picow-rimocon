import machine
import utime

# 赤外線受信ピンの設定
ir_pin = machine.Pin(16, machine.Pin.IN)
# タイマーの設定
timer = machine.Timer()

# 基準時間T（μs）
T = 562

# パルス幅の定義（μs）
LEADER_ON_MIN = T * 15.8
LEADER_ON_MAX = T * 16.2
LEADER_OFF_MIN = T * 7.8
LEADER_OFF_MAX = T * 7.2
BIT_ON_MIN = T * 0.9
BIT_ON_MAX = T * 1.1
BIT0_OFF_MIN = T * 0.9
BIT0_OFF_MAX = T * 1.1
BIT1_OFF_MIN = T * 2.9
BIT1_OFF_MAX = T * 3.1

# パルスのリスト
pulse_durations = []

# グローバル変数の初期化
prev_value = 1
count = 0
leader_detected = False
start_time = 0


def record_pulse(pin):
    global prev_value, start_time, pulse_durations, leader_detected, count
    # print(count)
    current_value = pin.value()
    return current_value
    current_time = utime.ticks_us()
    if prev_value != current_value:
        pulse_duration = utime.ticks_diff(current_time, start_time)
        if current_value == 1:
            if leader_detected:
                if BIT_ON_MIN <= pulse_duration <= BIT_ON_MAX:
                    pulse_durations.append(pulse_duration)
                elif BIT0_OFF_MIN <= pulse_duration <= BIT0_OFF_MAX or BIT1_OFF_MIN <= pulse_duration <= BIT1_OFF_MAX:
                    pulse_durations.append(-pulse_duration)
                else:
                    print("invalid pulse duration")
                    pulse_durations.clear()  # ノイズとして無視
                    leader_detected = False
        else:
            if not leader_detected and LEADER_ON_MIN <= pulse_duration <= LEADER_ON_MAX:
                start_time = current_time
            elif not leader_detected and LEADER_OFF_MIN <= pulse_duration <= LEADER_OFF_MAX:
                leader_detected = True
                pulse_durations = []
                print("Leader detected, recording pulses...")
            elif leader_detected:
                if BIT_ON_MIN <= pulse_duration <= BIT_ON_MAX or BIT0_OFF_MIN <= pulse_duration <= BIT0_OFF_MAX or BIT1_OFF_MIN <= pulse_duration <= BIT1_OFF_MAX:
                    pulse_durations.append(-pulse_duration)
                else:
                    pulse_durations.clear()  # ノイズとして無視
                    leader_detected = False
        start_time = current_time
        prev_value = current_value
    count += 1


# # 割り込みの設定
# ir_pin.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=record_pulse)


def main():
    global leader_detected
    print("Waiting for IR signal...")
    while True:
        for i in range(10):
            print(i, end=" ")
            print(record_pulse(ir_pin))

        utime.sleep(0.1)
        # if leader_detected:
        #     if len(pulse_durations) > 0:
        #         print("Pulse durations (us):", pulse_durations)
        #         if len(pulse_durations) == 66:
        #             print("Correct number of pulses detected!")
        #         else:
        #             print("Incorrect number of pulses detected:", len(pulse_durations))
        #         leader_detected = False
        #         pulse_durations.clear()  # データ収集後、リストをクリア
        #     print("Waiting for IR signal...")


# main()


while True:
    print(record_pulse(ir_pin))
    utime.sleep(T / 1000000)
