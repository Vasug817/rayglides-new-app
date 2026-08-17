# RayGlides 3W/4W EV Kit Cooling Controller — Wiring Diagram

This document details the external wiring harness hookups and connector interfaces.

---

## 1. Wiring Harness Layout Diagram

```text
               +----------------------------------------+
               |      COOLING CONTROLLER BOARD          |
               |                                        |
               |   [J1]               [J2]        [J3]  |
               +────┬──────────────────┬───────────┬────+
                    │                  │           │
           (48V vehicle input)     (To Fan)   (To Temp Sensor)
                    │                  │           │
       Pin 1: Red (48V+)      Pin 1: Red   Pin 1: Red (+5V)
       Pin 2: Blk (GND)       Pin 2: Blk   Pin 2: Wht (Vout)
                                           Pin 3: Blk (GND)
```

---

## 2. Connector Mappings and Pinouts

### A. Connector J1: Vehicle Power Input
*   **PCB Header Part**: Molex 43650-0215 (2-pin, single row, SMD, vertical)
*   **Cable Housing Part**: Molex 43645-0200 (2-pin receptacle)
*   **Crimp Terminal**: Molex 43030-0007 (female, tin-plated)
*   **Pin Definitions**:
    *   **Pin 1**: +48V DC nominal vehicle traction pack positive line (Red, 20 AWG)
    *   **Pin 2**: Ground power return (Black, 20 AWG)

### B. Connector J2: Cooling Fan Output
*   **PCB Header Part**: Molex 43650-0215 (2-pin, single row, SMD, vertical)
*   **Cable Housing Part**: Molex 43645-0200 (2-pin receptacle)
*   **Pin Definitions**:
    *   **Pin 1**: +12V DC filtered positive rail (Red, 20 AWG)
    *   **Pin 2**: Switched GND return (switched by Q1 low-side MOSFET, Black, 20 AWG)

### C. Connector J3: Temperature Sensor Extension
*   **PCB Header Part**: Molex 43650-0315 (3-pin, single row, SMD, vertical)
*   **Cable Housing Part**: Molex 43645-0300 (3-pin receptacle)
*   **Pin Definitions**:
    *   **Pin 1**: +5V DC filtered sensor power rail (Red, 24 AWG)
    *   **Pin 2**: Analog Vout signal return (White or Yellow, 24 AWG)
    *   **Pin 3**: Analog Ground return (Black, 24 AWG)
    *   *Shielding*: Twist the wires and wrap in copper braid shield. Connect the shield braid to **Pin 3** at the PCB side only.
