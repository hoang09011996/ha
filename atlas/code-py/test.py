import requests
import json

# Set up the API endpoint and authentication
ATLAS_HOST = 'http://192.168.1.100'
ATLAS_PORT = '32186'
ATLAS_USER = 'admin'
ATLAS_PASSWORD = 'admin'
BASE_URL = f'{ATLAS_HOST}:{ATLAS_PORT}/api/atlas/v2'
AUTH = (ATLAS_USER, ATLAS_PASSWORD)

def atlas_create_type( json_data):
    url = f'{BASE_URL}/types/typedefs'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    with open(f'/root/ha/atlas/json_api/{json_data}.json') as json_file:
        datafile = json.load(json_file)
    
    response = requests.post(url, headers=headers, auth=AUTH, data=json.dumps(datafile))
    response_json = response.json()
    if response.status_code == 409:
        error_message = response_json.get('errorMessage', 'Type creation failed due to conflict.')
        print(f"Error: {error_message}")
    elif response.status_code == 201:
        print("Type created successfully.")
    else:
        print(f"Unexpected response: {response.status_code} - {response.text}")
    
atlas_create_type('types/iceberg/1_iceberg_principal_type')
# atlas_create_type('iceberg/2_iceberg_serde')
# atlas_create_type('iceberg/3_iceberg_order')
# atlas_create_type('iceberg/4_iceberg_db')
# atlas_create_type('iceberg/5_iceberg_table')
# atlas_create_type('iceberg/6_iceberg_column')
# atlas_create_type('iceberg/7_iceberg_db_ddl')
# atlas_create_type('iceberg/8_iceberg_table_ddl')
# atlas_create_type('iceberg/9_iceberg_process_execution')
# atlas_create_type('iceberg/10_iceberg_process')
# atlas_create_type('iceberg/11_iceberg_column_lineage')
# atlas_create_type('iceberg/12_iceberg_table_storagedesc')
# atlas_create_type('iceberg/13_iceberg_db_ddl_queries')
# atlas_create_type('iceberg/14_iceberg_process_column_lineage')
# atlas_create_type('iceberg/15_iceberg_table_storagedesc')
# atlas_create_type('iceberg/16_iceberg_table_columns')
# atlas_create_type('iceberg/17_iceberg_table_partitionkeys')
# atlas_create_type('iceberg/18_iceberg_db_location')
# atlas_create_type('iceberg/19_iceberg_table_ddl_queries')
# atlas_create_type('iceberg/20_iceberg_table_db')






