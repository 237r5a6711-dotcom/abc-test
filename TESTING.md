# Testing and Verification Guide

## Pre-Flight Checks

### 1. Verify Dependencies

```bash
# Test GNU Radio
gnuradio-companion --version
# Expected: GNU Radio Companion 3.8.x or 3.10.x

# Test Python and NumPy
python3 -c "import numpy; print(f'NumPy {numpy.__version__}')"
# Expected: NumPy 1.x.x

# Test OpenCV
python3 -c "import cv2; print(f'OpenCV {cv2.__version__}')"
# Expected: OpenCV 4.x.x

# Test gr-video-sdl
python3 -c "from gnuradio import video_sdl; print('gr-video-sdl: OK')"
# Expected: gr-video-sdl: OK
```

### 2. Verify Camera

```bash
# List available cameras (Linux)
ls -l /dev/video*
# Expected: /dev/video0, /dev/video1, etc.

# Check camera permissions
groups | grep video
# Expected: video group should be listed

# Test camera access
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('Camera opened:', cap.isOpened()); cap.release()"
# Expected: Camera opened: True
```

### 3. Test Camera Capabilities

```bash
# Check camera formats (Linux)
v4l2-ctl --device=/dev/video0 --list-formats-ext

# Look for:
# - 640x480 resolution support
# - MJPEG format support
# - High frame rate support (30+ fps)
```

### 4. Benchmark Camera Performance

Save this as `test_camera.py`:

```python
#!/usr/bin/env python3
import cv2
import time
import numpy as np

def test_camera(index=0, width=640, height=480, target_fps=60, duration=5):
    """Test camera capture performance"""
    print(f"Testing camera {index} at {width}x{height} @ {target_fps}fps")
    
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"❌ Failed to open camera {index}")
        return False
    
    # Configure camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, target_fps)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    
    # Get actual settings
    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"Actual camera settings: {actual_width}x{actual_height} @ {actual_fps}fps")
    
    # Capture test
    print(f"Capturing for {duration} seconds...")
    start_time = time.time()
    frame_count = 0
    gray_times = []
    
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            continue
        
        frame_count += 1
        
        # Simulate processing
        t0 = time.time()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if gray.shape != (height, width):
            gray = cv2.resize(gray, (width, height))
        _ = gray.tobytes()
        t1 = time.time()
        gray_times.append(t1 - t0)
    
    elapsed = time.time() - start_time
    actual_fps_achieved = frame_count / elapsed
    avg_process_time = np.mean(gray_times) * 1000  # ms
    
    cap.release()
    
    # Results
    print(f"\n{'='*60}")
    print(f"Test Results:")
    print(f"{'='*60}")
    print(f"Frames captured: {frame_count}")
    print(f"Duration: {elapsed:.2f}s")
    print(f"Achieved FPS: {actual_fps_achieved:.1f}")
    print(f"Avg processing time: {avg_process_time:.2f}ms")
    print(f"Frame size: {width}x{height} = {width*height} bytes")
    print(f"Throughput: {width*height*actual_fps_achieved/1e6:.2f} MB/s")
    print(f"Bandwidth: {width*height*actual_fps_achieved*8/1e6:.2f} Mbps")
    
    # Evaluation
    print(f"\n{'='*60}")
    print(f"Evaluation:")
    print(f"{'='*60}")
    
    success = True
    
    if actual_fps_achieved >= target_fps * 0.95:
        print(f"✅ FPS: Excellent ({actual_fps_achieved:.1f} >= {target_fps * 0.95:.1f})")
    elif actual_fps_achieved >= target_fps * 0.8:
        print(f"⚠️  FPS: Good ({actual_fps_achieved:.1f} >= {target_fps * 0.8:.1f})")
    elif actual_fps_achieved >= target_fps * 0.5:
        print(f"⚠️  FPS: Fair ({actual_fps_achieved:.1f} >= {target_fps * 0.5:.1f})")
        success = False
    else:
        print(f"❌ FPS: Poor ({actual_fps_achieved:.1f} < {target_fps * 0.5:.1f})")
        success = False
    
    if avg_process_time < 5:
        print(f"✅ Processing: Fast ({avg_process_time:.2f}ms < 5ms)")
    elif avg_process_time < 10:
        print(f"⚠️  Processing: Moderate ({avg_process_time:.2f}ms < 10ms)")
    else:
        print(f"❌ Processing: Slow ({avg_process_time:.2f}ms >= 10ms)")
        success = False
    
    required_mbps = 147.5
    achieved_mbps = width*height*actual_fps_achieved*8/1e6
    
    if achieved_mbps >= required_mbps:
        print(f"✅ Bandwidth: Sufficient ({achieved_mbps:.1f} Mbps >= {required_mbps} Mbps)")
    elif achieved_mbps >= required_mbps * 0.5:
        print(f"⚠️  Bandwidth: Limited ({achieved_mbps:.1f} Mbps < {required_mbps} Mbps)")
        print(f"   Recommended: Use Standard version @ 30fps")
    else:
        print(f"❌ Bandwidth: Insufficient ({achieved_mbps:.1f} Mbps << {required_mbps} Mbps)")
        print(f"   Recommended: Reduce resolution or FPS")
        success = False
    
    print(f"\n{'='*60}")
    print(f"Recommendation:")
    print(f"{'='*60}")
    
    if actual_fps_achieved >= 55 and achieved_mbps >= required_mbps:
        print("✅ Your system can handle High Performance version @ 60fps")
    elif actual_fps_achieved >= 28:
        print("✅ Your system can handle Standard version @ 30fps")
        print("⚠️  Or High Performance version with frame_skip=2")
    else:
        print("⚠️  Consider reducing resolution to 480x360 or FPS to 15")
    
    return success

if __name__ == "__main__":
    print("="*60)
    print("OFDM Video System - Camera Performance Test")
    print("="*60)
    
    # Test 60fps
    print("\n\n" + "="*60)
    print("Test 1: 640x480 @ 60fps (High Performance target)")
    print("="*60)
    test_camera(0, 640, 480, 60, 5)
    
    # Test 30fps
    print("\n\n" + "="*60)
    print("Test 2: 640x480 @ 30fps (Standard target)")
    print("="*60)
    test_camera(0, 640, 480, 30, 5)
    
    print("\n\nTesting complete!")
```

