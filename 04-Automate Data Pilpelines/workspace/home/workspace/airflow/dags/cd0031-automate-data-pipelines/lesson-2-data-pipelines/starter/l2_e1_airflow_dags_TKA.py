import logging
import pendulum
from datetime import datetime

from airflow.decorators import dag, task

# @dag decorates the greet_task to denote it's the main function
@dag(
    start_date=datetime(2022, 6, 5),
    schedule_interval='@daily'
    #start_date=pendulum.now()
)
def greet_flow_tka():

#
# TODO: Uncomment the Welcome to Airflow 2 log statement below
#


    @task(task_id="Oliana_Oliana", retries=2)
    def hello_world():
        logging.info("Hello World!")
        logging.info("Welcome to Airflow 2!")

    @task(task_id="Oliana_Oliana2", retries=2)
    def hello_world2():
        logging.info("Hello World2!")
        logging.info("Welcome to Airflow 22!")
        

    #hello_world_task=hello_world()  
    #hello_world_task2=hello_world2()

    hello_world() >> hello_world2()
    
tka = greet_flow_tka()

