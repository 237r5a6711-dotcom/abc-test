# Video Streaming Solution - Smooth & Lag-Free

A complete, production-ready video streaming system for real-time transmission over network with minimal lag.

## 🚀 Features

- ✅ **Real-time streaming** with minimal latency (50-200ms)
- ✅ **Smooth playback** with intelligent buffering
- ✅ **Continuous transmission** without interruptions
- ✅ **High quality** video with adjustable compression
- ✅ **Network efficient** with JPEG compression
- ✅ **Easy to use** - just run transmitter and receiver
- ✅ **Robust** - handles network issues gracefully
- ✅ **Monitoring** - real-time FPS and bandwidth statistics

## 📋 Requirements

### Software
- Python 3.6 or higher
- OpenCV (opencv-python)
- NumPy

### Installation

```bash
# Install required packages
python -m pip install opencv-python numpy

# Or using the requirements file
python -m pip install -r requirements.txt
```

### Hardware
- Webcam (for transmitter)
- Network connection between transmitter and receiver

## 🎯 Quick Start

### Step 1: Start the Transmitter

On the computer with the webcam:

```bash
# Navigate to the solution folder
cd video_streaming_solution

# Run the transmitter (default settings: 640x480 @ 30fps)
python transmitter.py

# Or with custom settings
python transmitter.py --width 1280 --height 720 --fps 60 --quality 90
```

The transmitter will:
1. Open your default webcam
2. Start capturing video
3. Wait for receiver to connect
4. Stream video continuously

### Step 2: Start the Receiver

On the computer where you want to view the video:

```bash
# Same computer (for testing)
python receiver.py

# Different computer (replace with transmitter's IP)
python receiver.py --host 192.168.1.100

# With larger buffer for slower networks
python receiver.py --host 192.168.1.100 --buffer 20
```

The receiver will:
1. Connect to the transmitter
2. Buffer initial frames
3. Display video smoothly
4. Show FPS and buffer statistics

Press **Q** or **ESC** in the video window to stop the receiver.
Press **Ctrl+C** in the terminal to stop the transmitter.

## 📖 Usage Examples

### Example 1: Local Testing (Same Computer)

```bash
# Terminal 1 - Start transmitter
python transmitter.py

# Terminal 2 - Start receiver
python receiver.py
```

### Example 2: Network Streaming

```bash
# Transmitter computer (IP: 192.168.1.100)
python transmitter.py --host 0.0.0.0 --port 9999

# Receiver computer
python receiver.py --host 192.168.1.100 --port 9999
```

### Example 3: High Quality HD Streaming

```bash
# Transmitter - HD quality
python transmitter.py --width 1280 --height 720 --fps 30 --quality 95

# Receiver - larger buffer for HD
python receiver.py --buffer 15
```

### Example 4: High Frame Rate

```bash
# Transmitter - 60 FPS
python transmitter.py --fps 60 --quality 80

# Receiver
python receiver.py --buffer 20
```

### Example 5: Low Bandwidth Network

```bash
# Transmitter - lower quality for slow network
python transmitter.py --width 480 --height 360 --fps 20 --quality 60

# Receiver - smaller buffer
python receiver.py --buffer 5
```

## ⚙️ Configuration Options

### Transmitter Options

```bash
python transmitter.py [OPTIONS]

Options:
  --host HOST        IP address to bind to (default: 0.0.0.0)
                     Use 0.0.0.0 to accept connections from any IP
  --port PORT        Port number to bind to (default: 9999)
  --camera INDEX     Camera device index (default: 0)
                     Try 1, 2, etc. if camera 0 doesn't work
  --width WIDTH      Video width in pixels (default: 640)
  --height HEIGHT    Video height in pixels (default: 480)
  --fps FPS          Target frames per second (default: 30)
  --quality QUALITY  JPEG compression quality 1-100 (default: 80)
                     Higher = better quality but more bandwidth
```

### Receiver Options