Run the test:
```bash
python3 test_camera.py
```

## Testing the GRC Flowgraphs

### Test 1: Standard Version (Basic)

1. **Open the flowgraph**:
   ```bash
   gnuradio-companion ofdm_video_480p_60fps.grc
   ```

2. **Verify block parameters**:
   - Check `fft_len = 256`
   - Check `samp_rate = 10000000`
   - Check `packet_len = 4096`
   - Check embedded Python block has `fps_target = 60`

3. **Generate Python code**:
   - Press **F5** or click Generate button
   - Check console for any errors
   - Verify Python file is created

4. **Run the flowgraph**:
   - Press **F6** or click Execute button
   - Watch console output:
     ```
     Camera opened: 640x480 @60.0fps, skip=1
     ```

5. **Expected behavior**:
   - GUI window appears with spectrum display
   - Video SDL window opens showing webcam feed
   - Video may have some frame drops at 60fps
   - Console shows no errors

6. **Monitor performance**:
   - Watch video smoothness
   - Check CPU usage: `top` or `htop`
   - Expected CPU: 40-70% on i5

### Test 2: Standard Version @ 30fps (Smooth)

1. **Modify for 30fps**:
   - Double-click embedded Python block
   - Change `fps_target = 60` to `fps_target = 30`
   - Regenerate (F5) and run (F6)

2. **Expected behavior**:
   - ✅ Smooth video playback
   - ✅ No frame drops
   - ✅ Lower CPU usage (30-50%)

### Test 3: High Performance Version

1. **Open the flowgraph**:
   ```bash
   gnuradio-companion ofdm_video_480p_60fps_hiperf.grc
   ```

2. **Verify block parameters**:
   - Check `fft_len = 512`
   - Check `samp_rate = 20000000`
   - Check `packet_len = 8192`
   - Check embedded Python block has `fps_target = 60`, `frame_skip = 1`

3. **Generate and run**: F5, then F6

4. **Expected behavior**:
   - ✅ Smooth 60fps video (on capable hardware)
   - ✅ No visible frame drops
   - ⚠️ Higher CPU usage (60-90%)

5. **If video is choppy**:
   - Edit embedded Python block
   - Change `frame_skip = 1` to `frame_skip = 2`
   - Regenerate and run
   - Should now show smooth 30fps effective

## Performance Metrics to Check

### Visual Quality Checks

✅ **Good**:
- Smooth motion
- No tearing or artifacts
- Clear image
- Responsive to camera movement

❌ **Bad**:
- Jerky/stuttering motion
- Frozen frames
- Pixelated or blocky
- Significant lag

### Console Output Checks

**Good console output**:
```
Camera opened: 640x480 @60.0fps, skip=1
Frames captured: 300, Sent: 300
```

**Problem indicators**:
```
ERROR: Cannot open camera 0
WARNING: Frame queue full
gr::log :WARN: ...
```

### System Resource Checks

Run in another terminal:
```bash
# Monitor CPU usage
top -p $(pgrep -f python)

# Monitor memory
watch -n 1 'free -h'

# Monitor GPU (if applicable)
nvidia-smi -l 1
```

