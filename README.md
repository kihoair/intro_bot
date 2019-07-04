# intro_bot
Tweet bot for everyday Intro practice jam 

# How to use

## Environment
* node.js
* your own aws account
* awscli

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
