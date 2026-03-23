# Cosmos3D Embedded Post-Processing

This feature adds embedded C++ post-processing specifically for Cosmos3D printers.

## Overview

The Cosmos3D post-processing script is embedded directly in the source code and automatically runs for any printer with "Cosmos" in its `printer_model` configuration. This provides printer-specific optimizations without requiring external script files.

## Features

### Automatic Detection
- Detects Cosmos3D printers by checking if `printer_model` contains "Cosmos"
- Runs automatically during the post-processing phase
- Does not interfere with regular post-processing scripts

### G-Code Optimizations
The embedded script adds the following Cosmos3D-specific optimizations:

1. **Printer Identification Comments**
   ```gcode
   ; Post-processed for Cosmos3D printer
   ; Cosmos3D optimizations applied
   ```

2. **Print Section Markers**
   ```gcode
   ; === Cosmos3D Print Section Start ===
   M117 Cosmos3D Printing...
   ```

3. **Temperature Optimization Comments**
   - Adds comments before M104/M109 commands
   ```gcode
   ; Cosmos3D temperature optimization
   M104 S210
   ```

4. **Fan Control Optimization**
   - Adds comments before M106 commands
   ```gcode
   ; Cosmos3D fan control optimization
   M106 S255
   ```

5. **Layer Change Notifications**
   ```gcode
   ;LAYER_CHANGE
   M117 Layer changing...
   ```

6. **Print Completion Message**
   ```gcode
   ; === Cosmos3D Print Section End ===
   M117 Cosmos3D Print Complete!
   ```

## Integration with Existing System

### Execution Order
1. Regular environment setup
2. **Cosmos3D embedded processing** (if applicable)
3. Regular post-processing scripts (if defined)
4. Output file handling

### Compatibility
- Works alongside existing post-processing scripts
- Does not break existing functionality
- Gracefully handles failures (logs warning and continues)

## Implementation Details

### Files Modified
- `src/libslic3r/GCode/PostProcessor.hpp` - Added function declaration
- `src/libslic3r/GCode/PostProcessor.cpp` - Added implementation and integration

### Key Functions
- `run_cosmos_post_processing()` - Main embedded processing function
- Modified `run_post_process_scripts()` - Integrated cosmos processing

### Printer Configuration
Example printer configuration in `resources/profiles/Cosmos3D/machine/Cosmos3D.json`:
```json
{
  "printer_model": "Cosmos3D v1",
  "printer_variant": "0.4",
  ...
}
```

## Testing

The implementation includes comprehensive tests verifying:
- Cosmos3D printers are correctly detected and processed
- Non-Cosmos3D printers are skipped
- Regular post-processing scripts continue to work
- Both embedded and script processing can run together
- No processing occurs when no scripts are defined for non-Cosmos printers

## Usage

1. Configure a printer with "Cosmos" in the `printer_model` name
2. The embedded post-processing will automatically run during G-code generation
3. Optional: Add additional post-processing scripts as usual
4. Generated G-code will include Cosmos3D-specific optimizations

No additional configuration or external files are required.