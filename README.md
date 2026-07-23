# Cloud Resume Challenge

A personal resume website built on AWS, following the [Cloud Resume Challenge](https://cloudresumechallenge.dev/docs/the-challenge/aws/) framework.

## Architecture

```
resume/resume.md → build.py → frontend/ → S3 → CloudFront → yourdomain.com
                                                              │
Visitor Counter ← API Gateway ← Lambda ← DynamoDB
```

## Stack

| Layer | Service | Purpose |
|-------|---------|---------|
| Hosting | S3 + CloudFront | Static site with HTTPS |
| DNS | Route 53 | Custom domain |
| Backend | Lambda (Python 3.12) | Visitor counter API |
| Database | DynamoDB | Stores visit count |
| API | API Gateway v2 (HTTP) | Frontend ↔ Lambda |
| IaC | Terraform | All infrastructure |
| CI/CD | GitHub Actions | Auto-deploy on push |

## Project Structure

```
├── resume/
│   └── resume.md              # Your resume (edit this)
├── build.py                   # Markdown → HTML build script
├── frontend/
│   ├── index.html             # Generated (gitignored)
│   ├── style.css              # Resume styling
│   └── counter.js             # Visitor counter
├── backend/
│   ├── app.py                 # Lambda handler
│   ├── requirements.txt
│   └── tests/
│       ├── conftest.py
│       └── test_app.py        # 5 tests (moto + pytest)
├── terraform/
│   ├── main.tf                # Provider config
│   ├── variables.tf           # Input variables
│   ├── outputs.tf             # Outputs (bucket, CF distro, API URL)
│   ├── s3.tf                  # S3 bucket + OAC
│   ├── cloudfront.tf          # CloudFront distribution
│   ├── dynamodb.tf            # Visitor counter table
│   ├── lambda.tf              # Lambda function + IAM
│   ├── api_gateway.tf         # HTTP API
│   └── route53.tf             # DNS + ACM (optional)
├── .github/workflows/
│   ├── deploy-frontend.yml    # Build MD → S3 sync → CF invalidation
│   └── deploy-backend.yml     # pytest → terraform apply
├── iam-policy.json            # Scoped IAM policy reference
└── requirements.txt           # Build dependencies
```

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Build the site
python build.py

# Preview
open frontend/index.html

# Run backend tests
pip install pytest moto boto3
python -m pytest backend/tests/ -v
```

## Editing the Resume

1. Edit `resume/resume.md`
2. Run `python build.py`
3. Preview `frontend/index.html` in browser
4. Push to GitHub — Actions deploys automatically

## Deployment

### First Time Setup

1. Create an AWS account with an IAM user that has admin access
2. Configure AWS CLI: `aws configure`
3. From `terraform/`: `terraform init && terraform apply`
4. Add GitHub Secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
5. Add GitHub Variables: `S3_BUCKET_NAME`, `AWS_REGION`, `CLOUDFRONT_DISTRIBUTION_ID`

### Automatic

Push to `main` — GitHub Actions handles the rest:
- **Resume changes** → build MD, deploy frontend to S3, invalidate CloudFront
- **Backend/Terraform changes** → run tests, apply Terraform

### Domain (Optional)

1. Register a domain via Route 53 (~$10/year)
2. In `terraform/variables.tf`, set:
   ```hcl
   domain_name = "yourdomain.com"
   enable_dns  = true
   ```
3. Run `terraform apply`
4. Update GitHub Variable `CLOUDFRONT_DISTRIBUTION_ID` from `terraform output`

## Costs

All services use free tier or pay-per-request pricing:
- S3: pennies/month for a static site
- CloudFront: free tier covers typical personal site traffic
- DynamoDB: on-demand, essentially free for a visitor counter
- Lambda: free tier covers 1M requests/month
- API Gateway: free tier covers 1M requests/month
- Route 53: ~$1/month for a hosted zone + $0.40/million queries
