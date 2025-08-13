#!/usr/bin/env python3
"""
Cosmos3D Postprocessor Script for Concrete 3D Printing

This script performs postprocessing of G-code files generated for Cosmos3D concrete printers.
It optimizes the G-code for concrete printing applications and adds safety features
specific to large-scale concrete construction.

Usage:
    python3 cosmos3d_postprocessor.py <gcode_file>

The script receives the G-code file path as the first argument and can access
Orca Slicer configuration settings through environment variables:
    - SLIC3R_PP_HOST: Target host (e.g., "File", "OctoPrint")
    - SLIC3R_PP_OUTPUT_NAME: Final output file name

Author: Cosmos3D Slicer Team
License: Same as Orca Slicer
"""

import sys
import os
import argparse
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class Cosmos3DPostProcessor:
    """Postprocessor for Cosmos3D concrete printers."""
    
    def __init__(self):
        self.setup_logging()
        self.gcode_lines: List[str] = []
        self.metadata: Dict[str, str] = {}
        self.concrete_flow_rate = 1.0
        self.safety_pause_height = 500.0  # mm - height at which to add safety pauses
        self.layer_count = 0
        
    def setup_logging(self):
        """Configure logging for the postprocessor."""
        log_level = os.environ.get('COSMOS3D_LOG_LEVEL', 'INFO').upper()
        logging.basicConfig(
            level=getattr(logging, log_level, logging.INFO),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('Cosmos3DPostProcessor')
        
    def load_gcode(self, filepath: str) -> bool:
        """Load G-code file into memory."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.gcode_lines = f.readlines()
            self.logger.info(f"Loaded G-code file: {filepath} ({len(self.gcode_lines)} lines)")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load G-code file {filepath}: {e}")
            return False
    
    def save_gcode(self, filepath: str) -> bool:
        """Save processed G-code to file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(self.gcode_lines)
            self.logger.info(f"Saved processed G-code to: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save G-code file {filepath}: {e}")
            return False
    
    def extract_metadata(self):
        """Extract metadata from G-code comments."""
        for line in self.gcode_lines[:100]:  # Check first 100 lines for metadata
            line = line.strip()
            if line.startswith(';'):
                # Parse common metadata patterns
                if '=' in line:
                    parts = line[1:].split('=', 1)
                    if len(parts) == 2:
                        key, value = parts[0].strip(), parts[1].strip()
                        self.metadata[key] = value
                        
                # Extract layer height for concrete flow calculations
                if 'layer_height' in line.lower():
                    match = re.search(r'(\d+\.?\d*)', line)
                    if match:
                        self.metadata['layer_height'] = match.group(1)
                        
                # Extract nozzle diameter
                if 'nozzle_diameter' in line.lower():
                    match = re.search(r'(\d+\.?\d*)', line)
                    if match:
                        self.metadata['nozzle_diameter'] = match.group(1)
        
        self.logger.info(f"Extracted metadata: {self.metadata}")
    
    def add_cosmos3d_header(self):
        """Add Cosmos3D-specific header information."""
        header_lines = [
            "; Cosmos3D Concrete Printer G-code\n",
            f"; Processed by Cosmos3D Postprocessor on {datetime.now().isoformat()}\n",
            f"; Host: {os.environ.get('SLIC3R_PP_HOST', 'Unknown')}\n",
            f"; Output: {os.environ.get('SLIC3R_PP_OUTPUT_NAME', 'Unknown')}\n",
            ";\n",
            "; === CONCRETE PRINTING SAFETY NOTICE ===\n",
            "; This G-code is optimized for concrete 3D printing\n",
            "; Ensure proper material flow and safety protocols\n",
            "; Monitor print progress continuously\n",
            ";\n"
        ]
        
        # Insert header after any existing header comments but before actual G-code
        insert_index = 0
        for i, line in enumerate(self.gcode_lines):
            if line.strip().startswith(';'):
                insert_index = i + 1
            else:
                break
        
        for i, header_line in enumerate(header_lines):
            self.gcode_lines.insert(insert_index + i, header_line)
        
        self.logger.info("Added Cosmos3D header information")
    
    def add_safety_pauses(self):
        """Add safety pauses at specific heights for concrete printing."""
        modified_lines = []
        current_z = 0.0
        last_pause_z = 0.0
        
        for line in self.gcode_lines:
            stripped_line = line.strip()
            
            # Track Z position
            if stripped_line.startswith('G1') and 'Z' in stripped_line:
                z_match = re.search(r'Z(\d+\.?\d*)', stripped_line)
                if z_match:
                    current_z = float(z_match.group(1))
            
            # Add safety pause every safety_pause_height mm
            if (current_z - last_pause_z) >= self.safety_pause_height and current_z > 0:
                pause_comment = f"; Safety pause at height {current_z:.1f}mm\n"
                pause_command = "M226 ; Wait for user confirmation\n"
                modified_lines.extend([pause_comment, pause_command])
                last_pause_z = current_z
                self.logger.info(f"Added safety pause at height {current_z:.1f}mm")
            
            modified_lines.append(line)
        
        self.gcode_lines = modified_lines
    
    def optimize_concrete_flow(self):
        """Optimize extrusion flow for concrete printing."""
        modified_lines = []
        
        for line in self.gcode_lines:
            stripped_line = line.strip()
            
            # Modify flow rate for concrete
            if stripped_line.startswith('G1') and 'E' in stripped_line:
                e_match = re.search(r'E(\d+\.?\d*)', stripped_line)
                if e_match:
                    original_e = float(e_match.group(1))
                    optimized_e = original_e * self.concrete_flow_rate
                    modified_line = re.sub(r'E\d+\.?\d*', f'E{optimized_e:.4f}', line)
                    modified_lines.append(modified_line)
                    continue
            
            modified_lines.append(line)
        
        self.gcode_lines = modified_lines
        self.logger.info(f"Applied concrete flow optimization (factor: {self.concrete_flow_rate})")
    
    def add_layer_notifications(self):
        """Add notifications at the start of each layer."""
        modified_lines = []
        layer_number = 0
        
        for line in self.gcode_lines:
            stripped_line = line.strip()
            
            # Detect layer changes
            if stripped_line.startswith(';LAYER:') or stripped_line.startswith('; layer '):
                layer_number += 1
                notification = f"M117 Printing Layer {layer_number} ; Display layer progress\n"
                modified_lines.append(line)
                modified_lines.append(notification)
                continue
            
            modified_lines.append(line)
        
        self.gcode_lines = modified_lines
        self.layer_count = layer_number
        self.logger.info(f"Added layer notifications for {layer_number} layers")
    
    def add_concrete_specific_commands(self):
        """Add concrete-specific G-code commands."""
        # Add startup sequence for concrete printing
        startup_commands = [
            "; Concrete printing startup sequence\n",
            "M82 ; Set extruder to absolute mode\n",
            "G28 ; Home all axes\n",
            "M109 S0 ; Set extruder temperature (concrete doesn't need heating)\n",
            "M190 S0 ; Set bed temperature (concrete doesn't need heating)\n",
            "G92 E0 ; Reset extruder position\n",
            "M117 Starting concrete print ; Display message\n",
            ";\n"
        ]
        
        # Find position after header comments to insert startup commands
        insert_index = 0
        for i, line in enumerate(self.gcode_lines):
            if not line.strip().startswith(';') and line.strip():
                insert_index = i
                break
        
        for i, cmd in enumerate(startup_commands):
            self.gcode_lines.insert(insert_index + i, cmd)
        
        # Add end sequence
        end_commands = [
            ";\n",
            "; Concrete printing end sequence\n",
            "M104 S0 ; Turn off extruder\n",
            "M140 S0 ; Turn off bed\n",
            "G91 ; Relative positioning\n",
            "G1 Z10 F300 ; Move nozzle up 10mm\n",
            "G90 ; Absolute positioning\n",
            "G28 X Y ; Home X and Y axes\n",
            "M84 ; Disable motors\n",
            "M117 Concrete print complete ; Display completion message\n"
        ]
        
        self.gcode_lines.extend(end_commands)
        self.logger.info("Added concrete-specific startup and end sequences")
    
    def validate_gcode(self) -> bool:
        """Validate the processed G-code for concrete printing safety."""
        errors = []
        warnings = []
        
        # Check for reasonable feed rates
        for i, line in enumerate(self.gcode_lines):
            if 'F' in line and re.search(r'F(\d+)', line):
                feed_match = re.search(r'F(\d+)', line)
                if feed_match:
                    feed_rate = int(feed_match.group(1))
                    if feed_rate > 3000:  # Very high feed rate for concrete
                        warnings.append(f"Line {i+1}: High feed rate {feed_rate} may be too fast for concrete")
                    elif feed_rate < 5:  # Very low feed rate
                        warnings.append(f"Line {i+1}: Low feed rate {feed_rate} may cause flow issues")
        
        # Log validation results
        if errors:
            for error in errors:
                self.logger.error(error)
            return False
        
        if warnings:
            for warning in warnings:
                self.logger.warning(warning)
        
        self.logger.info("G-code validation completed successfully")
        return True
    
    def process(self, input_file: str, output_file: Optional[str] = None) -> bool:
        """Main processing function."""
        if output_file is None:
            output_file = input_file
        
        self.logger.info(f"Starting Cosmos3D postprocessing: {input_file}")
        
        # Load G-code
        if not self.load_gcode(input_file):
            return False
        
        # Extract metadata for optimization parameters
        self.extract_metadata()
        
        # Apply all processing steps
        self.add_cosmos3d_header()
        self.add_concrete_specific_commands()
        self.optimize_concrete_flow()
        self.add_safety_pauses()
        self.add_layer_notifications()
        
        # Validate processed G-code
        if not self.validate_gcode():
            self.logger.error("G-code validation failed")
            return False
        
        # Save processed G-code
        if not self.save_gcode(output_file):
            return False
        
        self.logger.info(f"Cosmos3D postprocessing completed successfully")
        self.logger.info(f"Processed {len(self.gcode_lines)} lines, {self.layer_count} layers")
        
        return True


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Cosmos3D Postprocessor for Concrete 3D Printing"
    )
    parser.add_argument(
        'gcode_file',
        help='Path to the G-code file to process'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (defaults to overwriting input file)'
    )
    parser.add_argument(
        '--flow-rate',
        type=float,
        default=1.0,
        help='Concrete flow rate multiplier (default: 1.0)'
    )
    parser.add_argument(
        '--safety-pause-height',
        type=float,
        default=500.0,
        help='Height interval for safety pauses in mm (default: 500.0)'
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not os.path.exists(args.gcode_file):
        print(f"Error: G-code file not found: {args.gcode_file}")
        return 1
    
    # Create postprocessor instance
    processor = Cosmos3DPostProcessor()
    processor.concrete_flow_rate = args.flow_rate
    processor.safety_pause_height = args.safety_pause_height
    
    # Process the file
    output_file = args.output if args.output else args.gcode_file
    success = processor.process(args.gcode_file, output_file)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())