**Expected resources**:
- **Standard @ 30fps**: 30-50% CPU, 200-300 MB RAM
- **Standard @ 60fps**: 40-70% CPU, 200-300 MB RAM (with drops)
- **High Perf @ 60fps**: 60-90% CPU, 300-400 MB RAM

## Common Issues and Solutions

### Issue 1: "Camera could not be opened"

**Test**:
```bash
ls -l /dev/video0
python3 -c "import cv2; cv2.VideoCapture(0).isOpened()"
```

**Solutions**:
- Add user to video group: `sudo usermod -aG video $USER`
- Logout and login
- Try different camera index (0, 1, 2)
- Close other apps using camera

### Issue 2: "ModuleNotFoundError: cv2"

**Test**:
```bash
python3 -c "import cv2"
```

**Solution**:
```bash
pip3 install opencv-python
```

### Issue 3: "No module named 'gnuradio.video_sdl'"

**Test**:
```bash
python3 -c "from gnuradio import video_sdl"
```

**Solution**:
```bash
sudo apt-get install gr-video-sdl
```

### Issue 4: Choppy video at 60fps

**Test**: Run camera benchmark script

**Solutions**:
1. Use Standard version @ 30fps
2. Use High Performance with frame_skip=2
3. Reduce resolution to 480x360
4. Close other applications
5. Set CPU governor to performance

### Issue 5: High CPU usage

**Test**: `top` while running

**Solutions**:
1. Use Standard version instead of High Performance
2. Disable spectrum display (frequency sink)
3. Reduce resolution
4. Reduce FPS

## Automated Test Script

Save this as `test_grc.sh`:

```bash
#!/bin/bash

echo "OFDM Video System - Automated Test"
echo "===================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

fail_count=0
pass_count=0

# Test function
test_command() {
    local desc="$1"
    local cmd="$2"
    echo -n "Testing $desc... "
    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        ((pass_count++))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        ((fail_count++))
        return 1
    fi
}

# Run tests
test_command "GNU Radio" "gnuradio-companion --version"
test_command "Python 3" "python3 --version"
test_command "NumPy" "python3 -c 'import numpy'"
test_command "OpenCV" "python3 -c 'import cv2'"
test_command "gr-video-sdl" "python3 -c 'from gnuradio import video_sdl'"
test_command "Camera access" "python3 -c 'import cv2; assert cv2.VideoCapture(0).isOpened()'"
test_command "Video device" "ls /dev/video0"
test_command "GRC files" "ls ofdm_video_480p_60fps.grc"

# Summary
echo ""
echo "===================================="
echo "Test Summary"
echo "===================================="
echo -e "Passed: ${GREEN}${pass_count}${NC}"
echo -e "Failed: ${RED}${fail_count}${NC}"

if [ $fail_count -eq 0 ]; then
    echo -e "\n${GREEN}✅ All tests passed! System is ready.${NC}"
    exit 0
else
    echo -e "\n${RED}❌ Some tests failed. Please fix issues above.${NC}"
    exit 1
fi
```

Run it:
```bash
chmod +x test_grc.sh
./test_grc.sh
```

## Final Verification Checklist

Before considering the system working:

- [ ] All dependencies installed (GNU Radio, OpenCV, gr-video-sdl)
- [ ] Camera accessible (tested with OpenCV)
- [ ] Camera can achieve 30+ fps at 640x480
- [ ] GRC files open without errors
- [ ] Python code generates successfully
- [ ] Standard version runs @ 30fps smoothly
- [ ] High Performance version runs (60fps or with frame_skip)
- [ ] Video displays in SDL window
- [ ] No error messages in console
- [ ] CPU usage acceptable
- [ ] Video quality is good

## Benchmarking Results Template

Record your results:

```
System: ___________________
CPU: ______________________
RAM: ______________________
Camera: ___________________

Standard Version @ 30fps:
- Achieved FPS: _____
- CPU Usage: ____%
- Smooth: Yes/No
- Rating: ⭐⭐⭐⭐⭐

Standard Version @ 60fps:
- Achieved FPS: _____
- CPU Usage: ____%
- Smooth: Yes/No
- Rating: ⭐⭐⭐⭐⭐

High Performance @ 60fps:
- Achieved FPS: _____
- CPU Usage: ____%
- Smooth: Yes/No
- Rating: ⭐⭐⭐⭐⭐

Recommendation: ____________
```

## Next Steps After Verification

Once everything works:

1. **Experiment with parameters**
   - Try different FFT sizes
   - Test different modulations
   - Adjust packet lengths

2. **Add features**
   - Channel impairments
   - Error correction
   - Recording capability

3. **Hardware testing**
   - Replace throttle with USRP
   - Test over-the-air transmission
   - Add antenna and RF components

4. **Optimization**
   - Profile performance
   - Optimize Python blocks
   - Add GPU acceleration

Congratulations! You have a working OFDM video transmission system! 🎉
