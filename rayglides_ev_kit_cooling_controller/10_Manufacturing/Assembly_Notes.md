# RayGlides 3W/4W EV Kit Cooling Controller — Assembly Notes

This document provides assembly line guidelines for solder paste application, components mounting, and visual inspection.

---

## 1. Moisture Sensitivity Level (MSL) Handling
*   **ESP32-S3-WROOM-1 Module**: Rated at **MSL 3**. If exposed to humidity for longer than 168 hours outside of protective vacuum packaging, it must be baked at $125^\circ\text{C}$ for 24 hours prior to reflow soldering to prevent internal delamination (popcorning).
*   **LM5017MR Regulator**: Rated at **MSL 3**. Follow standard J-STD-033 guidelines for moisture barrier bag exposure limits.

---

## 2. Stencil Design and Solder Paste Printing
*   **Stencil Material**: Stainless steel, laser-cut, 0.12 mm (5 mils) thickness.
*   **LM5017 Exposed Pad Stencil**: The stencil opening under the LM5017 thermal pad must be segmented into a $2 \times 2$ grid (matrix array) with $0.5\text{mm}$ bridges. This prevents component tilting or excessive solder paste squeezed out onto surrounding signal pins during reflow.
*   **Solder Paste Alignment**: Inspect paste printing registration prior to placing components. Solder coverage on pads must be $\ge 90\%$.

---

## 3. Visual Quality Inspection Criteria (IPC-A-610 Class 2)
1.  **Solder Fillet**: Solder joints on SOT-23 (Q1), SOT-23-6 (ESD1), TSOT26 (U2), SOIC-8 (U6), and SO-PowerPAD-8 (U1) must show a positive concave meniscus fillet, showing good wetting.
2.  **Thermal Vias**: Solder voiding inside the thermal vias under the LM5017 exposed pad must not exceed 25% of the total pad area (measured via X-ray inspection).
3.  **Through-Hole Connectors**: Verify that Molex connector solder pins project $0.5\text{mm}$ to $1.5\text{mm}$ beyond the bottom solder pad, showing full barrel fill (minimum 75% vertical fill).
