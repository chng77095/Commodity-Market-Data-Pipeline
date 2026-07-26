print(">>> SCRIPT IS LAUNCHING <<<")
print(">>> SCRIPT IS STARTING NOW <<<")
import time
import json
import boto3
import yfinance as yf

# 1. Credentials
AWS_ACCESS_KEY = 'YOUR-ACCESS-KEY-HERE'
AWS_SECRET_KEY = 'YOUR-SECRET-KEY-HERE'
AWS_REGION = 'YOUR-AWS-REGION'

QUEUE_URL = 'YOUR-QUEUE-URL'

# 2. Connect to AWS SQS
print("Connecting to AWS SQS...")
sqs = boto3.client(
    'sqs',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)
print("Connected successfully!")

def stream_ticker_data(symbol="CL=F"):
    ticker = yf.Ticker(symbol).fast_info
    
    payload = {
        'symbol': symbol,
        'last_price': ticker.last_price,
        'previous_close': ticker.previous_close,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    }
    
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(payload)
    )
    print(f"[STREAMING] Sent tick for {symbol} | Price: ${ticker.last_price:.2f}")

# 3. Direct Infinite Loop
print("Starting streaming loop. Press Ctrl+C to stop.")
try:
    while True:
        stream_ticker_data("CL=F")
        time.sleep(5)
except KeyboardInterrupt:
    print("\nPipeline stopped by user.")
except Exception as e:
    print(f"\n[ERROR] Something went wrong: {e}")
