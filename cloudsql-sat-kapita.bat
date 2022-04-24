@ECHO OFF

TITLE Cloud SQL Proxy SAT-KAPITA
ECHO Jangan di close selama koneksi
"cloud_sql_proxy_x64" -instances=sat-kapita-selekta-b:asia-southeast2:training-kapita-selekta=tcp:5432