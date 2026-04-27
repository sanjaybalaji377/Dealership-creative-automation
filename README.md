# Dealership Creative Automation Tool

A professional, web-based tool for automating the generation of dealership creatives by combining brands, panels, logos, and backgrounds with intelligent scaling and positioning.

## Features

- **Dynamic Account Mapping**: Brand-wise dealership filtering with multi-select support.
- **Admin Authentication**: Secure login system for administrative access.
- **Predefined Asset Gallery**: Quick selection from high-quality background templates.
- **Bulk Creative Generation**: Optimized parallel processing for rapid generation of multiple outputs.
- **Multi-Format Output**: Automatically scales and generates for:
  - Instagram Post (1:1 and 4:5)
  - Instagram Story (9:16)
- **ZIP Export**: Download all generated creatives in a single, well-organized bundle.

## Tech Stack

- **Frontend**: React (Vite) + Lucide Icons + Premium CSS (Glassmorphism & Micro-animations).
- **Backend**: Flask (Python 3.12) + Pillow for Image processing + SQLite for persistence.

## Intelligent Automation

1.  **Smart Scaling**: Uses focal centering (0.5, 0.4) to preserve key visual elements while filling the canvas.
2.  **Auto-Adaptive Positioning**: Shifts panels and logos based on the output format (Square vs. Story) for optimal layout.
3.  **Parallel Processing**: Implemented concurrent image processing for high-performance batch generation.

## Setup Instructions

### 1. Prerequisites
- **Python 3.12** is required (available via `winget install Python.Python.3.12` or python.org).

### 2. Backend Setup
```bash
cd backend
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run the server
python run.py
```
The backend will be available at `http://localhost:5000`.

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`.

## Testing

1.  **Login**: Use the credentials provided below.
2.  **Selection**: Choose a Brand (e.g., Tata) and select one or more dealerships.
3.  **Assets**: Upload a custom background or select from the **Predefined** gallery.
4.  **Generation**: Select your desired format(s) and click **Generate**.
5.  **Review**: Download the ZIP bundle and verify the creatives meet brand standards.

## Default Credentials

- **Email**: `admin@dealercreative.com`
- **Password**: `Admin@123`

---
*Built for scale and professional dealership creative production.*
