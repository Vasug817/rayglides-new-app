# RayGlides 3W/4W EV Kit Cooling Controller — ESP32 GPIO Mapping

This document provides a reference mapping of the ESP32-S3-N16R8 pins to the hardware interfaces, verified against `/Users/vasugupta/Downloads/RayGlides_EMS_firmware_PWM_AWS/RayGlides_EMS/include/config.h`.

---

## 1. GPIO Pin Allocations

| ESP32-S3 Pin | Function / Net | Signal Type | Active Level / Details |
| :--- | :--- | :--- | :--- |
| **GPIO 1** | BATTERY_VOLTAGE_PIN | Analog Input | ADC1_CH0 — Pack voltage sensing (Divider ratio 21.0) |
| **GPIO 2** | BATTERY_CURRENT_PIN | Analog Input | ADC1_CH1 — Current sensor midpoint 1.65V (midpoint) |
| **GPIO 4** | BATTERY_TEMP_PIN | Analog Input | ADC1_CH3 — Connected to LM35 output (LM35 Vout $\times$ 100) |
| **GPIO 5** | SOLAR_VOLTAGE_PIN | Analog Input | ADC1_CH4 — Solar voltage input (Divider ratio 8.0) |
| **GPIO 6** | SOLAR_CURRENT_PIN | Analog Input | ADC1_CH5 — Solar current input |
| **GPIO 7** | GRID_BUTTON_PIN | Digital Input | Pulled high, button connects to GND |
| **GPIO 8** | MPPT_PWM_PIN | PWM Output | LEDC Channel 0, 5 kHz frequency, 8-bit resolution |
| **GPIO 9** | CAN_TX_PIN | CAN TX | Connected to CAN Transceiver TXD |
| **GPIO 10** | CAN_RX_PIN | CAN RX | Connected to CAN Transceiver RXD |
| **GPIO 11** | RS485_TX_PIN | UART TX | Connected to UART2 TX |
| **GPIO 12** | RS485_RX_PIN | UART RX | Connected to UART2 RX |
| **GPIO 13** | RS485_DE_PIN | Digital Output | RS485 Transceiver direction pin (DE/RE) |
| **GPIO 14** | RELAY_PIN | Digital Output | Active High — Powers external charging relay |
| **GPIO 15** | CHARGE_LED_PIN | Digital Output | Active High — Charging status indicator |
| **GPIO 16** | FAULT_LED_PIN | Digital Output | Active High — Fault status indicator |
| **GPIO 18** | FAN_PWM_PIN | PWM Output | LEDC Channel 1, 5 kHz frequency, 8-bit resolution |

---

## 2. Strapping Pin Audit (Safety Check)
*   **GPIO 0, 3, 45, 46** are hardware strapping pins on the ESP32-S3. They are bypassed or skipped in this layout:
    *   `GPIO 3` (JTAG strapping pin) is skipped. `BATTERY_TEMP_PIN` was assigned to `GPIO 4` instead.
    *   `GPIO 0`, `GPIO 45`, `GPIO 46` are unused in our configuration, ensuring clean boot-loading.
*   **Octal PSRAM Constraints**: The ESP32-S3-N16R8 module uses Octal SPI PSRAM. All pins from `GPIO 26` through `GPIO 37` are reserved internally and must **never** be broken out or connected to external circuits. Our pinout strictly limits connections to the safe range `GPIO 1-18`, preventing memory collision crashes.
