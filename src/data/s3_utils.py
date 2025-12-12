"""
Lightweight S3/MinIO utilities using boto3.
Works locally with MinIO (docker-compose) and AWS.
"""
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from pathlib import Path
from typing import List
from src.utils import logger
import os


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT", "http://localhost:9000"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "minioadmin"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin"),
    )


def download_from_s3(bucket: str, key: str, local_path: Path) -> None:
    client = get_s3_client()
    local_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        client.download_file(bucket, key, str(local_path))
        logger.success(f"Downloaded s3://{bucket}/{key} → {local_path}")
    except (ClientError, NoCredentialsError) as e:
        logger.error(f"S3 download failed: {e}")


def upload_to_s3(local_path: Path, bucket: str, key: str) -> None:
    client = get_s3_client()
    try:
        client.upload_file(str(local_path), bucket, key)
        logger.success(f"Uploaded {local_path} → s3://{bucket}/{key}")
    except (ClientError, NoCredentialsError) as e:
        logger.error(f"S3 upload failed: {e}")


def list_s3_objects(bucket: str, prefix: str = "") -> List[str]:
    client = get_s3_client()
    response = client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    return [obj["Key"] for obj in response.get("Contents", [])]
