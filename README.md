# HDR Co⁶⁰ Brachytherapy Applicator Displacement Analysis Tool

## 📖 Overview
Python-based software for quantifying inter-fractional applicator displacement 
in cervical cancer HDR brachytherapy using orthogonal radiographs.

## 🎯 Features
- 3D displacement vector calculation from AP/lateral radiographs
- Integrated BED/EQD₂ radiobiological dose calculator
- Clinical report generation with statistical summaries
- DICOM image support with auto-enhancement
- User-friendly GUI (Tkinter-based)

## 📚 Associated Thesis
**Development of an Image-Based Tool for Detecting Inter-Fractional Applicator Variations and Their Dosimetric Impact in HDR Co⁶⁰ Brachytherapy for Cervical Cancer**

Author: W. V. A. S. Lochana (AHS/19/RAD/019)  
University: University of Peradeniya, Sri Lanka  
Year: 2025  
Supervisors: Dr. Buddhinie Karunarathne, Ms. L. P. G. Sherminie

🚀 Deployment & Installation Tools
This project includes two specialized deployment scripts:

1. deploy.py – Multi-Platform Deployment Script
Purpose: Creates distributable packages of the application for different deployment scenarios.

What it does:

✅ Checks for Python installation

✅ Installs required dependencies (Pillow, OpenCV, NumPy, tkcalendar, matplotlib, pydicom)

✅ Option 1: Creates a standalone Windows executable (.exe) using PyInstaller

✅ Option 2: Creates a portable package with platform-specific launchers

✅ Option 3: Does both simultaneously

Key outputs:

dist/HDR_Brachytherapy.exe – Single-file executable (Windows)

HDR_Brachytherapy_Portable/ – Cross-platform package with:

RUN_WINDOWS.bat

run_linux.sh

run_mac.sh

requirements.txt

README.txt

2. installer.py – One-Click Installation Wrapper
Purpose: Simplifies the deployment process for end-users with minimal technical knowledge.

What it does:

✅ Verifies Python installation and PATH configuration

✅ Automatically installs PyInstaller

✅ Runs deploy.py with optimal settings

✅ Provides clear success/error messages

✅ Creates both executable and portable versions by default

📥 How to Use
For Developers / Advanced Users:
bash
# 1. Clone/download all files
# 2. Run deployment directly
python deploy.py
# Follow on-screen prompts to choose deployment method
For End-Users / Simplified Installation:
bash
# 1. Download all files to a folder
# 2. Double-click installer.py (Windows) or run:
python installer.py
# 3. The script will automatically:
#    - Check for Python
#    - Install required tools
#    - Create the application executable
Running the Application:
Windows: Double-click HDR_Brachytherapy.exe in the dist folder

Portable version: Run the appropriate launcher for your OS

Direct Python: Run HDR Co60 Brachytherapy - Image Analysis Suite (136).py

🔧 Requirements
Python 3.8+ (for portable version)

Windows 7/10/11, macOS 10.14+, or Linux with GUI

4GB RAM minimum, 8GB recommended

500MB free disk space

Screen resolution: 1280×720 minimum

📦 Included Python Libraries
The deployment scripts automatically install:

Pillow (Image processing)

opencv-python (Computer vision)

numpy (Numerical computations)

tkcalendar (Date selection widgets)

matplotlib (Graphing and plotting)

pydicom (DICOM medical image handling)

🆘 Support
For technical issues or questions about this code:
📧 Email: lochanasachindra123@gmail.com


