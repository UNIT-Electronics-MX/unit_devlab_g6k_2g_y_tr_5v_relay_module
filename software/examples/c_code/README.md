# Relay Blink with On/Off Messages

This sketch toggles a single‐channel relay on and off every second and prints the current state of both the **Normally Open (NO)** and **Normally Closed (NC)** contacts to the serial console.

---

## Hardware Setup

1. **Relay module**  
   - Connect **VCC** on the relay to **5 V** (or 3.3 V, depending on your module).  
   - Connect **GND** on the relay to **GND** on the Arduino.  
   - Connect the relay’s **IN** pin to Arduino digital pin **4**.

---

## Pin Configuration

```cpp
int IN_PIN = 4;   // Pin wired to the relay’s IN pin
int T      = 1000; // Blink interval in milliseconds
```

## Setup() function

```cpp
void setup() {
  pinMode(IN_PIN, OUTPUT);     // Configure IN_PIN as a digital output
  Serial.begin(9600);          // Start serial at 9600 baud
  while (!Serial) ;            // Wait for the Serial Monitor
}
```

- `pinMode(IN_PIN, OUTPUT);`

  - Prepares the relay control line for digital output.

- `Serial.begin(9600);`

  - Opens the USB Serial port at 9600 bits per second.

- `while (!Serial);`

Blocks until the host PC opens the Serial Monitor

## loop() function

```cpp
void loop() {
  // --- Turn relay ON (LOW) ---
  digitalWrite(IN_PIN, LOW);
  Serial.print("NO: On ");
  Serial.println("NC: Off");
  delay(T);

  // --- Turn relay OFF (HIGH) ---
  digitalWrite(IN_PIN, HIGH);
  Serial.print("NO: Off ");
  Serial.println("NC: On");
  delay(T);
}
```

- **Turn relay ON**

  - `digitalWrite(IN_PIN, LOW);` energizes the coil → closes the NO contact, opens NC (active LOW).

  - `Serial.print("NO: On "); Serial.println("NC: Off");` reports NO: On and NC: Off.

  - `delay(T);` pauses for T ms before next action.

- **Turn relay OFF**

  - `digitalWrite(IN_PIN, HIGH);` de‑energizes the coil → opens NO, closes NC (active LOW).

  - `Serial.print("NO: Off "); Serial.println("NC: On");` reports NO: Off and NC: On.

  - `delay(T);` pauses again for T ms.

- **Turn relay ON**

  - `digitalWrite(IN_PIN, HIGH);` energizes the coil → closes the NO contact, opens NC.

  - `Serial.print("NO: On "); Serial.println("NC: Off");` reports NO: On and NC: Off.

  - `delay(T);` pauses for T ms before next action.

- **Turn relay OFF**

  - `digitalWrite(IN_PIN, LOW);` de‑energizes the coil → opens NO, closes NC.

  - `Serial.print("NO: Off "); Serial.println("NC: On");` reports NO: Off and NC: On.

  - `delay(T);` pauses again for T ms.
