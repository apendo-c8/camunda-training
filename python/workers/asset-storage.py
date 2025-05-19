import os
from dotenv import load_dotenv

# Load environment variables from .env located two levels up
ENV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "bruno", "training-collection", ".env")
)
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

        @worker.task(task_type="asset_storage")
        async def store_asset(job: Job):
            image_id = job.variables.get("imageId", "unknown")
            print(f"\n💾 Received asset: {image_id}")

            # Simulate storing the asset and generating an ID
            asset_id = image_id
            print(f"📦 Stored asset as: {asset_id}")

            return {"assetId": asset_id}

        print("🚀 Asset Storage worker is running... Press Ctrl+C to stop.")
        await worker.work()

    try:
        asyncio.run(run_worker())
    except KeyboardInterrupt:
        print("\n👋 Asset Storage worker stopped by user. Goodbye!")

if __name__ == "__main__":
    main()