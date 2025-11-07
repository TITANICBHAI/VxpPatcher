# VXP Patcher - Replit Project

## Overview
A server-side VXP patcher web application that patches MediaTek MRE VXP files with IMSI numbers for Nokia feature phones (5310, 225, etc.). Built to work without JavaScript for feature phone compatibility.

## Project Status
- **Created:** November 7, 2025
- **Stack:** Python Flask + HTML (no JavaScript)
- **Deployment Target:** Render (via Dockerfile)

## Recent Changes
- November 7, 2025: Initial project setup
  - Implemented VXP binary parsing and IMSI patching logic
  - Created Flask web server with file upload handling
  - Built feature-phone-compatible HTML interface
  - Added Dockerfile for Render deployment

## Project Architecture

### File Structure
```
/
├── app.py                 # Flask application with routes
├── vxp_patcher.py        # VXP binary parsing and IMSI patching logic
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration for Render
├── templates/
│   └── index.html        # HTML form (no JavaScript)
└── README.md             # Documentation
```

### Key Components
1. **VXP Patcher Logic** (`vxp_patcher.py`):
   - Parses ELF binary structure
   - Locates metadata tags section
   - Inserts/updates IMSI tag (TAG_IMSI = 0x01)
   - IMSI format: 15 digits, prefixed with '9' in tag

2. **Flask Application** (`app.py`):
   - GET /: Serves HTML form
   - POST /patch: Processes VXP upload and returns patched file
   - File size limit: 16MB
   - Server-side processing (no client-side JS)

3. **HTML Interface** (`templates/index.html`):
   - Pure HTML form (feature phone compatible)
   - IMSI input with validation pattern
   - File upload for .vxp files
   - Instructions for finding IMSI

### Dependencies
- Flask 3.0.0: Web framework
- gunicorn 21.2.0: Production WSGI server
- Werkzeug 3.0.1: WSGI utilities

## Deployment

### Render Deployment Steps
1. Push repository to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Render auto-detects Dockerfile
5. Deploy (automatic)

### Environment Variables
- `PORT`: Server port (default: 5000)
- `SESSION_SECRET`: Flask session secret (already configured in Replit)

## Technical Notes

### VXP File Format
- ELF 32-bit LSB executable (ARM architecture)
- Metadata tags appended after ELF sections
- Tag structure: [tag_id:1 byte][length:2 bytes][data:variable]
- IMSI tag ID: 0x01
- End tag ID: 0xFF

### IMSI Patching Process
1. Validate VXP is valid ELF file
2. Calculate metadata section offset from ELF headers
3. Parse existing tags to find/replace IMSI tag
4. Insert new IMSI tag (15 digits prefixed with '9', null-terminated)
5. Return modified binary data

### Security Considerations
- Files processed in memory (no disk storage)
- File size limit enforced (16MB)
- File extension validation (.vxp only)
- IMSI validation (must be 15 digits)

## User Preferences
None specified yet.
