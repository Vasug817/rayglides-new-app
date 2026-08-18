# RayGlides 3W/4W EV Kit Cooling Controller — Thermal Analysis

This document details the heat dissipation calculations, temperature rises, sensor placement, and enclosure airflow path.

---

## 1. Heat Dissipation of Major Components

1.  **LM5017 Buck Converter (U1)**:
    *   *Input Voltage*: 48V nominal
    *   *Output Voltage/Current*: 12V at 400mA continuous
    *   *Efficiency*: ~85%
    *   *Total Power Loss*: $P_{loss} = V_{out} \times I_{out} \times \left(\frac{1}{\eta} - 1\right) = 12\text{V} \times 0.4\text{A} \times (1.176 - 1) = 0.84\text{ W}$ (840 mW)
2.  **AP63205 5V Buck Regulator (U2)**:
    *   *Output Current*: 200mA at 5V
    *   *Efficiency*: ~92%
    *   *Total Power Loss*: $P_{loss} = 5\text{V} \times 0.2\text{A} \times (1.087 - 1) = 0.087\text{ W}$ (87 mW)
3.  **AP2112K-3.3 LDO Regulator (U3)**:
    *   *Input Voltage*: 5V
    *   *Output Voltage/Current*: 3.3V at 150mA average
    *   *Total Power Loss*: $P_{loss} = (5\text{V} - 3.3\text{V}) \times 0.15\text{A} = 0.255\text{ W}$ (255 mW)
4.  **AO3400A switching MOSFET (Q1)**:
    *   *Continuous Current*: 150mA (Delta Fan)
    *   *RDS(on)*: 33 mΩ
    *   *Total Power Loss*: $P_{loss} = I^2 \times R_{DS(on)} = (0.15\text{A})^2 \times 0.033\Omega = 0.00074\text{ W}$ (0.74 mW)

---

## 2. Junction Temperature and Thermal Rise
Assuming a maximum enclosure ambient temperature $T_A = 65^\circ\text{C}$ in summer operating conditions in India:

*   **LM5017 Converter Junction ($T_{J\_U1}$)**:
    *   SO PowerPAD-8 Thermal Resistance $R_{\theta JA} = 40^\circ\text{C/W}$ (with solid ground plane and thermal vias).
    *   $\Delta T_J = 0.84\text{W} \times 40^\circ\text{C/W} = 33.6^\circ\text{C}$ rise.
    *   $T_{J\_U1} = 65^\circ\text{C} + 33.6^\circ\text{C} = 98.6^\circ\text{C}$ (safe margin below junction limit $150^\circ\text{C}$).
*   **AP2112K LDO Junction ($T_{J\_U3}$)**:
    *   SOT-25 Thermal Resistance $R_{\theta JA} = 250^\circ\text{C/W}$.
    *   $\Delta T_J = 0.255\text{W} \times 250^\circ\text{C/W} = 63.75^\circ\text{C}$ rise.
    *   $T_{J\_U3} = 65^\circ\text{C} + 63.75^\circ\text{C} = 128.75^\circ\text{C}$ (very close to junction limit $150^\circ\text{C}$ under peak continuous Wi-Fi).
    *   *Thermal Mitigation*: Place wide copper pours on the LDO VCC and VOUT pins to act as heatsinks and reduce $R_{\theta JA}$ to $\sim 180^\circ\text{C/W}$, lowering the peak junction to $\sim 111^\circ\text{C}$.

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
