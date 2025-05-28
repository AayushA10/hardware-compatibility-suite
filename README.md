# Hardware Compatibility Test Suite

A Python-based GUI application for detecting, testing, and reporting system hardware compatibility. The tool is designed to assist in identifying the specifications of CPUs, GPUs, and Network Cards, performing simulated functional tests, and exporting comprehensive reports in multiple formats.

## Features

- Hardware detection (CPU, GPU, Network Cards)
- Basic functionality testing with power usage simulation
- System stats display (CPU, RAM, Disk, Uptime)
- Progress bar to track test execution
- Theme toggle (Light/Dark mode)
- Export results in TXT, JSON, and PDF formats
- Auto-email of PDF report

## Tech Stack

- Python 3
- Tkinter for GUI
- psutil for system monitoring
- FPDF for PDF generation
- subprocess and regex for hardware detection

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/AayushA10/hardware-compatibility-suite.git
   cd hardware-compatibility-suite
