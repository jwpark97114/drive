import boto3
from botocore.client import Config
from .. import config
import os
from urllib.parse import urlparse, urlunparse

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

s3_pub = session.client(
    "s3",
    region_name=config.S3_REGION,
    use_ssl=config.S3_USE_SSL,
    endpoint_url=config.S3_PUBLIC_ENDPOINT,
    aws_access_key_id=config.S3_ACCESS_KEY,
    aws_secret_access_key=config.S3_SECRET_KEY,
    config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
)

def convert2_public(url:str):
    pub = os.getenv("S3_PUBLIC_ENDPOINT")
    if not pub:
        return url
    
    prev_u = urlparse(url)
    parsed_pub = urlparse(pub)
    return urlunparse((parsed_pub.scheme, parsed_pub.netloc, prev_u.path, prev_u.params, prev_u.query,prev_u.fragment))


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

    return s3_pub.generate_presigned_url(
        ClientMethod="put_object",
        Params={"Bucket": config.S3_BUCKET, "Key": key, "ContentType": content_type},
        ExpiresIn=expires,
    )


def presign_get(key: str, expires: int = 300):
    return s3_pub.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": config.S3_BUCKET, "Key": key},
        ExpiresIn=expires,
    )
