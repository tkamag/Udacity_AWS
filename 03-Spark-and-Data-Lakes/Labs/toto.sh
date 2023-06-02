#!/bin/sh

DEFAULT_REGION=eu-west-3
ACCESS_KEY=
SECRET_KEY=
rep='23 Lab-S3 MFA delete'

echo $DEFAULT_REGION

aws configure set default.region $DEFAULT_REGION  --profile $1
aws configure set aws_access_key_id $ACCESS_KEY   --profile $1
aws configure set aws_secret_access_key $SECRET_KEY --profile $1

# 1. Get your MFA keys
#aws iam list-virtual-mfa-devices > $rep/mfa-codes.txt --profile $1

# Save your mfa key as an environment variable
export mfakey="arn:aws:iam::659296642281:mfa/root-account-mfa-device"

# 2. Create bucket
# You need to specify the location constraint for every region except us-east-1
# Regions outside of us-east-1 require the appropriate LocationConstraint to be
# specified in order to create the bucket in the desired region:
# $ aws s3api create-bucket --bucket my-bucket
#                           --region eu-west-1
#                           --create-bucket-configuration LocationConstraint=eu-west-1
#
# https://docs.aws.amazon.com/cli/latest/reference/s3api/create-bucket.html
# https://gist.github.com/res0nat0r/76d4b5434ba225a6916ac65fcf39bc8d
# https://github.com/aws/aws-cli/issues/2279
# https://stackoverflow.com/questions/34795780/how-to-use-mfa-with-aws-cli
# https://www.cloudmantra.net/blog/how-to-enable-mfa-delete-for-s3-bucket/
# https://stackoverflow.com/questions/39051477/the-aws-access-key-id-does-not-exist-in-our-records

aws s3api create-bucket --bucket $2\
                        --region $DEFAULT_REGION\
                        --create-bucket-configuration LocationConstraint=$DEFAULT_REGION\
                        --profile $1


# 3. Enable versioning and MFA delete on bucket (as root via aws configure and mfa arn)
#aws s3api put-bucket-versioning\
#                            --bucket $2\
#                            --versioning-configuration '{"MFADelete":"Enabled","Status":"Enabled"}' \
#                            --mfa 'arn:aws:iam::659296642281:mfa/root-account-mfa-device 491200'

#aws s3api put-bucket-versioning --bucket $2 --versioning-configuration Status=Enabled --mfa "$mfakey 562165"
aws sts get-session-token --serial-number arn:aws:iam::659296642281:mfa/root-account-mfa-device\
                            --token-code $3\
                            --profile $1
# https://www.cloudmantra.net/blog/how-to-enable-mfa-delete-for-s3-bucket/
# https://devopspoints.com/aws-setting-up-a-secure-amazon-s3-bucket.html
# https://www.google.com/search?q=aws+s3api+put-bucket-versioning&client=opera&hs=U8T&sxsrf=ALeKk02mGLTr0CDbteP4hk83VXd0EgPimA:1618349015347&ei=1wt2YM3fFMOLlwTVp5iAAQ&start=10&sa=N&ved=2ahUKEwiNp7rxk_zvAhXDxYUKHdUTBhAQ8NMDegQIARBN&biw=1880&bih=937

ACCESS_KEY=
SECRET_KEY=

aws configure set aws_access_key_id $ACCESS_KEY   --profile $1
aws configure set aws_secret_access_key $SECRET_KEY --profile $


# 4. List objects in your bucket with version ids
#aws s3api list-object-versions  --bucket $2\
#                                --query 'Versions[].{Key: Key, VersionId: VersionId}'