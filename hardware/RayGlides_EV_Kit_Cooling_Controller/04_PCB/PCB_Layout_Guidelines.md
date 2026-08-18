# RayGlides 3W/4W EV Kit Cooling Controller — PCB Layout Guidelines

This document outlines structural rules, routing widths, stackups, and EMI mitigation practices for the cooling controller board.

---

## 1. PCB Stackup and Copper Weight
*   **Layer Count**: 2-Layer FR4 Board
*   **Board Thickness**: 1.6 mm
*   **Copper Thickness (Outer Layers)**: 2 oz/ft² (70 µm) — chosen to optimize thermal dissipation for the LM5017 buck regulator and minimize impedance on 12V fan power traces.
*   **Dielectric Material**: Standard FR-4 ($T_g \ge 150^\circ\text{C}$) to withstand elevated enclosure temperatures.

---

## 2. IPC-2152 Trace Width Calculations
All trace widths are calculated for a maximum $10^\circ\text{C}$ temperature rise over ambient using 2 oz copper:

1.  **Vehicle Power Input Trace (48V_IN / Fused_48V)**:
    *   *Design Current*: 0.5 A continuous
    *   *Minimum Trace Width*: **0.25 mm (10 mils)**
    *   *Implemented Trace Width*: **0.60 mm (24 mils)** for low series resistance and structural reliability.
2.  **Fan Switching Path (12V / FAN_DRAIN)**:
    *   *Design Current*: 0.3 A continuous, 0.6 A peak startup
    *   *Minimum Trace Width*: **0.30 mm (12 mils)**
    *   *Implemented Trace Width*: **0.80 mm (32 mils)** to minimize inductive voltage drop over switching cables.
3.  **Low-Current Logic / Sensor Signals (3.3V / 5V / ADC)**:
    *   *Design Current*: < 50 mA
    *   *Implemented Trace Width*: **0.25 mm (10 mils)** (standard signal routing width).

---

## 3. High-Voltage Creepage and Clearance
Following IPC-2221B parameters for a maximum vehicle peak voltage of 72V DC:
*   **Minimum Electrical Clearance (Uncoated)**: 0.635 mm (25 mils)
*   **Implemented Electrical Clearance**: **1.27 mm (50 mils)** between any 48V net and low-voltage logic (5V/3.3V/Sensor) nets to prevent arcing due to condensation or carbon buildup.

---

## 4. Ground Planes and Isolation Zones
*   **GND_PWR Plane**: Placed on the bottom layer covering the LM5017 buck regulator, the AP63205 buck regulator, and the AO3400A switching MOSFET. This handles heavy return currents and switching noise.
*   **GND_SENS Plane**: Placed on the top layer directly beneath the ESP32-S3 module, the LM35 sensor circuitry, and the analog RC filtering nodes. This plane must remain quiet and free of high-current return loops.
*   **Star Ground connection**: GND_PWR and GND_SENS must be joined at a single point (star ground / net tie) close to the negative terminal of the 3.3V LDO output capacitor. This prevents power stage ripple from shifting the ADC signal reference.

---

## 5. Component Placement Rules
1.  **Input Protection**: Place the fuse F1, TVS diode D2, and reverse-polarity Schottky diode D1 as close to the input connector J1 as possible to clamp voltage spikes before they propagate.
2.  **Regulator Layout**: Place LM5017 input bypass capacitors (C3) immediately adjacent to the VIN and PGND pins. Loop area between Vin pin, inductor, and ground return must be kept as small as possible to minimize radiated EMI.
3.  **Decoupling Capacitors**: Place 100nF decoupling capacitors (C8, C9) within 2mm of their respective IC pins (ESP32 VDD and LM35 VCC).
4.  **Analog Routing**: Route the temperature sensor signal (TEMP_RAW) parallel to the quiet analog ground line. Keep the signal trace away from the SW (Switch node of LM5017) and the FAN_DRAIN switching lines.
5.  **Thermal Vias**: Place a matrix of $3 \times 3$ thermal vias (0.3mm drill, 0.7mm pad) under the exposed pad (PowerPAD) of the LM5017 to dissipate heat into the bottom ground plane copper pour.
