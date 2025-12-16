import os
import subprocess
import sys
import shutil
import platform

def check_python():

    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"✓ Python found: {result.stdout.strip()}")
            return True
        else:
            print("✗ Python not found or not working properly")
            return False
    except Exception as e:
        print(f"✗ Python check failed: {e}")
        return False

def install_dependencies():
    
    print("Installing dependencies...")
    
    packages = [
        "Pillow",
        "opencv-python", 
        "numpy",
        "tkcalendar",
        "matplotlib",
        "pydicom"
    ]
    
    success = True
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                shell=True)
            print(f"✓ Installed: {package}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")
            success = False
            
    return success

def create_executable():

    print("Creating standalone executable...")
    
    try:
        
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                            shell=True)
        
        
        hidden_imports = [
            "tkinter",
            "PIL",
            "PIL._tkinter_finder",
            "matplotlib.backends.backend_tkagg",
            "matplotlib.backends.backend_tk",
            "tkcalendar",
            "numpy",
            "cv2",
            "pydicom",
            "matplotlib.pyplot",
            "matplotlib.backends",
            "matplotlib.figure",
            "packaging",
            "packaging.version",
            "packaging.specifiers",
            "packaging.requirements"
        ]
        
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed", 
            "--name=HDR_Brachytherapy",
            "--add-data=Project_133.py;.",
        ]
        
      
        for imp in hidden_imports:
            cmd.append(f"--hidden-import={imp}")
        
       
        cmd.extend([
            "--collect-all=tkcalendar",
            "--collect-all=matplotlib",
            "--collect-all=PIL",
            "Project_133.py"
        ])
        
        print(f"Running PyInstaller command...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Executable created successfully!")
            print(f"✓ Location: {os.path.abspath('dist/HDR_Brachytherapy.exe')}")
            
            
            if os.path.exists("dist/HDR_Brachytherapy.exe"):
                print("✓ Executable verified in dist folder")
            else:
                print("⚠ Executable not found in dist folder - checking build log...")
                
            return True
        else:
            print(f"✗ PyInstaller failed with return code: {result.returncode}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            
           
            if os.path.exists("build/HDR_Brachytherapy/warn-HDR_Brachytherapy.txt"):
                print("\n=== Build Warnings ===")
                with open("build/HDR_Brachytherapy/warn-HDR_Brachytherapy.txt", "r") as f:
                    print(f.read())
            
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create executable: {e}")
        print(f"Error output: {e.output if hasattr(e, 'output') else 'No output'}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False
    
def create_portable_package():
  
    print("Creating portable package...")
    
    portable_dir = "HDR_Brachytherapy_Portable"
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    
    os.makedirs(portable_dir)
    
    
    shutil.copy("Project_133.py", os.path.join(portable_dir, "Project_133.py"))
    
    
    requirements = """Pillow>=9.0.0
opencv-python>=4.5.0
numpy>=1.21.0
tkcalendar>=1.6.1
matplotlib>=3.5.0
pydicom>=2.3.0
"""
    
    with open(os.path.join(portable_dir, "requirements.txt"), "w") as f:
        f.write(requirements)
    
    
    create_windows_launcher(portable_dir)
    create_linux_launcher(portable_dir)
    create_mac_launcher(portable_dir)
    create_readme(portable_dir)
    
    print(f"✓ Portable package created in: {portable_dir}")
    return True

def create_windows_launcher(portable_dir):
    """Create Windows batch launcher"""
    batch_content = """@echo off
chcp 65001 >nul
title HDR Brachytherapy Application
echo ========================================
echo    HDR Brachytherapy Analysis System
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Check and install dependencies
echo Checking and installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

:: Run application
echo.
echo Starting HDR Brachytherapy Application...
echo.
python Project_133.py

pause
"""
    
    with open(os.path.join(portable_dir, "RUN_WINDOWS.bat"), "w", encoding='utf-8') as f:
        f.write(batch_content)

def create_linux_launcher(portable_dir):
    
    bash_content = """#!/bin/bash
echo "========================================"
echo "   HDR Brachytherapy Analysis System"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed."
    echo ""
    echo "Please install Python 3.8+ using:"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "Fedora: sudo dnf install python3 python3-pip"
    echo ""
    exit 1
fi

# Check and install dependencies
echo "Checking and installing dependencies..."
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt

# Run application
echo ""
echo "Starting HDR Brachytherapy Application..."
echo ""
python3 Project_133.py
"""
    
    with open(os.path.join(portable_dir, "run_linux.sh"), "w", encoding='utf-8') as f:
        f.write(bash_content)
    
    os.chmod(os.path.join(portable_dir, "run_linux.sh"), 0o755)

def create_mac_launcher(portable_dir):
    
    mac_content = """#!/bin/bash
echo "========================================"
echo "   HDR Brachytherapy Analysis System"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed."
    echo ""
    echo "Please install Python 3.8+ from:"
    echo "https://www.python.org/downloads/"
    echo ""
    echo "Or using Homebrew:"
    echo "brew install python"
    echo ""
    exit 1
fi

# Check and install dependencies
echo "Checking and installing dependencies..."
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt

# Run application
echo ""
echo "Starting HDR Brachytherapy Application..."
echo ""
python3 Project_133.py
"""
    
    with open(os.path.join(portable_dir, "run_mac.sh"), "w", encoding='utf-8') as f:
        f.write(mac_content)
    
    os.chmod(os.path.join(portable_dir, "run_mac.sh"), 0o755)

def create_readme(portable_dir):
    
    readme_content = """HDR BRACHYTHERAPY ANALYSIS APPLICATION
================================================

System Requirements:
- Windows 7/10/11, macOS 10.14+, or Linux with GUI
- Python 3.8 or higher
- 4GB RAM minimum, 8GB recommended
- 500MB free disk space
- Screen resolution: 1280x720 minimum

QUICK START:
------------

Windows:
1. Double-click RUN_WINDOWS.bat
2. Application will automatically install dependencies
3. The main application will start

Linux:
1. Open terminal in this folder
2. Run: ./run_linux.sh
3. Or: bash run_linux.sh

macOS:
1. Open terminal in this folder  
2. Run: ./run_mac.sh
3. Or: bash run_mac.sh

FEATURES:
---------
- AP and Lateral image analysis
- Applicator tracking and measurement
- Fraction comparison
- DICOM support
- Advanced image processing

SUPPORT:
--------
For technical issues, please contact your system administrator.

================================================
"""
    
    with open(os.path.join(portable_dir, "README.txt"), "w", encoding='utf-8') as f:
        f.write(readme_content)

def main():
    print("HDR Brachytherapy Deployment Tool")
    print("=" * 50)
    
    if not check_python():
        print("\nPlease install Python first from https://python.org")
        input("Press Enter to exit...")
        return
    
    print("\nChoose deployment method:")
    print("1. Create Standalone Executable (Recommended for Windows)")
    print("2. Create Portable Package (All platforms)")
    print("3. Both")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
    except:
        choice = "2"
    
    success = True
    
    if choice in ["1", "3"]:
        print("\n" + "="*50)
        print("CREATING STANDALONE EXECUTABLE")
        print("="*50)
        if install_dependencies():
            success = create_executable() and success
        else:
            success = False
    
    if choice in ["2", "3"]:
        print("\n" + "="*50)
        print("CREATING PORTABLE PACKAGE")
        print("="*50)
        if install_dependencies():
            success = create_portable_package() and success
        else:
            success = False
    
    print("\n" + "="*50)
    if success:
        print("DEPLOYMENT COMPLETED SUCCESSFULLY!")
        print("\nWhat was created:")
        if choice in ["1", "3"]:
            print("✓ HDR_Brachytherapy.exe (in 'dist' folder)")
        if choice in ["2", "3"]:
            print("✓ HDR_Brachytherapy_Portable folder")
    else:
        print("DEPLOYMENT HAD SOME ERRORS!")
        print("Please check the messages above.")
    
    print("\nPress Enter to exit...")
    input()


def setup_encoding():
    """Fix encoding issues on Windows"""
    try:
        if sys.platform == "win32":
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

def print_status(message, is_success=True):
    """Print status with simple indicators"""
    indicator = "[OK]" if is_success else "[ERROR]"
    print(f"{indicator} {message}")

def check_python():
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True, encoding='utf-8')
        print_status(f"Python found: {result.stdout.strip()}")
        return True
    except Exception as e:
        print_status(f"Python check failed: {e}", False)
        return False

def main():
    setup_encoding()
    
    print("=" * 50)
    print("       HDR Brachytherapy Deployment")
    print("=" * 50)
    print()
    
    # Check Python
    if not check_python():
        input("Press Enter to exit...")
        sys.exit(1)
    


if __name__ == "__main__":
    main()
