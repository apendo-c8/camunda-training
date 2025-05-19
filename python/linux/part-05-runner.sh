#!/bin/bash

echo "🚀 Starting all workers..."

# Kill all background jobs on Ctrl+C
trap "echo '🛑 Stopping all workers...'; kill 0" SIGINT

python ../workers/model-uploading-online.py &
python ../workers/image-enhancement.py &
python ../workers/thumbnails-production.py &
python ../workers/asset-storage.py &

wait