import pendulum
import logging
from datetime import datetime

from airflow.decorators import dag, task

@dag(
    schedule_interval='@hourly',
    #start_date=pendulum.now()
    start_date=datetime(2022, 6, 5)
)
def task_dependencies_tka():

    @task(task_id="Hello_World")
    def hello_world():
        logging.info("Hello World")

    @task(task_id="Addition")
    def addition(first,second):
        logging.info(f"{first} + {second} = {first+second}")
        return first+second

    @task(task_id="Substraction")
    def subtraction(first,second):
        logging.info(f"{first -second} = {first-second}")
        return first-second

    @task(task_id="Division")
    def division(first,second):
        logging.info(f"{first} / {second} = {int(first/second)}")   
        return int(first/second)     

# TODO: call the hello world task function
    hello=hello_world()  
# TODO: call the addition function with some constants (numbers)
    two_plus_two=addition(2,2)
# TODO: call the subtraction function with some constants (numbers)
    two_from_six=subtraction(6,2)
# TODO: call the division function with some constants (numbers)
    eight_divided_by_two = division(8,2)
# TODO: create the dependency graph for the first three tasks
    #division_task >> [addition_task, subtraction_task] >> hello_world_task

# TODO: Configure the task dependencies such that the graph looks like the following:
#
#                    ->  addition_task
#                   /                 \
#   hello_world_task                   -> division_task
#                   \                 /
#                    ->subtraction_task

#  TODO: assign the result of the addition function to a variable
    #sum= addition(5,5)
#  TODO: assign the result of the subtraction function to a variable
    #difference = subtraction(6,4)
#  TODO: pass the result of the addition function, and the subtraction functions to the division function
# TODO: create the dependency graph for the last three tasks
    # sum_divided_by_difference represents the invocation of division with the sum and the difference
    #sum_divided_by_difference = division(sum,difference)
    
    # hello to run before two_plus_two and two_from_six
    hello >> two_plus_two 
    hello >> two_from_six

    # Notice, addition and subtraction can run at the same time

    # two_plus_two to run before eight_divided_by_two
    two_plus_two >> eight_divided_by_two

    # two_from_six to run before eight_divided_by_two
    two_from_six >> eight_divided_by_two


task_dependencies_dag=task_dependencies_tka()
