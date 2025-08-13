# Cosmos3D Printer Postprocessing Setup Guide

This guide helps you set up and use the Cosmos3D postprocessing script for optimal concrete 3D printing.

## Quick Setup

### 1. Ensure Python 3 is Available
The postprocessor requires Python 3.6 or later. You can check your Python version with:
```bash
python3 --version
```

### 2. Configure the Postprocessor in Orca Slicer

1. **Open Orca Slicer** and select your Cosmos3D X1 printer
2. **Go to Process Settings** → Open the "Concrete Printing @Cosmos3D X1 60 nozzle" profile
3. **Navigate to Output Settings** → Find "Post-processing Scripts" 
4. **Add the script path**: 
   ```
   python3 scripts/cosmos3d_postprocessor.py
   ```
   
   Or if you installed the slicer in a different location:
   ```
   python3 /full/path/to/Cosmos3D-Slicer/scripts/cosmos3d_postprocessor.py
   ```

### 3. Optional: Customize Settings

You can add parameters to customize the postprocessor behavior:

- **Custom flow rate**: `python3 scripts/cosmos3d_postprocessor.py --flow-rate 1.1`
- **Custom safety pause height**: `python3 scripts/cosmos3d_postprocessor.py --safety-pause-height 300`
- **Combined options**: `python3 scripts/cosmos3d_postprocessor.py --flow-rate 0.95 --safety-pause-height 600`

## What the Postprocessor Does

### Safety Features
- **Automatic pauses**: Adds safety pauses every 500mm (configurable) for inspection
- **Progress notifications**: Shows current layer on printer display
- **Flow validation**: Checks for reasonable extrusion rates

### Concrete Optimizations
- **Startup sequence**: Optimized homing and preparation for concrete printing
- **Flow adjustment**: Fine-tunes extrusion for concrete material properties  
- **End sequence**: Safe shutdown with proper material handling

### Output Enhancements
- **Detailed header**: Adds printing metadata and safety notices
- **Comprehensive logging**: Logs all processing steps for troubleshooting

## Testing the Setup

### Validate Installation
Run the test script to ensure everything is working:
```bash
cd /path/to/Cosmos3D-Slicer
python3 scripts/test_cosmos3d_postprocessor.py
```

### Manual Test
You can manually test the postprocessor on any G-code file:
```bash
python3 scripts/cosmos3d_postprocessor.py your_file.gcode
```

## Safety Guidelines for Concrete Printing

### Before Starting
- ✅ Verify concrete mix consistency
- ✅ Check nozzle diameter and flow rate settings
- ✅ Ensure adequate material supply
- ✅ Verify print bed preparation

### During Printing
- 👁️ Monitor print progress continuously
- ⏸️ Use safety pauses for inspection
- 🔧 Check layer adhesion and flow quality
- 📱 Watch for layer notifications on display

### Troubleshooting

**Q: Script not found error**
A: Ensure you're using the full path to the script or run from the slicer directory

**Q: Permission denied**
A: Make sure the script is executable: `chmod +x scripts/cosmos3d_postprocessor.py`

**Q: Python not found**
A: Install Python 3 or use the full path: `/usr/bin/python3`

**Q: No safety pauses appearing**
A: Check that your print height exceeds the safety pause interval (default 500mm)

## Advanced Configuration

### Environment Variables
The script reads these environment variables automatically set by Orca Slicer:
- `SLIC3R_PP_HOST`: Target destination (File, OctoPrint, etc.)
- `SLIC3R_PP_OUTPUT_NAME`: Final output filename
- `COSMOS3D_LOG_LEVEL`: Set to DEBUG for detailed logging

### Customization
For advanced users, the script can be modified to:
- Add custom G-code commands
- Implement different safety pause strategies  
- Adjust concrete-specific parameters
- Add material-specific optimizations

## Support

For issues or questions:
1. Check the logs in the script output
2. Run the test script to validate installation
3. Ensure your G-code file is valid
4. Check Python and script permissions

The postprocessor is designed specifically for Cosmos3D concrete printing applications and integrates seamlessly with the Cosmos3D printer profiles in this slicer.