#!/usr/bin/env python3
"""
Build script for Smriti Memory Library
This script helps build and distribute the Python package.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def print_banner():
    """Print build banner."""
    print("🏗️  Smriti Memory Library Build")
    print("=" * 40)
    print("Building Python package for distribution")
    print("=" * 40)


def clean_build_dirs():
    """Clean build and distribution directories."""
    print("🧹 Cleaning build directories...")
    
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    
    for pattern in dirs_to_clean:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"✅ Removed {path}")
            elif path.is_file():
                path.unlink()
                print(f"✅ Removed {path}")


def check_dependencies():
    """Check if build dependencies are available."""
    print("🔍 Checking build dependencies...")
    
    try:
        import setuptools
        import wheel
        print("✅ Build dependencies are available")
        return True
    except ImportError as e:
        print(f"❌ Missing build dependency: {e}")
        print("Install with: pip install setuptools wheel")
        return False


def run_tests():
    """Run tests before building."""
    print("🧪 Running tests...")
    
    try:
        result = subprocess.run([sys.executable, "test_smriti.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Tests passed")
            return True
        else:
            print("⚠️  Tests failed, but continuing with build")
            print("Test output:")
            print(result.stdout)
            print("Test errors:")
            print(result.stderr)
            return True  # Continue anyway
            
    except Exception as e:
        print(f"⚠️  Could not run tests: {e}")
        return True  # Continue anyway


def build_package():
    """Build the Python package."""
    print("📦 Building package...")
    
    try:
        # Build source distribution
        subprocess.check_call([sys.executable, "setup.py", "sdist"])
        print("✅ Source distribution built")
        
        # Build wheel
        subprocess.check_call([sys.executable, "setup.py", "bdist_wheel"])
        print("✅ Wheel distribution built")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False


def check_package():
    """Check the built package."""
    print("🔍 Checking built package...")
    
    try:
        # Check wheel
        subprocess.check_call([sys.executable, "-m", "pip", "check", "dist/*.whl"])
        print("✅ Package check passed")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Package check failed: {e}")
        return False


def show_build_info():
    """Show information about the built package."""
    print("\n📊 Build Information:")
    
    dist_dir = Path("dist")
    if dist_dir.exists():
        files = list(dist_dir.glob("*"))
        for file in files:
            size = file.stat().st_size / 1024  # KB
            print(f"  📁 {file.name} ({size:.1f} KB)")
    
    print("\n🚀 To install the package:")
    print("  pip install dist/smriti-memory-*.whl")
    
    print("\n📤 To upload to PyPI:")
    print("  python -m twine upload dist/*")
    
    print("\n📥 To install in development mode:")
    print("  pip install -e .")


def main():
    """Main build process."""
    print_banner()
    
    # Clean build directories
    clean_build_dirs()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Run tests
    run_tests()
    
    # Build package
    if not build_package():
        print("❌ Build failed. Please check the error messages above.")
        sys.exit(1)
    
    # Check package
    if not check_package():
        print("❌ Package check failed. Please check the error messages above.")
        sys.exit(1)
    
    # Show build info
    show_build_info()
    
    print("\n🎉 Build completed successfully!")


if __name__ == "__main__":
    main() 