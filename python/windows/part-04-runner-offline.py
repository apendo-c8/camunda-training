import subprocess
import signal
import sys

print("🚀 Starting all workers...")

# Define all worker scripts
worker_scripts = [
    "../workers/image-enhancement.py",
    "../workers/model-uploading-offline.py",
    "../workers/thumbnails-production.py"
]

# Start all workers
processes = [subprocess.Popen(["python", script]) for script in worker_scripts]

def shutdown(sig, frame):
    print("\n🛑 Stopping all workers...")
    for proc in processes:
        proc.terminate()
    for proc in processes:
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    sys.exit(0)

# Register signal handler for graceful shutdown
signal.signal(signal.SIGINT, shutdown)

# Wait for all workers to finish
for proc in processes:
    proc.wait()