[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![GitHub release](https://img.shields.io/github/release/stoicbear/serverless-awsapi.svg)](https://gitHub.com/stoicbear/serverless-awsapi/releases/)
![](https://codebuild.us-west-2.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiaEtybCttRW4yMHBMUnhLelluU0E4R2huM2dzRUJ3d3A3RnRRaTVSVUk1L3l4aUhWRWlPVHNraG50ZWlTbjdybzVCcS9UcVdBUy9waDN1Vm8xcFhDNUZZPSIsIml2UGFyYW1ldGVyU3BlYyI6Im5ZQkRibzkzUUpMWXRoemkiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

# Serverless Microservice via REST API with DynamoDB Store in Python

This project demonstrates how to setup a **Microservice & RESTful API** for a Note-taking app, using the Serverless framework and AWS, allowing you to create, search, read, update and delete Notes. DynamoDB is used to store the data. This is only an example; you could use any data model or data store as a backend in true microservice fashion.

After all is said and done, we'll end up with a microservice and API (contrary to some beliefs, they are not the same thing!). The end result is a self-contained, web-accessible microservice that is small, testable, customizable, scalable, resilient, monitor-able, clone-able, stateless, and fairly simple.

It can be served up as multiple Lambda functions unified under a common domain (multiple microservices behind one API proxy domain so consumers only need to remember one domain, regardless of how many functions and API Gateway endpoints exist). And we try to stick with the pattern of one service, one model, and one API.

It's built with some love using the following stack and tooling:

- AWS (Lambda, API Gateway, CloudFormation, CloudFront, CloudWatch, DynamoDB, IAM, Route53, Certificate Manager, VPC Endpoints)
- [Serverless framework](https://serverless.com/framework/docs/providers/aws/guide/quick-start/)
- [Docker](https://www.docker.com/get-started)
- [Pipenv](https://pipenv.readthedocs.io/)
- [Python 3.6](https://www.python.org/downloads/)
- [Visual Studio Code](https://code.visualstudio.com/download)

## Getting Dependencies

### Docker
You only need the community version, but you can pick which you want: https://www.docker.com/get-started. This is to be able to run DynamoDB Local for development and testing purposes.

### Python 3 and Pipenv
This microservice is built on a Python-based stack. Make sure you have an interpreter installed somewhere you can reference. Get one here: https://www.python.org/downloads/. Also, get Pipenv for a seamless `pip` and `virtualenv` experience. Get it here: https://pipenv.readthedocs.io/.

Note: if you want to follow the [Docker TLDR: (aka Quickstart)](#docker-tldr-aka-quickstart) then this step is not needed.

### Node.js and npm
We're using the Serverless framework with and AWS provider specified. It's built on Node.js, so we'll need it for some CLI commands. Get it here: https://nodejs.org/en/download/.

Note: if you want to follow the [Docker TLDR: (aka Quickstart)](#docker-tldr-aka-quickstart) then this step is not needed.

### Plugins Installed and Configured

Serverless relies on Node.js and npm for package management. Make sure to have Node.js and npm installed and configured for us. To ensure all Node.js packages are installed run `npm install`.

Note: if you want to follow the [Docker TLDR: (aka Quickstart)](#docker-tldr-aka-quickstart) then this step is not needed.

### AWS Account and Credentials
This an AWS Lambda, API Gateway microservice. Makes sure you have an account and you've configured your `~/.aws.credentials` with an access ID and secret. For simplicity, give the IAM user admin access, but fine-tune for production deployments.

## Project Structure

This service has a separate directory for all the Note service operations, the functions. For each operation exactly one file exists e.g. `functions/delete.py`. In each of these files there is exactly one function defined, the handler.

The idea behind the `functions` directory is that in case you want to create a service containing multiple resources e.g. users, notes, comments you could do so in the same service. While this is certainly possible you might consider creating a separate service for each resource. It depends on the use-case and your preference.

## Use-Cases

- API for a Web app
- API for a Mobile app
- API for IoT apps
- API for system-to-system interactions

## Docker TLDR: (aka Quickstart)

If you're a fan of using Docker for spinning up quick development environments, and you alredy have it installed, then there is a shorter path to being able to try out this project.

1. Build the Docker image based on the Dockerfile contained in this project.

    ```bash
    docker image build -t stoictechgroup/stoic-serverless-awsapi .
    ```

2. Make sure the `docker-run.sh` file is executable, then run the following command where the parameter passed at the end is the command you want your container to run, including any `serverless` or `sls` commands.

    ```bash
    ./docker-run.sh "sls --version"
    ```

3. Now jump down to [Normal TLDR; (aka Quickstart)](#normal-tldr-aka-quickstart) step 6, and go from there, injecting any command called out in to your Serverless-ready Docker container prompt.

4. Note that when calling `pytest` you may want to use `pipenv run pytest` instead, since you don't really need to create a virtual environment inside of your container. No need to go ["inception"](https://www.imdb.com/title/tt1375666/) on it.

## Normal TLDR; (aka Quickstart)

1. Time to install the Serverless framework.

    ```bash
    npm install -g serverless
    ```

    Verify that a current version is installed.

    ```bash
    serverless --version
    ```

2. If you've already installed the pre-requisites already listed, including the Serverless framework, then you're ready to clone this repository.

    ```bash
    git clone ssh://git@ssh.github.com:443/stoicbear/serverless-awsapi.git
    ```

3. Install `npm` packages and dependencies.

    ```bash
    npm i
    ```

4. Create a virtual environment and install Python dependencies, including `dev`.

    ```bash
    cd ~/stoic-serverless-awsapi
    pipenv install --dev
    ```

5. Activate your virtual environment.

    ```bash
    pipenv shell
    ```

6. Get the DynamoDB Local Docker image and start a container following the steps here: [DynamoDB Local](#dynamodb-local)

7. Now, check your tests configuration file at `/tests/config.yml` and make sure all values are set to your preference.

    ```bash
    vim ./tests/config.yml
    ```

8. Change the API url fixture values in `./tests/api/__init__.py` to match what your domain should be.

    ```bash
    vim ./tests/api/__init__.py
    ```

9. Run the unit tests to verify they are passing.

    ```bash
    pytest tests/unit
    ```

10. If the unit tests are passing, you're almost ready to start deploying. First, make sure you're set with Route53, a custom domain, and DNS by following the instructions here: [Route53 and Custom Domains](#route53-and-custom-domains)

11. Next, get your DynamoDB VPC Endpoint created using the steps here: [DynamoDB and VPC Endpoints](#dynamodb-and-vpc-endpoints). We favor a VPC endpoint because our data is important; we care about privacy and security.

12. We're now just about ready to deploy using the Serverless framework to our AWS provider. It's time to double check the values in the `serverless.yml` file in our project. Open up the file and sweep through to make sure the AWS region and other settings are valid. Pay particular attention to the service name, tags, VPC groups, subnets, region, resource names, custom domains, stages, and anything else you may want to customize.

    ```bash
    vim ./serverless.yml
    ```

13. Once you're done with your review of `serverless.yml` (the real magic behind this microservice), you're ready to deploy. Let's deploy to the `Dev` stage. We're using a named profile for AWS named `stoic`, but you may not need to.

    ```bash
    sls deploy -v --aws-profile stoic --stage dev
    ```

14. At this point, we should be seeing CloudFormation activity and messages indicating success that our resources were deployed. To verify, it's time to run the integration tests against the API endpoints that are exposed through API Gateway.

    ```bash
    pytest tests/api
    ```

15. If all our tests are passing now, then we have a working microservice with an interface via API Gateway. Now you can deploy to our `test` and `prod` stages to simulate what it would be like in a production environment.

From here, you can choose your own adventure: 1) play around with the API with `curl` or Postman, 2) maybe customize the data model or data store, 3) explore what it would take to add a Lambda authorizer to secure our endpoints, 4) start exploring Lambda event triggers to build a state machine, or 5) create another business-capable service that can work with our note-taking service to round out a more complete app.

This is the end of the [TLDR;](#tldr-aka-quickstart;) walkthrough. It's all details from here on out.

## Deploying to AWS

In order to deploy the endpoint, creating a CloudFormation stack in the process, simply run the below commands, where YOUR_PROFILE is the profile to use in your AWS CLI configured credentials file and YOUR_STAGE is the stage in API Gateway that you're deploying to.

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
..........
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

When we're done with this project, or if we need to make changes to resources that can't be handled by simply updating the `serverless.yml` file (via CloudFormation and Serverless framework), we may find that we need to remove the stack that we've created and then redeploy. Follow these steps to clean up, where YOUR_PROFILE is the profile to use in your AWS CLI configured credentials file and YOUR_STAGE is the stage in API Gateway that you're deploying to.

```bash
sls remove -v --aws-profile YOUR_PROFILE --stage YOUR_STAGE
```

After our stack is removed, along with the resources it created, we're going to have to manually remove the DynamoDB table it spun up. Do that now.

Once DynamoDB is removed, if we're aiming to completely remove any artifacts attached to this project, we're also going to need to remove the Route53 hosted zones, TLS certificates in `us-east-1`, and the VPC Endpoints that were configured outside of the scope of the CloudFormation stack.

## Unit, Integration & Automated API Testing

Get the DynamoDB Local Docker image and start a container following the steps here: [DynamoDB Local](#dynamodb-local). Now, check your tests configuration file at `/tests/config.yml` and make sure all values are set to your preference.

```bash
vim ./tests/config.yml
```

Change the API url fixture values in `./tests/api/__init__.py` to match what your domain should be.

```bash
vim ./tests/api/__init__.py
```

Run the unit tests to verify they are passing.

```bash
pytest tests/unit
```

If you've already deployed the AWS resources, it's time to run the integration tests against the API endpoints that are exposed through API Gateway.

```bash
pytest tests/api
```

If all our tests are passing now, then we have a working microservice with an interface via API Gateway.

## Serverless "Invoke" Testing

Local and remote testing of Lambda functions is a good practice, especially when developing, using the Serverless framework. 

When testing locally there are some considerations to keep in mind. Find the details here: https://serverless.com/framework/docs/providers/aws/cli-reference/invoke-local/. This method is fantastic for debugging; if you're getting environment variable exceptions, be sure to check the `serverless.yml` for which vars you need to have set.

When testing remotely, find the details here: https://serverless.com/framework/docs/providers/aws/cli-reference/invoke/

## Usage of Microservice / API

We can create, read, update, delete or search `notes` with the following commands.

### Create a Note

With API:

```bash
curl -X POST https://athena-dev.stoicapis.com/api/notes --data '{ "userId": "m3kan1cal", "notebook": "standard", "text": "Learn Serverless" }'

---response---

{"noteId": "UnpyiOkHQdChUghQX35uzA", "userId": "m3kan1cal", "notebook": "standard", "text": "Learn Serverless", "createdAt": 1536850636242, "updatedAt": 1536850636242}
```

With `sls` local:

```bash
sls invoke local -f create --data '{"body": "{\"userId\": \"m3kan1cal\", \"notebook\": \"standard\", \"text\": \"Do a test, fool!\"}"}'

---response---

{
    "isBase64Encoded": false,
    "statusCode": 201,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": "{\"noteId\": \"Q7wCwFCXQPmzKPScaEFKDw\", \"userId\": \"m3kan1cal\", \"notebook\": \"standard\", \"text\": \"Do a test, fool!\", \"createdAt\": 1536850788457, \"updatedAt\": 1536850788457}"
}
```

### Read a Note

With API:

```bash
# Replace the <id> part with a real id from your notes table
curl -X GET https://athena-dev.stoicapis.com/api/notes/Q7wCwFCXQPmzKPScaEFKDw

---response---

{"createdAt": 1536850788457, "text": "Do a test, fool!", "noteId": "Q7wCwFCXQPmzKPScaEFKDw", "notebook": "standard", "userId": "m3kan1cal", "updatedAt": 1536850788457}
```

With `sls` local:

```bash
sls invoke local -f read --data '{"pathParameters": {"id": "Q7wCwFCXQPmzKPScaEFKDw"}}'

---response---

{
    "isBase64Encoded": false,
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": "{\"createdAt\": 1536850788457, \"text\": \"Do a test, fool!\", \"noteId\": \"Q7wCwFCXQPmzKPScaEFKDw\", \"notebook\": \"standard\", \"userId\": \"m3kan1cal\", \"updatedAt\": 1536850788457}"
}
```

### Update a Note

```bash
# Replace the <id> part with a real id from your notes table
curl -X PUT https://athena-dev.stoicapis.com/api/notes/Q7wCwFCXQPmzKPScaEFKDw --data '{ "userId": "m3kan1cal", "notebook": "standard", "text": "Learn Serverless updated just now!" }'

---response---

{"createdAt": 1536850788457, "text": "Learn Serverless updated just now!", "noteId": "Q7wCwFCXQPmzKPScaEFKDw", "notebook": "standard", "updatedAt": 1536853504858, "userId": "m3kan1cal"}
```

With `sls` local:

```bash
sls invoke local -f update --data '{"pathParameters": {"id": "Q7wCwFCXQPmzKPScaEFKDw"}, "body": "{\"userId\": \"m3kan1cal\", \"notebook\": \"standard\", \"text\": \"Do a test, fool! Updated!\"}"}'

---response---

{
    "isBase64Encoded": false,
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": "{\"createdAt\": 1536850788457, \"text\": \"Do a test, fool! Updated!\", \"noteId\": \"Q7wCwFCXQPmzKPScaEFKDw\", \"notebook\": \"standard\", \"updatedAt\": 1536853630517, \"userId\": \"m3kan1cal\"}"
}
```

### Delete a Note

```bash
# Replace the <id> part with a real id from your notes table
curl -X DELETE https://athena-dev.stoicapis.com/api/notes/Q7wCwFCXQPmzKPScaEFKDw

---response---

{}
```

With `sls` local:

```bash
sls invoke local -f delete --data '{"pathParameters": {"id": "Q7wCwFCXQPmzKPScaEFKDw"}}'

---response---

{
    "isBase64Encoded": false,
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": "{}"
}
```

### Search all Notes from User

```bash
curl -X GET https://athena-dev.stoicapis.com/api/users/azrael/notes

---response---

[{"text": "Learn Serverless", "noteId": "CApwr0rITSyrb6OSLdzWhQ", "notebook": "standard", "userId": "m3kan1cal"}, {"text": "Learn Serverless", "noteId": "UnpyiOkHQdChUghQX35uzA", "notebook": "standard", "userId": "m3kan1cal"}]
```

With `sls` local:

```bash
sls invoke local -f searchByUser --data '{"pathParameters": {"id": "m3kan1cal"}}'

---response---

{
    "isBase64Encoded": false,
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": "[{\"text\": \"Learn Serverless\", \"noteId\": \"CApwr0rITSyrb6OSLdzWhQ\", \"notebook\": \"standard\", \"userId\": \"m3kan1cal\"}, {\"text\": \"Learn Serverless\", \"noteId\": \"UnpyiOkHQdChUghQX35uzA\", \"notebook\": \"standard\", \"userId\": \"m3kan1cal\"}]"
}
```

### Search all Notes from Notebook

```bash
curl -X GET https://athena-dev.stoicapis.com/api/notebooks/standard/notes

---response---

[{"text": "Learn Serverless", "noteId": "CApwr0rITSyrb6OSLdzWhQ", "notebook": "standard", "userId": "m3kan1cal"}, {"text": "Learn Serverless", "noteId": "UnpyiOkHQdChUghQX35uzA", "notebook": "standard", "userId": "m3kan1cal"}]
```

With `sls` local:

```bash
sls invoke local -f searchByNotebook --data '{"pathParameters": {"id": "standard"}}'

---response---

{
    "isBase64Encoded": false,
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": "[{\"text\": \"Learn Serverless\", \"noteId\": \"CApwr0rITSyrb6OSLdzWhQ\", \"notebook\": \"standard\", \"userId\": \"m3kan1cal\"}, {\"text\": \"Learn Serverless\", \"noteId\": \"UnpyiOkHQdChUghQX35uzA\", \"notebook\": \"standard\", \"userId\": \"m3kan1cal\"}]"
}
```

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
