#!/usr/bin/env python3
"""
Test script to verify video streaming solution
"""

import sys
import subprocess
import time

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def test_python():
    """Test Python installation"""
    print_header("Testing Python Installation")
    
    try:
        version = sys.version_info
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} found")
        
        if version.major < 3 or (version.major == 3 and version.minor < 6):
            print("✗ Python 3.6 or higher is required")
            return False
        return True
    except Exception as e:
        print(f"✗ Error checking Python: {e}")
        return False

def test_opencv():
    """Test OpenCV installation"""
    print_header("Testing OpenCV")
    
    try:
        import cv2
        print(f"✓ OpenCV {cv2.__version__} is installed")
        return True
    except ImportError:
        print("✗ OpenCV is not installed")
        print("  Install with: pip install opencv-python")
        return False

def test_numpy():
    """Test NumPy installation"""
    print_header("Testing NumPy")
    
    try:
        import numpy as np
        print(f"✓ NumPy {np.__version__} is installed")
        return True
    except ImportError:
        print("✗ NumPy is not installed")
        print("  Install with: pip install numpy")
        return False

def test_camera():
    """Test camera availability"""
    print_header("Testing Camera")
    
    try:
        import cv2
        
        cameras_found = []
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras_found.append(i)
                # Get camera info
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                fps = cap.get(cv2.CAP_PROP_FPS)
                print(f"✓ Camera {i} found ({width:.0f}x{height:.0f} @ {fps:.0f}fps)")
                cap.release()
        
        if not cameras_found:
            print("✗ No cameras found")
            print("  Make sure a webcam is connected")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Error testing camera: {e}")
        return False

def test_network():
    """Test network capability"""
    print_header("Testing Network")
    
    try:
        import socket
        
        # Test creating socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Test binding to port
        try:
            s.bind(('127.0.0.1', 9999))
            s.close()
            print("✓ Network socket can bind to port 9999")
            return True
        except OSError:
            print("⚠ Port 9999 is already in use")
            print("  This might be okay if transmitter is running")
            return True
            
    except Exception as e:
        print(f"✗ Error testing network: {e}")
        return False

def test_scripts():
    """Test that scripts are present"""
    print_header("Testing Scripts")
    
    import os
    
    scripts = ['transmitter.py', 'receiver.py', 'requirements.txt', 'README.md']
    all_found = True
    
    for script in scripts:
        if os.path.exists(script):
            print(f"✓ {script} found")
        else:
            print(f"✗ {script} not found")
            all_found = False
    
    return all_found

def test_syntax():
    """Test Python syntax of scripts"""
    print_header("Testing Script Syntax")
    
    import py_compile
    
    scripts = ['transmitter.py', 'receiver.py']
    all_valid = True
    
    for script in scripts:
        try:
            py_compile.compile(script, doraise=True)
            print(f"✓ {script} syntax is valid")
        except py_compile.PyCompileError as e:
            print(f"✗ {script} has syntax errors:")
            print(f"  {e}")
            all_valid = False
    
    return all_valid

def main():
    print("\n" + "="*60)
    print("  VIDEO STREAMING SOLUTION - SYSTEM TEST")
    print("="*60)
    
    results = {}
    
    # Run all tests
    results['Python'] = test_python()
    results['OpenCV'] = test_opencv()
    results['NumPy'] = test_numpy()
    results['Camera'] = test_camera()
    results['Network'] = test_network()
    results['Scripts'] = test_scripts()
    results['Syntax'] = test_syntax()
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:15} {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n" + "="*60)
        print("  ✓ ALL TESTS PASSED!")
        print("  Your system is ready for video streaming!")
        print("="*60)
        print("\nQuick Start:")
        print("  1. Run: python transmitter.py")
        print("  2. Run: python receiver.py")
        print("\nOr use: ./quickstart.sh (Linux/Mac) or quickstart.bat (Windows)")
        print("")
        return 0
    else:
        print("\n" + "="*60)
        print("  ✗ SOME TESTS FAILED")
        print("  Please fix the issues above before running")
        print("="*60)
        print("")
        return 1

if __name__ == '__main__':
    sys.exit(main())
