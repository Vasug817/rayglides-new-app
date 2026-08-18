# RayGlides 3W/4W EV Kit Cooling Controller — Production Test Plan

This document defines the validation procedures for newly manufactured cooling controller boards before installation in vehicles.

---

## 1. Power Supply Verification (Minimum, Nominal, Maximum)
*   **Equipment**: Adjustable DC Power Supply (0V to 100V, current limit set to 1.0A), Digital Multimeters.
*   **Procedure**:
    1.  Verify the input fuse F1 is installed and conductive.
    2.  Set the power supply to **36V DC** and connect to J1 input. Turn on power. Verify the 12V rail ($12.0\text{V} \pm 0.3\text{V}$), 5V rail ($5.0\text{V} \pm 0.1\text{V}$), and 3.3V rail ($3.3\text{V} \pm 0.05\text{V}$).
    3.  Set the supply to **48V DC** (Nominal). Re-verify all rails.
    4.  Set the supply to **72V DC** (Maximum). Re-verify all rails. Verify there is no excessive temperature rise on U1 (LM5017).
    5.  Turn off power. Reverse the supply wires and connect to J1. Turn on power. Verify that the current draw is $0.00\text{A}$ (proves Schottky diode D1 block works). Correct the connections.

---

## 2. Native USB-C Programming & JTAG Boot Test
1.  Connect a standard USB-C cable from a host PC to J5 connector.
2.  Verify the ESP32-S3 module powers up and is recognized by the operating system as a native USB Serial Device.
3.  Flash a test blinky script using PlatformIO over the native interface to confirm successful JTAG bootloading and connection.

---

## 3. CAN Bus Transceiver Validation
1.  Configure the ESP32-S3 TWAI peripheral in self-test loopback mode.
2.  Transmit a series of CAN frames over GPIO 9 and read them back on GPIO 10 via the TJA1050 transceiver.
3.  Connect a CAN analyzer to J4 (CANH/CANL). Confirm that the differential voltages are $2.5\text{V}$ during recessive state and $3.5\text{V}$ / $1.5\text{V}$ during dominant state.

---

## 4. Temperature Sensor Loop Verification
*   **Equipment**: Decade Resistance Box (or adjustable potentiometer to mock LM35 output), Multimeters.
*   **Procedure**:
    1.  Disconnect the physical LM35 sensor from J3.
    2.  Connect an adjustable DC voltage generator to J3 Pin 2 (Signal) and J3 Pin 3 (GND).
    3.  Inject **300 mV** (equivalent to $30^\circ\text{C}$). Verify the fan is **OFF** (0% duty cycle, voltage across J2 is 0V).
    4.  Increase the injected voltage to **450 mV** ($45^\circ\text{C}$, the ON threshold). Verify that the fan turns **ON** (duty cycle starts at 30%, voltage across J2 shows pulsed 12V output).
    5.  Increase the voltage to **550 mV** ($55^\circ\text{C}$ or higher). Verify that the fan increases to **100% duty cycle** (steady 12V across J2).
    6.  Decrease the voltage to **420 mV** ($42^\circ\text{C}$). Verify the fan **remains ON** (proves hysteresis works).
    7.  Decrease the voltage to **390 mV** ($39^\circ\text{C}$, below the OFF threshold). Verify that the fan turns **OFF**.

---

## 5. Fail-Safe and Fault Mode Tests
*   **Procedure**:
    1.  **Sensor Disconnect Test**: With the fan running, disconnect J3 Pin 2 (Sensor Output). Verify that the ADC voltage drops to 0V (pulled down by R7 200R). Verify that the firmware detects sensor failure and sets the fan to **100% duty cycle** (fail-safe speed) or triggers F004 over-temperature protection.
    2.  **Sensor Short Test**: Short J3 Pin 2 to Pin 1 (+5V). Verify that the ADC voltage rises above 1.25V. Verify that the firmware registers an out-of-bounds fault and triggers emergency shutdown.
    3.  **Fan Disconnect Test**: Unplug the fan from J2. Verify that the MOSFET Q1 continues to switch without damage.
    4.  **Loss of MCU Power**: Disconnect the 3.3V power to the ESP32. Verify that Q1 gate drops to 0V (pulled down by R5 10k), turning the fan **OFF** cleanly.
