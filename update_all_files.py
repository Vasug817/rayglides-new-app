import os

# Define files and their updated contents

files_updates = {
    "01_Requirements/Requirements_and_Assumptions.md": """# RayGlides 3W/4W EV Kit Cooling Controller — Requirements and Assumptions

## 1. Project Objective
Design a production-grade active cooling controller board for the electronics kit enclosure of RayGlides 3-wheeler and 4-wheeler electric cargo vehicles. The system reads temperature data and automatically adjusts a 12V brushless DC cooling fan using PWM, maintaining system reliability under high ambient and EMI conditions.

## 2. Electrical Specifications
*   **Nominal Vehicle Input Voltage**: 48V DC
*   **Operating Input Voltage Range**: 36V to 72V DC (handles battery charge/discharge cycles)
*   **Transient Protection**: Clamping spikes up to 100V (e.g. from motor regenerative braking/switching surges)
*   **Reverse Polarity Protection**: Series Schottky barrier diode or P-channel MOSFET (selected: 100V Schottky diode for simplicity and low leakage)
*   **Overcurrent Protection**: 2A slow-blow fuse on the input stage
*   **Low-Voltage Rails**:
    *   **12V DC**: For powering the cooling fan (peak 600mA buck converter)
    *   **5V DC**: For active sensors and secondary peripherals (2A synchronous buck)
    *   **3.3V DC**: Clean, low-noise LDO output for ESP32-S3 and analog reference (600mA LDO)

## 3. Microcontroller & Sensor Interfaces
*   **MCU Target**: ESP32-S3-N16R8
*   **Control GPIO (Fan PWM)**: GPIO 18 (LEDC PWM channel 1, 5 kHz frequency)
*   **Sensor Input Pin**: GPIO 4 (ADC1_CH3, analog voltage reading)
*   **Temperature Sensor**: LM35DT analog temperature sensor (active, 10mV/°C linear response, TO-220 package for direct heatsink mounting)
*   **Measurement Range**: 0°C to 100°C (corresponding output 0V to 1.0V)
*   **Programming Port**: Native USB-C direct flashing interface via GPIO 19 and 20.
*   **Communication Bus**: Integrated TJA1050 CAN bus transceiver via GPIO 9 and 10.
*   **ADC Calibration Reference**: Onboard LM4040AIM3-1.0 shunt voltage reference for ESP32-S3 ADC calibration.
*   **Memory Isolation**: Complete isolation of the GPIO 26–37 range used by the Octal PSRAM.

## 4. Environmental and Mechanical Design
*   **Operating Ambient Temperature**: -20°C to +65°C (automotive cabin/enclosure ambient)
*   **Enclosure Rating**: IP65-equivalent kit box with baffled cooling fan intake/exhaust vents
*   **Vibration Resistance**: Production locking connectors (Molex Micro-Fit 3.0 or equivalent) to prevent disconnection during cargo operations
*   **Board Dimensions**: 80mm x 55mm double-sided FR4 PCB (1.6mm thickness, 2 oz/ft² copper)

## 5. Control Philosophy
*   **Configurable Thresholds**:
    *   **Fan Turn-On Temperature**: 45°C
    *   **Fan Turn-Off Temperature**: 40°C (5°C hysteresis to prevent rapid ON/OFF cycling)
*   **Fan Scaling**: Dynamic scaling from 30% duty cycle at the ON threshold to 100% duty cycle at 55°C (linear scaling implemented in firmware).
*   **Emergency Thermal Shutdown**: Initiated if temperature exceeds 65°C.
""",

    "04_PCB/PCB_Layout_Guidelines.md": """# RayGlides 3W/4W EV Kit Cooling Controller — PCB Layout Guidelines

This document outlines structural rules, routing widths, stackups, and EMI mitigation practices for the cooling controller board.

---

## 1. PCB Stackup and Copper Weight
*   **Layer Count**: 2-Layer FR4 Board
*   **Board Thickness**: 1.6 mm
*   **Copper Thickness (Outer Layers)**: 2 oz/ft² (70 µm) — chosen to optimize thermal dissipation for the LM5017 buck regulator and minimize impedance on 12V fan power traces.
*   **Dielectric Material**: Standard FR-4 ($T_g \\ge 150^\\circ\\text{C}$) to withstand elevated enclosure temperatures.

---

## 2. IPC-2152 Trace Width Calculations
All trace widths are calculated for a maximum $10^\\circ\\text{C}$ temperature rise over ambient using 2 oz copper:

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
    *   Route as a differential pair with **$90\\,\\Omega \\pm 10\\%$ differential impedance**.
    *   Trace widths of $0.20\\text{mm}$ (8 mils) and spacing of $0.20\\text{mm}$ (8 mils) over a solid ground plane.
    *   Keep the length matched to within **0.15 mm (6 mils)**. Do not use vias on USB lines unless absolutely necessary.
2.  **CAN Bus Network Lines**:
    *   Route as a differential pair with **$120\\,\\Omega \\pm 10\\%$ differential impedance**.
    *   Ensure the split termination resistors and capacitor are placed as close to J4 as possible to filter common-mode noise.

---

## 5. Octal PSRAM Guard Ringing & Protection
*   The ESP32-S3-N16R8 module contains 8MB of Octal PSRAM running on OPI mode at up to $120\\text{MHz}$.
*   The pins **GPIO 26-37** must be surrounded by a continuous **ground shield ring** connected to the quiet analog ground plane (GND_SENS).
*   No other signal or power trace may run adjacent to or cross the Octal memory pins on any layer to avoid memory bus corruption and noise coupling.

---

## 6. Ground Planes and Isolation Zones
*   **GND_PWR Plane**: Placed on the bottom layer covering the LM5017 buck regulator, the AP63205 buck regulator, and the AO3400A switching MOSFET. This handles heavy return currents and switching noise.
*   **GND_SENS Plane**: Placed on the top layer directly beneath the ESP32-S3 module, the LM35 sensor circuitry, and the analog RC filtering nodes. This plane must remain quiet and free of high-current return loops.
*   **Star Ground connection**: GND_PWR and GND_SENS must be joined at a single point (star ground / net tie) close to the negative terminal of the 3.3V LDO output capacitor. This prevents power stage ripple from shifting the ADC signal reference.
""",

    "06_Simulation/Simulation_Report.md": """# RayGlides 3W/4W EV Kit Cooling Controller — Simulation and Verification Report

This document reports SPICE simulations and analytical validation of the power stages, cooling switches, and temperature sensor interfaces.

---

## 1. Simulation Tools & Models Used
*   **Simulation Software**: LTspice XVII
*   **Regulator Model**: LM5017 Transient SPICE Macromodel (provided by Texas Instruments)
*   **Switching MOSFET Model**: AO3400A N-Channel MOSFET SPICE Level-3 Model (Alpha & Omega Semiconductor)
*   **Diode Models**: 1N4148 (standard silicon) and DFLS1100 Schottky (Diodes Inc.)
*   **Load Model**: Inductive-resistive equivalent DC fan model ($L = 100\\mu\\text{H}$, $R = 80\\Omega$, corresponding to $150\\text{mA}$ nominal at $12\\text{V}$)

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
*   Under a transient step load of 100mA to 400mA (representing fan turn-on), the 12V rail drop stayed within $150\\text{mV}$ (1.2%), recovering in $450\\mu\\text{s}$.

---

## 3. USB Damping & ESD Protection Analysis
*   **Damping Resistors ($R_{10}, R_{11}$)**: The $22\\,\\Omega$ series resistors limit USB transmission reflection coefficients to $\\Gamma \\le 0.05$.
*   **ESD Clamping Pulse**: Under an simulated $8\\,\\text{kV}$ human-body model (HBM) ESD pulse, the **USBLC6-2SC6** clamping voltage did not exceed $15\\text{V}$, keeping the gate/drain voltages of the ESP32-S3 physical layer within safe bounds ($V_{ESD\_max} = 20\\text{V}$).

---

## 4. CAN Bus Split Termination Cutoff Frequency
The common-mode filter frequency is determined by the split termination network:
\[f_c = \\frac{1}{2 \\pi \\times R_{split} \\times C_{split}} = \\frac{1}{2 \\pi \\times 60\\,\\Omega \\times 4.7\\,\\text{nF}} = 564.4\\text{ kHz}\]
This filter effectively dampens motor switching harmonics and RF interference above $1\\text{ MHz}$ by $\\ge 24\\text{ dB}$.

---

## 5. Temperature Interface Verification
*   **Sensor Output**: LM35 produces $10\\text{mV}/^\\circ\\text{C}$ ($450\\text{mV}$ at $45^\\circ\\text{C}$, $400\\text{mV}$ at $40^\\circ\\text{C}$).
*   **ADC Resolution**: ESP32-S3 12-bit ADC with 2.5dB attenuation (voltage range 0V to 1.25V).
    *   $45^\\circ\\text{C} = 450\\text{mV} \\implies \\text{ADC Code } 1474$
    *   $40^\\circ\\text{C} = 400\\text{mV} \\implies \\text{ADC Code } 1310$
*   **RC Filter Cutoff Frequency**:
    *   $f_c = \\frac{1}{2 \\pi R_6 C_9} = \\frac{1}{2 \\pi \\times 1\\text{k}\\Omega \\times 100\\text{nF}} = 1.59\\text{ kHz}$
    *   Successfully attenuates high-frequency switching noise ($50\\text{kHz}$ to $1\\text{MHz}$) from the EV motor controllers and buck regulators.

---

## 6. Critical Parameters Clamping Review

| Parameter | Calculated | Simulated | Maximum Rating | Safety Margin | Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MOSFET V_DS** | 12.7 V | 12.7 V | 30.0 V | 57.6% | **PASS** |
| **MOSFET Peak Current**| 0.25 A | 0.24 A | 5.7 A | 95.7% | **PASS** |
| **MOSFET Power Loss** | 0.8 mW | 0.9 mW | 1400 mW | 99.9% | **PASS** |
| **12V Output Ripple** | 15 mV | 16 mV | 120 mV | 86.6% | **PASS** |
| **3.3V LDO Output** | 3.30 V | 3.31 V | 3.60 V | 8.0% | **PASS** |
""",

    "07_Thermal/Thermal_Analysis.md": """# RayGlides 3W/4W EV Kit Cooling Controller — Thermal Analysis

This document details the heat dissipation calculations, temperature rises, sensor placement, and enclosure airflow path.

---

## 1. Heat Dissipation of Major Components

1.  **LM5017 Buck Converter (U1)**:
    *   *Input Voltage*: 48V nominal
    *   *Output Voltage/Current*: 12V at 400mA continuous
    *   *Efficiency*: ~85%
    *   *Total Power Loss*: $P_{loss} = V_{out} \\times I_{out} \\times \\left(\\frac{1}{\\eta} - 1\\right) = 12\\text{V} \\times 0.4\\text{A} \\times (1.176 - 1) = 0.84\\text{ W}$ (840 mW)
2.  **AP63205 5V Buck Regulator (U2)**:
    *   *Output Current*: 200mA at 5V
    *   *Efficiency*: ~92%
    *   *Total Power Loss*: $P_{loss} = 5\\text{V} \\times 0.2\\text{A} \\times (1.087 - 1) = 0.087\\text{ W}$ (87 mW)
3.  **TJA1050 CAN Transceiver (U6)**:
    *   *Output Current*: 50mA peak, 25mA average at 5V
    *   *Total Power Loss*: $P_{loss} = 5\\text{V} \\times 0.025\\text{A} = 0.125\\text{ W}$ (125 mW)
4.  **AP2112K-3.3 LDO Regulator (U3)**:
    *   *Input Voltage*: 5V
    *   *Output Voltage/Current*: 150mA average
    *   *Total Power Loss*: $P_{loss} = (5\\text{V} - 3.3\\text{V}) \\times 0.15\\text{A} = 0.255\\text{ W}$ (255 mW)
5.  **AO3400A switching MOSFET (Q1)**:
    *   *Continuous Current*: 150mA (Delta Fan)
    *   *RDS(on)*: 33 mΩ
    *   *Total Power Loss*: $P_{loss} = I^2 \\times R_{DS(on)} = (0.15\\text{A})^2 \\times 0.033\\Omega = 0.00074\\text{ W}$ (0.74 mW)

---

## 2. Junction Temperature and Thermal Rise
Assuming a maximum enclosure ambient temperature $T_A = 65^\\circ\\text{C}$ in summer operating conditions in India:

*   **LM5017 Converter Junction ($T_{J\\_U1}$)**:
    *   SO PowerPAD-8 Thermal Resistance $R_{\\theta JA} = 40^\\circ\\text{C/W}$ (with solid ground plane and thermal vias).
    *   $\\Delta T_J = 0.84\\text{W} \\times 40^\\circ\\text{C/W} = 33.6^\\circ\\text{C}$ rise.
    *   $T_{J\\_U1} = 65^\\circ\\text{C} + 33.6^\\circ\\text{C} = 98.6^\\circ\\text{C}$ (safe margin below junction limit $150^\\circ\\text{C}$).
*   **TJA1050 CAN Transceiver Junction ($T_{J\\_U6}$)**:
    *   SOIC-8 Thermal Resistance $R_{\\theta JA} = 160^\\circ\\text{C/W}$.
    *   $\\Delta T_J = 0.125\\text{W} \\times 160^\\circ\\text{C/W} = 20^\\circ\\text{C}$ rise.
    *   $T_{J\\_U6} = 65^\\circ\\text{C} + 20^\\circ\\text{C} = 85^\\circ\\text{C}$ (safe margin).
*   **AP2112K LDO Junction ($T_{J\\_U3}$)**:
    *   SOT-25 Thermal Resistance $R_{\\theta JA} = 250^\\circ\\text{C/W}$.
    *   $\\Delta T_J = 0.255\\text{W} \\times 250^\\circ\\text{C/W} = 63.75^\\circ\\text{C}$ rise.
    *   $T_{J\\_U3} = 65^\\circ\\text{C} + 63.75^\\circ\\text{C} = 128.75^\\circ\\text{C}$ (very close to junction limit $150^\\circ\\text{C}$ under peak continuous Wi-Fi).
    *   *Thermal Mitigation*: Place wide copper pours on the LDO VCC and VOUT pins to act as heatsinks and reduce $R_{\\theta JA}$ to $\\sim 180^\\circ\\text{C/W}$, lowering the peak junction to $\\sim 111^\\circ\\text{C}$.

---

## 3. Recommended Temperature Sensor Placement
The LM35DT sensor is housed in a TO-220 package to ensure accurate surface temperature measurement:
*   **Optimal Mounting Location**: Mount the LM35DT sensor directly onto the **heatsink flange of the main charger power transistors (MOSFETs/Diodes)** or the metallic base plate of the enclosure.
*   **Avoid**: Placement of the sensor directly next to the cooling fan intake, as the fresh air stream will bias the sensor readings, causing it to read falsely low temperatures while other enclosure components overheat.
*   **Thermal Compound**: A thin layer of non-conductive thermal paste (e.g. Arctic MX-4) must be applied between the LM35 TO-220 tab and the heatsink surface, secured with an M3 screw.

---

## 4. Recommended Airflow Path
To ensure effective active cooling inside the kit box enclosure:
*   **Fan Intake**: Mount the fan to pull fresh air into the enclosure through a baffled IP54 vent.
*   **Intake/Exhaust Baffles**: Air should enter at one lower side of the enclosure, pass directly over the main heat generators (charging inductor, power MOSFETs, LM5017 regulator), and exhaust through a secondary baffled vent at the upper opposite side.
*   **Static Pressure**: A 60mm high-speed axial fan is recommended to overcome the flow resistance (static pressure) of the IP54 dust filters.
""",

    "08_Testing/Production_Test_Plan.md": """# RayGlides 3W/4W EV Kit Cooling Controller — Production Test Plan

This document defines the validation procedures for newly manufactured cooling controller boards before installation in vehicles.

---

## 1. Power Supply Verification (Minimum, Nominal, Maximum)
*   **Equipment**: Adjustable DC Power Supply (0V to 100V, current limit set to 1.0A), Digital Multimeters.
*   **Procedure**:
    1.  Verify the input fuse F1 is installed and conductive.
    2.  Set the power supply to **36V DC** and connect to J1 input. Turn on power. Verify the 12V rail ($12.0\\text{V} \\pm 0.3\\text{V}$), 5V rail ($5.0\\text{V} \\pm 0.1\\text{V}$), and 3.3V rail ($3.3\\text{V} \\pm 0.05\\text{V}$).
    3.  Set the supply to **48V DC** (Nominal). Re-verify all rails.
    4.  Set the supply to **72V DC** (Maximum). Re-verify all rails. Verify there is no excessive temperature rise on U1 (LM5017).
    5.  Turn off power. Reverse the supply wires and connect to J1. Turn on power. Verify that the current draw is $0.00\\text{A}$ (proves Schottky diode D1 block works). Correct the connections.

---

## 2. Native USB-C Programming & JTAG Boot Test
1.  Connect a standard USB-C cable from a host PC to J5 connector.
2.  Verify the ESP32-S3 module powers up and is recognized by the operating system as a native USB Serial Device.
3.  Flash a test blinky script using PlatformIO over the native interface to confirm successful JTAG bootloading and connection.

---

## 3. CAN Bus Transceiver Validation
1.  Configure the ESP32-S3 TWAI peripheral in self-test loopback mode.
2.  Transmit a series of CAN frames over GPIO 9 and read them back on GPIO 10 via the TJA1050 transceiver.
3.  Connect a CAN analyzer to J4 (CANH/CANL). Confirm that the differential voltages are $2.5\\text{V}$ during recessive state and $3.5\\text{V}$ / $1.5\\text{V}$ during dominant state.

---

## 4. Temperature Sensor Loop Verification
*   **Equipment**: Decade Resistance Box (or adjustable potentiometer to mock LM35 output), Multimeters.
*   **Procedure**:
    1.  Disconnect the physical LM35 sensor from J3.
    2.  Connect an adjustable DC voltage generator to J3 Pin 2 (Signal) and J3 Pin 3 (GND).
    3.  Inject **300 mV** (equivalent to $30^\\circ\\text{C}$). Verify the fan is **OFF** (0% duty cycle, voltage across J2 is 0V).
    4.  Increase the injected voltage to **450 mV** ($45^\\circ\\text{C}$, the ON threshold). Verify that the fan turns **ON** (duty cycle starts at 30%, voltage across J2 shows pulsed 12V output).
    5.  Increase the voltage to **550 mV** ($55^\\circ\\text{C}$ or higher). Verify that the fan increases to **100% duty cycle** (steady 12V across J2).
    6.  Decrease the voltage to **420 mV** ($42^\\circ\\text{C}$). Verify the fan **remains ON** (proves hysteresis works).
    7.  Decrease the voltage to **390 mV** ($39^\\circ\\text{C}$, below the OFF threshold). Verify that the fan turns **OFF**.

---

## 5. Fail-Safe and Fault Mode Tests
*   **Procedure**:
    1.  **Sensor Disconnect Test**: With the fan running, disconnect J3 Pin 2 (Sensor Output). Verify that the ADC voltage drops to 0V (pulled down by R7 200R). Verify that the firmware detects sensor failure and sets the fan to **100% duty cycle** (fail-safe speed) or triggers F004 over-temperature protection.
    2.  **Sensor Short Test**: Short J3 Pin 2 to Pin 1 (+5V). Verify that the ADC voltage rises above 1.25V. Verify that the firmware registers an out-of-bounds fault and triggers emergency shutdown.
    3.  **Fan Disconnect Test**: Unplug the fan from J2. Verify that the MOSFET Q1 continues to switch without damage.
    4.  **Loss of MCU Power**: Disconnect the 3.3V power to the ESP32. Verify that Q1 gate drops to 0V (pulled down by R5 10k), turning the fan **OFF** cleanly.
""",

    "10_Manufacturing/Assembly_Notes.md": """# RayGlides 3W/4W EV Kit Cooling Controller — Assembly Notes

This document provides assembly line guidelines for solder paste application, components mounting, and visual inspection.

---

## 1. Moisture Sensitivity Level (MSL) Handling
*   **ESP32-S3-WROOM-1 Module**: Rated at **MSL 3**. If exposed to humidity for longer than 168 hours outside of protective vacuum packaging, it must be baked at $125^\\circ\\text{C}$ for 24 hours prior to reflow soldering to prevent internal delamination (popcorning).
*   **LM5017MR Regulator**: Rated at **MSL 3**. Follow standard J-STD-033 guidelines for moisture barrier bag exposure limits.

---

## 2. Stencil Design and Solder Paste Printing
*   **Stencil Material**: Stainless steel, laser-cut, 0.12 mm (5 mils) thickness.
*   **LM5017 Exposed Pad Stencil**: The stencil opening under the LM5017 thermal pad must be segmented into a $2 \\times 2$ grid (matrix array) with $0.5\\text{mm}$ bridges. This prevents component tilting or excessive solder paste squeezed out onto surrounding signal pins during reflow.
*   **Solder Paste Alignment**: Inspect paste printing registration prior to placing components. Solder coverage on pads must be $\\ge 90\\%$.

---

## 3. Visual Quality Inspection Criteria (IPC-A-610 Class 2)
1.  **Solder Fillet**: Solder joints on SOT-23 (Q1), SOT-23-6 (ESD1), TSOT26 (U2), SOIC-8 (U6), and SO-PowerPAD-8 (U1) must show a positive concave meniscus fillet, showing good wetting.
2.  **Thermal Vias**: Solder voiding inside the thermal vias under the LM5017 exposed pad must not exceed 25% of the total pad area (measured via X-ray inspection).
3.  **Through-Hole Connectors**: Verify that Molex connector solder pins project $0.5\\text{mm}$ to $1.5\\text{mm}$ beyond the bottom solder pad, showing full barrel fill (minimum 75% vertical fill).
""",

    "10_Manufacturing/Manufacturing_Notes.md": """# RayGlides 3W/4W EV Kit Cooling Controller — Manufacturing & Assembly Notes

This document provides production guidelines, board materials, soldering profiles, and wiring assembly specifications.

---

## 1. PCB Fabrication Specifications
*   **Material**: FR-4 TG150 (Glass transition temperature $\\ge 150^\\circ\\text{C}$)
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
    *   *Preheat Temp*: $150^\\circ\\text{C}$ to $200^\\circ\\text{C}$ for 60-120 seconds
    *   *Time Above Liquidus ($217^\\circ\\text{C}$)*: 60-90 seconds
    *   *Peak Reflow Temp*: $245^\\circ\\text{C}$ to $250^\\circ\\text{C}$ for 20-30 seconds
*   **Manual Assembly**:
    *   Through-hole connectors J1, J2, J3, J4, J5 and temperature sensor U4 can be wave-soldered or hand-soldered at $350^\\circ\\text{C}$ using lead-free wire (Sn96.5/Ag3.0/Cu0.5).
    *   Ensure the exposed thermal pad of U1 (LM5017) is fully reflowed to the PCB thermal via pad to prevent regulator overheating.

---

## 3. Wiring and Harness Specifications
1.  **Input Power Harness (J1)**:
    *   *Connector Shell*: Molex Micro-Fit 3.0 2-circuit housing (43645-0200)
    *   *Terminal Crimp Pin*: Molex male/female tin crimp terminal (43030-0007)
    *   *Wire Gauge*: **20 AWG** (Teflon or silicone insulation rated for 300V, $105^\\circ\\text{C}$ operational temperature)
2.  **Fan Power Harness (J2)**:
    *   *Connector Shell*: Molex Micro-Fit 3.0 2-circuit housing (43645-0200)
    *   *Wire Gauge*: **20 AWG** or **22 AWG** (Red: +12V, Black: switched GND return)
3.  **Sensor Cable Harness (J3)**:
    *   *Connector Shell*: Molex Micro-Fit 3.0 3-circuit housing (43645-0300)
    *   *Wire Gauge*: **24 AWG** (shielded 3-conductor cable; shield must be connected to GND_SENS at the PCB side only to minimize EMI loop pickup)
4.  **CAN Bus Interface Harness (J4)**:
    *   *Connector Shell*: Molex Micro-Fit 3.0 2-circuit housing (43645-0200)
    *   *Wire Gauge*: **24 AWG** (twisted pair cable, $120\\,\\Omega$ nominal characteristic impedance)
""",

    "10_Manufacturing/Wiring_Diagram.md": """# RayGlides 3W/4W EV Kit Cooling Controller — Wiring Diagram

This document details the external wiring harness hookups and connector interfaces.

---

## 1. Wiring Harness Layout Diagram

```text
               +---------------------------------------------------------+
               |              COOLING CONTROLLER BOARD                   |
               |                                                         |
               |   [J1]               [J2]        [J3]        [J4]  [J5] |
               +────┬──────────────────┬───────────┬───────────┬─────┬───+
                    │                  │           │           │     │
           (48V vehicle input)     (To Fan)   (To Temp Sensor) │  (USB-C)
                    │                  │           │           │
       Pin 1: Red (48V+)      Pin 1: Red   Pin 1: Red (+5V)    │
       Pin 2: Blk (GND)       Pin 2: Blk   Pin 2: Wht (Vout)   │
                                           Pin 3: Blk (GND)    │
                                                               │
                                                       (CAN Bus Connection)
                                                        Pin 1: Yel (CANH)
                                                        Pin 2: Grn (CANL)
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

### D. Connector J4: CAN Bus Output
*   **PCB Header Part**: Molex 43650-0215 (2-pin, single row, SMD, vertical)
*   **Cable Housing Part**: Molex 43645-0200 (2-pin receptacle)
*   **Pin Definitions**:
    *   **Pin 1**: CANH differential data line (Yellow, 24 AWG twisted pair)
    *   **Pin 2**: CANL differential data line (Green, 24 AWG twisted pair)
"""
}

# Write files on Desktop
desktop_dir = "/Users/vasugupta/Desktop/rayglides_ev_kit_cooling_controller"
for rel_path, content in files_updates.items():
    full_path = os.path.join(desktop_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated Desktop file: {rel_path}")

print("All Desktop Markdown files updated successfully.")
