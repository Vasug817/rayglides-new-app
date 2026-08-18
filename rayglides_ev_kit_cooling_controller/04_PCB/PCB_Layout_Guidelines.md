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
*   **Implemented Clearance**: **1.27 mm (50 mils)** between any 48V net and low-voltage logic (5V/3.3V/Sensor) nets to prevent arcing due to condensation or carbon buildup.

---

## 4. High-Speed USB and CAN Differential Routing
1.  **Native USB D+/D- Lines**:
    *   Route as a differential pair with **$90\,\Omega \pm 10\%$ differential impedance**.
    *   Trace widths of $0.20\text{mm}$ (8 mils) and spacing of $0.20\text{mm}$ (8 mils) over a solid ground plane.
    *   Keep the length matched to within **0.15 mm (6 mils)**. Do not use vias on USB lines unless absolutely necessary.
2.  **CAN Bus Network Lines**:
    *   Route as a differential pair with **$120\,\Omega \pm 10\%$ differential impedance**.
    *   Ensure the split termination resistors and capacitor are placed as close to J4 as possible to filter common-mode noise.

---

## 5. Octal PSRAM Guard Ringing & Protection
*   The ESP32-S3-N16R8 module contains 8MB of Octal PSRAM running on OPI mode at up to $120\text{MHz}$.
*   The pins **GPIO 26-37** must be surrounded by a continuous **ground shield ring** connected to the quiet analog ground plane (GND_SENS).
*   No other signal or power trace may run adjacent to or cross the Octal memory pins on any layer to avoid memory bus corruption and noise coupling.

---

## 6. Ground Planes and Isolation Zones
*   **GND_PWR Plane**: Placed on the bottom layer covering the LM5017 buck regulator, the AP63205 buck regulator, and the AO3400A switching MOSFET. This handles heavy return currents and switching noise.
*   **GND_SENS Plane**: Placed on the top layer directly beneath the ESP32-S3 module, the LM35 sensor circuitry, and the analog RC filtering nodes. This plane must remain quiet and free of high-current return loops.
*   **Star Ground connection**: GND_PWR and GND_SENS must be joined at a single point (star ground / net tie) close to the negative terminal of the 3.3V LDO output capacitor. This prevents power stage ripple from shifting the ADC signal reference.
