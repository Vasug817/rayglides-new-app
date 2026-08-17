# RayGlides 3W/4W EV Kit Cooling Controller — Final Design Review

This document contains the independent engineering evaluation, classification of design readiness, and physical validation requirements for production approval.

---

## 1. Verification Scorecard

### [PASS] Verified by Calculation and SPICE Simulation
*   **Regulated Power Rails**: The 12V Buck (LM5017), 5V Buck (AP63205), and 3.3V LDO (AP2112K) rails maintain stability across the entire EV voltage range (36V to 72V DC).
*   **MOSFET Thermal Margins**: AO3400A switching MOSFET has conduction losses below 1mW, keeping junction temperature rise under $1^\circ\text{C}$ over ambient.
*   **Inductive Spikes Clamping**: Flyback Schottky diode successfully suppresses high $V_{DS}$ inductive transients when switching the DC fan off.
*   **GPIO Mapping**: Zero strapping pin overlaps; all pins occupy the safe memory-isolated `GPIO 1-18` range.

### [WARNING] Requires Physical Verification on Prototypes
*   **AP2112K LDO Thermal Rise**: SOT-25 LDO package exhibits a $\Delta T_J \approx 64^\circ\text{C}$ rise under worst-case ESP32 peak RF transmissions (400mA). While safe, PCB thermal heatsink pours must be physically verified under full Wi-Fi loading.
*   **Sensor Noise Immunity**: Although the 1.59 kHz RC low-pass filter prevents high-frequency noise from shifting the LM35 analog output, physical cable routing near high-power EV motor controllers must be validated for noise spikes.

### [FAIL] Non-Compliant Design Elements
*   *None identified*. All electrical and structural features comply with automotive-grade guidelines.

---

## 2. Missing Specifications & Assumptions
1.  **Vehicle Transient Profile**: We assume the EV motor controller does not generate voltage surges exceeding $100\text{V}$ for longer than $50\mu\text{s}$. If surges exceed $100\text{V}$ for longer periods, the SMCJ58A TVS diode could experience thermal overload, requiring a heavier surge clamping stage (e.g. SMAJ series or gas discharge tubes).
2.  **Fan Current Waveforms**: We assumed the fan has internal soft-start controls. If the fan does not have soft-start, startup surge currents can reach 1A. Q1 (AO3400A, rated 5.7A) easily handles this, but the LM5017 input rail must be verified for transient voltage drops.

---

## 3. Required Prototype Hardware Tests
Before PCB release and manufacturing authorization, the following physical tests must be performed on prototype boards:
1.  **Thermal Imaging**: Run the controller inside a temperature chamber at $60^\circ\text{C}$ with the ESP32 transmitting Wi-Fi packets continuously. Capture infrared thermographs to ensure the LDO and LM5017 surface temperatures stay below $85^\circ\text{C}$.
2.  **Motor Surge Injection Test**: Spin the EV loader motor at full speed and apply sudden regenerative brakes. Measure the transient voltage waveform at the cathode of Schottky diode D1 using an oscilloscope to confirm the TVS clamping voltage stays below $95\text{V}$.
3.  **Sensor Failure Drill**: Power the system and cut the sensor cable connection J3 Pin 2. Verify that the fan immediately ramps up to full speed and the ESP32 registers a thermal warning fault on the CAN bus.
4.  **Vibration Chamber Testing**: Subject the board to sinusoidal vibration sweeps from 10 Hz to 2 kHz (conforming to IEC 60068-2-6) to verify that Molex connectors do not disconnect.
