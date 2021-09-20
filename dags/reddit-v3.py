from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient
from azure.storage.blob import BlobClient

import requests
 
def get_reddit(subreddit,listing,limit,timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()

def get_post_titles(ds, **kwargs):
    subreddit = 'cryptocurrencies'
    limit = 100
    timeframe = 'month' #hour, day, week, month, year, all
    listing = 'top' # controversial, best, hot, new, random, rising, top
    r = get_reddit(subreddit,listing,limit,timeframe)
    posts = []

    blob_service_client = BlobServiceClient(account_url="https://fradatalake.blob.core.windows.net/", credential = DefaultAzureCredential())
    container_client = blob_service_client.get_container_client("reddit")
    for post in r['data']['children']:
        x = post['data']['title']
        posts.append(x)
    
    fn = "a_file_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    with open(fn  + ".txt", "w") as tf:
        for post in posts:
            tf.write(post + "\n")

    with open(fn  + ".txt", "rb") as data:
        container_client.upload_blob(name=fn, data=data)

    return posts
 
default_args = {
    'owner': 'fra',
    'depends_on_past': False,
    'start_date': days_ago(2),
    #'email': ['francesco1093@gmail.com'],
    #'email_on_failure': False,
    #'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': '@hourly',
}

with DAG(
    'reddit-v3',
    description='A basic reddit scraper DAG',
    tags=['reddit'],
    default_args=default_args
) as dag:

    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    t2 = PythonOperator(
        task_id='write_to_file',
        python_callable=get_post_titles,
    )

    t1 >> t2