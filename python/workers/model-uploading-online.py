import os
import re
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

if not all([ZEEBE_CLIENT_ID, ZEEBE_CLIENT_SECRET, CAMUNDA_CLUSTER_ID]):
    raise EnvironmentError("❌ Missing required environment variables")

def main():
    import asyncio
    from pyzeebe import ZeebeWorker, create_camunda_cloud_channel
    from pyzeebe.job.job import Job, JobController

    async def run_worker():
        channel = create_camunda_cloud_channel(
            client_id=ZEEBE_CLIENT_ID,
            client_secret=ZEEBE_CLIENT_SECRET,
            cluster_id=CAMUNDA_CLUSTER_ID,
            region=CAMUNDA_CLUSTER_REGION
        )

        worker = ZeebeWorker(channel)

        async def worker_exception_handler(exception: Exception, job: Job, job_controller: JobController) -> None:
            print(f"⚠️ Exception caught: {exception}")
            await job_controller.set_failure_status(f"Failed to run task {job.type}. Reason: {exception}")

        @worker.task(task_type="model_uploading", exception_handler=worker_exception_handler)
        async def upload_model(job: Job):
            model_id = job.variables.get("modelId", "")
            print(f"\n📦 Received modelId: {model_id}")

            if not re.fullmatch(r"mid-\d+", model_id):
                print("❌ Invalid modelId format! Expected: mid-<number>")
                raise Exception("Invalid modelId format. Expected: mid-<number>")

            print(f"✅ Model with modelId '{model_id}' was successfully uploaded.")
            return {}

        print("🚀 Model Uploading worker (online) is running... Press Ctrl+C to stop.")
        await worker.work()

    try:
        asyncio.run(run_worker())
    except KeyboardInterrupt:
        print("\n👋 Model Uploading worker (online) stopped by user. Goodbye!")

if __name__ == "__main__":
    main()