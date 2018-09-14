#!/bin/bash

# AWS creds profile we're using.
profile="stoic"

# Command to execute at Serverless-ready prompt.
command="$1"

# Get our AWS profile access creds.
AWS_ACCESS_KEY_ID=$(aws --profile $profile configure get aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(aws --profile $profile configure get aws_secret_access_key)

# Run our container with env vars.
docker container run -v "$(pwd)":/app -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY stoictechgroup/stoic-serverless-awsapi -c "$command"
