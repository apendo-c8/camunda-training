# This script demonstrates how to use the Zeebe client to start a process instance and to send a BPMN message.

import os
import sys
import asyncio
from dotenv import load_dotenv
from pyzeebe import ZeebeClient, create_camunda_cloud_channel

# Load environment variables for credentials and cluster info (same as in the worker)
ENV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "bruno", "training-collection", ".env")
)
load_dotenv(dotenv_path=ENV_PATH)

client_id = os.getenv("ZEEBE_CLIENT_ID")
client_secret = os.getenv("ZEEBE_CLIENT_SECRET")
cluster_id = os.getenv("CAMUNDA_CLUSTER_ID")
region = os.getenv("CAMUNDA_CLUSTER_REGION", "bru-2")

if not all([client_id, client_secret, cluster_id]):
    raise EnvironmentError("❌ Missing Zeebe credentials in environment.")

# Notice the distinction: in the worker, we used the channel directly with ZeebeWorker,
# but here, we instantiate a ZeebeClient to perform process and messaging operations.
# ZeebeClient exposes the API for starting processes and publishing messages.
def create_zeebe_client():
    channel = create_camunda_cloud_channel(
        client_id=client_id,
        client_secret=client_secret,
        cluster_id=cluster_id,
        region=region
    )
    return ZeebeClient(channel)

async def main():
    zeebe = create_zeebe_client()

    #Selects the action based on CLI input: either starting a process or sending a message.
    if len(sys.argv) >= 3 and sys.argv[1] == "start":
        model_id = sys.argv[2]
        print(f"🚀 Starting process with modelId: {model_id}")

        # This code pattern is found in the client you'll use for your assignment.
        # run_process starts a new BPMN process instance in Camunda.
        # The bpmn_process_id must match the process ID from your deployed BPMN model.
        # The variables dictionary passes initial data into the process.
        bpmn_process_id = "Image_Production_Process"
        result = await zeebe.run_process(
            bpmn_process_id=bpmn_process_id,
            variables={"modelId": model_id}
        )
        # The result object contains the process instance key, which you can use for correlation or logging.
        print(f"✅ Process started with instance key: {result.process_instance_key}")

    # --- Send Message Example ---
    elif len(sys.argv) >= 5 and sys.argv[1] == "message":
        correlation_key = sys.argv[2]
        image_id = sys.argv[3]
        try:
            image_rendering_quality = float(sys.argv[4])
        except ValueError:
            print("❌ imageRenderingQuality must be a numeric value (e.g., 0.8)")
            sys.exit(1)

        print("📨 Sending message:")
        print(f"   Correlation key: {correlation_key}")
        print(f"   imageId: {image_id}")
        print(f"   imageRenderingQuality: {image_rendering_quality}")

        # This code pattern is found in the client you'll use for your assignment.
        # publish_message sends a BPMN message to Camunda.
        # - name must match the message catch event in the BPMN model.
        # - correlation_key selects the process instance to receive the message.
        # - variables contains the payload delivered to the process.
        # - time_to_live_in_milliseconds sets how long Zeebe will retain the message if not correlated immediately.
        await zeebe.publish_message(
            name="MessageRenderImageComplete",
            correlation_key=correlation_key,
            variables={
                "imageId": image_id,
                "imageRenderingQuality": image_rendering_quality
            },
            time_to_live_in_milliseconds=60000
        )
        print("✅ Message sent successfully.")

   
    else:
        print("❗ Usage:")
        print("   python zeebe-client-example.py start <modelId>")
        print("   python zeebe-client-example.py message <correlationKey> <imageId> <imageRenderingQuality>")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 Cancelled by user.")