```bash
python receiver.py [OPTIONS]

Options:
  --host HOST        Transmitter IP address (default: 127.0.0.1)
                     Use 127.0.0.1 for same computer
                     Use actual IP for network streaming
  --port PORT        Transmitter port number (default: 9999)
  --buffer SIZE      Buffer size in frames (default: 10)
                     Larger buffer = smoother but more delay
                     Smaller buffer = less delay but may stutter
```

## 📊 Performance Guide

### Recommended Settings by Use Case

#### Use Case 1: Same Computer (Testing)
```bash
# Transmitter
python transmitter.py --fps 30 --quality 80

# Receiver  
python receiver.py --buffer 5
```
- Expected: 30 FPS, 50-100ms latency
- Bandwidth: ~2-5 Mbps

#### Use Case 2: Local Network (LAN)
```bash
# Transmitter
python transmitter.py --width 1280 --height 720 --fps 30 --quality 85

# Receiver
python receiver.py --host <transmitter_ip> --buffer 10
```
- Expected: 30 FPS, 100-200ms latency
- Bandwidth: ~5-10 Mbps

#### Use Case 3: Slow Network (WiFi/Mobile)
```bash
# Transmitter
python transmitter.py --width 480 --height 360 --fps 15 --quality 60

# Receiver
python receiver.py --host <transmitter_ip> --buffer 5
```
- Expected: 15 FPS, 200-500ms latency
- Bandwidth: ~0.5-2 Mbps

#### Use Case 4: High Quality/Performance
```bash
# Transmitter
python transmitter.py --width 1920 --height 1080 --fps 60 --quality 90

# Receiver
python receiver.py --host <transmitter_ip> --buffer 20
```
- Expected: 60 FPS, 100-300ms latency
- Bandwidth: ~20-40 Mbps

### Bandwidth Calculation

Approximate bandwidth per quality setting:

| Resolution | FPS | Quality | Bandwidth |
|-----------|-----|---------|-----------|
| 640x480   | 30  | 80      | 2-5 Mbps  |
| 1280x720  | 30  | 80      | 5-10 Mbps |
| 1920x1080 | 30  | 80      | 10-20 Mbps|
| 640x480   | 60  | 80      | 4-10 Mbps |
| 1280x720  | 60  | 80      | 10-20 Mbps|

## 🔧 Troubleshooting

### Camera Not Found

**Problem**: `ERROR: Could not open camera 0`

**Solution**:
```bash
# List available cameras
python -c "import cv2; [print(f'Camera {i}') for i in range(10) if cv2.VideoCapture(i).isOpened()]"

# Try different camera index
python transmitter.py --camera 1
```

### Connection Failed

**Problem**: `ERROR: Could not connect to transmitter`

**Solutions**:
1. Make sure transmitter is running first
2. Check firewall settings (allow port 9999)
3. Verify IP address is correct
4. Try pinging the transmitter computer

```bash
# Check if port is open
telnet <transmitter_ip> 9999

# On Linux, check firewall
sudo ufw status
sudo ufw allow 9999/tcp
```

### Choppy/Laggy Video

**Problem**: Video playback is not smooth

**Solutions**:

1. **Increase buffer size** (more smoothness, more delay):
   ```bash
   python receiver.py --buffer 20
   ```

2. **Reduce resolution**:
   ```bash
   python transmitter.py --width 480 --height 360
   ```

3. **Reduce frame rate**:
   ```bash
   python transmitter.py --fps 20
   ```

4. **Lower quality** (less bandwidth):
   ```bash
   python transmitter.py --quality 60
   ```

5. **Check network bandwidth**:
   ```bash
   # Monitor bandwidth usage
   iftop  # Linux
   ```

### High CPU Usage

**Problem**: Transmitter or receiver using too much CPU

**Solutions**:

1. **Reduce FPS**:
   ```bash
   python transmitter.py --fps 20
   ```

2. **Reduce resolution**:
   ```bash
   python transmitter.py --width 480 --height 360
   ```

3. **Lower quality**:
   ```bash
   python transmitter.py --quality 70
   ```

### Video Quality Issues

