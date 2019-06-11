# intro_bot

Tweet bot executed by AWS Lambda
https://twitter.com/intro_tweetbot

Except `lambda_function.py` and `webscrape.py`, all files and directories are packages for executing by AWS Lambda.

# how to deploy

You must already have `aws-cli` installed and also have configured with the `aws configure` command.


Execute this command.

```shell
$ sh deploy.sh lambda.yml YOUR_BUCKET_NAME_TO_PUT_CFN_TEMPLATE YOUR_CFN_STACK_NAME CK CS AT AS  
```

### Arguments
$1 (lambda.yml): CFn template file of this repo.

$2 (YOUR_BUCKET_NAME_TO_PUT_CFN_TEMPLATE): S3 bucket name in which you put CFn template file(lambda.yml)

$3 (YOUR_CFN_STACK_NAME): CFn stack name of the resource described in lambda.yml

$4 (CK): Twitter's Consumer Key (API Key) 

$5 (CS): Twitter'sConsumer Secret (API Secret)

$6 (AT): Twitter's Access Token

$7 (AS): Twitter's Access Token Secret
