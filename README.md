<!--
title: AWS Serverless REST API with DynamoDB store in Python
description: This example demonstrates how to setup a RESTful Web Service allowing you to create, list, get, update and delete Notes. DynamoDB is used to store the data.
layout: Doc
-->
# Serverless Microservice via REST API

This example demonstrates how to setup a [RESTful Web API](https://en.wikipedia.org/wiki/Representational_state_transfer#Applied_to_web_services) interface to expose a Note-taking microserivce, allowing you to create, search, read, update and delete Notes. DynamoDB is used to store the data. This is just an example and, of course, you could use any data model or data store as a backend in true microservice fashion.

## Getting Dependencies

### Docker
You only need the community version, but you can pick which you want: https://www.docker.com/get-started 

This is to be able to run DynamoDB Local for development and testing purposes.

### Python 3 and Pipenv
This microservice is built on a Python-based stack. Make sure you have an interpreter installed somewhere you can reference. Get one here: https://www.python.org/downloads/ 

Also, get Pipenv for a seamless `pip` and `virtualenv` experience. Get it here: https://pipenv.readthedocs.io/

### Node.js and npm
We're using the Serverless framework with and AWS provider specified. It's built on Node.js, so we'll need it for some CLI commands. Get it here: https://nodejs.org/en/download/

### AWS Account and Credentials
This an AWS Lambda, API Gateway microservice. Makes sure you have an account and you've configured your `~/.aws.credentials` with an access ID and secret. For simplicity, give the IAM user admin access, but fine-tune for production deployments.

### Plugins Installed and Configured

Serverless relies on Node.js and npm for package management. Make sure to have Node.js and npm installed and configured for us. To ensure all Node.js packages are installed run `npm install`.

## Project Structure

This service has a separate directory for all the Note service operations, the functions. For each operation exactly one file exists e.g. `functions/delete.py`. In each of these files there is exactly one function defined, the handler.

The idea behind the `functions` directory is that in case you want to create a service containing multiple resources e.g. users, notes, comments you could do so in the same service. While this is certainly possible you might consider creating a separate service for each resource. It depends on the use-case and your preference.

## End Result Microservice

The end result is a self-contained, web-accessible microservice that is small, testable, customizable, scalable, resilient, monitor-able, clone-able, stateless, and fairly simple.

It can be served up as multiple Lambda functions unified under a common domain (multiple APIs but one API proxy domain so consumers only need to remember one domain, regardless of how many functions and API Gateway endpoints exist). And we try to stick with the pattern of one service, one model, one service.

It's built with some love using the following stack and tooling: 

- AWS (Lambda, API Gateway, CloudFormation, CloudFront, CloudWatch, DynamoDB, IAM, Route53, Certificate Manager, VPC Endpoints)
- [Serverless framework](https://serverless.com/framework/docs/providers/aws/guide/quick-start/)
- [Docker](https://www.docker.com/get-started)
- [Pipenv](https://pipenv.readthedocs.io/)
- [Python 3.6](https://www.python.org/downloads/)
- [Visual Studio Code](https://code.visualstudio.com/download)

## Use-Cases

- API for a Web app
- API for a Mobile app
- API for IoT apps
- API for system-to-system interactions

## Setup Serverless

```bash
npm install -g serverless
```

Verify that a current version is installed.

```bash
serverless --version
```

## TLDR; (aka Quickstart)

If you've already installed the pre-requisites already listed, including the Serverless framework, then you're ready to clone this repository.

```bash
git clone ssh://git@altssh.bitbucket.org:443/m3kan1cal/stoic-serverless-awsapi.git
```

Install `npm` packages and dependencies.

```bash
npm i
```

Create a virtual environment and install Python dependencies.

```bash
cd ~/stoic-serverless-awsapi
pipenv install
```

Activate your virtual environment.

```bash
pipenv shell
```

Get the DynamoDB Local Docker image and start a container following the steps here: [DynamoDB Local](#dynamodb-local)

Now, check your tests configuration file at `/tests/config.yml` and make sure all values are set to your preference.

```bash
vim ./tests/config.yml
```

Change the API url fixture values in `./tests/rest/__init__.py` to match what your domain should be.

```bash
vim ./tests/rest/__init__.py
```

Run the unit tests to verify they are passing.

```bash
pytest tests/unit
```

If the unit tests are passing, you're almost ready to start deploying. First, make sure you're set with Route53, a custom domain, and DNS by following the instructions here: [Route53 and Custom Domains](#route53-and-custom-domains)

Next, get your DynamoDB VPC Endpoint created using the steps here: [DynamoDB and VPC Endpoints](#dynamodb-and-vpc-endpoints). We favor a VPC endpoint because our data is important; we care about privacy and security.

We're now just about ready to deploy using the Serverless framework to our AWS provider. It's time to double check the values in the `serverless.yml` file in our project. Open up the file and sweep through to make sure the AWS region and other settings are valid. Pay particular attention to the service name, tags, VPC groups, subnets, region, resource names, custom domains, stages, and anything else you may want to customize.

```bash
vim ./serverless.yml
```

Once you're done with your review of `serverless.yml` (the real magic behind this microservice), you're ready to deploy. Let's deploy to the `dev` stage. We're using a named profile for AWS named `stoic`, but you may not need to.

```bash
sls deploy -v --aws-profile stoic --stage dev
```

At this point, we should be seeing CloudFormation activity and messages indicating success that our resources were deployed. To verify, it's time to run the integration tests against the API endpoints that are exposed through API Gateway.

```bash
pytest tests/rest
```

If all our tests are passing now, then we have a working microservice with an interface via API Gateway. Now you can deploy to our `test` and `prod` stages to simulate what it would be like in a production environment.

From here, you can choose your own adventure: 1) maybe customize the data model or data store, 2) explore what it would take to add a Lambda authorizer to secure our endpoints, 3) start exploring Lambda event triggers to build a state machine, or 4) create another business-capable service that can work with our note-taking service to round out a more complete app.

This is the end of the [TLDR;](#tldr-aka-quickstart;) walkthrough. It's all details from here on out.

## Deploying to AWS

In order to deploy the endpoint, creating a CloudFormation stack in the process, simply run:

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

## Cleaning Up After Ourselves

Add the delete commands here

Manually delete DynammoDB and VPC Endpoint

Manually delete the Route53 and certs

## Unit, Integration & Automated API Testing

Get the DynamoDB Local Docker image and start a container following the steps here: [DynamoDB Local](#dynamodb-local). Now, check your tests configuration file at `/tests/config.yml` and make sure all values are set to your preference.

```bash
vim ./tests/config.yml
```

Change the API url fixture values in `./tests/rest/__init__.py` to match what your domain should be.

```bash
vim ./tests/rest/__init__.py
```

Run the unit tests to verify they are passing.

```bash
pytest tests/unit
```

If you've already deployed the AWS resources, it's time to run the integration tests against the API endpoints that are exposed through API Gateway.

```bash
pytest tests/rest
```

If all our tests are passing now, then we have a working microservice with an interface via API Gateway.

Local testing of Lambda functions is a good practice. When testig locally there are some considerations to keep in mind. Find the details here: https://serverless.com/framework/docs/providers/aws/cli-reference/invoke-local/. This method is fantastic for debugging; if you're getting environment variable exceptions, be sure to check the `serverless.yml` for which vars you need to have set.

## Usage of Microservice / API

You can create, read, update, delete or search `notes` with the following commands.

### Create a Note

With API:

```bash
curl -X POST https://athena-dev.stoicapis.com/api/notes --data '{ "userId": "m3kan1cal", "notebook": "standard", "text": "Learn Serverless" }'
```

With `sls` local:

```bash
sls invoke local -f create --data '{"body": "{ \"text\": \"Do a test, fool!\" }"}'
```

### Read a Note

With API:

```bash
# Replace the <id> part with a real id from your notes table
curl https://athena-dev.stoicapis.com/api/notes/<id>

{"text":"Learn Serverless","userId":"ee6490d0-aa81-11e6-9ede-afdfa051af86","createdAt":1479138570824,"checked":false,"updatedAt":1479138570824}%
```

With `sls` local:

### Update a Note

```bash
# Replace the <id> part with a real id from your notes table
curl -X PUT https://athena-dev.stoicapis.com/api/notes/<id> --data '{ "text": "Learn Serverless", "checked": true }'

{"text":"Learn Serverless","userId":"ee6490d0-aa81-11e6-9ede-afdfa051af86","createdAt":1479138570824,"checked":true,"updatedAt":1479138570824}%
```

With `sls` local:

### Delete a Note

```bash
# Replace the <id> part with a real id from your notes table
curl -X DELETE https://athena-dev.stoicapis.com/api/notes/<id>
```

With `sls` local:

### Search all Notes from User

```bash
curl https://athena-dev.stoicapis.com/api/notes

[{"text":"Deploy my first service","userId":"ac90fe80-aa83-11e6-9ede-afdfa051af86","checked":true,"updatedAt":1479139961304},{"text":"Learn Serverless","userId":"20679390-aa85-11e6-9ede-afdfa051af86","createdAt":1479139943241,"checked":false,"updatedAt":1479139943241}]%
```

With `sls` local:

### Search all Notes from Notebook

```bash
curl https://athena-dev.stoicapis.com/api/notes

[{"text":"Deploy my first service","userId":"ac90fe80-aa83-11e6-9ede-afdfa051af86","checked":true,"updatedAt":1479139961304},{"text":"Learn Serverless","userId":"20679390-aa85-11e6-9ede-afdfa051af86","createdAt":1479139943241,"checked":false,"updatedAt":1479139943241}]%
```

With `sls` local:

## Scaling

### AWS Lambda

By default, AWS Lambda limits the total concurrent executions across all functions within a given region to 100. The default limit is a safety limit that protects you from costs due to potential runaway or recursive functions during initial development and testing. To increase this limit above the default, follow the steps in [To request a limit increase for concurrent executions](http://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html#increase-concurrent-executions-limit).

## DynamoDB

### DynamoDB and VPC Endpoints

We are deploying our microservice to a private VPC managed by our team. This means our Lambda functions will be running in the private VPC they are deployed to. DynamoDB is typically treated as a "public internet" AWS service, which means our Lambda functions can't talk to DynamoDB without some networking configurations. The easiest way to accomplish this is to make create a VPC endpoint for the DynamoDB service, which allows our private VPC to communicate with the DynamoDB service without having to go through the interwebs; we take security and privacy very seriously.

A few things need to be in place for our Lambda functions, in our private VPC, to talk with the DynamoDB service. The steps below are a quickstart approach, but more details can be found here: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/vpc-endpoints-dynamodb.html#vpc-endpoints-dynamodb-tutorial.create-endpoint

Make sure you have a main routing table in your AWS VPC that allows the proper network traffic. Using AWS CLI, verify that DynamoDB is an available service for creating VPC endpoints in the current AWS region.

```bash
aws ec2 describe-vpc-endpoint-services

{
    "ServiceNames": [
        "com.amazonaws.us-west-2.s3",
        "com.amazonaws.us-west-2.dynamodb"
    ]
}
```

Determine your VPC identifier to build your VPC endpoint in.

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

Create the DynamoDB VPC endpoint.

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

## Route53 and Custom Domains

Before you get going to far here, you need to make sure the following criteria are met:

- An AWS certificate for all domains being used in custom domain must be created for the domains in use.
- The AWS certificate **MUST** be in the `us-east-1` region currently to be picked up by the `serverless-domain-manager` plugin.
- The AWS certificate must have the correct domains attached that will be used for the API Gateway.
- In general, if you have a certificate with the `mydomain.com` and `*.mydomain.com` domains attached to it then you should be good to proceed with the below.

Pay particular attention to this line in the `serverless.yml` file:

```
domainName: ${self:custom.domains.${self:custom.stage}}"
```

We want to be able to server up multiple microservices under a common base domain. We're using a plugin called `serverless-domain-manager` in combination with the Serverless Framework's powerful variable system to achieve this.
 
We use that variable system to infer the domain name based on the stage. We have three stages in the domains block of the custom section. This will use the given stage to determine which domain to use.

Once this is set up, create a custom domain for each of your stages. This is a one-time setup step and is run with:

```
$ sls create_domain --stage dev --profile stoic
$ sls create_domain --stage test --profile stoic
$ sls create_domain --stage prod --profile stoic
```

Once the domains are set up, you can deploy to the proper stages. Use `sls deploy --stage prod` to deploy to `athena.stoicapis.com` and the other stages to deploy to their respective domains. Adjust the settings in this service for your own configuration, including the domain you'll use.

Other considerations:

- For specifics, reference this walkthrough: https://serverless.com/blog/serverless-api-gateway-domain/
- To ensure that domains are created for each of the `stage` custom domains, create a custom domain for each `stage` with the instructions near the end of this walkthrough: https://serverless.com/blog/api-gateway-multiple-services/
