import os
import json
import boto3
import pandas as pd    
from datetime import date
        
# def load_results_to_s3(results):
# 	client = boto3.client(
# 	    's3', 
# 	    endpoint_url='https://s3.amazonaws.com',
# 	    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
# 	    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
# 	)
# 	for i, obj in enumerate(results):
# 		if len(obj) > 0:
# 			json_data = json.dumps(obj)
# 			client.put_object(
# 				Bucket=os.getenv('BUCKET_NAME'), 
# 				Key=f'real_estate/listings/{date.today()}/result_{i}.json',
# 				Body=json_data
# 			)

def main():
    counties_urls = {
        'kent_county': 'https://livingwage.mit.edu/counties/10001',
        'new_castle_county': 'https://livingwage.mit.edu/counties/10003',
        'sussex_county': 'https://livingwage.mit.edu/counties/10005'
    }
    for k, v in counties_urls.items():
	    pass


if __name__ == '__main__':
    main()
