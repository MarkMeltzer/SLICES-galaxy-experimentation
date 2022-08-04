import argparse, sys, boto3
from botocore.config import Config
import json

parser = argparse.ArgumentParser()
parser.add_argument("--region_name", required=True)
parser.add_argument("--AWS_ACCESS_KEY_ID", required=True)
parser.add_argument("--AWS_SECRET_ACCESS_KEY", required=True)
parser.add_argument("--AWS_SESSION_TOKEN", help="Only required when using temporary credentials.")
parser.add_argument("--InstanceId", help="The id of the AMI image to launch the instance from.", required=True)
args = parser.parse_args()

print("Getting EC2 client...", file=sys.stderr)
client = boto3.client(
    "ec2",
    config=Config(region_name = args.region_name),
    aws_access_key_id=args.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=args.AWS_SECRET_ACCESS_KEY
)

print("Terminating instance...", file=sys.stderr)
result = client.terminate_instances(
    InstanceIds=[args.InstanceId]
)

print("Returning result...", file=sys.stderr)
print(json.dumps(result, indent=2, default=str))