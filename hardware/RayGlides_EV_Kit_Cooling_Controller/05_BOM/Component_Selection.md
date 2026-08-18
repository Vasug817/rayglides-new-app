# RayGlides 3W/4W EV Kit Cooling Controller — Component Selection Rationale (Optimized for ESP32-S3-N16R8)

This document provides a detailed engineering review of the primary component selections, package decisions, and alternative source allocations.

---

## 1. Primary Component Choices

### A. Power Regulator: LM5017MR/NOPB (Texas Instruments)
*   **Alternative Part**: LMR16006YQ5DDCTQ1 (Automotive-grade, 60V, SOT-23-6)
*   **Package**: SO-PowerPAD-8 (with exposed bottom thermal pad)
*   **Voltage/Current Rating**: 100V peak input voltage, 600mA maximum output current
*   **Key Specifications**: Constant On-Time (COT) control loop, integrated high-side and low-side N-Channel switches, UVLO threshold.
*   **Selection Rationale**: In 3W/4W EV traction power networks, transient voltage spikes from the motor controller switching and regenerative braking cycles can exceed $80\text{V}$. The LM5017's 100V operating limit provides a massive safety margin, preventing regulator breakdown without requiring large shunt clamp resistors.

### B. Switching MOSFET: AO3400A (Alpha & Omega Semiconductor)
*   **Alternative Part**: BSS138 (50V, SOT-23, lower current) or PMV16XNR (30V, SOT-23, automotive)
*   **Package**: SOT-23
*   **Voltage/Current Rating**: 30V maximum drain-source voltage, 5.7A maximum continuous drain current
*   **Key Specifications**: $R_{DS(on)} < 33\text{m}\Omega$ at $V_{GS} = 3.3\text{V}$, gate threshold voltage $V_{GS(th)} \approx 1.0\text{V}$.
*   **Selection Rationale**: The ESP32-S3 microcontroller outputs a $3.3\text{V}$ logic signal. Standard MOSFETs require $5\text{V}$ or $10\text{V}$ gate drive to saturate. The AO3400A is a true logic-level MOSFET that saturates at $2.5\text{V}$ gate voltage. The low $R_{DS(on)}$ at $3.3\text{V}$ minimizes conduction heating, allowing the SOT-23 package to switch the $150\text{mA}$ fan safely.

### C. Temperature Sensor: LM35DT/NOPB (Texas Instruments)
*   **Alternative Part**: MCP9700A-E/TO (Active analog, 10mV/°C, 500mV offset at 0°C)
*   **Package**: TO-220-3 (Metal tab package)
*   **Accuracy**: $\pm0.5^\circ\text{C}$ at room temperature, calibrated directly in Celsius
*   **Key Specifications**: 10 mV/°C scale factor, works from 4V to 30V VCC.
*   **Selection Rationale**: The TO-220 package can be directly bolted to a heatsink using an M3 screw. LM35 has a linear output ($10\text{mV}/^\circ\text{C}$), which requires no complex polynomial scaling in the firmware, unlike thermistors.

### D. CAN Transceiver: TJA1050T/3 (NXP Semiconductors)
*   **Alternative Part**: SN65HVD230 (3.3V powered CAN transceiver) or MCP2551
*   **Package**: SOIC-8
*   **Voltage Rating**: 5V VCC power supply, 1 Mbps high-speed transmission
*   **Selection Rationale**: The ESP32-S3 has a built-in TWAI (CAN) controller. The TJA1050T interfaces directly with ESP32-S3 GPIO 9 and 10 to establish robust differential CANH/CANL lines. Powered from the stable 5V rail, it provides high noise immunity and electrostatic discharge (ESD) protection for automotive CAN bus environments.

### E. ADC Voltage Reference: LM4040AIM3-1.0/NOPB (Texas Instruments)
*   **Alternative Part**: ADR510ARTZ (1.0V precision shunt voltage reference)
*   **Package**: SOT-23
*   **Key Specifications**: 1.0 V output, 0.1% accuracy, low temperature coefficient.
*   **Selection Rationale**: The ESP32-S3's internal ADC reference is unstable and exhibits non-linear behavior under RF loading. Using the LM4040AIM3-1.0 reference diode enables precise calibration of the ADC, mapping the LM35's 0-1.0V (0°C to 100°C) linear analog voltage with maximum resolution.

### F. ESD Protection: USBLC6-2SC6 (STMicroelectronics)
*   **Package**: SOT-23-6
*   **Selection Rationale**: A low-capacitance rail-to-rail ESD protection array placed directly on the USB-C D+/D- lines prevents electro-static discharges from the programming cable from damaging the ESP32-S3 native USB peripheral.
