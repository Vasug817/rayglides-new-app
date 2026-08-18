# RayGlides 3W/4W EV Kit Cooling Controller — Requirements and Assumptions

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
