<!--
title: AWS Serverless REST API with DynamoDB store in Python
description: This example demonstrates how to setup a RESTful Web Service allowing you to create, list, get, update and delete Notes. DynamoDB is used to store the data.
layout: Doc
-->
# Serverless REST API

This example demonstrates how to setup a [RESTful Web Services](https://en.wikipedia.org/wiki/Representational_state_transfer#Applied_to_web_services) allowing you to create, list, get, update and delete Notes. DynamoDB is used to store the data. This is just an example and of course you could use any data storage as a backend.

## Getting Dependencies

### AWS credentials configured with correct permission

Appropriate credentials under a valid profile should be stored and configured in `~/.aws/credentials` on your local resource.

### Pipenv for Python Package Management (not Virtual Environments)

Pipenv (https://github.com/pypa/pipenv) should be installed and configured on your local resource. We use Docker for our containerized or virtual environments, but we use Pipenv for Python dependency management.

To ensure that all Python 3.* packages are installed for use in the project, run `pipenv install` against the `Pipfile` in the solution.

### Plugins Installed and Configured

Serverless relies on Node.js and npm for package management. Make sure to have Node.js and npm installed and configured for us. To ensure all Node.js packages are installed run `npm install`.

## Structure

This service has a separate directory for all the note operations. For each operation exactly one file exists e.g. `functions/delete.py`. In each of these files there is exactly one function defined.

The idea behind the `notes` directory is that in case you want to create a service containing multiple resources e.g. users, notes, comments you could do so in the same service. While this is certainly possible you might consider creating a separate service for each resource. It depends on the use-case and your preference.

## Use-cases

- API for a Web Application
- API for a Mobile Application

## Setup

```bash
npm install -g serverless
```

## Deploying

In order to deploy the endpoint simply run

```bash
sls deploy -v --aws-profile YOUR_PROFILE --stage YOUR_STAGE
```

The expected result should be similar to:

```bash
Serverless: Generating requirements.txt from Pipfile...
Serverless: Installing requirements of requirements.txt in .serverless...
Serverless: Docker Image: lambci/lambda:build-python3.6
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Injecting required Python packages to package...
Serverless: Creating Stack...
Serverless: Checking Stack create progress...
CloudFormation - CREATE_IN_PROGRESS - AWS::CloudFormation::Stack - stoic-notes-stack-dev
CloudFormation - CREATE_IN_PROGRESS - AWS::S3::Bucket - ServerlessDeploymentBucket
CloudFormation - CREATE_IN_PROGRESS - AWS::S3::Bucket - ServerlessDeploymentBucket
CloudFormation - CREATE_COMPLETE - AWS::S3::Bucket - ServerlessDeploymentBucket
CloudFormation - CREATE_COMPLETE - AWS::CloudFormation::Stack - stoic-notes-stack-dev
Serverless: Stack create finished...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service .zip file to S3 (1.04 MB)...
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
CloudFormation - UPDATE_IN_PROGRESS - AWS::CloudFormation::Stack - stoic-notes-stack-dev
CloudFormation - CREATE_IN_PROGRESS - AWS::DynamoDB::Table - notesDynamoDbTable
CloudFormation - CREATE_IN_PROGRESS - AWS::Logs::LogGroup - DeleteLogGroup
CloudFormation - CREATE_IN_PROGRESS - AWS::IAM::Role - IamRoleLambdaExecution
CloudFormation - CREATE_IN_PROGRESS - AWS::Logs::LogGroup - UpdateLogGroup
CloudFormation - CREATE_IN_PROGRESS - AWS::Logs::LogGroup - ReadLogGroup
CloudFormation - CREATE_IN_PROGRESS - AWS::Logs::LogGroup - SearchByUserLogGroup
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::RestApi - ApiGatewayRestApi
CloudFormation - CREATE_IN_PROGRESS - AWS::Logs::LogGroup - SearchByNotebookLogGroup
CloudFormation - CREATE_IN_PROGRESS - AWS::Logs::LogGroup - CreateLogGroup
CloudFormation - CREATE_IN_PROGRESS - AWS::DynamoDB::Table - notesDynamoDbTable
CloudFormation - CREATE_IN_PROGRESS - AWS::Logs::LogGroup - DeleteLogGroup
CloudFormation - CREATE_IN_PROGRESS - AWS::Logs::LogGroup - ReadLogGroup
CloudFormation - CREATE_COMPLETE - AWS::Logs::LogGroup - DeleteLogGroup
CloudFormation - CREATE_COMPLETE - AWS::Logs::LogGroup - ReadLogGroup
CloudFormation - CREATE_IN_PROGRESS - AWS::Logs::LogGroup - UpdateLogGroup
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::RestApi - ApiGatewayRestApi
CloudFormation - CREATE_IN_PROGRESS - AWS::Logs::LogGroup - SearchByNotebookLogGroup
CloudFormation - CREATE_COMPLETE - AWS::Logs::LogGroup - UpdateLogGroup
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::RestApi - ApiGatewayRestApi
CloudFormation - CREATE_IN_PROGRESS - AWS::IAM::Role - IamRoleLambdaExecution
CloudFormation - CREATE_COMPLETE - AWS::Logs::LogGroup - SearchByNotebookLogGroup
CloudFormation - CREATE_IN_PROGRESS - AWS::Logs::LogGroup - SearchByUserLogGroup
CloudFormation - CREATE_COMPLETE - AWS::Logs::LogGroup - SearchByUserLogGroup
CloudFormation - CREATE_IN_PROGRESS - AWS::Logs::LogGroup - CreateLogGroup
CloudFormation - CREATE_COMPLETE - AWS::Logs::LogGroup - CreateLogGroup
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Resource - ApiGatewayResourceNotebooks
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Resource - ApiGatewayResourceUsers
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Resource - ApiGatewayResourceNotebooks
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Resource - ApiGatewayResourceUsers
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Resource - ApiGatewayResourceUsers
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Resource - ApiGatewayResourceNotebooks
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Resource - ApiGatewayResourceNotes
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Resource - ApiGatewayResourceNotes
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Resource - ApiGatewayResourceNotes
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Resource - ApiGatewayResourceNotebooksIdVar
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Resource - ApiGatewayResourceNotebooksIdVar
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Resource - ApiGatewayResourceUsersIdVar
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Resource - ApiGatewayResourceNotebooksIdVar
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodNotesOptions
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodNotesOptions
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Resource - ApiGatewayResourceNotesIdVar
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Resource - ApiGatewayResourceUsersIdVar
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Resource - ApiGatewayResourceUsersIdVar
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Resource - ApiGatewayResourceNotesIdVar
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Method - ApiGatewayMethodNotesOptions
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Resource - ApiGatewayResourceNotesIdVar
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Resource - ApiGatewayResourceNotebooksIdVarNotes
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Resource - ApiGatewayResourceNotebooksIdVarNotes
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Resource - ApiGatewayResourceNotebooksIdVarNotes
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Resource - ApiGatewayResourceUsersIdVarNotes
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodNotesIdVarOptions
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Resource - ApiGatewayResourceUsersIdVarNotes
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodNotesIdVarOptions
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Resource - ApiGatewayResourceUsersIdVarNotes
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Method - ApiGatewayMethodNotesIdVarOptions
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodNotebooksIdVarNotesOptions
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodNotebooksIdVarNotesOptions
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodUsersIdVarNotesOptions
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Method - ApiGatewayMethodNotebooksIdVarNotesOptions
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodUsersIdVarNotesOptions
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Method - ApiGatewayMethodUsersIdVarNotesOptions
CloudFormation - CREATE_COMPLETE - AWS::IAM::Role - IamRoleLambdaExecution
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Function - SearchByNotebookLambdaFunction
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Function - ReadLambdaFunction
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Function - DeleteLambdaFunction
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Function - SearchByUserLambdaFunction
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Function - CreateLambdaFunction
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Function - UpdateLambdaFunction
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Function - SearchByNotebookLambdaFunction
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Function - DeleteLambdaFunction
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Function - ReadLambdaFunction
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Function - SearchByUserLambdaFunction
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Function - UpdateLambdaFunction
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Function - ReadLambdaFunction
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Function - CreateLambdaFunction
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Function - UpdateLambdaFunction
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Function - SearchByUserLambdaFunction
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Function - SearchByNotebookLambdaFunction
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Function - DeleteLambdaFunction
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Function - CreateLambdaFunction
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodNotesIdVarGet
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodUsersIdVarNotesGet
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Version - UpdateLambdaVersionme0GSR57A876455wY7Pdi8u4NdOo0LEbNI1OVmro
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Version - ReadLambdaVersionkoJsXhmVXXsvU4M577CRsKwjX2IW2M7K92SqasvGhGY
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Permission - SearchByUserLambdaPermissionApiGateway
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodNotesIdVarGet
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Permission - SearchByNotebookLambdaPermissionApiGateway
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Version - CreateLambdaVersioneEbhf2bhMy6KAOM5FngrYXjAJkHysRvPppjTMsoC0
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Permission - ReadLambdaPermissionApiGateway
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodNotesIdVarDelete
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Permission - CreateLambdaPermissionApiGateway
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Version - SearchByNotebookLambdaVersion0wHAl4zuKstuKGq22FXHgUz4EeLBOLeb7jziWyZiuM
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Permission - SearchByUserLambdaPermissionApiGateway
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Method - ApiGatewayMethodNotesIdVarGet
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Permission - ReadLambdaPermissionApiGateway
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodNotebooksIdVarNotesGet
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Permission - SearchByNotebookLambdaPermissionApiGateway
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodNotesIdVarPut
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Permission - CreateLambdaPermissionApiGateway
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodUsersIdVarNotesGet
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Version - DeleteLambdaVersionkhq8jGGlWbwvEpKjtsc8ulaSxsH0EEvDm6ZR8ZTd2s
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodNotesIdVarDelete
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Version - UpdateLambdaVersionme0GSR57A876455wY7Pdi8u4NdOo0LEbNI1OVmro
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodNotebooksIdVarNotesGet
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodNotesIdVarPut
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Version - CreateLambdaVersioneEbhf2bhMy6KAOM5FngrYXjAJkHysRvPppjTMsoC0
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Method - ApiGatewayMethodUsersIdVarNotesGet
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Version - UpdateLambdaVersionme0GSR57A876455wY7Pdi8u4NdOo0LEbNI1OVmro
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Version - CreateLambdaVersioneEbhf2bhMy6KAOM5FngrYXjAJkHysRvPppjTMsoC0
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodNotesPost
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Method - ApiGatewayMethodNotesIdVarDelete
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Method - ApiGatewayMethodNotebooksIdVarNotesGet
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Method - ApiGatewayMethodNotesIdVarPut
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Version - SearchByNotebookLambdaVersion0wHAl4zuKstuKGq22FXHgUz4EeLBOLeb7jziWyZiuM
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Version - ReadLambdaVersionkoJsXhmVXXsvU4M577CRsKwjX2IW2M7K92SqasvGhGY
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Version - SearchByNotebookLambdaVersion0wHAl4zuKstuKGq22FXHgUz4EeLBOLeb7jziWyZiuM
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Version - DeleteLambdaVersionkhq8jGGlWbwvEpKjtsc8ulaSxsH0EEvDm6ZR8ZTd2s
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Method - ApiGatewayMethodNotesPost
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Permission - DeleteLambdaPermissionApiGateway
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Version - ReadLambdaVersionkoJsXhmVXXsvU4M577CRsKwjX2IW2M7K92SqasvGhGY
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Version - DeleteLambdaVersionkhq8jGGlWbwvEpKjtsc8ulaSxsH0EEvDm6ZR8ZTd2s
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Method - ApiGatewayMethodNotesPost
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Permission - DeleteLambdaPermissionApiGateway
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Permission - UpdateLambdaPermissionApiGateway
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Permission - UpdateLambdaPermissionApiGateway
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Version - SearchByUserLambdaVersion8ysaefzCBNVKKZUXqgDt6TZu17QmPDxnziwTn7p0hUI
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Deployment - ApiGatewayDeployment1536542303605
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::Deployment - ApiGatewayDeployment1536542303605
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::Deployment - ApiGatewayDeployment1536542303605
CloudFormation - CREATE_IN_PROGRESS - AWS::Lambda::Version - SearchByUserLambdaVersion8ysaefzCBNVKKZUXqgDt6TZu17QmPDxnziwTn7p0hUI
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Version - SearchByUserLambdaVersion8ysaefzCBNVKKZUXqgDt6TZu17QmPDxnziwTn7p0hUI
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::BasePathMapping - pathmapping
CloudFormation - CREATE_IN_PROGRESS - AWS::ApiGateway::BasePathMapping - pathmapping
CloudFormation - CREATE_COMPLETE - AWS::ApiGateway::BasePathMapping - pathmapping
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Permission - SearchByUserLambdaPermissionApiGateway
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Permission - ReadLambdaPermissionApiGateway
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Permission - SearchByNotebookLambdaPermissionApiGateway
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Permission - CreateLambdaPermissionApiGateway
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Permission - DeleteLambdaPermissionApiGateway
CloudFormation - CREATE_COMPLETE - AWS::Lambda::Permission - UpdateLambdaPermissionApiGateway
CloudFormation - CREATE_COMPLETE - AWS::DynamoDB::Table - notesDynamoDbTable
CloudFormation - UPDATE_COMPLETE_CLEANUP_IN_PROGRESS - AWS::CloudFormation::Stack - stoic-notes-stack-dev
CloudFormation - UPDATE_COMPLETE - AWS::CloudFormation::Stack - stoic-notes-stack-dev
Serverless: Stack update finished...
Service Information
service: notes
stage: dev
region: us-west-2
stack: stoic-notes-stack-dev
api keys:
  None
endpoints:
  POST - https://0lrzqvyna7.execute-api.us-west-2.amazonaws.com/dev/notes
  GET - https://0lrzqvyna7.execute-api.us-west-2.amazonaws.com/dev/notes/{id}
  PUT - https://0lrzqvyna7.execute-api.us-west-2.amazonaws.com/dev/notes/{id}
  DELETE - https://0lrzqvyna7.execute-api.us-west-2.amazonaws.com/dev/notes/{id}
  GET - https://0lrzqvyna7.execute-api.us-west-2.amazonaws.com/dev/users/{id}/notes
  GET - https://0lrzqvyna7.execute-api.us-west-2.amazonaws.com/dev/notebooks/{id}/notes
functions:
  create: notes-dev-create
  read: notes-dev-read
  update: notes-dev-update
  delete: notes-dev-delete
  searchByUser: notes-dev-searchByUser
  searchByNotebook: notes-dev-searchByNotebook

Stack Outputs
DeleteLambdaFunctionQualifiedArn: arn:aws:lambda:us-west-2:750444023825:function:stoic-notes-delete-lambda-dev:12
SearchByUserLambdaFunctionQualifiedArn: arn:aws:lambda:us-west-2:750444023825:function:stoic-notes-search-by-user-lambda-dev:7
CreateLambdaFunctionQualifiedArn: arn:aws:lambda:us-west-2:750444023825:function:stoic-notes-create-lambda-dev:12
DomainName: dx7gtrgmdf73e.cloudfront.net
UpdateLambdaFunctionQualifiedArn: arn:aws:lambda:us-west-2:750444023825:function:stoic-notes-update-lambda-dev:12
SearchByNotebookLambdaFunctionQualifiedArn: arn:aws:lambda:us-west-2:750444023825:function:stoic-notes-search-by-notebook-lambda-dev:7
HostedZoneId: Z2FDTNDATAQYW2
ServiceEndpoint: https://0lrzqvyna7.execute-api.us-west-2.amazonaws.com/dev
ServerlessDeploymentBucketName: stoic-notes-stack-dev-serverlessdeploymentbucket-ozzg3mjemrum
ReadLambdaFunctionQualifiedArn: arn:aws:lambda:us-west-2:750444023825:function:stoic-notes-read-lambda-dev:12

Serverless Domain Manager Summary
Domain Name
  athena-dev.stoicapis.com
Distribution Domain Name
  dx7gtrgmdf73e.cloudfront.net
```

## Deleting

Add the delete commands here

## Testing

Local testing of Lambda functions is a good practice. When testig locally there are some considerations to keep in mind. Find the details here: https://serverless.com/framework/docs/providers/aws/cli-reference/invoke-local/

Talk about Unit Testing here

Talk about Integration Testing here

Talk about considerations for testing like modifying settings and DynamoDB resource definitions

### Create a Note from Local

```bash
sls invoke local -f create --data '{"body": "{ \"text\": \"Do a test, fool!\" }"}'
```

## Usage

You can create, retrieve, update, or delete `notes` with the following commands:

### Create a Note

```bash
curl -X POST https://athena-dev.stoicapis.com/api/notes --data '{ "userId": "m3kan1cal", "notebook": "standard", "text": "Learn Serverless" }'
```

No output

### List all Notes

```bash
curl https://athena-dev.stoicapis.com/api/notes
```

Example output:
```bash
[{"text":"Deploy my first service","userId":"ac90fe80-aa83-11e6-9ede-afdfa051af86","checked":true,"updatedAt":1479139961304},{"text":"Learn Serverless","userId":"20679390-aa85-11e6-9ede-afdfa051af86","createdAt":1479139943241,"checked":false,"updatedAt":1479139943241}]%
```

### Get one Note

```bash
# Replace the <id> part with a real id from your notes table
curl https://athena-dev.stoicapis.com/api/notes/<id>
```

Example Result:
```bash
{"text":"Learn Serverless","userId":"ee6490d0-aa81-11e6-9ede-afdfa051af86","createdAt":1479138570824,"checked":false,"updatedAt":1479138570824}%
```

### Update a Note

```bash
# Replace the <id> part with a real id from your notes table
curl -X PUT https://athena-dev.stoicapis.com/api/notes/<id> --data '{ "text": "Learn Serverless", "checked": true }'
```

Example Result:
```bash
{"text":"Learn Serverless","userId":"ee6490d0-aa81-11e6-9ede-afdfa051af86","createdAt":1479138570824,"checked":true,"updatedAt":1479138570824}%
```

### Delete a Note

```bash
# Replace the <id> part with a real id from your notes table
curl -X DELETE https://athena-dev.stoicapis.com/api/notes/<id>
```

No output

## Scaling

### AWS Lambda

By default, AWS Lambda limits the total concurrent executions across all functions within a given region to 100. The default limit is a safety limit that protects you from costs due to potential runaway or recursive functions during initial development and testing. To increase this limit above the default, follow the steps in [To request a limit increase for concurrent executions](http://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html#increase-concurrent-executions-limit).

### DynamoDB and VPC

We are deploying our microservice to a private VPC managed by our team. This means our Lambda functions will be running in the private VPC they are deployed to. DynamoDB is typically treated as a "public internet" AWS service, which means our Lambda functions can't talk to DynamoDB without some networking configurations. The easiest way to accomplish this is to make create a VPC endpoint for the DynamoDB service, which allows our private VPC to communicate with the DynamoDB service without having to go through the interwebs; we take security and privacy very seriously.

A few things need to be in place for our Lambda functions, in our private VPC, to talk with the DynamoDB service. The steps below are a quickstart approach, but more details can be found here: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/vpc-endpoints-dynamodb.html#vpc-endpoints-dynamodb-tutorial.create-endpoint

- Make sure you have a main routing table in your AWS VPC that allows the proper network traffic.

- Using AWS CLI, verify that DynamoDB is an available service for creating VPC endpoints in the current AWS region.

  ```bash
  aws ec2 describe-vpc-endpoint-services
  
  {
      "ServiceNames": [
          "com.amazonaws.us-east-1.s3",
          "com.amazonaws.us-east-1.dynamodb"
      ]
  }
  ```

- Determine your VPC identifier to build your VPC endpoint in.

  ```bash
  aws ec2 describe-vpcs
  
  {
      "Vpcs": [
          {
              "VpcId": "vpc-0bbc736e", 
              "InstanceTenancy": "default", 
              "State": "available", 
              "DhcpOptionsId": "dopt-8454b7e1", 
              "CidrBlock": "172.31.0.0/16", 
              "IsDefault": true
          }
      ]
  }
  ```

- Create the DynamoDB VPC endpoint.

  ```bash
  aws ec2 create-vpc-endpoint --vpc-id YOUR_VPC_ID --service-name com.amazonaws.YOUR_AWS-REGION.dynamodb --route-table-ids YOUR_ROUTE_TABLE_IDS

  {
      "VpcEndpoint": {
          "VpcEndpointId": "vpce-0f8c1f5da4a1afe69",
          "VpcEndpointType": "Gateway",
          "VpcId": "vpc-9bea4efd",
          "ServiceName": "com.amazonaws.us-west-2.dynamodb",
          "State": "available",
          "PolicyDocument": "{\"Version\":\"2008-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Principal\":\"*\",\"Action\":\"*\",\"Resource\":\"*\"}]}",
          "RouteTableIds": [
              "rtb-0b644314ae3e5d2f1"
          ],
          "SubnetIds": [],
          "Groups": [],
          "PrivateDnsEnabled": false,
          "NetworkInterfaceIds": [],
          "DnsEntries": [],
          "CreationTimestamp": "2018-09-07T00:42:40Z"
      }
  }
  ```

Now you should be good to go, with no other configurations required. Our AWS Lambda functions in our private VPC should now be communicating through AWS network pipes, without going through the interwebs, securely and privately, with DynamoDB.

### DynamoDB Throughput

When you create a table, you specify how much provisioned throughput capacity you want to reserve for reads and writes. DynamoDB will reserve the necessary resources to meet your throughput needs while ensuring consistent, low-latency performance. You can change the provisioned throughput and increasing or decreasing capacity as needed.

This is can be done via settings in the `serverless.yml`.

```yaml
  ProvisionedThroughput:
    ReadCapacityUnits: 1
    WriteCapacityUnits: 1
```

In case you expect a lot of traffic fluctuation we recommend to checkout this guide on how to auto scale DynamoDB [https://aws.amazon.com/blogs/aws/auto-scale-dynamodb-with-dynamic-dynamodb/](https://aws.amazon.com/blogs/aws/auto-scale-dynamodb-with-dynamic-dynamodb/)

### DynamoDB Local

DynamoDB local is a downloadable version of DynamoDB that enables developers to develop and test applications using a version of DynamoDB running in your own development environment.

The new DynamoDB local Docker image (https://hub.docker.com/r/amazon/dynamodb-local/) enables you to get started with DynamoDB local quickly by using a docker image with all the DynamoDB local dependencies and necessary configuration built in. The new Docker image also enables you to include DynamoDB local in your containerized builds and as part of your continuous integration testing.

Using DynamoDB local does not require an internet connection and DynamoDB local works with your existing DynamoDB API calls. There are no provisioned throughput, data storage, or data transfer costs with DynamoDB local. To get it going for development, simply run the following to pull and run:

```bash
docker image pull amazon/dynamodb-local
docker container run -p 8000:8000 -d amazon/dynamodb-local
```

### Route53 and Custom Domains

Before you get going to far here, you need to make sure the following criteria are met:

- An AWS certificate for all domains being used in custom domain must be created for the domains in use.
- The AWS certificate must be in the `us-east-1` region currently to be picked up by the `serverless-domain-manager` plugin.
- The AWS certificate must have the correct domains attached that will be used for the API Gateway.
- In general, if you have a certificate with the `mydomain.com` and `*.mydomain.com` domains then you should be good to proceed with the below.

Pay particular attention to this line in the `serverless.yml` file:

```
domainName: ${self:custom.domains.${self:custom.stage}}"
```

We want to be able to server up multiple microservices under a common base domain. We're using a plugin called `serverless-domain-manager` in combination with the Serverless Framework's powerful variable system to achieve this.
 
We use that variable system to infer the domain name based on the stage. We have three stages in the domains block of the custom section. This will use the given stage to determine which domain to use.

Once this is set up, create a custom domain for each of your stages. This is a one-time setup step and is run with:

```
$ sls create_domain --stage prod
$ sls create_domain --stage test
$ sls create_domain --stage dev
```

Once the domains are set up, you can deploy to the proper stages. Use `sls deploy --stage prod` to deploy to `athena.stoicapis.com` and the other stages to deploy to their respective domains.

Other considerations:

- 
- For specifics, reference this walkthrough: https://serverless.com/blog/serverless-api-gateway-domain/
- To ensure that domains are created for each of the `stage` custom domains, create a custom domain for each `stage` with the instructions near the end of this walkthrough: https://serverless.com/blog/api-gateway-multiple-services/


### Still To Do

- Figure out why handler unit tests are going to remove DynamoDB table
- Update Readme.md with quickstart steps
- Update Readme.md with correct deploy CF outputs and paths
- Document API with meaningful Swagger-specific docs
- Make repo public
- Call out dependencies and assumptions (like what is already installed and not part of this tutorial: Docker, python, pipenv)