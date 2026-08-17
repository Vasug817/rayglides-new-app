# RayGlides 3W/4W EV Kit Cooling Controller — SPICE Simulation Configurations

This folder contains the LTspice netlist configurations, macromodels, and transient control parameters.

---

## 1. LTspice Simulation Netlist (.asc Structure)
*   **Simulation File**: `RayGlides_Cooling_Simulation.asc`
*   **Configuration**:
    *   **Power Input Stage**: Independent voltage source `V1` sweeping from 36V to 72V DC.
    *   **Transient Command**: `.tran 0 5m 0 1u` (Simulates startup transient from 0 to 5 milliseconds with a 1 microsecond resolution step).
    *   **PWM Pulse Source (ESP32 Gate Drive)**: Pulse source `V_PWM` (0V to 3.3V, rise time 10ns, fall time 10ns, period 200us equivalent to 5 kHz, pulse width 100us for 50% duty cycle).

---

## 2. Integrated SPICE Models
The following raw SPICE macromodel directives are embedded within the project files:

```spice
* SPICE Model for AO3400A N-Channel MOSFET
.SUBCKT AO3400A 1 2 3
* Drain=1 Gate=2 Source=3
M1 10 2 3 3 NMOS W=1 L=1
R1 1 10 0.015
CGS 2 3 650p
CGD 1 2 50p
.MODEL NMOS PMOS (VTO=1.05 KP=35 Lambda=0.02)
.ENDS

* SPICE Simulation command for transient evaluation
.tran 0 10m 0 10u
```
