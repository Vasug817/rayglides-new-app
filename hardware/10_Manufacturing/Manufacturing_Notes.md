# RayGlides 3W/4W EV Kit Cooling Controller — Manufacturing & Assembly Notes

This document provides production guidelines, board materials, soldering profiles, and wiring assembly specifications.

---

## 1. PCB Fabrication Specifications
*   **Material**: FR-4 TG150 (Glass transition temperature $\ge 150^\circ\text{C}$)
*   **Layer Count**: 2 Layers
*   **Board Thickness**: 1.6 mm
*   **Copper Weight (Outer)**: 2 oz/ft² (70 µm)
*   **Surface Finish**: HASL Lead-Free (RoHS compliant) or ENIG (Electroless Nickel Immersion Gold)
*   **Solder Mask Color**: Matte Green or Blue (LPI - Liquid Photoimageable)
*   **Silkscreen**: White (Lead-Free legibility)
*   **Minimum Drill Size**: 0.3 mm
*   **Minimum Trace/Space**: 0.15 mm (6 mils)

---

## 2. Component Assembly Instructions
*   **Solder Paste**: SAC305 (96.5% Sn, 3% Ag, 0.5% Cu) Lead-Free solder paste.
*   **SMD Reflow Profile**: Conforms to IPC/JEDEC J-STD-020E standard:
    *   *Preheat Temp*: $150^\circ\text{C}$ to $200^\circ\text{C}$ for 60-120 seconds
    *   *Time Above Liquidus ($217^\circ\text{C}$)*: 60-90 seconds
    *   *Peak Reflow Temp*: $245^\circ\text{C}$ to $250^\circ\text{C}$ for 20-30 seconds
*   **Manual Assembly**:
    *   Through-hole connectors J1, J2, J3, and temperature sensor U4 can be wave-soldered or hand-soldered at $350^\circ\text{C}$ using lead-free wire (Sn96.5/Ag3.0/Cu0.5).
    *   Ensure the exposed thermal pad of U1 (LM5017) is fully reflowed to the PCB thermal via pad to prevent regulator overheating.

---

## 3. Wiring and Harness Specifications
1.  **Input Power Harness (J1)**:
    *   *Connector Shell*: Molex Micro-Fit 3.0 2-circuit housing (43645-0200)
    *   *Terminal Crimp Pin*: Molex male/female tin crimp terminal (43030-0007)
    *   *Wire Gauge*: **20 AWG** (Teflon or silicone insulation rated for 300V, $105^\circ\text{C}$ operational temperature)
2.  **Fan Power Harness (J2)**:
    *   *Connector Shell*: Molex Micro-Fit 3.0 2-circuit housing (43645-0200)
    *   *Wire Gauge*: **20 AWG** or **22 AWG** (Red: +12V, Black: switched GND return)
3.  **Sensor Cable Harness (J3)**:
    *   *Connector Shell*: Molex Micro-Fit 3.0 3-circuit housing (43645-0300)
    *   *Wire Gauge*: **24 AWG** (shielded 3-conductor cable; shield must be connected to GND_SENS at the PCB side only to minimize EMI loop pickup)
