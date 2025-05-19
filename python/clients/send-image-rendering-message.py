import os
import sys
import asyncio
from dotenv import load_dotenv
from pyzeebe import ZeebeClient, create_camunda_cloud_channel

# Load environment variables from .env located two levels up
ENV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "bruno", "training-collection", ".env")
)
print(f"📥 Loading environment from: {ENV_PATH}")
load_dotenv(dotenv_path=ENV_PATH)

# Zeebe credentials
client_id = os.getenv("ZEEBE_CLIENT_ID")
client_secret = os.getenv("ZEEBE_CLIENT_SECRET")
cluster_id = os.getenv("CAMUNDA_CLUSTER_ID")
region = os.getenv("CAMUNDA_CLUSTER_REGION", "bru-2")

if not all([client_id, client_secret, cluster_id]):
    raise EnvironmentError("❌ Missing Zeebe credentials in environment.")

# Check CLI input
if len(sys.argv) < 4:
    print("❗ Usage: python send-message.py <correlationKey> <imageId> <imageRenderingQuality>")
    sys.exit(1)

correlation_key = sys.argv[1]
image_id = sys.argv[2]

try:
    image_rendering_quality = float(sys.argv[3])
except ValueError:
    print("❌ imageRenderingQuality must be a numeric value (e.g., 0.8)")
    sys.exit(1)

print("📨 Sending message:")
print(f"   Correlation key: {correlation_key}")
print(f"   imageId: {image_id}")
print(f"   imageRenderingQuality: {image_rendering_quality}")

# Async message sender
async def main():
    channel = create_camunda_cloud_channel(
        client_id=client_id,
        client_secret=client_secret,
        cluster_id=cluster_id,
        region=region
    )

    zeebe = ZeebeClient(channel)

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

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 Cancelled by user.")