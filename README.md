<!--
title: AWS Serverless REST API with DynamoDB store example in Python
description: This example demonstrates how to setup a RESTful Web Service allowing you to create, list, get, update and delete Todos. DynamoDB is used to store the data.
layout: Doc
-->
# Serverless REST API

This example demonstrates how to setup a [RESTful Web Services](https://en.wikipedia.org/wiki/Representational_state_transfer#Applied_to_web_services) allowing you to create, list, get, update and delete Todos. DynamoDB is used to store the data. This is just an example and of course you could use any data storage as a backend.

## Structure

This service has a separate directory for all the todo operations. For each operation exactly one file exists e.g. `todos/delete.py`. In each of these files there is exactly one function defined.

The idea behind the `todos` directory is that in case you want to create a service containing multiple resources e.g. users, notes, comments you could do so in the same service. While this is certainly possible you might consider creating a separate service for each resource. It depends on the use-case and your preference.

## Use-cases

- API for a Web Application
- API for a Mobile Application

## Setup

```bash
npm install -g serverless
```

## Deploy

In order to deploy the endpoint simply run

```bash
serverless deploy
```

The expected result should be similar to:

```bash
Serverless: Packaging service…
Serverless: Uploading CloudFormation file to S3…
Serverless: Uploading service .zip file to S3…
Serverless: Updating Stack…
Serverless: Checking Stack update progress…
Serverless: Stack update finished…

Service Information
service: serverless-rest-api-with-dynamodb
stage: dev
region: us-west-2
api keys:
  None
endpoints:
  POST - https://45wf34z5yf.execute-api.us-west-2.amazonaws.com/dev/todos
  GET - https://45wf34z5yf.execute-api.us-west-2.amazonaws.com/dev/todos
  GET - https://45wf34z5yf.execute-api.us-west-2.amazonaws.com/dev/todos/{id}
  PUT - https://45wf34z5yf.execute-api.us-west-2.amazonaws.com/dev/todos/{id}
  DELETE - https://45wf34z5yf.execute-api.us-west-2.amazonaws.com/dev/todos/{id}
functions:
  serverless-rest-api-with-dynamodb-dev-update: arn:aws:lambda:us-west-2:488110005556:function:serverless-rest-api-with-dynamodb-dev-update
  serverless-rest-api-with-dynamodb-dev-get: arn:aws:lambda:us-west-2:488110005556:function:serverless-rest-api-with-dynamodb-dev-get
  serverless-rest-api-with-dynamodb-dev-list: arn:aws:lambda:us-west-2:488110005556:function:serverless-rest-api-with-dynamodb-dev-list
  serverless-rest-api-with-dynamodb-dev-create: arn:aws:lambda:us-west-2:488110005556:function:serverless-rest-api-with-dynamodb-dev-create
  serverless-rest-api-with-dynamodb-dev-delete: arn:aws:lambda:us-west-2:488110005556:function:serverless-rest-api-with-dynamodb-dev-delete
```

## Testing

Local testing of Lambda functions is a good practice. When testig locally there are some considerations to keep in mind. Find the details here: https://serverless.com/framework/docs/providers/aws/cli-reference/invoke-local/

### Create a Todo from Local

```bash
sls invoke local -f create --data '{"body": "{ \"text\": \"Do a test, fool!\" }"}'
```

## Usage

You can create, retrieve, update, or delete `todos` with the following commands:

### Create a Todo

```bash
curl -X POST https://stoic-dev.caasapis.com/api/todos --data '{ "text": "Learn Serverless" }'
```

No output

### List all Todos

```bash
curl https://stoic-dev.caasapis.com/api/todos
```

Example output:
```bash
[{"text":"Deploy my first service","id":"ac90fe80-aa83-11e6-9ede-afdfa051af86","checked":true,"updatedAt":1479139961304},{"text":"Learn Serverless","id":"20679390-aa85-11e6-9ede-afdfa051af86","createdAt":1479139943241,"checked":false,"updatedAt":1479139943241}]%
```

### Get one Todo

```bash
# Replace the <id> part with a real id from your todos table
curl https://stoic-dev.caasapis.com/api/todos/<id>
```

Example Result:
```bash
{"text":"Learn Serverless","id":"ee6490d0-aa81-11e6-9ede-afdfa051af86","createdAt":1479138570824,"checked":false,"updatedAt":1479138570824}%
```

### Update a Todo

```bash
# Replace the <id> part with a real id from your todos table
curl -X PUT https://stoic-dev.caasapis.com/api/todos/<id> --data '{ "text": "Learn Serverless", "checked": true }'
```

Example Result:
```bash
{"text":"Learn Serverless","id":"ee6490d0-aa81-11e6-9ede-afdfa051af86","createdAt":1479138570824,"checked":true,"updatedAt":1479138570824}%
```

### Delete a Todo

```bash
# Replace the <id> part with a real id from your todos table
curl -X DELETE https://stoic-dev.caasapis.com/api/todos/<id>
```

No output

## Scaling

### AWS Lambda

By default, AWS Lambda limits the total concurrent executions across all functions within a given region to 100. The default limit is a safety limit that protects you from costs due to potential runaway or recursive functions during initial development and testing. To increase this limit above the default, follow the steps in [To request a limit increase for concurrent executions](http://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html#increase-concurrent-executions-limit).

### DynamoDB

When you create a table, you specify how much provisioned throughput capacity you want to reserve for reads and writes. DynamoDB will reserve the necessary resources to meet your throughput needs while ensuring consistent, low-latency performance. You can change the provisioned throughput and increasing or decreasing capacity as needed.

This is can be done via settings in the `serverless.yml`.

```yaml
  ProvisionedThroughput:
    ReadCapacityUnits: 1
    WriteCapacityUnits: 1
```

In case you expect a lot of traffic fluctuation we recommend to checkout this guide on how to auto scale DynamoDB [https://aws.amazon.com/blogs/aws/auto-scale-dynamodb-with-dynamic-dynamodb/](https://aws.amazon.com/blogs/aws/auto-scale-dynamodb-with-dynamic-dynamodb/)

### Route53 and Custom Domains

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

Once the domains are set up, you can deploy to the proper stages. Use `sls deploy --stage prod` to deploy to `stoic.caasapis.com` and the other stages to deploy to their respective domains.

## Dependencies and Considerations

### DynamoDB Local

DynamoDB local is a downloadable version of DynamoDB that enables developers to develop and test applications using a version of DynamoDB running in your own development environment.

The new DynamoDB local Docker image (https://hub.docker.com/r/amazon/dynamodb-local/) enables you to get started with DynamoDB local quickly by using a docker image with all the DynamoDB local dependencies and necessary configuration built in. The new Docker image also enables you to include DynamoDB local in your containerized builds and as part of your continuous integration testing.

Using DynamoDB local does not require an internet connection and DynamoDB local works with your existing DynamoDB API calls. There are no provisioned throughput, data storage, or data transfer costs with DynamoDB local. To get it going for development, simply run the following to pull and run:

```bash
docker pull amazon/dynamodb-local
docker run -p 8000:8000 amazon/dynamodb-local
```

* Route53 domain configuration
* AWS Certificate for all domains being used in custom domain
* AWS credentials configured with correct permission
* Pipenv installed and configured
* Python and Node.js installed and configured
* Serverless plugins installed and configured
* npm plugins installed and configured
