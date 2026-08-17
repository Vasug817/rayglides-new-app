# RayGlides 3W/4W EV Kit Cooling Controller — Complete Schematic

This document describes the complete schematic design, net names, and connectivity details for the RayGlides Cooling Controller PCB.

---

## 1. ASCII Circuit Schematics

### A. Input Filter and Overvoltage Protection Stage
```text
 48V_IN (J1.1) ────[ F1: Fuse 2A SB ]───┬────────[ D1: Schottky DFLS1100 ]───┬───────[ L1: 47uH ]───┬─────── Raw_EV_48V
                                         │                                    │                      │
                                    [D2: TVS]                            [C1: 10uF]             [C2: 10uF]
                                    SMCJ58A                              100V Elect.            100V Elect.
                                         │                                    │                      │
 GND_VEH (J1.2) ─────────────────────────┴────────────────────────────────────┴──────────────────────┴─────── GND_PWR
```

### B. 12V Synchronous Buck Stage (LM5017)
```text
                    L2: 220uH
 Raw_EV_48V ───┬───[ LM5017 ]───┬──────────────┬──────── 12V
               │    SW (Pin 8)  │              │
           [C3: 1uF]            ├──[D3: Boot]  ├──[C5: 10uF 25V]
           100V Cer.            │  (1N4148)    │
               │            [C4: 0.01uF]       ├──[R1: 88.7k]
               │                │              │
 GND_PWR ──────┴────────────────┴──────────────┼──[R2: 10k]─── FB (Pin 4)
                                               │
                                               └────────────── GND_PWR
```

### C. Fan Switching MOSFET Stage
```text
                   +12V
                    │
                [ J2: Fan Connector ]
                 Pin 1  Pin 2
                    │     │
                    │     ├───[ D4: Flyback Diode 1N4148 ]───┐
                    │     │                                  │
                    │     ├──────────────────────────────────┘
                    │     │
                    │     └───┐
                    │         │
                    │      [ Drain ]
                    │     MOSFET Q1 (AO3400A)
                    │    [ Gate ]  [ Source ]
                    │       │          │
 ESP32_GPIO18 ──[ R4: 100R ]┼          │
                            │          │
                       [ R5: 10k ]     │
                            │          │
 GND_PWR ───────────────────┴──────────┴────────────────────── GND_PWR
```

### D. Analog Temperature Sensor Interface (LM35)
```text
  +5V ────────┬───────────────────────────────┐
              │                               │
          [C8: 100nF]                      [ LM35 ]
              │                            VCC  V_OUT (Pin 2)
              │                             │     │
 GND_SENS ────┴─────────────────────────────┴     ├───[ R6: 1k ]───┬─── ESP32_GPIO4 (ADC1_CH3)
                                                  │                │
                                              [R7: 200R]      [C9: 100nF]
                                             (Pulldown)            │
                                                  │           [D5: TVS 3.3V]
 GND_SENS ────────────────────────────────────────┴────────────────┴─── GND_SENS
```

---

## 2. Component Pinout and Interconnect Netlist

| Net Name | From Component (Pin) | To Component (Pin) | Description |
| :--- | :--- | :--- | :--- |
| **48V_IN** | J1 Vehicle Power (1) | F1 Fuse Input (1) | Raw vehicle DC positive line |
| **GND_VEH** | J1 Vehicle Power (2) | D2 TVS Anode (2) | Ground return line from vehicle battery |
| **Raw_EV_48V**| F1 Fuse Output (2) | D1 Schottky Anode (1) | Internal fused power bus |
| **Protected_48V**| D1 Schottky Cathode (2) | L1 Inductor Input (1) | Schottky protected supply line |
| **12V** | LM5017 Buck Output (Pin 8 SW) | J2 Fan Output (1) | 12V rail for Fan and 5V Buck input |
| **5V** | AP63205 Output (Pin 6) | LM35 VCC (Pin 1) | 5V rail for Sensor and 3.3V LDO input |
| **3.3V** | AP2112K LDO Output (Pin 5) | ESP32-S3 VDD (Pin 3) | 3.3V MCU logic supply rail |
| **GND_PWR** | LM5017 Ground (Pin 5) | Q1 Source (Pin 3) | Primary buck converter ground plane |
| **GND_SENS** | LM35 Ground (Pin 3) | ESP32 Analog Ground (Pin 2) | Isolated quiet analog ground return |
| **ESP32_GPIO18**| ESP32-S3 (Pin 22 / GPIO18)| R4 Resistor Input (1) | Fan switching PWM control signal |
| **ESP32_GPIO4**| R6 Resistor Output (2) | ESP32-S3 (Pin 8 / GPIO4) | Temperature sensor ADC input line |
| **FAN_GATE** | R4 Resistor Output (2) | Q1 Gate (Pin 1) | MOSFET gate driving node |
| **FAN_DRAIN** | J2 Fan Pin (2) | Q1 Drain (Pin 2) | MOSFET switching node |
| **TEMP_RAW** | LM35 Output (Pin 2) | R6 Resistor Input (1) | Unfiltered analog temperature signal |
