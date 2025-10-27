# Quick Start Guide - OFDM Video Transmission

## For 480p @ 60fps Smooth Playback

### Prerequisites Check
```bash
# Check if GNU Radio is installed
gnuradio-companion --version

# Check if OpenCV is installed
python3 -c "import cv2; print(cv2.__version__)"

# Check if gr-video-sdl is available
python3 -c "from gnuradio import video_sdl; print('gr-video-sdl OK')"

# List available cameras (Linux)
ls /dev/video*

# Check camera capabilities (Linux)
v4l2-ctl --device=/dev/video0 --list-formats-ext
```

### Installation (if needed)
```bash
# Install OpenCV
pip3 install opencv-python

# Install gr-video-sdl (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install gr-video-sdl

# Add user to video group (Linux)
sudo usermod -aG video $USER
# Logout and login again for group changes to take effect
```

## Running the System

### Option 1: High Performance (Recommended for 60fps)

1. **Open the flowgraph**:
   ```bash
   cd /path/to/repository
   gnuradio-companion ofdm_video_480p_60fps_hiperf.grc
   ```

2. **Verify parameters** (already optimized):
   - FFT length: 512
   - Sample rate: 20 MHz
   - Packet length: 8192
   - FPS target: 60
   - Frame skip: 1 (no skipping)

3. **Generate and run**:
   - Press **F5** to generate Python code
   - Press **F6** to execute
   - A video window should appear showing your webcam feed

4. **Monitor performance**:
   - Check console for "Camera opened" message
   - Watch for smooth video playback
   - If video is choppy, see troubleshooting below

### Option 2: Standard Performance (Lower CPU usage)

1. **Open the flowgraph**:
   ```bash
   gnuradio-companion ofdm_video_480p_60fps.grc
   ```

2. **Adjust for smooth 30fps** (or accept some 60fps drops):
   - In embedded Python block, change `fps_target` to `30` for guaranteed smooth
   - Or keep at `60` and accept occasional frame drops

3. **Generate and run**: Press F5, then F6

## Troubleshooting

### Video is Choppy / Low FPS

**Solution 1: Use Standard version with 30fps**
- Open `ofdm_video_480p_60fps.grc`
- Edit embedded Python block
- Change `fps_target` from `60` to `30`
- Regenerate and run

**Solution 2: Enable frame skipping (High Performance version)**
- Open `ofdm_video_480p_60fps_hiperf.grc`
- Edit embedded Python block
- Change `frame_skip` from `1` to `2` (transmits 30fps effective)
- Regenerate and run

**Solution 3: Reduce resolution**
- Edit embedded Python block
- Change `frame_width` to `480` and `frame_height` to `360`
- Regenerate and run

**Solution 4: Close other applications**
- Close browser, video players, other camera apps
- Stop background services
- Run: `gnuradio-companion` with higher priority
  ```bash
  nice -n -10 gnuradio-companion
  ```

### Camera Not Opening

**Check camera**:
```bash
# List cameras
ls /dev/video*

# Test with OpenCV
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('Opened:', cap.isOpened()); cap.release()"

# Check permissions
ls -l /dev/video0
groups  # Should include 'video' group
```

**Try different camera index**:
- Edit embedded Python block
- Change `camera_index` from `0` to `1` or `2`
- Regenerate and run

### No Video Display / SDL Error

**Install gr-video-sdl**:
```bash
# Ubuntu/Debian
sudo apt-get install gr-video-sdl

# From source
git clone https://github.com/gnuradio/gr-video-sdl
cd gr-video-sdl
mkdir build && cd build
cmake ..
make -j4
sudo make install
sudo ldconfig
```

**Check SDL**:
```bash
python3 -c "from gnuradio import video_sdl"
```

### High CPU Usage

**Standard version**: Should use 50-70% CPU on modern i5
**High Performance version**: May use 80-100% CPU

**Reduce CPU usage**:
1. Use Standard version instead of High Performance
2. Disable frequency sink (spectrum display)
3. Reduce sample rate
4. Lower resolution or FPS

### Python Block Errors

**ModuleNotFoundError: cv2**:
```bash
pip3 install opencv-python
```

**ModuleNotFoundError: gnuradio.video_sdl**:
```bash
sudo apt-get install gr-video-sdl
```

## Performance Tuning

### For Maximum Smoothness

1. **Use High Performance version** with these settings:
   - FFT: 512 (default)
   - Sample rate: 20 MHz (default)
   - Packet length: 8192 (default)
   - Frame skip: 1 (default)

2. **System optimizations**:
   ```bash
   # Set CPU governor to performance
   echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
   
   # Disable CPU frequency scaling
   sudo systemctl disable ondemand
   
   # Run with real-time priority (careful!)
   sudo nice -n -20 gnuradio-companion
   ```

3. **Camera optimizations**:
   - Use USB 3.0 port for camera
   - Enable MJPEG mode (automatic in code)
   - Reduce camera exposure time
   - Use good lighting conditions

### For Lower CPU Usage

1. **Use Standard version** with 30fps:
   - Set `fps_target` to `30`
   
2. **Or use High Performance with frame skip**:
   - Set `frame_skip` to `2` (30fps effective)

## Expected Results

### High Performance Version (Smooth 60fps)
- Resolution: 640x480
- Frame rate: 60 fps
- Latency: 50-100ms
- CPU usage: 70-100% (i7/i9)
- Throughput: ~180 Mbps

### Standard Version (30fps or 60fps with drops)
- Resolution: 640x480
- Frame rate: 30-60 fps
- Latency: 100-200ms
- CPU usage: 40-70% (i5)
- Throughput: ~70 Mbps

## Next Steps

Once you have smooth video:
1. Experiment with different modulations (edit OFDM blocks)
2. Add channel impairments for testing
3. Replace loopback with USRP hardware for real transmission
4. Add FEC (forward error correction) for robustness
5. Implement video compression (H.264/VP8) in Python block

## Support

For issues:
1. Check console output for error messages
2. Verify all prerequisites are installed
3. Test camera independently with OpenCV
4. Start with Standard version at 30fps
5. Gradually increase to 60fps

## Key Files

- `ofdm_video_480p_60fps.grc` - Standard version
- `ofdm_video_480p_60fps_hiperf.grc` - High performance version
- `README.md` - Complete documentation
- `QUICKSTART.md` - This file
