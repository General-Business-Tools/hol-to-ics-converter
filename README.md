# HOL Converter

Convert `.hol` calendar files to ICS (iCalendar), CSV, or JSON formats.

## Overview

This repository provides two ways to convert `.hol` files:
- **Web Application**: Browser-based converter with drag-and-drop interface
- **Python Script**: Command-line tool for batch processing

## What is a .hol file?

A `.hol` file is a simple text-based calendar format structured as:

```
[Category Name] event_count
Event Name, YYYY/MM/DD
Event Name, YYYY/MM/DD
...
```

Example:
```
[CA State Holidays 2026] 3
New Year's Day, 2026/01/01
Martin Luther King Jr Day, 2026/01/19
President's Day, 2026/02/16
```

## Web Application

### Features
- 🎨 Beautiful, modern interface
- 📤 Drag & drop file upload
- 🔄 Convert to ICS, CSV, or JSON
- 👁️ Preview categories and event counts
- 📱 Mobile-friendly
- 🔒 All processing happens in your browser (privacy-focused)

### Usage

1. Open `index.html` in any web browser, or
2. Deploy to a static hosting service:
   - GitHub Pages
   - Netlify
   - Vercel
   - AWS S3
   - Cloudflare Pages

3. Upload or drag & drop your `.hol` file
4. Select output format (ICS, CSV, or JSON)
5. Click "Download File"

### Output Formats

**ICS (iCalendar)**
- Standard calendar format
- Import into Google Calendar, Apple Calendar, Outlook, etc.
- All-day events with categories preserved

**CSV (Comma-Separated Values)**
- Spreadsheet-compatible format
- Columns: Category, Event Name, Date
- Open in Excel, Google Sheets, etc.

**JSON**
- Structured data format
- Perfect for developers and data processing
- Includes category hierarchy

## Python Script

### Requirements
- Python 3.6 or higher
- No external dependencies

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/hol-converter.git
cd hol-converter

# Make the script executable (optional)
chmod +x hol_to_ics.py
```

### Usage

```bash
python hol_to_ics.py input_file.hol
```

This will create `input_file.ics` in the same directory.

### Features
- Automatically detects file encoding (UTF-8, Latin-1, Windows-1252, ISO-8859-1)
- Handles special characters (e.g., é, ñ, ü)
- Validates dates and provides helpful error messages
- Preserves category information
- Creates RFC 5545-compliant iCalendar files

### Examples

```bash
# Convert a single file
python hol_to_ics.py holidays_2026.hol

# Process multiple files
for file in *.hol; do python hol_to_ics.py "$file"; done
```

## File Structure

```
hol-converter/
├── index.html          # Web application
├── hol_to_ics.py      # Python converter script
└── README.md          # This file
```

## Example Output

### ICS Format
```ics
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//HOL to ICS Converter//EN
BEGIN:VEVENT
UID:20260101-New-Years-Day@holconverter
DTSTART;VALUE=DATE:20260101
SUMMARY:New Year's Day
CATEGORIES:CA State Holidays 2026
END:VEVENT
END:VCALENDAR
```

### CSV Format
```csv
Category,Event Name,Date
"CA State Holidays 2026","New Year's Day","2026/01/01"
"CA State Holidays 2026","Martin Luther King Jr Day","2026/01/19"
```

### JSON Format
```json
{
  "categories": [
    {
      "name": "CA State Holidays 2026",
      "events": [
        {
          "name": "New Year's Day",
          "date": "2026/01/01"
        }
      ]
    }
  ]
}
```

## Browser Compatibility

The web application works in all modern browsers:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Ideas for future enhancements:
- Support for recurring events
- Time-based events (not just all-day)
- Batch conversion in web interface
- Additional output formats (XML, Excel)
- Event reminders/alarms

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions:
1. Check that your `.hol` file follows the correct format
2. Ensure dates are in YYYY/MM/DD format
3. Open an issue on GitHub with a sample of your file (remove sensitive data)

## Acknowledgments

Created to simplify calendar management and make `.hol` files more accessible across different platforms and applications.