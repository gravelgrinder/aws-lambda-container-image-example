# aws-lambda-container-image-example
Repo describing how to deploy a Lambda function based on a container image


## Build Docker Image
1. Build Docker Image
```
docker build -t hello-world-lambda app/.
```

2. Run Docker Image Locally
```
docker run -p 9000:8080 hello-world-lambda
```

3. (Optional) Test your application locally using the [runtime interface emulator](https://docs.aws.amazon.com/lambda/latest/dg/images-test.html). From a new terminal window, post an event to the following endpoint using a curl command:
```
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

## Upload Docker Image to ECR
1. Authenticate the Docker CLI to your Amazon ECR registry. Replace `{accountId}` and `{region}` with your actual account ID for ECR.
```
aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {accountId}.dkr.ecr.{region}.amazonaws.com
```
for example `accountId=123456789012` and `region=us-east-1`...
```
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
```

2. Create a repository in Amazon ECR using the `create-repository` command.
```
aws ecr create-repository --repository-name hello-world-lambda --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
```

3. Tag your image to match your repository name, and deploy the image to Amazon ECR using the `docker push` command.
```
docker tag  hello-world-lambda:latest {accountId}.dkr.ecr.{region}.amazonaws.com/hello-world-lambda:latest
docker push {accountId}.dkr.ecr.{region}.amazonaws.com/hello-world-lambda:latest
```

## Create Lambda from Container Image
```
aws lambda create-function \
    --function-name djl-hello-world-lambda \
    --package-type Image \
    --role arn:aws:iam::614129417617:role/service-role/my-s3-function-role \
    --code "ImageUri=614129417617.dkr.ecr.us-east-1.amazonaws.com/hello-world-lambda:latest" \
    --vpc-config SubnetIds="subnet-069a69e50bd1ebb23",SecurityGroupIds="sg-091fff29ba7c79318"

```


Run the following to Initialize the Terraform environment.

```
terraform init
```

2. Provision the resources in the `main.tf` script

```
terraform apply
```

3. The Dev Endpoint should move into a "Provisioning status" = "READY" (~10mins). The Sagemaker Notebook should also change into a Status = "InService".

4. Confirm you are connect to your Dev Endpoint from your SageMaker Notebook.

## Notes to Consider
* When selecting the VPC, it must have access to an S3 endpoint to allow private connections to the S3 service.  This is needed if you define your Python library and dependent jars paths.
* When selecting the VPC, Subnet and Security Groups, you must only select a Security Group that has a "self-referencing" rule.

## Clean up Resources
1. To delete the resources created from the terraform script run the following.the destroy command.
```
terraform destroy
```

## Helpful Resources
[Creating Lambda container images](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)
[Amazon ECR Interface VPC Endpoints (AWS PrivateLink)](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html)

## Questions & Comments
If you have any questions or comments on the demo please reach out to me [Devin Lewis - AWS Solutions Architect](mailto:lwdvin@amazon.com?subject=AWS%2FTerraform%20FMS%20Create%20Application%20List%20%28aws-terraform-fms-put-apps-list%29)

Of if you would like to provide personal feedback to me please click [Here](https://feedback.aws.amazon.com/?ea=lwdvin&fn=Devin&ln=Lewis)
