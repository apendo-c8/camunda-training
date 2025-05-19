import os
from dotenv import load_dotenv

# Load environment variables from .env located two levels up
ENV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "bruno", "training-collection", ".env")
)
print(f"📥 Loading environment from: {ENV_PATH}")
load_dotenv(dotenv_path=ENV_PATH)

# Read required credentials
ZEEBE_CLIENT_ID = os.getenv("ZEEBE_CLIENT_ID")
ZEEBE_CLIENT_SECRET = os.getenv("ZEEBE_CLIENT_SECRET")
CAMUNDA_CLUSTER_ID = os.getenv("CAMUNDA_CLUSTER_ID")
CAMUNDA_CLUSTER_REGION = os.getenv("CAMUNDA_CLUSTER_REGION", "bru-2")

# Validate
if not all([ZEEBE_CLIENT_ID, ZEEBE_CLIENT_SECRET, CAMUNDA_CLUSTER_ID]):
    raise EnvironmentError("❌ Missing required environment variables")

def main():
    import asyncio
    from pyzeebe import ZeebeWorker, create_camunda_cloud_channel
    from pyzeebe.job.job import Job

    async def run_worker():
        channel = create_camunda_cloud_channel(
            client_id=ZEEBE_CLIENT_ID,
            client_secret=ZEEBE_CLIENT_SECRET,
            cluster_id=CAMUNDA_CLUSTER_ID,
            region=CAMUNDA_CLUSTER_REGION
        )

        worker = ZeebeWorker(channel)

        @worker.task(task_type="image_enhancement")
        async def enhance_image(job: Job):
            image_id = job.variables.get("imageIdentity", "unknown")
            quality = job.variables.get("imageRenderingQuality", 0)

            print(f"\n📸 Enhancing image: {image_id}")
            print(f"🔍 Original quality: {quality}")

            enhanced_quality = min(quality + 0.2, 1.0)
            print(f"✅ Enhanced quality: {enhanced_quality}")

            return {"imageEnhancementQuality": enhanced_quality}

        print("🚀 Worker is running... Press Ctrl+C to stop.")
        await worker.work()

    try:
        asyncio.run(run_worker())
    except KeyboardInterrupt:
        print("\n👋 Worker stopped by user. Goodbye!")

if __name__ == "__main__":
    main()