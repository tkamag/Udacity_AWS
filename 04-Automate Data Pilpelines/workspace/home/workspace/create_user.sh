#!/bin/bash
#chmod +x set_connections_and_variables.sh
#./set_connections_and_variables.sh
airflow users create --email student@example.com --firstname aStudent --lastname aStudent --password admin --role Admin --username admin
airflow scheduler