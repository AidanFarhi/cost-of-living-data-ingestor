import os
import boto3
import pandas as pd    
from datetime import date
from io import StringIO
from dotenv import load_dotenv
load_dotenv()

def load_df_to_s3(table_name_and_df):
	client = boto3.client(
	    's3', 
	    endpoint_url='https://s3.amazonaws.com',
	    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
	    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
	)
	table_name = table_name_and_df['table']
	df = table_name_and_df['df']
	csv_buffer = StringIO()
	df.to_csv(csv_buffer, index=False)
	client.put_object(
		Bucket=os.getenv('BUCKET_NAME'), 
		Key=f'real_estate/cost_of_living/{date.today()}/{table_name}.csv',
		Body=csv_buffer.getvalue().encode('utf-8')
	)

def extract_expenses_table(county, url):
	tables = pd.read_html(url)
	expenses = tables[1]
	expense_categories = expenses['Unnamed: 0_level_0']
	expenses = expenses.iloc[:, 1:]
	expenses = expenses.rename(mapper={
		'1 ADULT': '1,1', 
		'2 ADULTS(1 WORKING)': '2,1', 
		'2 ADULTS(BOTH WORKING)': '2,2'
	}, axis=1)
	result = pd.DataFrame()
	for col in set([c[0] for c in expenses.columns]):
		num_adults, num_working = col.split(',')
		df = expenses[col]
		df.index = [v[0] for v in expense_categories.values]
		df = df.melt(var_name='num_children', value_name='usd_amount', ignore_index=False)
		df = df.reset_index()
		df['num_adults'] = num_adults
		df['num_working'] = num_working
		df = df.rename(columns={'index': 'expense_category'})
		df['expense_category'] = df['expense_category'].apply(str.upper)
		df['usd_amount'] = df['usd_amount'].apply(lambda x: x[x.index('$')+1:])
		df['num_children'] = df['num_children'].apply(lambda x: x[:x.index('Child')])
		df['county'] = ' '.join(county.split('_')).upper()
		result = pd.concat([result, df])
	return result

def extract_living_wage_table(county, url):
	tables = pd.read_html(url)
	living_wage = tables[0]
	wage_levels = living_wage['Unnamed: 0_level_0']
	living_wage = living_wage.iloc[:, 1:]
	living_wage = living_wage.rename(mapper={
		'1 ADULT': '1,1', 
		'2 ADULTS(1 WORKING)': '2,1', 
		'2 ADULTS(BOTH WORKING)': '2,2'
	}, axis=1)
	result = pd.DataFrame()
	for col in set([c[0] for c in living_wage.columns]):
		num_adults, num_working = col.split(',')
		df = living_wage[col]
		df.index = [v[0] for v in wage_levels.values]
		df = df.melt(var_name='num_children', value_name='usd_amount', ignore_index=False)
		df = df.reset_index()
		df['num_adults'] = num_adults
		df['num_working'] = num_working
		df = df.rename(columns={'index': 'wage_level'})
		df['wage_level'] = df['wage_level'].apply(lambda x: x[:x.index('Wage')].upper())
		df['usd_amount'] = df['usd_amount'].apply(lambda x: x[x.index('$')+1:])
		df['num_children'] = df['num_children'].apply(lambda x: x[:x.index('Child')])
		df['county'] = ' '.join(county.split('_')).upper()
		result = pd.concat([result, df])
	return result

def main():
	counties_urls = {
		'kent': 'https://livingwage.mit.edu/counties/10001',
		'new_castle': 'https://livingwage.mit.edu/counties/10003',
		'sussex': 'https://livingwage.mit.edu/counties/10005'
	}
	all_tables = []
	for county, url in counties_urls.items():
		all_tables.append({
			'table': f'{county}_living_wage',
			'df': extract_living_wage_table(county, url)
		})
		all_tables.append({
			'table': f'{county}_expenses',
			'df': extract_expenses_table(county, url)
		})
	for obj in all_tables:
		load_df_to_s3(obj)


if __name__ == '__main__':
    main()
