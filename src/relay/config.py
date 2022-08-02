import os

# General
SLACK_WEB_HOOK = os.getenv('SLACK_WEB_HOOK')
RELAY_DOMAINS = ["maily.org"]
REPLY_EMAIL = "replies@maily.org"
RELAY_FROM_ADDRESS = "relay@maily.org"
LOCKER_API_RELAY_DESTINATION = os.getenv('LOCKER_API_RELAY_DESTINATION')
LOCKER_TOKEN_API = os.getenv('LOCKER_TOKEN_API')

# AWS
AWS_REGION = os.getenv('AWS_REGION')

# SES
AWS_SES_CONFIG_SET = os.getenv('AWS_SES_CONFIG_SET')

# SNS
AWS_SNS_TOPIC = os.getenv('AWS_SNS_TOPIC')
SUPPORTED_SNS_TYPES = [
    "SubscriptionConfirmation",
    "Notification",
]

# Queue
SQS_URL = os.getenv('SQS_URL')
PROCESS_EMAIL_BATCH_SIZE = 10
PROCESS_EMAIL_VISIBILITY_SECONDS = 120
PROCESS_EMAIL_WAIT_SECONDS = 5
PROCESS_EMAIL_DELETE_FAILED_MESSAGES = False
