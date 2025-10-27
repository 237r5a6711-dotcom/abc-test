#!/usr/bin/env python3
"""
Video Transmitter - Continuous Smooth Streaming
Captures video from webcam and transmits it over network with minimal lag
"""

import cv2
import socket
import pickle
import struct
import threading
import time
import queue
import numpy as np
from datetime import datetime

class VideoTransmitter:
    def __init__(self, host='0.0.0.0', port=9999, camera_index=0, 
                 width=640, height=480, fps=30, quality=80):
        """
        Initialize video transmitter
        
        Args:
            host: IP address to bind to (0.0.0.0 for all interfaces)
            port: Port number to bind to
            camera_index: Camera device index
            width: Video width
            height: Video height
            fps: Target frames per second
            quality: JPEG compression quality (1-100, higher is better)
        """
        self.host = host
        self.port = port
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.fps = fps
        self.quality = quality
        
        self.frame_queue = queue.Queue(maxsize=30)
        self.running = False
        self.capture_thread = None
        self.transmit_thread = None
        
        # Statistics
        self.frames_sent = 0
        self.bytes_sent = 0
        self.start_time = None
        
    def _capture_loop(self, cap):
        """Capture frames from camera in background thread"""
        frame_interval = 1.0 / self.fps
        next_frame_time = time.time()
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Capture thread started")
        
        while self.running:
            try:
                current_time = time.time()
                
                # Read frame from camera
                ret, frame = cap.read()
                if not ret:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed to read frame from camera")
                    time.sleep(0.1)
                    continue
                
                # Resize frame
                frame = cv2.resize(frame, (self.width, self.height))
                
                # Encode frame as JPEG for compression
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.quality]
                result, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
                
                if not result:
                    continue
                
                # Add to queue (drop old frames if queue is full)
                if self.frame_queue.full():
                    try:
                        self.frame_queue.get_nowait()
                    except queue.Empty:
                        pass
                
                self.frame_queue.put(encoded_frame.tobytes())
                
                # Wait for next frame time to maintain target FPS
                next_frame_time += frame_interval
                sleep_time = next_frame_time - time.time()
                if sleep_time > 0:
                    time.sleep(sleep_time)
                else:
                    # Catch up if we're running behind
                    next_frame_time = time.time()
                    
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Error in capture loop: {e}")
                time.sleep(0.1)
    
    def _transmit_loop(self, server_socket):
        """Transmit frames to connected clients"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Waiting for client connection...")
        
        while self.running:
            try:
                # Accept client connection
                client_socket, addr = server_socket.accept()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Client connected from {addr}")
                
                try:
                    while self.running:
                        # Get frame from queue
                        try:
                            frame_data = self.frame_queue.get(timeout=1.0)
                        except queue.Empty:
                            continue
                        
                        # Serialize frame data with size header
                        message = struct.pack("Q", len(frame_data)) + frame_data
                        
                        # Send data
                        try:
                            client_socket.sendall(message)
                            self.frames_sent += 1
                            self.bytes_sent += len(message)
                            
                            # Print statistics every 100 frames
                            if self.frames_sent % 100 == 0:
                                elapsed = time.time() - self.start_time
                                fps = self.frames_sent / elapsed
                                mbps = (self.bytes_sent * 8) / (elapsed * 1000000)
                                print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                                      f"Sent {self.frames_sent} frames, "
                                      f"{fps:.1f} fps, {mbps:.2f} Mbps")
                        except (BrokenPipeError, ConnectionResetError):
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] Client disconnected")
                            break
                            
                except Exception as e:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Error transmitting to client: {e}")
                finally:
                    client_socket.close()
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Connection closed, waiting for new client...")
                    
            except Exception as e:
                if self.running:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Error accepting connection: {e}")
                    time.sleep(1)
    
    def start(self):
        """Start video transmission"""
        print(f"\n{'='*60}")
        print(f"Video Transmitter Starting")
        print(f"{'='*60}")
        print(f"Camera Index: {self.camera_index}")
        print(f"Resolution: {self.width}x{self.height}")
        print(f"Target FPS: {self.fps}")
        print(f"Quality: {self.quality}%")
        print(f"Listening on: {self.host}:{self.port}")
        print(f"{'='*60}\n")
        
        # Open camera
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: Could not open camera {self.camera_index}")
            print("Available cameras:")
            for i in range(5):
                test_cap = cv2.VideoCapture(i)
                if test_cap.isOpened():
                    print(f"  - Camera {i} is available")
                    test_cap.release()
            return
        
        # Configure camera
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        cap.set(cv2.CAP_PROP_FPS, self.fps)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        # Try to use MJPEG mode for better performance
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        
        actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        actual_fps = cap.get(cv2.CAP_PROP_FPS)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Camera opened successfully")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Actual resolution: {actual_width}x{actual_height}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Actual FPS: {actual_fps}")
        
        # Create server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Server socket bound and listening\n")
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: Could not bind to {self.host}:{self.port}")
            print(f"Error: {e}")
            cap.release()
            return
        
        # Start threads
        self.running = True
        self.start_time = time.time()
        
        self.capture_thread = threading.Thread(target=self._capture_loop, args=(cap,), daemon=True)
        self.transmit_thread = threading.Thread(target=self._transmit_loop, args=(server_socket,), daemon=True)
        
        self.capture_thread.start()
        self.transmit_thread.start()
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Transmitter is running. Press Ctrl+C to stop.\n")
        
        try:
            # Keep main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Shutting down...")
        finally:
            self.stop()
            cap.release()
            server_socket.close()
            
            # Print final statistics
            if self.start_time:
                elapsed = time.time() - self.start_time
                fps = self.frames_sent / elapsed if elapsed > 0 else 0
                mbps = (self.bytes_sent * 8) / (elapsed * 1000000) if elapsed > 0 else 0
                print(f"\n{'='*60}")
                print(f"Final Statistics:")
                print(f"  Total frames sent: {self.frames_sent}")
                print(f"  Total data sent: {self.bytes_sent / 1024 / 1024:.2f} MB")
                print(f"  Average FPS: {fps:.1f}")
                print(f"  Average bitrate: {mbps:.2f} Mbps")
                print(f"  Total time: {elapsed:.1f} seconds")
                print(f"{'='*60}\n")
    
    def stop(self):
        """Stop video transmission"""
        self.running = False
        if self.capture_thread:
            self.capture_thread.join(timeout=2)
        if self.transmit_thread:
            self.transmit_thread.join(timeout=2)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Video Transmitter - Continuous Smooth Streaming')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=9999, help='Port to bind to (default: 9999)')
    parser.add_argument('--camera', type=int, default=0, help='Camera index (default: 0)')
    parser.add_argument('--width', type=int, default=640, help='Video width (default: 640)')
    parser.add_argument('--height', type=int, default=480, help='Video height (default: 480)')
    parser.add_argument('--fps', type=int, default=30, help='Target FPS (default: 30)')
    parser.add_argument('--quality', type=int, default=80, help='JPEG quality 1-100 (default: 80)')
    
    args = parser.parse_args()
    
    transmitter = VideoTransmitter(
        host=args.host,
        port=args.port,
        camera_index=args.camera,
        width=args.width,
        height=args.height,
        fps=args.fps,
        quality=args.quality
    )
    
    transmitter.start()


if __name__ == '__main__':
    main()
