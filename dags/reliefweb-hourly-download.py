from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from datetime import datetime
import pyscripts.reliefweb as reliefweb


with DAG(
    'reliefweb-houly-download',
    owner = 'francesco',
    description='Extracting hourly reports hourly from Relief Web',
    tags=['reliefweb'],
    schedule_interval = '10 * * * *',
    catchup=False,
    start_date = datetime(2021,9,1)
) as dag:

    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    t2 = PythonOperator(
        task_id='extract_reports',
        python_callable=reliefweb.extract_res,
        op_kwargs={
            "resource":"reports",
            "datalake":"https://fradatalake.blob.core.windows.net/",
            "container":"reliefweb-reports"
            }
    )

    t3 = PythonOperator(
    task_id='extract_disasters',
    python_callable=reliefweb.extract_res,
    op_kwargs={
        "resource":"disasters",
        "datalake":"https://fradatalake.blob.core.windows.net/",
        "container":"reliefweb-disasters"
        }
    )

    t4 = PythonOperator(
    task_id='extract_sources',
    python_callable=reliefweb.extract_res,
    op_kwargs={
        "resource":"sources",
        "datalake":"https://fradatalake.blob.core.windows.net/",
        "container":"reliefweb-sources"
        }
    )
    t1 >> [t2, t3, t4]