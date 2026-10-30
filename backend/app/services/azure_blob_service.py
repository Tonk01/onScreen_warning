import json
import os

from azure.storage.blob.aio import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER", "alerts")
AZURE_STORAGE_BLOB = os.getenv("AZURE_STORAGE_BLOB", "alerts.json")

async def get_alert_snapshot():
    if not AZURE_STORAGE_CONNECTION_STRING:
        raise RuntimeError("AZURE_STORAGE_CONNECTION_STRING is not configured correctly")

    blob_service = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

    async with blob_service:
        blob_client = blob_service.get_blob_client(
            container=AZURE_STORAGE_CONTAINER,
            blob=AZURE_STORAGE_BLOB,
        )

        downloader = await blob_client.download_blob()
        data = await downloader.readall()

    return json.loads(data)