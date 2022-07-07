import argparse, sys, boto3
from botocore.config import Config

parser = argparse.ArgumentParser()
parser.add_argument("--region_name", required=True)
parser.add_argument("--AWS_ACCESS_KEY_ID", required=True)
parser.add_argument("--AWS_SECRET_ACCESS_KEY", required=True)
parser.add_argument("--AWS_SESSION_TOKEN", help="Only required when using temporary credentials.")
parser.add_argument("--ImageId", help="The id of the AMI image to launch the instance from.", required=True)
parser.add_argument("--InstanceType", required=True)
parser.add_argument("--KeyName",  help="The id of the key pair to be used to access the instance.", required=True)
parser.add_argument("--MinCount", type=int, required=True)
parser.add_argument("--MaxCount", type=int, required=True)
args = parser.parse_args()

print("Getting EC2 client...", file=sys.stderr)
client = boto3.client(
    "ec2",
    config=Config(region_name = args.region_name),
    aws_access_key_id=args.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=args.AWS_SECRET_ACCESS_KEY
)

print("Running instances...", file=sys.stderr)
result = client.run_instances(
    ImageId=args.ImageId,
    InstanceType=args.InstanceType,
    KeyName=args.KeyName,
    MinCount=args.MinCount,
    MaxCount=args.MaxCount
)

print("Returning result...", file=sys.stderr)
print(result)