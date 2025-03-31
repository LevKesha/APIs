# Unified PowerShell Script to Test AWS Monitoring API Endpoints
#Set-ExecutionPolicy Bypass
# --- Step 1: Authenticate and obtain a token ---
$loginUri = "http://localhost:5000/api/v1/auth/login"
$loginBody = '{
  "aws_access_key_id": "<Key_ID>",
  "aws_secret_access_key": "<Key_Secret>",
  "aws_region": "us-east-1"
}'
$loginHeaders = @{ "Content-Type" = "application/json" }

Write-Output "Logging in to obtain token..."
$loginResponse = Invoke-WebRequest -Uri $loginUri -Method POST -Headers $loginHeaders -Body $loginBody | ConvertFrom-Json

if (-not $loginResponse.token) {
    Write-Error "Failed to obtain token. Check your credentials."
    exit
}

$token = $loginResponse.token
Write-Output "Token obtained: $token"
# Create a global header for subsequent requests
$globalHeaders = @{ "Authorization" = "Bearer $token" }

# --- Step 2: Test each API endpoint ---

# 2.1 Test ECS Clusters Endpoint
$ecsClustersUri = "http://localhost:5000/api/v1/ecs/clusters"
Write-Output "`nTesting ECS Clusters endpoint..."
$ecsClustersResponse = Invoke-WebRequest -Uri $ecsClustersUri -Method GET -Headers $globalHeaders | ConvertFrom-Json
Write-Output "ECS Clusters Response:"
$ecsClustersResponse | Format-Table -AutoSize

# 2.2 Test ECS Cluster Services Endpoint (using a sample cluster name 'cluster1')
$ecsServicesUri = "http://localhost:5000/api/v1/ecs/clusters/cluster1/services"
Write-Output "`nTesting ECS Cluster Services endpoint for 'cluster1'..."
$ecsServicesResponse = Invoke-WebRequest -Uri $ecsServicesUri -Method GET -Headers $globalHeaders | ConvertFrom-Json
Write-Output "ECS Cluster Services Response:"
$ecsServicesResponse | Format-Table -AutoSize

# 2.3 Test S3 Buckets Endpoint
$s3BucketsUri = "http://localhost:5000/api/v1/s3/buckets"
Write-Output "`nTesting S3 Buckets endpoint..."
$s3BucketsResponse = Invoke-WebRequest -Uri $s3BucketsUri -Method GET -Headers $globalHeaders | ConvertFrom-Json
Write-Output "S3 Buckets Response:"
$s3BucketsResponse | Format-Table -AutoSize

# 2.4 Test S3 Bucket Details Endpoint (using a sample bucket name 'mybucket')
$s3BucketDetailsUri = "http://localhost:5000/api/v1/s3/buckets/mybucket/details"
Write-Output "`nTesting S3 Bucket Details endpoint for bucket 'mybucket'..."
$s3BucketDetailsResponse = Invoke-WebRequest -Uri $s3BucketDetailsUri -Method GET -Headers $globalHeaders | ConvertFrom-Json
Write-Output "S3 Bucket Details Response:"
$s3BucketDetailsResponse | Format-Table -AutoSize

# 2.5 Test EBS Volumes Endpoint
$ebsVolumesUri = "http://localhost:5000/api/v1/ebs/volumes"
Write-Output "`nTesting EBS Volumes endpoint..."
$ebsVolumesResponse = Invoke-WebRequest -Uri $ebsVolumesUri -Method GET -Headers $globalHeaders | ConvertFrom-Json
Write-Output "EBS Volumes Response:"
$ebsVolumesResponse | Format-Table -AutoSize

# 2.6 Test EBS Volume Metrics Endpoint (using a sample volume ID 'vol-001')
$ebsMetricsUri = "http://localhost:5000/api/v1/ebs/volumes/vol-001/metrics"
Write-Output "`nTesting EBS Volume Metrics endpoint for volume 'vol-001'..."
$ebsMetricsResponse = Invoke-WebRequest -Uri $ebsMetricsUri -Method GET -Headers $globalHeaders | ConvertFrom-Json
Write-Output "EBS Volume Metrics Response:"
$ebsMetricsResponse | Format-Table -AutoSize

# 2.7 Test Network VPCs Endpoint
$networkVpcsUri = "http://localhost:5000/api/v1/network/vpcs"
Write-Output "`nTesting Network VPCs endpoint..."
$networkVpcsResponse = Invoke-WebRequest -Uri $networkVpcsUri -Method GET -Headers $globalHeaders | ConvertFrom-Json
Write-Output "Network VPCs Response:"
$networkVpcsResponse | Format-Table -AutoSize

# 2.8 Test Network Security Groups Endpoint (using a sample VPC ID 'vpc-1111')
$networkSgUri = "http://localhost:5000/api/v1/network/vpcs/vpc-1111/security-groups"
Write-Output "`nTesting Network Security Groups endpoint for VPC 'vpc-1111'..."
$networkSgResponse = Invoke-WebRequest -Uri $networkSgUri -Method GET -Headers $globalHeaders | ConvertFrom-Json
Write-Output "Network Security Groups Response:"
$networkSgResponse | Format-Table -AutoSize

# 2.9 Test Dashboard Summary Endpoint
$dashboardUri = "http://localhost:5000/api/v1/dashboard/summary"
Write-Output "`nTesting Dashboard Summary endpoint..."
$dashboardResponse = Invoke-WebRequest -Uri $dashboardUri -Method GET -Headers $globalHeaders | ConvertFrom-Json
Write-Output "Dashboard Summary Response:"
$dashboardResponse | Format-Table -AutoSize
