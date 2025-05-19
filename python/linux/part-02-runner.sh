#!/bin/bash

echo "🚀 Starting all workers..."

# Kill all background jobs on Ctrl+C
trap "echo '🛑 Stopping all workers...'; kill 0" SIGINT

python ../workers/model-uploading-online.py &

wait