from machine import *
import time
from signals import light

pin_sw = Pin(14, Pin.IN, Pin.PULL_DOWN)
pin_led_ir = Pin(15, Pin.OUT)

# 38kHzのキャリア周波数を生成するためのPWM設定
pwm_led_ir = PWM(pin_led_ir)
pwm_led_ir.freq(38000)


def set_led_ir(val):
    if val:
        pwm_led_ir.duty_u16(21845)  # 33% Duty cycleでHIGHのパルス (65536 * 0.33 ≈ 21845)
    else:
        pwm_led_ir.duty_u16(0)


# 信号を送信する関数
def send_signal(signal):
    for duration in signal:
        if duration > 0:
            set_led_ir(1)
        else:
            set_led_ir(0)
        time.sleep_us(abs(duration))
    set_led_ir(0)  # 信号をオフにするのを忘れないこと


# メインプログラム
while True:
    if pin_sw.value():
        print("send signal on")
        send_signal(light.on[1])
        time.sleep(1)
