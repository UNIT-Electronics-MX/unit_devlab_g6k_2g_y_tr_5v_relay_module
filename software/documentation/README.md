---
title: "UNIT Relay Module"
version: "1.0"
modified: "2025-05-02"
output: "relay_module"
subtitle: "This dual-channel relay module safely interfaces microcontrollers with higher-voltage or high-current loads by separating control from power."
---

<!--
# README_TEMPLATE.md
Este archivo sirve como entrada para generar un PDF técnico estilo datasheet.
Edita las secciones respetando el orden, sin eliminar los encabezados.
-->
 <!-- logo -->

# UNIT Relay Module

![product](images/top.png)

## Introduction

This dual-channel relay module isolates high-power operations from sensitive MCU logic. It supplies a dedicated 5V rail (JDVCC) for relay coils while using the VCC pin to match the MCU’s operating voltage (3.3V or 5V). A digital high on the IN pin triggers an optocoupler that switches the NO, NC, and COM contacts. LED indicators provide immediate feedback on power and control status.


## Functional Description

- The module includes two independent electromechanical relays, each controlled through optocouplers for complete electrical isolation between control logic and relay coil voltage.
- A dedicated power rail (JDVCC) provides 5V specifically to energize the relay coils, while a separate VCC pin supplies 3.3V or 5V to the optocoupler input stage.
- Each relay channel is triggered via an active-high digital input signal (IN1, IN2) from the microcontroller.
- The relay outputs provide access to a set of contacts: Normally Open (NO), Normally Closed (NC), and Common (COM).
- When triggered, the relay switches the contacts, allowing control of external AC/DC loads while protecting the MCU from high-voltage transients.
- LED indicators (LED PWR and LED IN) provide immediate visual feedback of power and activation status.

## Electrical Characteristics & Signal Overview

- Operating voltage (logic side): 3.0 V – 5.5 V (via VCC pin)
- Relay coil voltage: 5 V nominal (via JDVCC)
- Trigger current per channel: 2–15 mA depending on input logic level
- Contact rating: Up to 10 A - 250 VAC or 10 A - 30 VDC
- Optocoupler logic threshold: Compatible with 3.3 V and 5 V logic
- Isolation resistance: ≥ 100 M Ohm - 500 VDC between control and relay side

## Applications

- Home automation and IoT-based appliance control
- Industrial machinery switching
- Smart lighting systems
- Motor or actuator control
- Security and alarm systems
- HVAC and environmental controllers

## Features

- Dual-channel electromechanical relay outputs
- Optical isolation between control and power stages
- Dedicated 5V relay coil supply (JDVCC)
- 3.3V or 5V logic compatibility (VCC)
- LED indicators for control signal and power presence
- Breakout access to NO, NC, and COM terminals per channel
- Supports both AC and DC loads up to 10 A


## Pin & Connector Layout

| Signal  | Description                                                       |
|---------|-------------------------------------------------------------------|
| JDVCC   | +5V supply to energize relay coils                                |
| VCC     | MCU logic voltage (3.3V or 5V) for the optocoupler/driver circuit     |
| IN      | MCU input to activate relay channel 1                             |
| NO1     | Relay 1 normally open contact                                       |
| COM1    | Relay 1 common terminal                                             |
| NC1     | Relay 1 normally closed contact                                     |
| NO2     | Relay 2 normally open contact                                       |
| COM2    | Relay 2 common terminal                                             |
| NC2     | Relay 2 normally closed contact                                     |
| LED PWR | Indicator LED for power (active when JDVCC is present)              |
| LED IN  | Indicator LED showing active input from the MCU                     |



## Settings

### Interface Overview

### Interface Overview

| Interface  | Signals / Pins                  | Typical Use                                     |
|------------|----------------------------------|-------------------------------------------------|
| Power      | JDVCC, VCC, GND                  | Power relay coils and optocoupler driver circuit|
| Control    | IN1, IN2                         | Trigger signals from MCU                        |
| Output     | NO1, COM1, NC1 / NO2, COM2, NC2  | Switching terminals for AC/DC load             |
| Indicators | LED_PWR, LED_IN                  | Visual status of power and input activation     |




### Supports

| Symbol | I/O   | Description                                 |
|--------|-------|---------------------------------------------|
| JDVCC  | Input | 5V supply input for relay coil energization |
| VCC    | Input | Logic voltage input (3.3V or 5V)            |
| GND    | Input | Shared ground for logic and relay power     |
| IN1    | Input | Control signal to activate relay 1          |
| IN2    | Input | Control signal to activate relay 2          |
| NOx    | Output| Normally open contact (connected when active) |
| NCx    | Output| Normally closed contact (disconnected when active) |
| COMx   | Output| Common terminal for relay switching          |


## Block Diagram

![Function Diagram](./images/pinout.png)

## Dimensions

![Dimensions](./images/dimension.png)

## Usage

Works with:

- Arduino AVR
- Raspberry Pi RP2040
- STM32
- NRF
- PY32
- MAX II 

## Downloads

- [Schematic PDF](docs/schematic.pdf)


## Purchase

- [Buy from UNIT Electronics](https://www.uelectronics.com)
