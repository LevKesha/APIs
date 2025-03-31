import uuid
import datetime
from functools import wraps
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, abort
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError

app = Flask(__name__)
api = Api(app)

# Global in-memory store for user sessions (mapping token -> boto3 Session and expiry)
USER_SESSIONS = {}

# Token expiry time (in minutes)
TOKEN_EXPIRY_MINUTES = 60

def create_session(aws_access_key_id, aws_secret_access_key, aws_region):
    """Create a boto3 session with provided AWS credentials."""
    try:
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )
        # Optionally, do a simple call to verify credentials
        sts_client = session.client('sts')
        sts_client.get_caller_identity()
        return session
    except (NoCredentialsError, BotoCoreError, ClientError) as e:
        abort(401, message="Invalid AWS credentials or region provided.")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth or not auth.startswith("Bearer "):
            abort(401, message="Authorization token is missing.")
        token = auth.split("Bearer ")[1]
        session_info = USER_SESSIONS.get(token)
        if not session_info:
            abort(401, message="Invalid or expired token.")
        # Check token expiry
        if datetime.datetime.utcnow() > session_info['expires_at']:
            USER_SESSIONS.pop(token, None)
            abort(401, message="Token has expired.")
        # Attach the session to the Flask request context for easy access
        request.aws_session = session_info['session']
        return f(*args, **kwargs)
    return decorated

# Authentication Resource
class AuthLogin(Resource):
    def post(self):
        data = request.get_json(force=True)
        aws_access_key_id = data.get("aws_access_key_id")
        aws_secret_access_key = data.get("aws_secret_access_key")
        aws_region = data.get("aws_region", "us-east-1")
        if not aws_access_key_id or not aws_secret_access_key:
            abort(400, message="AWS access key and secret key are required.")
        # Create a boto3 session using provided credentials
        session = create_session(aws_access_key_id, aws_secret_access_key, aws_region)
        token = uuid.uuid4().hex
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRY_MINUTES)
        USER_SESSIONS[token] = {"session": session, "expires_at": expires_at}
        return {"token": token, "expires_at": expires_at.isoformat() + "Z"}, 200

# ECS Monitoring Resources
class ECSClusters(Resource):
    @token_required
    def get(self):
        session = request.aws_session
        ecs_client = session.client('ecs')
        try:
            clusters_response = ecs_client.list_clusters()
            cluster_arns = clusters_response.get("clusterArns", [])
            # Optionally, describe clusters to get additional details
            if cluster_arns:
                details = ecs_client.describe_clusters(clusters=cluster_arns)
                clusters = details.get("clusters", [])
            else:
                clusters = []
            return {"clusters": clusters}, 200
        except ClientError as e:
            abort(500, message=str(e))

class ECSClusterServices(Resource):
    @token_required
    def get(self, cluster_name):
        session = request.aws_session
        ecs_client = session.client('ecs')
        try:
            # List services for the given cluster
            list_response = ecs_client.list_services(cluster=cluster_name)
            service_arns = list_response.get("serviceArns", [])
            if service_arns:
                services_response = ecs_client.describe_services(cluster=cluster_name, services=service_arns)
                services = services_response.get("services", [])
            else:
                services = []
            return {"cluster_name": cluster_name, "services": services}, 200
        except ClientError as e:
            abort(500, message=str(e))

# S3 Monitoring Resources
class S3Buckets(Resource):
    @token_required
    def get(self):
        session = request.aws_session
        s3_client = session.client('s3')
        try:
            response = s3_client.list_buckets()
            buckets = response.get("Buckets", [])
            return {"buckets": buckets}, 200
        except ClientError as e:
            abort(500, message=str(e))

class S3BucketDetails(Resource):
    @token_required
    def get(self, bucket_name):
        session = request.aws_session
        s3_client = session.client('s3')
        try:
            # Get bucket location as one detail
            location = s3_client.get_bucket_location(Bucket=bucket_name)
            # More details could be added (e.g., encryption, lifecycle rules) using additional API calls
            details = {
                "bucket_name": bucket_name,
                "region": location.get("LocationConstraint") or "us-east-1"
            }
            return details, 200
        except ClientError as e:
            abort(500, message=str(e))

