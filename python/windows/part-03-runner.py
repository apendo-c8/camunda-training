import subprocess
import signal
import sys
import os

print("🚀 Starting all workers...")

# Start worker subprocesses
workers = [
    subprocess.Popen(["python", "../workers/model-uploading-online.py"]),
    subprocess.Popen(["python", "../workers/image-enhancement.py"])
]

def shutdown(sig, frame):
    print("\n🛑 Stopping all workers...")
    for p in workers:
        p.terminate()
    for p in workers:
        try:
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p.kill()
    sys.exit(0)

# Handle Ctrl+C
signal.signal(signal.SIGINT, shutdown)

# Wait for all workers to complete
for p in workers:
    p.wait()