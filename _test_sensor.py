from machine import *
from pin import *


def is_receiving():
    return not pin_sensor.value()


def is_button_being_pressed():
    return pin_sw.value()


def set_led_ir(val):
    if val:
        pwm_led_ir.duty_u16(21845)  # 33% Duty cycleでHIGHのパルス (65536 * 0.33 ≈ 21845)
    else:
        pwm_led_ir.duty_u16(0)


while True:
    b = pin_sw.value()
    s = pin_sensor.value()
    print(f"button: {b}, sensor: {s}")

    set_led_ir(is_button_being_pressed())
    pin_led_r.value(is_receiving())
