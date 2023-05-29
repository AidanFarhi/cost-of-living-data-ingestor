## This script scrapes cost of living data from the MIT Living Wage Calculator website and loads it to a S3 data lake.

#### To run locally

Create a .env file placed in the root of the project with the following environment variables:

```
BUCKET_NAME
AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY
```

Build and run the docker container

`docker compose up --build`

*If you encounter a 403 during this step, try restarting docker hub and runnning this:

`aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws`

Post an event to trigger the script

`curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'`
