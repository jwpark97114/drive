import boto3
from botocore.client import Config
from .. import config

session = boto3.session.Session()
s3 = session.client(
    "s3",
    region_name=config.S3_REGION,
    use_ssl=config.S3_USE_SSL,
    endpoint_url=config.S3_ENDPOINT_URL,
    aws_access_key_id=config.S3_ACCESS_KEY,
    aws_secret_access_key=config.S3_SECRET_KEY,
    config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
)


def ensure_bucket():
    list_buckets = [elem["Name"] for elem in s3.list_buckets().get("Buckets", [])]
    if config.S3_BUCKET not in list_buckets:
        kwargs = {"Bucket": config.S3_BUCKET}
        if config.S3_ENDPOINT_URL is None:
            if config.S3_REGION != "us-west-1":
                kwargs["CreateBucketConfiguration"] = {
                    "LocationConstraint": config.S3_REGION
                }
            s3.create_bucket(**kwargs)


def presign_put(key: str, content_type: str, expires: int = 300):

    return s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={"Bucket": config.S3_BUCKET, "Key": key, "ContentType": content_type},
        ExpiresIn=expires,
    )


def presign_get(key: str, expires: int = 300):
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": config.S3_BUCKET, "Key": key},
        ExpiresIn=expires,
    )
