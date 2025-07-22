# Non‑blocking Relay Blink with On/Off Messages

This sketch demonstrates how to blink a single‑channel relay in MicroPython without using blocking delays. Instead of halting the entire program with `sleep`, we use timestamp comparisons (`utime.ticks_ms()` and `utime.ticks_diff()`) to toggle the relay and print its state, while leaving the main loop free to perform other tasks.

## Prerequisites

- A MicroPython‑capable board (e.g., ESP8266, ESP32, Raspberry Pi Pico).  
- A UNIT relay module connected to a GPIO pin.  
- MicroPython firmware installed and the Thonny or ampy tool to upload scripts.

---

## Pinout and Wiring

1. **RELAY_PIN** → connect to your relay’s control input.  
2. **GND** → relay module ground.  
3. **VCC** → relay module 5 V or 3.3 V (depending on your board and module).

---

## Configuration

```python
import utime
from machine import Pin

# ————— Configuration —————
RELAY_PIN = Pin(4, Pin.OUT)   # GPIO pin for the relay
ON_TIME   = 500               # ON duration in milliseconds
OFF_TIME  = 1500              # OFF duration in milliseconds
```

- **RELAY_PIN**

  - A machine.Pin object in output mode.

  - Change the number 4 to match the GPIO you’re using on your board.

- **ON_TIME** and **OFF_TIME**

  - Control how long the relay stays energized (ON_TIME) and de‑energized (OFF_TIME).

  - Measured in milliseconds.

## Initialization

```python
last_tick = utime.ticks_ms()  # Record the first timestamp
relay_on  = False             # Current relay state: False = OFF, True = ON
RELAY_PIN.value(0)            # Ensure the relay starts in the OFF position
```

1. last_tick stores the result of utime.ticks_ms(), which returns the number of milliseconds since the board started.

2. relay_on is a Boolean flag tracking whether the relay is currently ON (True) or OFF (False).

3. We drive the pin LOW (0) to guarantee a defined initial state.

## Main Loop Logic

```python
while True:
    now = utime.ticks_ms()

    if not relay_on and utime.ticks_diff(now, last_tick) >= OFF_TIME:
        # Time to turn the relay ON
        relay_on   = True
        last_tick  = now
        RELAY_PIN.value(1)
        print("NO: On NC: Off")

    elif relay_on and utime.ticks_diff(now, last_tick) >= ON_TIME:
        # Time to turn the relay OFF
        relay_on   = False
        last_tick  = now
        RELAY_PIN.value(0)
        print("NO: Off NC: On")

    # Other non‑blocking tasks can go here
```

- **Read current time**

  - `now = utime.ticks_ms()`

- **Check OFF→ON transition**

  - If the relay is currently OFF (`not relay_on`)

  - And at least **OFF_TIME** milliseconds have elapsed since `last_tick`

  - Then:

      - Set `relay_on = True`

     - Update `last_tick = now`

     - Energize the relay (`RELAY_PIN.value(1)`)

     - Print the state message

- **Check ON→OFF transition**

  - If the relay is currently ON (`relay_on`)

  - And at least **ON_TIME** milliseconds have elapsed

  - Then:

    - Set `relay_on = False`

    - Reset `last_tick = now`

    - De‑energize the relay (`RELAY_PIN.value(0)`)

    - Print the state message

- **Non‑blocking design**

  - Since we never call `sleep_ms()` inside the loop, the code can immediately check sensors, respond to buttons, or handle communications in the same cycle.