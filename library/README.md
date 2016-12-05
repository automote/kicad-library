## Kicad Library ##

### power ###

Power Ports

* +1.2V, +1.8V, +2.5V, +3.3V, +5V, +6V, +9V, +12V, +15V, +18V
* +BATT : Battery voltage
* -5V, -6V, -9V, -12V, -15V, -18V
* VAA, VCC, VCOM, VDD, VEE, VPP, VSS
* GND : Ground
* GNDPWR : Chassis ground
* GNDREF : Reference ground

* SUP_**** : Power ports with combined power flag

Note : Prefix SUP_ means that the type of pin in the symbol is defined as "power output". To avoid ERC warnings, each power nets must have one or a PWR_FLAG symbol attached to it.

----------------------------------

### connectors ###

* BARREL_JACK : DC Barrel Jack
* DB15 : D-SUB Connector - 15 pos
* DB25 : D-SUB Connector - 25 pos
* DB9 : D-SUB Connector - 9 pos (serial)
* HEADER-1x** : Header - Single Row - 1 to 40 pos
* HEADER-2x** : Header - Dual Row - 2 to 40 pos
* Micro_SD : Micro SD card connector
* SD_Card : SD Card connector
* RJ45 : RJ45 Connector
* RJ45-W-LED : RJ45 Connector with leds
* RJ45-W-MAG-LED : RJ45 Connector with magnetics and leds
* Hole : PCB mounting hole
* TEST-POINT
* USB-A : USB Connector - Type A
* USB-B : USB Connector - Tybe B
* USB-MINI-B : USB Connector - Type B mini

----------------------------------

### passive ###

* CAP : Capacitor
* CAP-E : Polarized Capacitor
* CMC : Common Mode Choke
* CRYSTAL
* DIODE
* FUSE
* INDUCTOR
* POT : Potentiometer
* RESISTOR
* SR05 : TVS Diode Array
* ZENNER
* MOSFET-N

----------------------------------

### switches ###

* MOM-SPST : Momentary SPST switch
* MOM-SPST-GND : Momentary SPST switch with ground tabs

----------------------------------

### ic-misc ###

* CAT811 : 4-Pin Microprocessor Power Supply Supervisor
* PCM2704C : Stereo Audio DAC with USB Interface
* TPA2005 : 1.4W Mono Class-D Audio Amplifier
* TSL256X : Light sensor

----------------------------------

### ic-power ###

* ADP2302 : 2A Step-down regulator
* ADP2303 : 3A Step-down regulator
* LM3526 : Dual port USB power switch
* LP2981 : 100 mA LDO Regulator w/ Shutdown
* AMS1117 :3.3V fixed output voltage
----------------------------------

### ic-cpu ###

* ARIA-G25 : AT91SAM9G25 SOM

----------------------------------

### ic-io ###

* AT42QT1070 : 7 channel QTouch Touch sensor IC
* MCP9804 : Digital Temperature Sensor
* RFM92/95/96/98
----------------------------------

### opto ###

* WS2812B : Smart RGB LED (Pixel)
* ER-OLED1602 : 16x2 character OLED display