# EBS Monitoring Resources
class EBSVolumes(Resource):
    @token_required
    def get(self):
        session = request.aws_session
        ec2_client = session.client('ec2')
        try:
            response = ec2_client.describe_volumes()
            volumes = response.get("Volumes", [])
            return {"volumes": volumes}, 200
        except ClientError as e:
            abort(500, message=str(e))

class EBSVolumeMetrics(Resource):
    @token_required
    def get(self, volume_id):
        session = request.aws_session
        cloudwatch_client = session.client('cloudwatch')
        try:
            # Example: Get read ops metric for the past hour (adjust as needed)
            end_time = datetime.datetime.utcnow()
            start_time = end_time - datetime.timedelta(hours=1)
            stats = cloudwatch_client.get_metric_statistics(
                Namespace='AWS/EBS',
                MetricName='VolumeReadOps',
                Dimensions=[{'Name': 'VolumeId', 'Value': volume_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Average']
            )
            return {"volume_id": volume_id, "metrics": stats}, 200
        except ClientError as e:
            abort(500, message=str(e))

# Network Monitoring Resources
class NetworkVPCs(Resource):
    @token_required
    def get(self):
        session = request.aws_session
        ec2_client = session.client('ec2')
        try:
            response = ec2_client.describe_vpcs()
            vpcs = response.get("Vpcs", [])
            return {"vpcs": vpcs}, 200
        except ClientError as e:
            abort(500, message=str(e))

class NetworkSecurityGroups(Resource):
    @token_required
    def get(self, vpc_id):
        session = request.aws_session
        ec2_client = session.client('ec2')
        try:
            response = ec2_client.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
            security_groups = response.get("SecurityGroups", [])
            return {"vpc_id": vpc_id, "security_groups": security_groups}, 200
        except ClientError as e:
            abort(500, message=str(e))

# Dashboard Resource
class DashboardSummary(Resource):
    @token_required
    def get(self):
        # For demonstration, aggregate simple counts from ECS, S3, EBS, and Network
        session = request.aws_session
        summary = {}
        try:
            ecs_client = session.client('ecs')
            ecs_clusters = ecs_client.list_clusters().get("clusterArns", [])
            summary["total_clusters"] = len(ecs_clusters)

            s3_client = session.client('s3')
            s3_buckets = s3_client.list_buckets().get("Buckets", [])
            summary["total_buckets"] = len(s3_buckets)

            ec2_client = session.client('ec2')
            volumes = ec2_client.describe_volumes().get("Volumes", [])
            summary["total_volumes"] = len(volumes)

            vpcs = ec2_client.describe_vpcs().get("Vpcs", [])
            summary["total_vpcs"] = len(vpcs)

            return {"summary": summary}, 200
        except ClientError as e:
            abort(500, message=str(e))

# Register routes with Flask-RESTful
api.add_resource(AuthLogin, '/api/v1/auth/login')
api.add_resource(ECSClusters, '/api/v1/ecs/clusters')
api.add_resource(ECSClusterServices, '/api/v1/ecs/clusters/<string:cluster_name>/services')
api.add_resource(S3Buckets, '/api/v1/s3/buckets')
api.add_resource(S3BucketDetails, '/api/v1/s3/buckets/<string:bucket_name>/details')
api.add_resource(EBSVolumes, '/api/v1/ebs/volumes')
api.add_resource(EBSVolumeMetrics, '/api/v1/ebs/volumes/<string:volume_id>/metrics')
api.add_resource(NetworkVPCs, '/api/v1/network/vpcs')
api.add_resource(NetworkSecurityGroups, '/api/v1/network/vpcs/<string:vpc_id>/security-groups')
api.add_resource(DashboardSummary, '/api/v1/dashboard/summary')

if __name__ == '__main__':
    # Set debug=True for development; remove in production.
    app.run(host='0.0.0.0', port=5000, debug=True)
