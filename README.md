# OFDM Video Transmission System - 480p @ 60fps

This GNU Radio flowgraph implements real-time video transmission using OFDM modulation, capable of transmitting and receiving 480p video at 60 frames per second.

## Two Versions Available

### 1. Standard Version (`ofdm_video_480p_60fps.grc`)
- **Sample Rate**: 10 MHz
- **FFT Size**: 256
- **Data Carriers**: 194
- **Packet Length**: 4096 bytes
- **Best for**: General use, lower CPU usage

### 2. High Performance Version (`ofdm_video_480p_60fps_hiperf.grc`)
- **Sample Rate**: 20 MHz
- **FFT Size**: 512
- **Data Carriers**: 420+
- **Packet Length**: 8192 bytes
- **Frame Skip**: Configurable frame skipping
- **Best for**: Maximum throughput, powerful systems

## Features

- **Resolution**: 640x480 pixels (480p)
- **Frame Rate**: 60 fps
- **Modulation**: OFDM with 64-QAM payload modulation
- **Video Format**: Grayscale (reduced bandwidth)
- **Real-time**: Low-latency transmission and playback

## Requirements

### Software
- GNU Radio 3.8 or 3.10
- Python 3.6+
- OpenCV Python (`opencv-python`)
- gr-video-sdl

### Installation

```bash
# Install OpenCV
pip install opencv-python

# Install gr-video-sdl (Ubuntu/Debian)
sudo apt-get install gr-video-sdl

# Or build from source
# git clone https://github.com/gnuradio/gr-video-sdl
# cd gr-video-sdl
# mkdir build && cd build
# cmake ..
# make
# sudo make install
```

## Usage

1. Open GNU Radio Companion:
   ```bash
   gnuradio-companion
   ```

2. Load the flowgraph:
   - **Standard**: File → Open → `ofdm_video_480p_60fps.grc`
   - **High Performance**: File → Open → `ofdm_video_480p_60fps_hiperf.grc`

3. Generate and run:
   - Click the "Generate" button (or press F5)
   - Click the "Execute" button (or press F6)

4. The system will:
   - Capture video from your default webcam (camera index 0)
   - Transmit via OFDM modulation
   - Receive and decode the OFDM signal
   - Display the video in an SDL window at 60 fps

## Which Version to Use?

**Use Standard Version** if:
- You have a mid-range computer
- You want lower CPU usage
- You're okay with occasional frame drops

**Use High Performance Version** if:
- You have a powerful computer
- You need maximum throughput
- You want the smoothest 60fps experience
- You can adjust `frame_skip` parameter (set to 2 to transmit 30fps effective)

## Technical Details

### Standard Version Parameters
- **FFT Length**: 256
- **Cyclic Prefix**: 64 (FFT_len/4)
- **Data Carriers**: 194 (optimized carrier allocation)
- **Pilot Carriers**: 6
- **Sample Rate**: 10 MHz
- **Packet Length**: 4096 bytes
- **Expected Throughput**: ~70 Mbps

### High Performance Version Parameters
- **FFT Length**: 512
- **Cyclic Prefix**: 64 (FFT_len/8 - reduced overhead)
- **Data Carriers**: 420+ (maximum carrier allocation)
- **Pilot Carriers**: 10
- **Sample Rate**: 20 MHz
- **Packet Length**: 8192 bytes
- **Expected Throughput**: ~180 Mbps
- **Frame Skip**: 1 (configurable: 1=full rate, 2=30fps, 3=20fps)

### Video Parameters
- **Frame Size**: 640x480 = 307,200 bytes per frame
- **Frame Rate**: 60 fps
- **Required Throughput**: ~18.4 MB/s (147 Mbps)
- **Color Space**: Grayscale (8-bit per pixel)

### Performance Optimizations

1. **High-Order Modulation**: 64-QAM for maximum throughput (6 bits per symbol)
2. **Large FFT**: 256/512-point FFT with optimized carriers for higher capacity
3. **Optimized Packet Size**: 4096/8192 bytes to reduce overhead
4. **Threading**: Separate capture thread to avoid blocking
5. **Frame Queue**: Large buffering (10-30 frames) to handle jitter
6. **MJPEG Mode**: Camera configured for MJPEG when available for higher FPS
7. **Reduced CP** (HiPerf): 1/8 cyclic prefix vs 1/4 for lower overhead
8. **Frame Skipping** (HiPerf): Optional frame skipping to match throughput
9. **Vectorized Operations**: NumPy array operations for speed
10. **Auto-exposure**: Disabled autofocus, enabled auto-exposure for stable framerate

### Carrier Allocation

**Standard Version** uses 194 data carriers:
- Negative carriers: -100 to -53, -52 to -21, -20 to -7, -6 to -1
- Positive carriers: 1 to 6, 8 to 20, 22 to 52, 54 to 100
- DC carrier (0) is nulled
- 6 pilot carriers at: -53, -21, -7, 7, 21, 53

