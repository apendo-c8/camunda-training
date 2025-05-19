import os
from dotenv import load_dotenv

# Load environment variables from .env located two levels up
ENV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "bruno", "training-collection", ".env")
)
load_dotenv(dotenv_path=ENV_PATH)

# Read credentials
ZEEBE_CLIENT_ID = os.getenv("ZEEBE_CLIENT_ID")
ZEEBE_CLIENT_SECRET = os.getenv("ZEEBE_CLIENT_SECRET")
CAMUNDA_CLUSTER_ID = os.getenv("CAMUNDA_CLUSTER_ID")
CAMUNDA_CLUSTER_REGION = os.getenv("CAMUNDA_CLUSTER_REGION", "bru-2")

if not all([ZEEBE_CLIENT_ID, ZEEBE_CLIENT_SECRET, CAMUNDA_CLUSTER_ID]):
    raise EnvironmentError("❌ Missing required environment variables")

def main():
    import asyncio
    from pyzeebe import (
        Job,
        ZeebeWorker,
        create_camunda_cloud_channel,
    )
    from pyzeebe.job.job import JobController

    async def run_worker():
        channel = create_camunda_cloud_channel(
            client_id=ZEEBE_CLIENT_ID,
            client_secret=ZEEBE_CLIENT_SECRET,
            cluster_id=CAMUNDA_CLUSTER_ID,
            region=CAMUNDA_CLUSTER_REGION
        )

        worker = ZeebeWorker(channel)

        async def worker_exception_handler(exception: Exception, job: Job, job_controller: JobController) -> None:
            retries_remaining = job.retries - 1
            attempt = 3 - retries_remaining  # assumes 3 retries total; adjust if needed
            retry_backoff = min(2 ** attempt * 1000, 30000)  # cap at 30s

            print(f"⚠️ Exception caught: {exception}")
            print(f"🔁 Remaining retries: {retries_remaining}")
            print(f"⏳ Setting backoff to {retry_backoff} ms")

            await job_controller.set_failure_status(
                message=f"Simulated backend failure: {exception}",
                retry_back_off_ms=retry_backoff
            )

        @worker.task(task_type="model_uploading", exception_handler=worker_exception_handler)
        async def upload_model(job: Job):
            model_id = job.variables.get("modelId", "unknown")
            print(f"\n📦 Simulating backend upload for modelId: {model_id}")
            print(f"🔁 Zeebe-reported retries remaining: {job.retries}")
            raise Exception("Backend is offline.")

        print("🚀 Model Uploading worker (offline) is running... Press Ctrl+C to stop.")
        await worker.work()

    try:
        asyncio.run(run_worker())
    except KeyboardInterrupt:
        print("\n👋 Model Uploading worker (offline) stopped by user. Goodbye!")

if __name__ == "__main__":
    main()