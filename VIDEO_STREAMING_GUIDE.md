# Video Streaming Solution Guide

This repository contains two different video transmission implementations:

## 🆕 **NEW: Standalone Video Streaming Solution (RECOMMENDED)**

**Location:** `video_streaming_solution/`

A complete, production-ready Python implementation that works out-of-the-box without any special software requirements.

### ✨ Key Features:
- ✅ **Works immediately** - No GNU Radio installation needed
- ✅ **Smooth streaming** - Optimized for minimal lag
- ✅ **Easy to use** - Just run transmitter and receiver
- ✅ **Network ready** - Stream over LAN or internet
- ✅ **Well documented** - Comprehensive guides included
- ✅ **Cross-platform** - Works on Windows, Linux, Mac

### 🚀 Quick Start:
```bash
cd video_streaming_solution
python -m pip install -r requirements.txt
python transmitter.py  # Terminal 1
python receiver.py     # Terminal 2
```

**[👉 Go to Video Streaming Solution →](video_streaming_solution/)**

---

## 🔧 GNU Radio OFDM Implementation (Advanced)

**Files:** `ofdm_video_480p_60fps.grc` and `ofdm_video_480p_60fps_hiperf.grc`

Advanced implementation using GNU Radio Companion for OFDM-based video transmission.

### Requirements:
- GNU Radio 3.8 or 3.10
- gr-video-sdl module
- OpenCV Python

### Usage:
```bash
gnuradio-companion ofdm_video_480p_60fps.grc
```

**Note:** This requires GNU Radio software installation and is more complex to set up. For most users, the standalone solution above is recommended.

---

## 📖 Documentation

### Standalone Solution (Recommended)
- [README](video_streaming_solution/README.md) - Complete guide with examples
- [Requirements](video_streaming_solution/requirements.txt) - Dependencies

### GNU Radio Implementation
- [README](README.md) - OFDM implementation details
- [QUICKSTART](QUICKSTART.md) - GNU Radio setup guide
- [TECHNICAL_COMPARISON](TECHNICAL_COMPARISON.md) - Version comparison
- [ARCHITECTURE](ARCHITECTURE.md) - System architecture
- [TESTING](TESTING.md) - Testing procedures

---

## 🎯 Which Solution Should I Use?

### Use the **Standalone Solution** if:
- ✅ You want something that just works
- ✅ You don't have GNU Radio installed
- ✅ You need network streaming over LAN/internet
- ✅ You want simple, production-ready code
- ✅ You're new to video streaming

### Use the **GNU Radio OFDM** if:
- 🔧 You already have GNU Radio installed
- 🔧 You're learning about OFDM modulation
- 🔧 You need RF transmission (with USRP hardware)
- 🔧 You're working on a research project
- 🔧 You need specific OFDM parameters

---

## 🆘 Getting Help

### For Standalone Solution:
1. Check [video_streaming_solution/README.md](video_streaming_solution/README.md)
2. Run the test script: `python video_streaming_solution/test_system.py`
3. Review troubleshooting section in README

### For GNU Radio Implementation:
1. Check [QUICKSTART.md](QUICKSTART.md)
2. Review [TESTING.md](TESTING.md)
3. Ensure GNU Radio and gr-video-sdl are installed

---

## 📋 Comparison

| Feature | Standalone Solution | GNU Radio OFDM |
|---------|-------------------|----------------|
| Setup Complexity | ⭐ Easy | ⭐⭐⭐⭐ Complex |
| Dependencies | Python + OpenCV | GNU Radio + more |
| Installation Time | ~2 minutes | ~30 minutes |
| Network Streaming | ✅ Yes (TCP/IP) | ⚠️ Loopback only* |
| Learning Curve | ⭐ Beginner-friendly | ⭐⭐⭐⭐ Advanced |
| Production Ready | ✅ Yes | ⚠️ Research/Educational |
| Documentation | ✅ Comprehensive | ✅ Comprehensive |
| Platform Support | Windows, Linux, Mac | Linux primarily |

*GNU Radio version requires USRP hardware for real RF transmission

---

## 🚀 Get Started Now!

**Recommended path for most users:**

1. Go to the standalone solution:
   ```bash
   cd video_streaming_solution
   ```

2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. Run the test script:
   ```bash
   python test_system.py
   ```

4. Start streaming:
   ```bash
   # Terminal 1
   python transmitter.py
   
   # Terminal 2
   python receiver.py
   ```

**That's it! You should see smooth video streaming! 🎉**

---

## 📄 License

This project is provided as-is for educational and production use.

## 🙏 Credits

- OpenCV library for video processing
- NumPy for efficient array operations
- GNU Radio project for OFDM implementation
- gr-video-sdl module for video display
