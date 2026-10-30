from datetime import datetime, timezone
import json
import os

from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob import ContentSettings
from dotenv import load_dotenv

from backend.app.models.alert import Alert

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

async def upload_alert_snapshot(alerts: list[Alert]):
    if not AZURE_STORAGE_CONNECTION_STRING:
        raise RuntimeError("AZURE_STORAGE_CONNECTION_STRING is not configured correctly")

    snapshot = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "alerts": [ alert.model_dump(mode="json")
                   for alert in alerts
            ],
    }

    payload = json.dumps(
        snapshot,
        ensure_ascii=False,
        indent=2,
    )

    blob_service = BlobServiceClient.from_connection_string(
        AZURE_STORAGE_CONNECTION_STRING
    )

    async with blob_service:
        blob_client = blob_service.get_blob_client(
            container=AZURE_STORAGE_CONTAINER,
            blob = AZURE_STORAGE_BLOB
        )

        await blob_client.upload_blob(
            payload,
            overwrite=True,
            content_settings=ContentSettings(content_Type="application/json")
        )