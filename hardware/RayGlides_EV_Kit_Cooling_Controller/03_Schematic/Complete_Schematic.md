# RayGlides 3W/4W EV Kit Cooling Controller — Complete Schematic (Optimized for ESP32-S3-N16R8)

This document describes the optimized schematic design, net names, and connectivity details for the RayGlides Cooling Controller PCB.

---

## 1. ASCII Circuit Schematics

### A. Power Input and Back-Power Safety Stage
```text
 48V_IN (J1.1) ────[ F1: Fuse 2A SB ]───┬────────[ D1: Schottky DFLS1100 ]───┬───────[ L1: 47uH ]───┬─────── Raw_EV_48V
                                         │                                    │                      │
                                    [D2: TVS]                            [C1: 10uF]             [C2: 10uF]
                                    SMCJ58A                              100V Elect.            100V Elect.
                                         │                                    │                      │
 GND_VEH (J1.2) ─────────────────────────┴────────────────────────────────────┴──────────────────────┴─────── GND_PWR

 VBUS_USB (J5) ───[ D6: Schottky MBRA210 ]───┬─── 5V (USB Powered mode)
                                             │
                                         [C11: 4.7uF]
                                             │
 GND_PWR ────────────────────────────────────┴────────────────────── GND_PWR
```
*   *Note*: D6 prevents back-feeding 5V from the vehicle's 48V-to-5V buck regulator into the host PC's USB port when programming the module on the vehicle.

### B. ESP32-S3-N16R8 Native USB-C Interface
```text
                  VBUS
                   │
           [ J5: USB-C Connector ]
             A6/B6 (D+)   A7/B7 (D-)   A1/B12 (GND)   A5 (CC1)   B5 (CC2)
                 │            │            │             │          │
                 ├──────┐     ├──────┐     │         [R8:5.1k]  [R9:5.1k]
                 │      │     │      │     │             │          │
             [ESD: USBLC6-2SC6]      │     │             └────┬─────┘
                 │      │     │      │     │                  │
           [R10: 22R] [R11: 22R]     │     │                  │
                 │      │     │      │     │                  │
 ESP32_GPIO20 ───┘      │     │      │     │                  │
 ESP32_GPIO19 ──────────┘     │      │     │                  │
 GND_PWR ─────────────────────┴──────┴─────┴──────────────────┴─── GND_PWR
```
*   *Note*: CC1/CC2 pull-down resistors (5.1k) configure the Type-C interface to request 5V from host power supplies. USBLC6-2SC6 clamps high-speed ESD transients.

### C. Integrated CAN Bus (TJA1050) Interface
```text
                              +5V
                               │
                          [ TJA1050 ]
            TXD (Pin 1)  RXD (Pin 4)  CANH (Pin 7)  CANL (Pin 6)  GND (Pin 2)
                 │            │            │             │             │
 ESP32_GPIO9 ────┘            │            │             │             │
 ESP32_GPIO10 ────────────────┘            ├─────[R12:60R]─────┐       │
                                           │                   │       │
                                           │               [C12:4.7nF] │
                                           │                   │       │
                                           ├─────[R13:60R]─────┴───────┤
                                           │                           │
                                        J4.1 (CANH)                J4.2 (CANL)
                                                                       │
 GND_PWR ──────────────────────────────────────────────────────────────┴─── GND_PWR
```
*   *Note*: CAN bus uses a split $120\Omega$ termination ($60\Omega + 60\Omega$) with a $4.7\text{nF}$ capacitor to bypass high-frequency common-mode noise.

### D. Analog Reference and RC Filter Stage (LM35)
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
                                                  │                │
                      [LM4040-1.0V]               │                │
                       V_REF Output ──────────────┴────────────────┴─── GND_SENS
```
*   *Note*: The LM4040 1.0V precision shunt reference provides a calibrated reference voltage, ensuring linear ADC conversions.

---

## 2. Component Pinout and Interconnect Netlist

| Net Name | From Component (Pin) | To Component (Pin) | Description |
| :--- | :--- | :--- | :--- |
| **48V_IN** | J1 Vehicle Power (1) | F1 Fuse Input (1) | Raw vehicle DC positive line |
| **GND_VEH** | J1 Vehicle Power (2) | D2 TVS Anode (2) | Ground return line from vehicle battery |
| **Raw_EV_48V**| F1 Fuse Output (2) | D1 Schottky Anode (1) | Internal fused power bus |
| **Protected_48V**| D1 Schottky Cathode (2) | L1 Inductor Input (1) | Schottky protected supply line |
| **12V** | LM5017 Buck Output (SW) | J2 Fan Output (1) | 12V rail for Fan and 5V Buck input |
| **5V** | AP63205 Output (Pin 6) | LM35 VCC (Pin 1) | 5V rail for Sensor and 3.3V LDO input |
| **3.3V** | AP2112K LDO Output (Pin 5) | ESP32-S3 VDD (Pin 3) | 3.3V MCU logic supply rail |
| **GND_PWR** | LM5017 Ground (Pin 5) | Q1 Source (Pin 3) | Primary buck converter ground plane |
| **GND_SENS** | LM35 Ground (Pin 3) | ESP32 Analog Ground (Pin 2) | Isolated quiet analog ground return |
| **ESP32_GPIO18**| ESP32-S3 (Pin 22 / GPIO18)| R4 Resistor Input (1) | Fan switching PWM control signal |
| **ESP32_GPIO4**| R6 Resistor Output (2) | ESP32-S3 (Pin 8 / GPIO4) | Temperature sensor ADC input line |
| **ESP32_GPIO9**| ESP32-S3 (Pin 13 / GPIO9) | TJA1050 TXD (Pin 1) | CAN TX communication line |
| **ESP32_GPIO10**| ESP32-S3 (Pin 14 / GPIO10)| TJA1050 RXD (Pin 4) | CAN RX communication line |
| **ESP32_GPIO19**| ESP32-S3 (Pin 23 / GPIO19)| R11 Resistor Output (2) | Native USB D- data line |
| **ESP32_GPIO20**| ESP32-S3 (Pin 24 / GPIO20)| R10 Resistor Output (2) | Native USB D+ data line |
| **CANH** | TJA1050 CANH (Pin 7) | J4 CAN Connector (Pin 1) | CAN high-level differential line |
| **CANL** | TJA1050 CANL (Pin 6) | J4 CAN Connector (Pin 2) | CAN low-level differential line |
| **FAN_GATE** | R4 Resistor Output (2) | Q1 Gate (Pin 1) | MOSFET gate driving node |
| **FAN_DRAIN** | J2 Fan Pin (2) | Q1 Drain (Pin 2) | MOSFET switching node |
| **TEMP_RAW** | LM35 Output (Pin 2) | R6 Resistor Input (1) | Unfiltered analog temperature signal |
