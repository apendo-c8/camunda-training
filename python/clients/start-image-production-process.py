import os
import sys
import asyncio
from dotenv import load_dotenv
from pyzeebe import ZeebeClient, create_camunda_cloud_channel

# Load .env
ENV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "bruno", "training-collection", ".env")
)
load_dotenv(dotenv_path=ENV_PATH)

# Zeebe credentials
client_id = os.getenv("ZEEBE_CLIENT_ID")
client_secret = os.getenv("ZEEBE_CLIENT_SECRET")
cluster_id = os.getenv("CAMUNDA_CLUSTER_ID")
region = os.getenv("CAMUNDA_CLUSTER_REGION", "bru-2")

if not all([client_id, client_secret, cluster_id]):
    raise EnvironmentError("❌ Missing Zeebe credentials in environment.")

# Check CLI input
if len(sys.argv) < 2:
    print("❗ Usage: python start-process-instance.py <modelId>")
    sys.exit(1)

model_id = sys.argv[1]
print(f"🚀 Starting process with modelId: {model_id}")

# Async process starter
async def main():
    channel = create_camunda_cloud_channel(
        client_id=client_id,
        client_secret=client_secret,
        cluster_id=cluster_id,
        region=region
    )

    zeebe = ZeebeClient(channel)

    # Replace this with the actual BPMN process ID
    bpmn_process_id = "Image_Production_Process"

    result = await zeebe.run_process(
        bpmn_process_id=bpmn_process_id,
        variables={"modelId": model_id}
    )

    print(f"✅ Process started with instance key: {result.process_instance_key}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 Cancelled by user.")