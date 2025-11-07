# VXP Patcher

A web-based tool to patch VXP files with IMSI numbers for MediaTek MRE phones (Nokia 5310, 225, 220, etc.).

## Features

- Simple HTML interface (works on feature phones without JavaScript)
- Server-side VXP file processing
- Patches IMSI tags into VXP application files
- Instant download of patched files
- Docker support for easy deployment

## What is VXP?

VXP files are executable applications for MediaTek's MRE (MAUI Runtime Environment) platform, used on Nokia S30+ feature phones. These phones require apps to be signed with your SIM card's IMSI number to run.

## How to Use

1. Find your IMSI number:
   - On Android: Settings → About phone → Status → IMSI
   - Or use ADB: `adb shell service call iphonesubinfo 1`

2. Visit the website and enter your 15-digit IMSI

3. Upload your .vxp file

4. Click "Patch!" and download the patched file

5. Copy the patched VXP to your phone's SD card and install it

## Local Development

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`

## Docker Deployment

### Build and Run

```bash
docker build -t vxp-patcher .
docker run -p 5000:5000 vxp-patcher
```

### Deploy on Render

**Option 1: Using render.yaml (Recommended - One-Click Deploy)**
1. Push this repository to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect `render.yaml` and configure everything
6. Click "Apply" to deploy

**Option 2: Manual Setup**
1. Push this repository to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Render will automatically detect the Dockerfile
6. Click "Create Web Service"

Render will build and deploy your application automatically!

## Configuration

### Timeouts
- Request timeout: 300 seconds (5 minutes) - handles slow uploads/downloads
- File size limit: 16MB maximum
- Keep-alive: 5 seconds for persistent connections

### Environment Variables

- `PORT` - Server port (default: 5000)
- `SESSION_SECRET` - Flask session secret (auto-generated on Render)

## Supported Phones

- Nokia 215, 220, 225, 230
- Nokia 5310 (2020)
- Nokia 106, 108
- Other MediaTek MRE-based feature phones

## Technical Details

VXP files are ELF 32-bit ARM executables with metadata tags. This tool:
- Parses the ELF structure
- Locates or creates IMSI metadata tag
- Embeds your IMSI (prefixed with '9' as per MRE spec)
- Generates patched file for download

## License

MIT License - Free to use and modify
