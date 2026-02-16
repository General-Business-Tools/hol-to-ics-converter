#!/usr/bin/env python3
"""
Convert .hol files to .ics (iCalendar) format
"""

import re
import sys
from datetime import datetime
from pathlib import Path


def parse_hol_file(filepath):
    """Parse a .hol file and return structured data."""
    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    content = None
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue
    
    if content is None:
        raise ValueError("Could not decode file with any common encoding")
    
    
    categories = []
    lines = content.strip().split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for category header: [Category Name] count
        match = re.match(r'\[(.*?)\]\s+(\d+)', line)
        if match:
            category_name = match.group(1)
            event_count = int(match.group(2))
            events = []
            
            # Read the specified number of events
            for j in range(1, event_count + 1):
                if i + j < len(lines):
                    event_line = lines[i + j].strip()
                    if event_line:
                        # Parse: Event Name, YYYY/MM/DD
                        parts = event_line.rsplit(',', 1)
                        if len(parts) == 2:
                            name = parts[0].strip()
                            date_str = parts[1].strip()
                            events.append({'name': name, 'date': date_str})
            
            categories.append({
                'name': category_name,
                'events': events
            })
            
            i += event_count + 1
        else:
            i += 1
    
    return categories


def create_ics(categories, output_filepath):
    """Create an .ics file from parsed categories."""
    ics_lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//HOL to ICS Converter//EN',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH'
    ]
    
    for category in categories:
        for event in category['events']:
            try:
                # Parse date (format: YYYY/MM/DD)
                date_obj = datetime.strptime(event['date'], '%Y/%m/%d')
                date_str = date_obj.strftime('%Y%m%d')
                
                # Create unique ID
                uid = f"{date_str}-{event['name'].replace(' ', '-')}@holconverter"
                
                # Create timestamp
                now = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
                
                ics_lines.extend([
                    'BEGIN:VEVENT',
                    f'UID:{uid}',
                    f'DTSTAMP:{now}',
                    f'DTSTART;VALUE=DATE:{date_str}',
                    f'SUMMARY:{event["name"]}',
                    f'CATEGORIES:{category["name"]}',
                    'TRANSP:TRANSPARENT',
                    'STATUS:CONFIRMED',
                    'END:VEVENT'
                ])
            except ValueError as e:
                print(f"Warning: Skipping event '{event['name']}' - invalid date format: {e}", file=sys.stderr)
    
    ics_lines.append('END:VCALENDAR')
    
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write('\r\n'.join(ics_lines))


def main():
    if len(sys.argv) != 2:
        print("Usage: python hol_to_ics.py <input.hol>")
        print("Output will be saved as <input.ics>")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    if not input_file.exists():
        print(f"Error: File '{input_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    if not input_file.suffix.lower() == '.hol':
        print("Warning: Input file doesn't have .hol extension", file=sys.stderr)
    
    # Generate output filename
    output_file = input_file.with_suffix('.ics')
    
    try:
        print(f"Reading {input_file}...")
        categories = parse_hol_file(input_file)
        
        total_events = sum(len(cat['events']) for cat in categories)
        print(f"Found {len(categories)} categories with {total_events} total events")
        
        print(f"Creating {output_file}...")
        create_ics(categories, output_file)
        
        print(f"✓ Successfully converted to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
