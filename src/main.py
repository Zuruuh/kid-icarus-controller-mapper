import time
import pynput
import threading
from pyjoystick.sdl2 import Key, Joystick, run_event_loop

CENTER = (950, 784)
LIMIT_MAP = {
    'left': 640,
    'right': 1278,
    'top': 523,
    'bottom': 1002,
}

mouse = pynput.mouse.Controller()

def main():
    print('hello, world')
    run_event_loop(print_add, print_remove, key_received)

def print_add(joy: Joystick):
    print('Added', joy.get_name())

def print_remove(joy: Joystick):
    print('Removed', joy.get_name())

MULTIPLIER = 5
latest_timeout = threading.Timer(9999999999, lambda : None, ())

def key_received(key: Key):
    if key.joystick.__str__() != 'Xbox 360 Controller':
        return

    modifiers = (0, 0)

    if key.keytype != Key.AXIS:
        print(f'Received key of type {key.keytype}! ignoring')
        return

    if key.number != 3 and key.number != 4:
        print(f'Received input for left stick! ignoring')
        return

    if not key.value:
        return

    print(key.number)
    if key.number == 3:
        modifiers = (key.value, modifiers[1])
    elif key.number == 4:
        modifiers = (modifiers[0], key.value)

    modifiers = (modifiers[0] * MULTIPLIER, modifiers[1] * MULTIPLIER)
    print(modifiers)

    position = (mouse.position[0] + modifiers[0], mouse.position[1] + modifiers[1])

    if position[0] < LIMIT_MAP['left'] or position[0] > LIMIT_MAP['right'] or position[1] < LIMIT_MAP['top'] or position[1] > LIMIT_MAP['bottom']:
        print("Out of bound, teleporting back to center")
        mouse.release(pynput.mouse.Button.left)
        time.sleep(0.1)
        move_to(CENTER[0], CENTER[1])
        time.sleep(0.1)
        mouse.press(pynput.mouse.Button.left)

        return

    ensure_pressed()
    move_to(position[0], position[1])

def ensure_pressed():
    global latest_timeout
    if latest_timeout != None and not latest_timeout.finished.is_set():
        print("Cancelling timeout")
        latest_timeout.cancel()

    print("Pressing mouse and scheduling release in 2 seconds")
    mouse.press(pynput.mouse.Button.left)
    latest_timeout = threading.Timer(1, release_mouse, ())
    latest_timeout.start()

def release_mouse():
    print("releasing mouse")
    mouse.release(pynput.mouse.Button.left)

def move_to(x, y):
    print(f'Moving to {x}:{y}')
    mouse.move(x - mouse.position[0], y - mouse.position[1])

if __name__ == '__main__':
    main()
