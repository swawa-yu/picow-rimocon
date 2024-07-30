import machine
import utime

# GP1U782RのVoutを接続したピン
ir_pin = machine.Pin(16, machine.Pin.IN)

# パルスのタイミングと状態を記録するリスト
pulse_times = []
pulse_states = []

# バッファサイズの制限
MAX_BUFFER_SIZE = 1000

# 先行バーストの検出フラグ
leader_detected = False

# NECフォーマットの先行バーストの閾値（マイクロ秒）
LEADER_PULSE_MIN = 8500  # 9msのキャリアパルス
LEADER_PULSE_MAX = 9500
LEADER_SPACE_MIN = 4000  # 4.5msのオフタイム
LEADER_SPACE_MAX = 5000


def record_pulses(pin):
    global leader_detected
    current_time = utime.ticks_us()

    if len(pulse_times) > 0:
        duration = utime.ticks_diff(current_time, pulse_times[-1])
        if not leader_detected:
            if LEADER_PULSE_MIN < duration < LEADER_PULSE_MAX and pin.value() == 0:
                # 先行バーストのパルス検出
                pulse_times.append(current_time)
                pulse_states.append(pin.value())
            elif LEADER_SPACE_MIN < duration < LEADER_SPACE_MAX and pin.value() == 1:
                # 先行バーストのスペース検出
                leader_detected = True
                pulse_times.append(current_time)
                pulse_states.append(pin.value())
        elif leader_detected and len(pulse_times) < MAX_BUFFER_SIZE:
            pulse_times.append(current_time)
            pulse_states.append(pin.value())
    else:
        pulse_times.append(current_time)
        pulse_states.append(pin.value())


# 割り込みを設定してパルスを記録
ir_pin.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=record_pulses)

# 信号受信待機
print("Waiting for IR signal...")

# 先行バーストが検出されるまで待機
while not leader_detected:
    utime.sleep(0.1)

print("Leader detected, recording pulses...")

# 一定時間信号を受信し続けた後に処理を終了
END_WAIT_TIME = 20000  # 信号終了後の待機時間

while True:
    current_time = utime.ticks_us()
    if len(pulse_times) > 0 and (current_time - pulse_times[-1] > END_WAIT_TIME):
        break

# パルスの持続時間を計算
durations = []
for i in range(1, len(pulse_times)):
    duration = utime.ticks_diff(pulse_times[i], pulse_times[i - 1])
    if pulse_states[i - 1] == 0:
        duration = -duration
    durations.append(duration)

# デバッグ用に全パルス持続時間を表示
print("Pulse durations (us):", durations)

# バッファをクリア
pulse_times.clear()
pulse_states.clear()
