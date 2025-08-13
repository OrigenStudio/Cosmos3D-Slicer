# Cosmos3D Postprocessor Script

This directory contains the Cosmos3D postprocessing script for concrete 3D printing applications.

## cosmos3d_postprocessor.py

A Python script specifically designed for postprocessing G-code files generated for Cosmos3D concrete printers. This script optimizes G-code for large-scale concrete construction applications.

### Features

- **Concrete-specific optimizations**: Adjusts flow rates and commands for concrete printing
- **Safety features**: Adds safety pauses at configurable height intervals
- **Layer progress tracking**: Displays layer progress on printer display
- **Validation**: Validates G-code for concrete printing safety
- **Comprehensive logging**: Provides detailed logging of all processing steps
- **Slicer integration**: Reads slicer configuration from environment variables

### Usage

#### From Command Line
```bash
python3 scripts/cosmos3d_postprocessor.py input.gcode [-o output.gcode] [options]
```

#### From Orca Slicer
Add the following to your printer's "Post-processing Scripts" field:
```
python3 /path/to/Cosmos3D-Slicer/scripts/cosmos3d_postprocessor.py
```

### Options

- `-o, --output`: Output file path (defaults to overwriting input file)
- `--flow-rate`: Concrete flow rate multiplier (default: 1.0)
- `--safety-pause-height`: Height interval for safety pauses in mm (default: 500.0)

### Environment Variables

The script automatically reads the following environment variables set by Orca Slicer:

- `SLIC3R_PP_HOST`: Target host (e.g., "File", "OctoPrint")
- `SLIC3R_PP_OUTPUT_NAME`: Final output file name
- `COSMOS3D_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

### Safety Features

- **Safety pauses**: Automatic pauses every 500mm (configurable) for inspection
- **Flow validation**: Checks for reasonable flow rates for concrete
- **Layer notifications**: Display layer progress for monitoring
- **Concrete-specific commands**: Optimized startup and end sequences

### Requirements

- Python 3.6 or later
- No additional dependencies required (uses only standard library)

### Integration with Cosmos3D Printers

This script is specifically designed for the Cosmos3D X1 concrete printer and integrates seamlessly with the Cosmos3D printer profiles in this slicer configuration.