import os
import asyncio
from dotenv import load_dotenv
from pyzeebe import ZeebeWorker, create_camunda_cloud_channel
from pyzeebe.job.job import Job

# Load environment variables
ENV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "bruno", "training-collection", ".env")
)
print(f"📥 Loading environment from: {ENV_PATH}")
load_dotenv(dotenv_path=ENV_PATH)

ZEEBE_CLIENT_ID = os.getenv("ZEEBE_CLIENT_ID")
ZEEBE_CLIENT_SECRET = os.getenv("ZEEBE_CLIENT_SECRET")
CAMUNDA_CLUSTER_ID = os.getenv("CAMUNDA_CLUSTER_ID")
CAMUNDA_CLUSTER_REGION = os.getenv("CAMUNDA_CLUSTER_REGION", "bru-2")

if not all([ZEEBE_CLIENT_ID, ZEEBE_CLIENT_SECRET, CAMUNDA_CLUSTER_ID]):
    raise EnvironmentError("❌ Missing required environment variables")

def main():
    async def run():
        channel = create_camunda_cloud_channel(
            client_id=ZEEBE_CLIENT_ID,
            client_secret=ZEEBE_CLIENT_SECRET,
            cluster_id=CAMUNDA_CLUSTER_ID,
            region=CAMUNDA_CLUSTER_REGION
        )
        worker = ZeebeWorker(channel)

        @worker.task(task_type="thumbnails_production")
        async def produce_thumbnails(job: Job):
            image_id = job.variables.get("imageId", "unknown")
            rendering_quality = job.variables.get("imageRenderingQuality", 0)
            enhancement_quality = job.variables.get("imageEnhancementQuality", 0)
            number_of_thumbnails = job.variables.get("numberOfThumbnails", 3)

            print(f"🖼️ Processing image: {image_id}")
            print(f"🔍 Rendering: {rendering_quality}, Enhancement: {enhancement_quality}, Thumbnails: {number_of_thumbnails}")

            # TODO: Throw a business error with error code 'thumbnail-production-error'

            thumbnail_ids = [f"tid-{i}" for i in range(1, number_of_thumbnails + 1)]
            print(f"✅ Created thumbnail IDs: {thumbnail_ids}")
            return {"thumbnailIds": thumbnail_ids}

        print("🚀 Worker is running... Press Ctrl+C to stop.")
        await worker.work()

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\n👋 Worker stopped by user.")

if __name__ == "__main__":
    main()