**Problem**: Video looks pixelated or blocky

**Solutions**:

1. **Increase quality**:
   ```bash
   python transmitter.py --quality 95
   ```

2. **Increase resolution** (if bandwidth allows):
   ```bash
   python transmitter.py --width 1280 --height 720
   ```

## 🌐 Network Setup Guide

### Same Computer
- Use default settings
- Transmitter: `python transmitter.py`
- Receiver: `python receiver.py`

### Local Network (LAN)
1. Find transmitter computer's IP:
   ```bash
   # Linux/Mac
   ifconfig | grep "inet "
   
   # Windows
   ipconfig
   ```

2. Start transmitter:
   ```bash
   python transmitter.py --host 0.0.0.0
   ```

3. Start receiver with transmitter's IP:
   ```bash
   python receiver.py --host 192.168.1.100
   ```

### Different Networks (Internet)
1. **Port forwarding** on transmitter's router:
   - Forward external port 9999 to transmitter's local IP
   
2. Find external IP:
   ```bash
   curl ifconfig.me
   ```

3. Start transmitter:
   ```bash
   python transmitter.py --host 0.0.0.0
   ```

4. Start receiver with external IP:
   ```bash
   python receiver.py --host <external_ip>
   ```

## 📈 Monitoring and Statistics

Both transmitter and receiver display real-time statistics:

### Transmitter Statistics
- Frames sent
- Current FPS
- Bandwidth (Mbps)
- Updates every 100 frames

### Receiver Statistics  
- Frames received and displayed
- Current FPS
- Bandwidth (Mbps)
- Buffer usage
- On-screen overlay showing FPS and buffer

## 🔐 Security Notes

- This is designed for trusted networks
- No encryption by default
- For production use, consider:
  - Adding SSL/TLS encryption
  - Authentication mechanisms
  - Rate limiting

## 🎓 Technical Details

### Architecture

```
┌──────────────┐                    ┌──────────────┐
│ TRANSMITTER  │                    │   RECEIVER   │
├──────────────┤                    ├──────────────┤
│   Webcam     │                    │              │
│      ↓       │                    │              │
│  Capture     │                    │              │
│   Thread     │                    │   Receive    │
│      ↓       │                    │    Thread    │
│   Frame      │    TCP Socket      │      ↓       │
│   Queue      │  ─────────────→    │    Frame     │
│      ↓       │   (JPEG data)      │    Queue     │
│  Transmit    │                    │      ↓       │
│   Thread     │                    │   Display    │
│              │                    │    Thread    │
└──────────────┘                    └──────────────┘
```

### Key Features

1. **Multi-threaded Architecture**
   - Separate threads for capture, transmit, receive, and display
   - Prevents blocking and ensures smooth operation

2. **Intelligent Buffering**
   - Queue-based frame management
   - Drops old frames when queue is full (low latency)
   - Configurable buffer size for different network conditions

3. **JPEG Compression**
   - Reduces bandwidth by 10-20x compared to raw frames
   - Adjustable quality/bandwidth tradeoff
   - Fast encoding/decoding with OpenCV

4. **Network Protocol**
   - TCP for reliable transmission
   - Size header + data format
   - Handles partial packet reception

5. **Timing Control**
   - Precise FPS control on transmitter side
   - Frame rate limiting to prevent overload
   - Adaptive timing for consistent frame rate

## 📝 License

This code is provided as-is for educational and production use.

## 🤝 Support

If you encounter issues:

1. Check the troubleshooting section
2. Verify all requirements are installed
3. Test with default settings first
4. Check network connectivity
5. Review console output for error messages

## 🎉 Success Checklist

- [ ] Python 3.6+ installed
- [ ] OpenCV and NumPy installed
- [ ] Webcam connected and working
- [ ] Transmitter starts without errors
- [ ] Receiver connects successfully
- [ ] Video displays smoothly
- [ ] FPS is stable
- [ ] No lag or stuttering

If all boxes are checked, congratulations! Your video streaming system is working perfectly! 🎊