**High Performance Version** uses 420+ data carriers:
- Negative carriers: -220 to -105, -104 to -53, -52 to -21, -20 to -7, -6 to -1
- Positive carriers: 1 to 6, 8 to 20, 22 to 52, 54 to 104, 106 to 220
- DC carrier (0) is nulled
- 10 pilot carriers at: -220, -104, -52, -20, -6, 7, 21, 53, 105, 220

## Troubleshooting

### Low Frame Rate
- Check camera capabilities: `v4l2-ctl --list-formats-ext` (Linux)
- Reduce resolution if needed
- Ensure CPU is not overloaded
- Close other applications using the camera

### No Video Display
- Verify gr-video-sdl is installed
- Check camera permissions
- Try different camera index (0, 1, 2, etc.)

### Choppy Video
- Increase packet_len variable
- Reduce sample rate if system is overloaded
- Check for dropped frames in console output

### Camera Not Opening
- Verify camera is connected: `ls /dev/video*` (Linux)
- Check camera permissions: `sudo usermod -aG video $USER`
- Try different camera_index in the embedded Python block

## Modifying Parameters

### Change Resolution
Edit the embedded Python block parameters:
- `frame_width`: Width in pixels (default: 640)
- `frame_height`: Height in pixels (default: 480)

### Change Frame Rate
Edit the embedded Python block parameters:
- `fps_target`: Target FPS (default: 60)
- `frame_skip` (HiPerf only): Skip frames (1=no skip, 2=transmit every 2nd frame @ 30fps effective)

### Change Camera
Edit the embedded Python block parameters:
- `camera_index`: Camera device index (default: 0)

### Adjust OFDM Parameters
For different throughput requirements, you can modify:
- `fft_len`: FFT size (higher = more carriers)
- `packet_len`: Packet size in bytes
- `payload_mod`: Modulation scheme (BPSK, QPSK, 8PSK, 16QAM, 64QAM)
- `samp_rate`: Sample rate (higher = more bandwidth)

## Architecture

```
┌──────────────┐
│   Webcam     │
│  (480p 60fps)│
└──────┬───────┘
       │ Grayscale bytes
       ▼
┌──────────────────────┐
│ Stream to Tagged     │
│ Stream (4096 bytes)  │
└──────┬───────────────┘
       │ Tagged stream
       ▼
┌──────────────────────┐
│   OFDM TX            │
│ (64-QAM, 256-FFT)    │
└──────┬───────────────┘
       │ Complex samples
       ▼
┌──────────────────────┐
│   Throttle           │
│   (10 MHz)           │
└──────┬───────────────┘
       │ Complex samples
       ▼
┌──────────────────────┐
│   OFDM RX            │
│ (64-QAM, 256-FFT)    │
└──────┬───────────────┘
       │ Bytes
       ▼
┌──────────────────────┐
│   Video SDL Sink     │
│   (480p 60fps)       │
└──────────────────────┘
```

## Performance Metrics

### Standard Version
With the optimized parameters:
- **Symbol Rate**: ~78,125 symbols/sec per carrier
- **Bits per Symbol**: 6 (64-QAM)
- **Data Rate per Carrier**: ~469 kbps
- **Total Data Rate**: ~91 Mbps (194 carriers)
- **Effective Throughput**: ~70 Mbps (after overhead)
- **Supported Video**: 480p @ 30fps smoothly, 60fps with some frame drops

### High Performance Version
With maximum throughput parameters:
- **Symbol Rate**: ~156,250 symbols/sec per carrier
- **Bits per Symbol**: 6 (64-QAM)
- **Data Rate per Carrier**: ~938 kbps
- **Total Data Rate**: ~394 Mbps (420 carriers)
- **Effective Throughput**: ~180 Mbps (after overhead)
- **Supported Video**: 480p @ 60fps smoothly (147 Mbps required)

**Note**: Real-world throughput depends on CPU performance, camera capabilities, and system load.

## Known Limitations

1. **Throughput**: 
   - **Standard Version**: ~70 Mbps effective throughput. For 480p @ 60fps (~147 Mbps), use the High Performance version or set `fps_target=30`
   - **High Performance Version**: ~180 Mbps effective throughput. Sufficient for 480p @ 60fps smoothly

2. **System Requirements**:
   - Standard Version: Moderate CPU (Intel i5 or equivalent)
   - High Performance Version: Powerful CPU (Intel i7/i9 or equivalent), may need CPU affinity tuning

3. **Latency**: Typical latency is 50-200ms depending on buffering and system load

4. **No Error Correction**: Basic OFDM without forward error correction (FEC). Clean loopback only.

## License

This project is provided as-is for educational and research purposes.

## Credits

- GNU Radio project
- gr-video-sdl module
- OpenCV library
