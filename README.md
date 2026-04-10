
# 📧 Serverless Email System on AWS

[![AWS](https://img.shields.io/badge/AWS-Serverless-orange)](https://aws.amazon.com)
[![Lambda](https://img.shields.io/badge/Runtime-Python%203.9-blue)](https://aws.amazon.com/lambda)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A fully automated, zero‑server email pipeline — emails arrive, get stored, processed, and become accessible via a REST API. Built entirely with AWS serverless services.

## 🎯 What It Does

| Step | Service | What Happens |
|------|---------|--------------|
| 1 | **SES** | Catches every incoming email automatically |
| 2 | **S3** | Stores raw `.eml` files permanently |
| 3 | **Lambda** | Parses email, extracts metadata, sends alert |
| 4 | **DynamoDB** | Stores searchable email metadata |
| 5 | **API Gateway** | Exposes REST endpoint to query emails |

## 🏗️ Architecture

```
Email → SES → S3 → Lambda → DynamoDB → API Gateway → JSON Response
                                    ↘ SNS → Email Alert
```

## 📋 Prerequisites

- [AWS Account](https://aws.amazon.com) (Free Tier works)
- Any email address (Gmail, Outlook, Yahoo, etc.)
- Code editor (VS Code, Notepad++, etc.)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/serverless-email-system.git
cd serverless-email-system
```

### 2. Deploy the Infrastructure

**Option A: Manual Setup (10 steps)**

Follow the steps in the [Setup Guide](docs/setup-guide.md):

1. Create S3 bucket → `serverless-emails-[yourname]`
2. Create DynamoDB table → `EmailMetadata` (partition key: `email_id`)
3. Create SNS topic → `EmailNotifications`
4. Verify email in SES
5. Create `EmailProcessor` Lambda (paste code from `/lambda/email_processor.py`)
6. Add S3 trigger to Lambda
7. Create `APIHandler` Lambda (paste code from `/lambda/api_handler.py`)
8. Create API Gateway (REST API → GET method)
9. Create SES receipt rule
10. Add S3 bucket policy (SES write permission)

**Option B: CloudFormation / SAM (Recommended)**

```bash
sam deploy --guided
```

### 3. Test Your System

| Test | Expected Result |
|------|----------------|
| Send test email via SES | `.eml` file appears in S3 |
| Check DynamoDB | New row with email metadata |
| Call API in browser | JSON response with email list |

## 📁 Repository Structure

```
serverless-email-system/
├── lambda/
│   ├── email_processor.py    # Parses S3 email → DynamoDB
│   └── api_handler.py        # Reads DynamoDB → JSON API
├── policies/
│   └── s3_bucket_policy.json # SES write permission
├── docs/
│   └── setup-guide.md        # Detailed 10-step walkthrough
├── slides/
│   └── serverless_email_aws.pptx  # Presentation deck
├── .gitignore
└── README.md
```

## 📝 Lambda Code

### EmailProcessor (S3 → DynamoDB)

```python
import boto3, json, email, uuid, time
from email import policy
from email.parser import BytesParser

def lambda_handler(event, context):
    # Extracts email from S3, parses metadata, stores in DynamoDB
    # Full code in lambda/email_processor.py
    pass
```

### APIHandler (DynamoDB → JSON)

```python
import boto3, json

def lambda_handler(event, context):
    # Scans DynamoDB, returns emails as JSON via API Gateway
    # Full code in lambda/api_handler.py
    pass
```

## 🔧 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| `Could not write to bucket` | Add S3 bucket policy (SES write permission) |
| `Table not found` | Table name must be exactly `EmailMetadata` |
| `AccessDeniedException` | Attach IAM policies to Lambda role |
| `Lambda timeout` | Set timeout to 30 seconds in config |

## 💰 Cost Breakdown

All services run within **AWS Free Tier**:

| Service | Free Tier Limits |
|---------|------------------|
| SES | 62,000 emails/month (outbound) + 1,000 inbound/day |
| Lambda | 1 million requests/month |
| DynamoDB | 25 GB storage + 25 WCU/RCU |
| API Gateway | 1 million API calls/month |
| S3 | 5 GB storage + 20,000 GET/2,000 PUT |

**Total for this demo: $0.00**

## 🧹 Cleanup

Delete these resources to avoid charges:

```bash
# Delete S3 bucket (empty first)
aws s3 rm s3://your-bucket-name --recursive
aws s3 rb s3://your-bucket-name

# Delete DynamoDB table
aws dynamodb delete-table --table-name EmailMetadata

# Delete Lambda functions
aws lambda delete-function --function-name EmailProcessor
aws lambda delete-function --function-name APIHandler

# Delete API Gateway
aws apigateway delete-rest-api --rest-api-id your-api-id

# Delete SNS topic
aws sns delete-topic --topic-arn your-topic-arn

# Delete SES receipt rule
aws ses delete-receipt-rule --rule-set-name default --rule-name your-rule
```

## 🚀 Next Steps (Advanced Features)

| Feature | How to Implement |
|---------|------------------|
| Email search | Add DynamoDB Global Secondary Index on `from_address` or `subject` |
| Attachment support | Store attachments in S3, generate pre-signed URLs |
| Auto-reply | Trigger SES to send confirmation email |
| Web dashboard | React/Vue app calling your API |
| Slack/Discord webhooks | Forward notifications to team channels |

## 📚 Resources

- [AWS SES Documentation](https://docs.aws.amazon.com/ses)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda)
- [AWS DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb)
- [AWS API Gateway Documentation](https://docs.aws.amazon.com/apigateway)

## 👤 Author

**Jason Oladipo Hughes**  
AWS Cloud Club, Nile University  
April 9, 2026

## 📄 License

MIT — feel free to use, modify, and distribute.

---

## ⭐ Support

If this project helped you learn serverless AWS, give it a star ⭐ and share with your cloud club!



This README includes everything you need: architecture overview, setup instructions, code references, troubleshooting, cost breakdown, cleanup, and next steps. Just replace `yourusername` and `your-bucket-name` with your actual values.
