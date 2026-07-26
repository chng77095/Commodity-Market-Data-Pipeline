# Commodity-Market-Data-Pipeline
An automated ETL pipeline using Python, SQL, APIs, and AWS cloud services to ingest, clean, transform, and validate financial market datasets, implementing data quality checks and structured data storage for downstream analytics and forecasting workflows


# Real-Time Commodity Market Data Pipeline (AWS)

An end-to-end **real-time data streaming pipeline** that ingests, validates, and stores high-frequency commodity market data using **AWS SQS**, **AWS Lambda**, and **AWS S3**.

The pipeline continuously streams commodity ticker data, performs serverless data validation, and stores clean JSON records in an AWS S3 data lake for downstream analytics and machine learning.

---

## Architecture

```text
                 +---------------------------+
                 |  Local Python Producer    |
                 |      (yfinance API)       |
                 +------------+--------------+
                              |
                              |
                              ▼
                 +---------------------------+
                 |      AWS SQS Queue        |
                 |  Buffers incoming ticks   |
                 +------------+--------------+
                              |
                              ▼
                 +---------------------------+
                 |     AWS Lambda Function   |
                 | Validates & enriches data |
                 +------------+--------------+
                              |
                              ▼
                 +---------------------------+
                 |        AWS S3 Bucket      |
                 | Stores timestamped JSON   |
                 +---------------------------+
```

---

#Pipeline Workflow

### 1. Data Ingestion (Producer)

A local Python application retrieves live commodity market prices (for example, **Crude Oil Futures (`CL=F`)**) using the `yfinance` library.

The producer publishes a new market tick to an **AWS SQS** queue every **5 seconds**.

---

### 2. Message Buffer (AWS SQS)

Amazon Simple Queue Service (SQS) acts as a reliable message broker that:

- Buffers incoming market data
- Decouples ingestion from processing
- Prevents data loss during traffic spikes
- Enables scalable downstream processing

---

### 3. Data Validation (AWS Lambda)

Each SQS message automatically triggers an AWS Lambda function that:

- Validates incoming price data
- Rejects invalid or non-positive prices
- Enriches records with timestamps
- Converts messages into clean JSON objects

---

### 4. Data Lake Storage (AWS S3)

Validated records are stored in Amazon S3 as timestamped JSON files, making the data suitable for:

- Analytics
- Reporting
- Machine Learning
- Historical market analysis

---

# Tech Stack

### Programming Language

- Python 3.9+

### AWS Services

- **AWS SQS** – Distributed message queue
- **AWS Lambda** – Serverless event processing
- **AWS S3** – Object storage / Data lake
- **AWS IAM** – Identity & Access Management

### Python Libraries

- `boto3`
- `yfinance`
- `json`
- `datetime`

---

#  Project Structure

```text
.
├── aws_producer.py          # Streams commodity ticks to SQS
├── lambda_function.py       # Validates and stores records in S3
└── README.md
```

---

# Deployment & Setup

## Prerequisites

- Python 3.9+
- AWS Account
- IAM User with permissions for:
  - Amazon SQS
  - AWS Lambda
  - Amazon S3

---

## 1️Create an S3 Bucket

Create an S3 bucket in your preferred AWS Region.

Example:

```
commodity-market-data-yourname
```

Keep **Block Public Access** enabled.

---

## 2️Create an SQS Queue

Create a **Standard Queue** named:

```
commodity-market-queue
```

Copy the Queue URL for use in the producer application.

---

## 3️Deploy the Lambda Function

Create a Lambda function:

```
validate_and_store_ticks
```

Runtime:

```
Python 3.10+
```

Attach the following IAM policies:

- AmazonS3FullAccess
- AWSLambdaSQSQueueExecutionRole

Then:

1. Upload `lambda_function.py`
2. Update the `BUCKET_NAME`
3. Add an SQS Trigger pointing to:

```
commodity-market-queue
```

---

## 4 Configure the Producer

Install dependencies:

```bash
pip install boto3 yfinance
```

Update `aws_producer.py` with:

- AWS Access Key
- AWS Secret Key
- SQS Queue URL

# Security Note

This project requires AWS authentication to access Amazon SQS, AWS Lambda, and Amazon S3.

**Never commit your AWS credentials to GitHub or include them directly in your source code.** This includes:

- AWS Access Key ID
- AWS Secret Access Key


Run the producer:

```bash
python aws_producer.py
```

---

# Data Flow

```text
yfinance
    │
    ▼
Python Producer
    │
    ▼
AWS SQS
    │
    ▼
AWS Lambda
    │
    ▼
AWS S3
```

---

# ✨ Key Features

## ✅ Real-Time Streaming

Continuously ingests live commodity market data every 5 seconds.

## ✅ Decoupled Architecture

Uses Amazon SQS to separate producers from consumers, improving reliability and scalability.

## ✅ Automatic Data Validation

Filters invalid, corrupted, or non-positive price records before storage.

## ✅ Serverless Processing

AWS Lambda automatically scales based on queue depth with no server management required.

## ✅ Cloud Data Lake

Stores validated JSON records in Amazon S3 for future analytics and machine learning workflows.


---

# 📜 License

This project is intended for educational and portfolio purposes.

If all goes well, the result of your code should look something like this. Do note that due to the market being closed during the weekend when this project was preformed, the price ticker shown is fixed.

---<img width="1004" height="269" alt="clf" src="https://github.com/user-attachments/assets/27ccf419-e342-419b-9441-7fbd9a187ea3" />



