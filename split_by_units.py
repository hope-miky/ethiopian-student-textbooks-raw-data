#!/usr/bin/env python3
"""
Script to split rawText.txt by chapters/units
"""

import re

def split_text_by_units(input_file, output_dir='units'):
    """Split the text file by units/chapters"""
    
    # Read the entire file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find all unit headers with line numbers
    unit_starts = []
    for i, line in enumerate(lines, start=1):
        # Match "Unit X: " at the start of line (case insensitive)
        match = re.match(r'^Unit\s+(\d+):\s*(.+)$', line, re.IGNORECASE)
        if match:
            unit_num = int(match.group(1))
            unit_title = match.group(2).strip()
            unit_starts.append((i, unit_num, unit_title))
    
    # Filter to get only the main unit headers (first occurrence of each unit after TOC)
    # The TOC appears before line 221, so we'll use the first occurrence of each unit after that
    main_units = {}
    for line_num, unit_num, unit_title in unit_starts:
        # Skip TOC entries (they appear before actual content)
        if line_num < 221:
            continue
        # Keep the first occurrence of each unit number
        if unit_num not in main_units:
            main_units[unit_num] = (line_num, unit_title)
    
    # Sort by unit number
    sorted_units = sorted(main_units.items())
    
    # Create output directory
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Split and save each unit
    for idx, (unit_num, (start_line, unit_title)) in enumerate(sorted_units):
        # Determine end line (next unit start or end of file)
        if idx + 1 < len(sorted_units):
            end_line = sorted_units[idx + 1][1][0]
        else:
            end_line = len(lines) + 1
        
        # Extract unit content (1-based to 0-based indexing)
        unit_content = ''.join(lines[start_line - 1:end_line - 1])
        
        # Clean filename from unit title
        safe_title = re.sub(r'[^\w\s-]', '', unit_title).strip()
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        filename = f"Unit_{unit_num:02d}_{safe_title}.txt"
        filepath = os.path.join(output_dir, filename)
        
        # Write unit to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(unit_content)
        
        print(f"Created: {filepath} (lines {start_line}-{end_line-1}, {end_line-start_line} lines)")
    
    print(f"\n✓ Split into {len(sorted_units)} unit files in '{output_dir}' directory")

if __name__ == '__main__':
    input_file = 'rawText.txt'
    split_text_by_units(input_file)
