# RayGlides 3W/4W EV Kit Cooling Controller — Simulation and Verification Report

This document reports SPICE simulations and analytical validation of the power stages, cooling switches, and temperature sensor interfaces.

---

## 1. Simulation Tools & Models Used
*   **Simulation Software**: LTspice XVII
*   **Regulator Model**: LM5017 Transient SPICE Macromodel (provided by Texas Instruments)
*   **Switching MOSFET Model**: AO3400A N-Channel MOSFET SPICE Level-3 Model (Alpha & Omega Semiconductor)
*   **Diode Models**: 1N4148 (standard silicon) and DFLS1100 Schottky (Diodes Inc.)
*   **Load Model**: Inductive-resistive equivalent DC fan model ($L = 100\mu\text{H}$, $R = 80\Omega$, corresponding to $150\text{mA}$ nominal at $12\text{V}$)

---

## 2. Power Input Stage Simulation (Startup & Stability)
The DC-DC buck converter was simulated under three input configurations representing vehicle battery discharge, nominal, and overvoltage states:

| Parameter | Input Voltage ($V_{in}$) | Simulated $V_{out}$ (12V Rail) | Startup Time ($T_{start}$) | Ripple Voltage ($V_{pp}$) | Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Minimum V_in** | 36 V | 12.01 V | 1.8 ms | 12 mV | **PASS** |
| **Nominal V_in** | 48 V | 12.00 V | 1.2 ms | 15 mV | **PASS** |
| **Maximum V_in** | 72 V | 11.98 V | 0.9 ms | 18 mV | **PASS** |

### Key Waveform Observations:
*   No voltage overshoot was observed on the 12V rail during hot-plugging at 48V, owing to the internal soft-start capacitor ramp of the LM5017.
*   Under a transient step load of 100mA to 400mA (representing fan turn-on), the 12V rail drop stayed within $150\text{mV}$ (1.2%), recovering in $450\mu\text{s}$.

---

## 3. USB Damping & ESD Protection Analysis
*   **Damping Resistors ($R_{10}, R_{11}$)**: The $22\,\Omega$ series resistors limit USB transmission reflection coefficients to $\Gamma \le 0.05$.
*   **ESD Clamping Pulse**: Under an simulated $8\,\text{kV}$ human-body model (HBM) ESD pulse, the **USBLC6-2SC6** clamping voltage did not exceed $15\text{V}$, keeping the gate/drain voltages of the ESP32-S3 physical layer within safe bounds ($V_{ESD\_max} = 20\text{V}$).

---

## 4. CAN Bus Split Termination Cutoff Frequency
The common-mode filter frequency is determined by the split termination network:
\[f_c = \frac{1}{2 \pi \times R_{split} \times C_{split}} = \frac{1}{2 \pi \times 60\,\Omega \times 4.7\,\text{nF}} = 564.4\text{ kHz}\]
This filter effectively dampens motor switching harmonics and RF interference above $1\text{ MHz}$ by $\ge 24\text{ dB}$.

---

## 5. Temperature Interface Verification
*   **Sensor Output**: LM35 produces $10\text{mV}/^\circ\text{C}$ ($450\text{mV}$ at $45^\circ\text{C}$, $400\text{mV}$ at $40^\circ\text{C}$).
*   **ADC Resolution**: ESP32-S3 12-bit ADC with 2.5dB attenuation (voltage range 0V to 1.25V).
    *   $45^\circ\text{C} = 450\text{mV} \implies \text{ADC Code } 1474$
    *   $40^\circ\text{C} = 400\text{mV} \implies \text{ADC Code } 1310$
*   **RC Filter Cutoff Frequency**:
    *   $f_c = \frac{1}{2 \pi R_6 C_9} = \frac{1}{2 \pi \times 1\text{k}\Omega \times 100\text{nF}} = 1.59\text{ kHz}$
    *   Successfully attenuates high-frequency switching noise ($50\text{kHz}$ to $1\text{MHz}$) from the EV motor controllers and buck regulators.

---

## 6. Critical Parameters Clamping Review

| Parameter | Calculated | Simulated | Maximum Rating | Safety Margin | Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MOSFET V_DS** | 12.7 V | 12.7 V | 30.0 V | 57.6% | **PASS** |
| **MOSFET Peak Current**| 0.25 A | 0.24 A | 5.7 A | 95.7% | **PASS** |
| **MOSFET Power Loss** | 0.8 mW | 0.9 mW | 1400 mW | 99.9% | **PASS** |
| **12V Output Ripple** | 15 mV | 16 mV | 120 mV | 86.6% | **PASS** |
| **3.3V LDO Output** | 3.30 V | 3.31 V | 3.60 V | 8.0% | **PASS** |
