#!/usr/bin/env bash

TEMPLATE_FILE=$1
BUCKET_NAME=$2
STACK_NAME=$3
CK=$4
CS=$5
AT=$6
AS=$7


aws cloudformation package \
    --template-file ${TEMPLATE_FILE} \
    --s3-bucket ${BUCKET_NAME} \
    --output-template-file packaged-template.yml
aws cloudformation deploy \
    --template-file packaged-template.yml \
    --stack-name ${STACK_NAME} \
    --parameter-overrides \
      CK=${CK} \
      CS=${CS} \
      AT=${AT} \
      AS=${AS} \
    --capabilities CAPABILITY_NAMED_IAM CAPABILITY_IAM