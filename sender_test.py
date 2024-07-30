import machine

# 入力ピンと赤外線LED制御ピンの設定
input_pin = machine.Pin(16, machine.Pin.IN)
ir_led_pin = machine.Pin(17, machine.Pin.OUT)

# 38kHzのキャリア周波数を生成するためのPWM設定
pwm = machine.PWM(ir_led_pin)
pwm.freq(38000)


def update_ir_signal():
    pin_state = input_pin.value()
    if pin_state:
        pwm.duty_u16(21845)  # 33% Duty cycleでHIGHのパルス (65536 * 0.33 ≈ 21845)
    else:
        pwm.duty_u16(0)  # Duty cycleを0にしてLOWのパルス


# 割り込みハンドラの設定
def handle_input_change(pin):
    update_ir_signal()


# メインループ（何もしないで待機）
while True:
    if input_pin.value():
        pwm.duty_u16(21845)  # 33% Duty cycleでHIGHのパルス (65536 * 0.33 ≈ 21845)
    else:
        pwm.duty_u16(0)  # Duty cycleを0にしてLOWのパルス
