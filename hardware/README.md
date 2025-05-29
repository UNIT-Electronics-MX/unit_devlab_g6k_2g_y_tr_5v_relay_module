# Hardware

<div align="center">
    <a href="#"><img src="resources/img/Schematics_icon.jpg" width="400px"><br/>Schematic</a>
    <br/>

</div>

# Pinout

<div align="center">
    <a href="#"><img src="resources/UE0082-PINOUT-UNIT_G6K-2G-Y-TR DC5-RELAY-EN.png" width="500px"><br/>Pinout</a>
    <br/>


</div>

| Function                    | PCB Label | Description                                                      |
|-----------------------------|-----------|------------------------------------------------------------------|
| Relay coil supply           | JDVCC     | +5 V supply to energize the relay coils                          |
| Logic supply                | VCC       | MCU logic voltage (3.3 V or 5 V) for optocoupler/driver circuit  |
| Control input channel 1     | IN        | Logic-level input from MCU to activate relay channel 1           |
| Normally open contact 1     | NO1       | Relay 1 contact that closes when the coil is energized           |
| Common contact 1            | COM1      | Relay 1 common terminal                                          |
| Normally closed contact 1   | NC1       | Relay 1 contact that opens when the coil is energized            |
| Normally open contact 2     | NO2       | Relay 2 contact that closes when the coil is energized           |
| Common contact 2            | COM2      | Relay 2 common terminal                                          |
| Normally closed contact 2   | NC2       | Relay 2 contact that opens when the coil is energized            |
| Power indicator LED         | LED_PWR   | Lights whenever the module is powered (JDVCC present)            |
| Input-signal indicator LED  | LED_IN    | Lights or flashes to show an active IN signal from the MCU       |

---

# Dimensions

<div align="center">
    <a href="#"><img src="resources/dimensions.png" width="500px"><br/>Dimensions</a>
    <br/>


</div>

