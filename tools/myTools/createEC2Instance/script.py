import argparse, sys, boto3
from ast import Try
from botocore.config import Config
import json
import time

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

# wait until the instance is running so we get the public ip address
instance_id = result["Instances"][0]["InstanceId"]
update = None
for i in range(24):
    print(f"Checking for running state {i}", file=sys.stderr)
    try:
        update = client.describe_instances(InstanceIds=[instance_id])
    except:
        update = None
    
    if update is not None and update["Reservations"][0]["Instances"][0]["State"]["Name"] == "running":
        break
    else:
        time.sleep(5)

print("Returning result...", file=sys.stderr)
if update is None:
    print(json.dumps(result, indent=2, default=str))
else:
    print(json.dumps(update["Reservations"][0], indent=2, default=str))
