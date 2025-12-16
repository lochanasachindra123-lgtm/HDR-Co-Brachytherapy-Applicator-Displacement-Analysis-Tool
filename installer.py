import os
import sys
import subprocess
import platform

def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def main():
    print("=" * 50)
    print("       HDR Brachytherapy Installation")
    print("=" * 50)
    print()
    
    # Check Python
    print("Checking Python installation...")
    success, output = run_command("python --version")
    
    if not success:
        print("❌ ERROR: Python is not installed or not in PATH!")
        print("\nPlease install Python 3.8+ from:")
        print("https://python.org/downloads/")
        print("\nIMPORTANT: During installation, check 'Add Python to PATH'")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("✅ Python is installed")
    print()
    
    # Install PyInstaller
    print("Installing PyInstaller...")
    success, output = run_command("pip install pyinstaller")
    if success:
        print("✅ PyInstaller installed")
    else:
        print("❌ Failed to install PyInstaller")
        print(f"Error: {output}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print()
    print("Creating HDR Brachytherapy executable...")
    print()
    
    # Run deployment
    success, output = run_command("python deploy.py")
    if success:
        print("✅ Deployment completed successfully!")
    else:
        print("❌ Deployment failed")
        print(f"Error: {output}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print()
    print("=" * 50)
    print("       Installation Complete!")
    print("=" * 50)
    print("\nWhat was created:")
    print("- HDR_Brachytherapy.exe (in dist folder)")
    print("- HDR_Brachytherapy_Portable folder")
    print("\nYou can now:")
    print("1. Run HDR_Brachytherapy.exe directly")
    print("2. Or use the portable version")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
