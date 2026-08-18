# RayGlides 3W/4W EV Kit Cooling Controller — PCB Project & Design Files

This folder contains the CAD design specifications, PCB project netlists, and Gerber layer exports.

---

## 1. PCB Project Specifications (KiCad-based format)
*   **Project File**: `RayGlides_Cooling_Controller.kicad_pro`
*   **Schematic File**: `RayGlides_Cooling_Controller.kicad_sch`
*   **PCB Layout File**: `RayGlides_Cooling_Controller.kicad_pcb`

---

## 2. Gerber Export Configurations
The following standard RS-274X Gerber extensions are used for exporting to PCB manufacturers:

| Gerber File | Layer Type | Description |
| :--- | :--- | :--- |
| **`RayGlides_Cooling_Controller.GTL`** | Top Copper | Copper routing, ground pours, and component pads on Layer 1 |
| **`RayGlides_Cooling_Controller.GBL`** | Bottom Copper | Power ground return plane and power trace routing on Layer 2 |
| **`RayGlides_Cooling_Controller.GTS`** | Top Solder Mask | Solder mask openings for components soldering |
| **`RayGlides_Cooling_Controller.GBS`** | Bottom Solder Mask | Solder mask coverage for bottom routing |
| **`RayGlides_Cooling_Controller.GTO`** | Top Silkscreen | Silk markings, reference designators, and board labels |
| **`RayGlides_Cooling_Controller.GBO`** | Bottom Silkscreen | Optional bottom manufacturer branding and RoHS labels |
| **`RayGlides_Cooling_Controller.GKO`** | Keep-Out / Outline | Board boundary profile (80mm x 55mm) |
| **`RayGlides_Cooling_Controller.DRL`** | Drill File | NC Drill files for plated-through holes and thermal vias |
