#!/usr/bin/env python3
"""
Video Receiver - Continuous Smooth Streaming
Receives video stream from transmitter and displays it smoothly with minimal lag
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

class VideoReceiver:
    def __init__(self, host='127.0.0.1', port=9999, buffer_size=10):
        """
        Initialize video receiver
        
        Args:
            host: IP address of transmitter
            port: Port number of transmitter
            buffer_size: Number of frames to buffer for smooth playback
        """
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        
        self.frame_queue = queue.Queue(maxsize=buffer_size)
        self.running = False
        self.receive_thread = None
        self.display_thread = None
        
        # Statistics
        self.frames_received = 0
        self.bytes_received = 0
        self.frames_displayed = 0
        self.start_time = None
        
    def _receive_loop(self, client_socket):
        """Receive frames from transmitter in background thread"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Receive thread started")
        
        data = b""
        payload_size = struct.calcsize("Q")
        
        while self.running:
            try:
                # Receive message size
                while len(data) < payload_size:
                    packet = client_socket.recv(4096)
                    if not packet:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Connection closed by transmitter")
                        self.running = False
                        return
                    data += packet
                
                # Extract message size
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]
                
                # Receive frame data
                while len(data) < msg_size:
                    packet = client_socket.recv(4096)
                    if not packet:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Connection closed by transmitter")
                        self.running = False
                        return
                    data += packet
                
                # Extract frame data
                frame_data = data[:msg_size]
                data = data[msg_size:]
                
                # Update statistics
                self.frames_received += 1
                self.bytes_received += len(frame_data) + payload_size
                
                # Decode frame
                nparr = np.frombuffer(frame_data, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if frame is not None:
                    # Add to queue (drop old frames if queue is full for low latency)
                    if self.frame_queue.full():
                        try:
                            self.frame_queue.get_nowait()
                        except queue.Empty:
                            pass
                    
                    self.frame_queue.put(frame)
                    
                    # Print statistics every 100 frames
                    if self.frames_received % 100 == 0:
                        elapsed = time.time() - self.start_time
                        fps = self.frames_received / elapsed
                        mbps = (self.bytes_received * 8) / (elapsed * 1000000)
                        queue_size = self.frame_queue.qsize()
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                              f"Received {self.frames_received} frames, "
                              f"{fps:.1f} fps, {mbps:.2f} Mbps, "
                              f"Buffer: {queue_size}/{self.buffer_size}")
                
            except Exception as e:
                if self.running:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Error in receive loop: {e}")
                    time.sleep(0.1)
    
    def _display_loop(self):
        """Display frames in main thread or separate thread"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Display thread started")
        
        cv2.namedWindow('Video Stream - Press Q to quit', cv2.WINDOW_NORMAL)
        
        # Wait for first frames to buffer
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Buffering frames...")
        while self.frame_queue.qsize() < min(3, self.buffer_size) and self.running:
            time.sleep(0.1)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting playback")
        
        fps_update_time = time.time()
        fps_frame_count = 0
        display_fps = 0
        
        while self.running:
            try:
                # Get frame from queue
                try:
                    frame = self.frame_queue.get(timeout=1.0)
                except queue.Empty:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] No frames in buffer, waiting...")
                    continue
                
                self.frames_displayed += 1
                fps_frame_count += 1
                
                # Calculate display FPS every second
                current_time = time.time()
                if current_time - fps_update_time >= 1.0:
                    display_fps = fps_frame_count / (current_time - fps_update_time)
                    fps_update_time = current_time
                    fps_frame_count = 0
                
                # Add FPS and statistics overlay
                queue_size = self.frame_queue.qsize()
                stats_text = f"FPS: {display_fps:.1f} | Buffer: {queue_size}/{self.buffer_size} | Frames: {self.frames_displayed}"
                
                # Add semi-transparent background for text
                overlay = frame.copy()
                cv2.rectangle(overlay, (5, 5), (600, 35), (0, 0, 0), -1)
                frame = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)
                
                # Add text
                cv2.putText(frame, stats_text, (10, 25), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Display frame
                cv2.imshow('Video Stream - Press Q to quit', frame)
                
                # Check for quit key
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == ord('Q') or key == 27:  # Q or ESC
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Quit key pressed")
                    self.running = False
                    break
                
            except Exception as e:
                if self.running:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Error in display loop: {e}")
                    time.sleep(0.1)
        
        cv2.destroyAllWindows()
    
    def start(self):
        """Start video reception and display"""
        print(f"\n{'='*60}")
        print(f"Video Receiver Starting")
        print(f"{'='*60}")
        print(f"Connecting to: {self.host}:{self.port}")
        print(f"Buffer size: {self.buffer_size} frames")
        print(f"{'='*60}\n")
        
        # Connect to transmitter
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Attempting to connect to transmitter...")
        
        max_retries = 5
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                client_socket.connect((self.host, self.port))
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Connected successfully!\n")
                break
            except Exception as e:
                retry_count += 1
                if retry_count < max_retries:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Connection failed, retrying in 2 seconds... ({retry_count}/{max_retries})")
                    time.sleep(2)
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: Could not connect to {self.host}:{self.port}")
                    print(f"Error: {e}")
                    print("\nMake sure the transmitter is running first!")
                    return
        
        # Start threads
        self.running = True
        self.start_time = time.time()
        
        self.receive_thread = threading.Thread(target=self._receive_loop, args=(client_socket,), daemon=True)
        self.receive_thread.start()
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Receiver is running. Press 'Q' in video window to stop.\n")
        
        try:
            # Display frames in main thread for proper GUI handling
            self._display_loop()
        except KeyboardInterrupt:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Shutting down...")
        finally:
            self.stop()
            client_socket.close()
            
            # Print final statistics
            if self.start_time:
                elapsed = time.time() - self.start_time
                fps = self.frames_received / elapsed if elapsed > 0 else 0
                display_fps = self.frames_displayed / elapsed if elapsed > 0 else 0
                mbps = (self.bytes_received * 8) / (elapsed * 1000000) if elapsed > 0 else 0
                print(f"\n{'='*60}")
                print(f"Final Statistics:")
                print(f"  Total frames received: {self.frames_received}")
                print(f"  Total frames displayed: {self.frames_displayed}")
                print(f"  Total data received: {self.bytes_received / 1024 / 1024:.2f} MB")
                print(f"  Average receive FPS: {fps:.1f}")
                print(f"  Average display FPS: {display_fps:.1f}")
                print(f"  Average bitrate: {mbps:.2f} Mbps")
                print(f"  Total time: {elapsed:.1f} seconds")
                print(f"{'='*60}\n")
    
    def stop(self):
        """Stop video reception"""
        self.running = False
        if self.receive_thread:
            self.receive_thread.join(timeout=2)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Video Receiver - Continuous Smooth Streaming')
    parser.add_argument('--host', default='127.0.0.1', help='Transmitter host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=9999, help='Transmitter port (default: 9999)')
    parser.add_argument('--buffer', type=int, default=10, help='Buffer size in frames (default: 10)')
    
    args = parser.parse_args()
    
    receiver = VideoReceiver(
        host=args.host,
        port=args.port,
        buffer_size=args.buffer
    )
    
    receiver.start()


if __name__ == '__main__':
    main()
