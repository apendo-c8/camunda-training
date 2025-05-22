import os # os is used to manage environment variables and file paths.
import re # Regular expressions are used to validate the modelId format.
from dotenv import load_dotenv # dotenv is used to load environment variables from a .env file.

# Camunda 8 SaaS requires authentication using client credentials and cluster information.

# In development, .env files are convenient for managing environment variables locally.
# In production, use secure systems like AWS Secrets Manager, Azure Key Vault, Kubernetes Secrets
# to inject these variables into the runtime environment.

ENV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "bruno", "training-collection", ".env")
)
load_dotenv(dotenv_path=ENV_PATH)

# These environment variables map directly to Zeebe's connection parameters.
# The client_id and client_secret authenticate the client; the cluster_id and region define the target cluster.
ZEEBE_CLIENT_ID = os.getenv("ZEEBE_CLIENT_ID")
ZEEBE_CLIENT_SECRET = os.getenv("ZEEBE_CLIENT_SECRET")
CAMUNDA_CLUSTER_ID = os.getenv("CAMUNDA_CLUSTER_ID")
CAMUNDA_CLUSTER_REGION = os.getenv("CAMUNDA_CLUSTER_REGION", "bru-2")  # default region for Camunda Cloud

# Without credentials, the worker cannot connect to Camunda Cloud and must fail fast.
if not all([ZEEBE_CLIENT_ID, ZEEBE_CLIENT_SECRET, CAMUNDA_CLUSTER_ID]):
    raise EnvironmentError("❌ Missing required environment variables")

# A worker is an external service that polls Zeebe for available jobs of specific types and performs their business logic.
def main():
    import asyncio
    from pyzeebe import (
        Job,
        ZeebeWorker,
        create_camunda_cloud_channel,
    )
    from pyzeebe.job.job import JobController

    # Job workers fetch jobs using a long-polling mechanism and handle them concurrently.
    async def run_worker():
        # Pyzeebe provides helper methods like create_camunda_cloud_channel to simplify gRPC authentication.
        channel = create_camunda_cloud_channel(
            client_id=ZEEBE_CLIENT_ID,
            client_secret=ZEEBE_CLIENT_SECRET,
            cluster_id=CAMUNDA_CLUSTER_ID,
            region=CAMUNDA_CLUSTER_REGION
        )

        # The ZeebeWorker object encapsulates polling, activation, and job execution behavior.
        worker = ZeebeWorker(channel)

        # When a worker fails a job, it can report the failure and request a retry.
        # Zeebe will retry the job according to the remaining retry count.
        # This custom handler logs the exception and signals a failure to Zeebe with a message.
        async def worker_exception_handler(exception: Exception, job: Job, job_controller: JobController) -> None:
            retries_remaining = job.retries - 1
            attempt = 3 - retries_remaining  # Assuming default retry count is 3
            retry_backoff = min(2 ** attempt * 1000, 30000)  # Exponential backoff, capped at 30s

            # Zeebe allows specifying a retry backoff delay when failing a job.
            # This gives downstream systems time to recover before retrying.
            print(f"⚠️ Exception caught: {exception} for job: {job.key}")
            print(f"🔁 Remaining retries: {retries_remaining}")
            print(f"⏳ Applying retry backoff: {retry_backoff} ms")

            await job_controller.set_failure_status(
                message=f"Failed to run task {job.type}. Reason: {exception}",
                retry_back_off_ms=retry_backoff
            )

        # Jobs in Zeebe are activated by type. The task_type below must match the BPMN model.
        # This job handler is registered to handle jobs of type "model_uploading". using the decorator @worker.task from pyzeebe.
        @worker.task(task_type="model_uploading", exception_handler=worker_exception_handler, timeout_ms=30000)
        async def upload_model(job: Job):
            # Process variables passed from the BPMN instance. Here, we expect "modelId", if it doesnt exist it defaults to empty string "".
            model_id = job.variables.get("modelId", "")
            print(f"\n📦 Received modelId: {model_id}")

            # Validate that modelId matches the expected pattern: "mid hyphen <number>" (e.g., mid-1234)
            if not re.fullmatch(r"mid-\d+", model_id):
                # This simulates a technical failure (e.g., malformed input that wasn't caught earlier).
                # Zeebe will retry this unless all retries are exhausted.
                print("❌ Invalid modelId format! Expected: mid-<number>")
                raise Exception("Invalid modelId format. Expected: mid-<number>")

            # Simulate a backend outage for a specific ID to demonstrate retry/backoff/incident creation.
            # Useful for demonstrating retry behavior, incident creation, and system resilience in Camunda Operate.
            if model_id == "mid-404":
                print("💥 Simulating backend outage for modelId mid-404")
                raise Exception("Backend service is temporarily unavailable.")

            # If all checks pass, simulate successful model upload.
            
            print(f"✅ Model with modelId '{model_id}' was successfully uploaded.")
            return {}

        # Workers run in a continuous polling loop, subscribing to jobs as they appear in the broker queue.
        # Pyzeebe handles job activation, completion, and failure in the background.
        print("🚀 Model Uploading worker (online) is running... Press Ctrl+C to stop.")
        await worker.work()

    # Pyzeebe uses asyncio to run its job execution loop.
    try:
        asyncio.run(run_worker())
    except KeyboardInterrupt:
        # Job workers should shut down cleanly.
        print("\n👋 Model Uploading worker (offline) stopped by user. Goodbye!")

# A worker must declare itself ready and invoke its main event loop to start handling jobs.
# Workers can be deployed as long-running services and scale horizontally.
if __name__ == "__main__":
    main()
