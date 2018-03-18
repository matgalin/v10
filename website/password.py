global db_name
global db_user
global db_password
global db_host
global grafana_key
global db

db_name="system_lab"  ## name of the postgresql database
db_user="website" ## database user
db_password="Dupa.8"  ## database password
db_host="localhost" ##database host ip
grafana_key="Bearer eyJrIjoidzMwZ1NNRFhYVTdzamFxa2wxdlZScDFyYnE0anFMdmYiLCJuIjoibWFuZWdlbWVudCIsImlkIjoxfQ==" ##grafana API key
grafana_dashboard_uid="0cfUOngmz"
zabbix_template_id="10254"


###dont touch
db="dbname="+db_name+" user="+db_user+" password="+db_password+" host="+db_host
