# ELECTRICAL & SIGNAL LOGIC SPECIFICATION: UNIVAC IX HEX MATRIX

## 1. 16-State Voltage Interval Mapping
The computing core bypasses traditional binary logic constraints by utilizing a native 16-state analog voltage array operating over a precise 0.0V to 1.0V window.

Each hexadecimal symbol state maps to a specific physical voltage interval of exactly **0.0625V**:

| Hex State | Target Voltage | Lower Bound | Upper Bound |
| :---: | :---: | :---: | :---: |
| **0** | 0.0000V | 0.0000V | 0.0312V |
| **1** | 0.0625V | 0.0313V | 0.0937V |
| **2** | 0.1250V | 0.0938V | 0.1562V |
| **3** | 0.1875V | 0.1563V | 0.2187V |
| **4** | 0.2500V | 0.2188V | 0.2812V |
| **5** | 0.3125V | 0.2813V | 0.3437V |
| **6** | 0.3750V | 0.3438V | 0.4062V |
| **7** | 0.4375V | 0.4063V | 0.4687V |
| **8** | 0.5000V | 0.4688V | 0.5312V |
| **9** | 0.5625V | 0.5313V | 0.5937V |
| **A** | 0.6250V | 0.5938V | 0.6562V |
| **B** | 0.6875V | 0.6563V | 0.7187V |
| **C** | 0.7500V | 0.7188V | 0.7812V |
| **D** | 0.8125V | 0.7813V | 0.8437V |
| **E** | 0.8750V | 0.8438V | 0.9062V |
| **F** | 1.0000V | 0.9063V | 1.0000V |

## 2. Printed Circuit Board (PCB) Copper Requirements
To handle high-draw, multi-state voltage telemetry streams without causing signal decay or thermal bleeding:
- **Trace Thickness:** All multi-state parallel signal channels must use **2oz or 3oz thick copper traces**.
- **Trace Geometry:** High-frequency trace pathways are layout-restricted to **45-degree angles exclusively** to minimize signal loss and eliminate impedance reflections.
- **Cross-talk Mitigation:** Isolation barriers via dedicated hardware ground rings must wrap completely around the analog logic arrays.
