import subprocess
import signal
import sys
import os

print("🚀 Starting all workers...")

# Start the worker as a subprocess
worker_process = subprocess.Popen(["python", "../workers/model-uploading-online.py"])

def shutdown(sig, frame):
    print("\n🛑 Stopping all workers...")
    worker_process.terminate()
    try:
        worker_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        worker_process.kill()
    sys.exit(0)

# Handle Ctrl+C
signal.signal(signal.SIGINT, shutdown)

# Wait for the process to complete
worker_process.wait()