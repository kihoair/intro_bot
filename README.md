# intro_bot

Tweet bot executed by AWS Lambda
https://twitter.com/intro_tweetbot

Except lambda_function.py and webscrape.py, all files and directories are packages for executing by AWS Lambda.

# how to use

After Cloning this repo as ZIP, deploy the zip by uploading to AWS Lambda.
You should also set Twitter's consumer API keys, access token and access token secret, as environment variables on AWS Lambda.

hello

```
zip -r webscraping_tweetbot.zip ./
```