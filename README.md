# intro_bot
Tweet bot for everyday Intro practice jam 

# How to use

## Environment
* serverless (node.js > v4)
* your own aws account
* awscli (python)

## How to deploy
At first, deploy selenium and chromedriver as Lambda layers.

```shell
$ cd selenium-layer
$ sls deploy
```

Second, deploy the Lambda function.

```shell
$ cd ../lambda
$ sls deploy
```

Login to AWS console and set 4 Twitter tokens and keys(AS,AT,CK,CS) for API as Lambda Function Environment Variables.
