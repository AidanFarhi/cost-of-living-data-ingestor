## This script scrapes cost of living data from the MIT Living Wage Calculator website and loads it to an S3 bucket.

To run locally, this code depends on a .env file placed in the root of the project with the following environment variables:

```
SNOWFLAKE_USERNAME
SNOWFLAKE_PASSWORD
SNOWFLAKE_ACCOUNT
BUCKET_NAME
AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY
```

### Command to run script.

`docker compose up --build`