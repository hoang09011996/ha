import requests
import json
from jinja2 import Template

def atlas_connect(atlas_host, atlas_port, atlas_user, atlas_password):
    base_url = f'http://{atlas_host}:{atlas_port}/api/atlas/v2'
    # Create a session and set up authentication
    session = requests.Session()
    session.auth = (atlas_user, atlas_password)
    # Test the connection by making a simple API request
    test_url = f'{base_url}/types/typedefs'
    try:
        response = session.get(test_url)
        response.raise_for_status()
        print("Connection to Apache Atlas successful.")
        return session
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Apache Atlas: {e}")
        return None

def atlas_create_type(session, json_path):
    base_url = f'http://{ATLAS_HOST}:{ATLAS_PORT}/api/atlas/v2'
    url = f'{base_url}/types/typedefs'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    json_data = f'/root/ha/atlas/json_api/types/{json_path}.json'

    with open(json_data) as json_file:
        datafile = json.load(json_file)

    response = session.post(url, headers=headers, data=json.dumps(datafile))
    
    response_json = response.json()
    if response.status_code == 409:
        error_message = response_json.get('errorMessage', 'Type creation failed due to conflict.')
        print(f"Error: {error_message}")
    elif response.status_code == 201:
        print("Type created successfully.")
    else:
        print(f"Unexpected response: {response.status_code} - {response.text}")

def read_and_replace_json(file_path, replacements):
    with open(file_path, 'r') as json_file:
        json_content = json_file.read()

    # Perform replacements
    for key, value in replacements.items():
        placeholder = f'{{{{ {key} }}}}'

        if placeholder in json_content:
            json_content = json_content.replace(placeholder, str(value))

    return json_content

def atlas_create_iceberg_db(session, qualified_name, name, display_name, description):
    base_url = f'http://{ATLAS_HOST}:{ATLAS_PORT}/api/atlas/v2'
    url = f'{base_url}/entity'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    file_path = f'/root/ha/atlas/json_api/entities/iceberg/iceberg_db.json.j2'

    replacements = {
        'qualified_name': qualified_name,
        'display_name': display_name,
        'name': name,
        'description': description
    }
    # Read the JSON.j2 file, replace the variables, and get the modified JSON data
    modified_json_data = read_and_replace_json(file_path, replacements)
    # print(modified_json_data)

    # Use modified_json_data directly without json.dumps()
    response = session.post(url, headers=headers, data=modified_json_data)
    print(response.json())
    print(response.status_code)

def atlas_create_iceberg_table(session, qualified_name, name, display_name,db_qualified_name, description):
    base_url = f'http://{ATLAS_HOST}:{ATLAS_PORT}/api/atlas/v2'
    url = f'{base_url}/entity'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    file_path = f'/root/ha/atlas/json_api/entities/iceberg/iceberg_table.json.j2'

    replacements = {
        'qualified_name': qualified_name,
        'display_name': display_name,
        'name': name,
        'description': description,
        'db_qualified_name': db_qualified_name
    }
    
    # Read the JSON.j2 file, replace the variables, and get the modified JSON data
    modified_json_data = read_and_replace_json(file_path, replacements)
    # print(modified_json_data)

    # Use modified_json_data directly without json.dumps()
    response = session.post(url, headers=headers, data=modified_json_data)
    print(response.json())
    print(response.status_code)

def atlas_create_iceberg_column(session,  column_name, table_qualified_name ):
    base_url = f'http://{ATLAS_HOST}:{ATLAS_PORT}/api/atlas/v2'
    url = f'{base_url}/entity'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    file_path = f'/root/ha/atlas/json_api/entities/iceberg/iceberg_column.json.j2'

    qualified_name = f'{table_qualified_name}.{column_name}'
    replacements = {
        'column_qualified_name': qualified_name,
        'column_name': column_name,
        'table_qualified_name': table_qualified_name
    }
    
    # Read the JSON.j2 file, replace the variables, and get the modified JSON data
    modified_json_data = read_and_replace_json(file_path, replacements)
    # print(modified_json_data)

    # Use modified_json_data directly without json.dumps()
    response = session.post(url, headers=headers, data=modified_json_data)
    print(response.json())
    print(response.status_code)

def atlas_create_iceberg_process(session, qualifiedName, name, outputs, inputs, queryText, queryId):
    base_url = f'http://{ATLAS_HOST}:{ATLAS_PORT}/api/atlas/v2'
    url = f'{base_url}/entity'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    file_path = f'/root/ha/atlas/json_api/entities/iceberg/iceberg_process.json.j2'
    with open(file_path, 'r') as file:
        template_content = file.read()

    template = Template(template_content)

    rendered_template = template.render(qualifiedName=qualifiedName,
                                        name=name,
                                        inputs=inputs,
                                        outputs=outputs,
                                        queryText=queryText,
                                        queryId=queryId
                                        )
    # print("Rendered Template:")
    # print(rendered_template)

    response = session.post(url, headers=headers, data=rendered_template)
    print("Response JSON:")
    print(response.json())
    print("Response Status Code:")
    print(response.status_code)

def atlas_create_iceberg_column_lineage(session, qualifiedName, name, outputs, inputs, query ):
    base_url = f'http://{ATLAS_HOST}:{ATLAS_PORT}/api/atlas/v2'
    url = f'{base_url}/entity'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    file_path = f'/root/ha/atlas/json_api/entities/iceberg/iceberg_column_lineage.json.j2'
    with open(file_path, 'r') as file:
        template_content = file.read()

    template = Template(template_content)
    rendered_template = template.render(qualifiedName=qualifiedName,
                                        name=name,
                                        inputs=inputs,
                                        outputs=outputs,
                                        query=query
                                        )
    # print("Rendered Template:")
    # print(rendered_template)

    response = session.post(url, headers=headers, data=rendered_template)
    print("Response JSON:")
    print(response.json())
    print("Response Status Code:")
    print(response.status_code)

#___________________________________MAIN_____________________________________
# Set up the API endpoint and authentication
ATLAS_HOST = '192.168.1.21'
ATLAS_PORT = '31113'
ATLAS_USER = 'admin'
ATLAS_PASSWORD = 'admin'

# Connect to Apache Atlas
session = atlas_connect(ATLAS_HOST, ATLAS_PORT, ATLAS_USER, ATLAS_PASSWORD)

# Check if the connection was successful before proceeding
if session:
    ##Create types using the atlas_create_type function
    atlas_create_type(session,'iceberg/1_iceberg_principal_type')
    atlas_create_type(session,'iceberg/2_iceberg_serde')
    atlas_create_type(session,'iceberg/3_iceberg_order')
    atlas_create_type(session,'iceberg/4_iceberg_db')
    atlas_create_type(session,'iceberg/5_iceberg_table')
    atlas_create_type(session,'iceberg/6_iceberg_column')
    atlas_create_type(session,'iceberg/7_iceberg_db_ddl')
    atlas_create_type(session,'iceberg/8_iceberg_table_ddl')
    atlas_create_type(session,'iceberg/9_iceberg_process_execution')
    atlas_create_type(session,'iceberg/10_iceberg_process')
    atlas_create_type(session,'iceberg/11_iceberg_column_lineage')
    atlas_create_type(session,'iceberg/12_iceberg_table_storagedesc')
    atlas_create_type(session,'iceberg/13_iceberg_db_ddl_queries')
    atlas_create_type(session,'iceberg/14_iceberg_process_column_lineage')
    atlas_create_type(session,'iceberg/15_iceberg_table_storagedesc')
    atlas_create_type(session,'iceberg/16_iceberg_table_columns')
    atlas_create_type(session,'iceberg/17_iceberg_table_partitionkeys')
    atlas_create_type(session,'iceberg/18_iceberg_db_location')
    atlas_create_type(session,'iceberg/19_iceberg_table_ddl_queries')
    atlas_create_type(session,'iceberg/20_iceberg_table_db')
    #Add more calls to atlas_create_type for other types
    ...

#atlas_create_iceberg_db ####qualified_name,name,display_name,description
# atlas_create_iceberg_db(session, qualified_name, name, display_name, description):
    atlas_create_iceberg_db(session, 'landingzone.corebanking2' , 'landingzone.corebanking2' , 'corebanking2', 'landingzone.corebanking2')
    atlas_create_iceberg_db(session,'standardizedzone.hub2' , 'standardizedzone.hub2' , 'hub2', 'standardizedzone.hub2')
    atlas_create_iceberg_db(session,'standardizedzone.link2' , 'standardizedzone.link2' , 'link2', 'standardizedzone.link2')
    atlas_create_iceberg_db(session,'standardizedzone.satellite2' , 'standardizedzone.satellite2' , 'satellite', 'standardizedzone.satellite2')
    atlas_create_iceberg_db(session,'curatedzone.curated2' , 'curatedzone.curated2' , 'curated2', 'curatedzone.curated2')



    #atlas_create_iceberg_table  #qualified_name, name, display_name,db_qualified_name, description
    atlas_create_iceberg_table(session,'landingzone.corebanking2.cdc_customer' , 'landingzone.corebanking2.cdc_customer' , 'cdc_customer', 'landingzone.corebanking2','landingzone.corebanking2.cdc_customer')
    atlas_create_iceberg_column(session,  'DATA_DATE'      ,'landingzone.corebanking2.cdc_customer')
    atlas_create_iceberg_column(session,  'ID'             ,'landingzone.corebanking2.cdc_customer')
    atlas_create_iceberg_column(session,  'T_SEGMENT_CODE' ,'landingzone.corebanking2.cdc_customer')
    atlas_create_iceberg_column(session,  'T_COMPANY_BOOK' ,'landingzone.corebanking2.cdc_customer')
    atlas_create_iceberg_column(session,  'T_CREATE_DATE'  ,'landingzone.corebanking2.cdc_customer')
    atlas_create_iceberg_column(session,  'T_CUST_STATUS'  ,'landingzone.corebanking2.cdc_customer')
    atlas_create_iceberg_column(session,  'T_FRAUD'        ,'landingzone.corebanking2.cdc_customer')

    atlas_create_iceberg_table(session,'landingzone.corebanking2.cdc_account' , 'landingzone.corebanking2.cdc_account' , 'cdc_account', 'landingzone.corebanking2','landingzone.corebanking2.cdc_account')
    atlas_create_iceberg_column(session,  'DAY_ID'                 ,'landingzone.corebanking2.cdc_account')
    atlas_create_iceberg_column(session,  'DATA_DATE'              ,'landingzone.corebanking2.cdc_account')
    atlas_create_iceberg_column(session,  'ID'                     ,'landingzone.corebanking2.cdc_account')
    atlas_create_iceberg_column(session,  'T_CUSTOMER'             ,'landingzone.corebanking2.cdc_account')
    atlas_create_iceberg_column(session,  'T_STATUS'               ,'landingzone.corebanking2.cdc_account')
    atlas_create_iceberg_column(session,  'T_AVAILABLE_BALANCE_LCY','landingzone.corebanking2.cdc_account')
    atlas_create_iceberg_column(session,  'T_AVAILABLE_BALANCE'    ,'landingzone.corebanking2.cdc_account')
    atlas_create_iceberg_column(session,  'T_BALANCE_LCY'          ,'landingzone.corebanking2.cdc_account')
    atlas_create_iceberg_column(session,  'T_BALANCE'              ,'landingzone.corebanking2.cdc_account')
    atlas_create_iceberg_column(session,  'T_CURRENCY'             ,'landingzone.corebanking2.cdc_account')


    ##HUB
    atlas_create_iceberg_table(session,'standardizedzone.hub2.h_account_new' , 'standardizedzone.hub2.h_account_new' , 'h_account_new', 'standardizedzone.hub2','standardizedzone.hub2.h_account_new')
    atlas_create_iceberg_column(session,  'Record_Source' 	, 'standardizedzone.hub2.h_account_new' )
    atlas_create_iceberg_column(session,  'Load_Date'       , 'standardizedzone.hub2.h_account_new' )
    atlas_create_iceberg_column(session,  'Account_HashKey' , 'standardizedzone.hub2.h_account_new' )
    atlas_create_iceberg_column(session,  'Account_Number'  , 'standardizedzone.hub2.h_account_new' )
    atlas_create_iceberg_table(session,'standardizedzone.hub2.h_customer_new' , 'standardizedzone.hub2.h_customer_new' , 'h_customer_new', 'standardizedzone.hub2','standardizedzone.hub2.h_customer_new')
    atlas_create_iceberg_column(session,  'Record_Source' 	 , 'standardizedzone.hub2.h_customer_new' )	 
    atlas_create_iceberg_column(session,  'Customer_HashKey' , 'standardizedzone.hub2.h_customer_new' ) 
    atlas_create_iceberg_column(session,  'Load_Date' 		 , 'standardizedzone.hub2.h_customer_new' ) 
    atlas_create_iceberg_column(session,  'Customer_Number'  , 'standardizedzone.hub2.h_customer_new' )
    ##LINK
    atlas_create_iceberg_table(session,'standardizedzone.link2.l_account_customer' , 'standardizedzone.link2.l_account_customer' , 'l_account_customer', 'standardizedzone.link2','standardizedzone.link2l_account_customer')
    atlas_create_iceberg_column(session,  'Record_Source' 	 , 'standardizedzone.link2.l_account_customer' )	 
    atlas_create_iceberg_column(session,  'Customer_HashKey' 	 , 'standardizedzone.link2.l_account_customer' )	 
    atlas_create_iceberg_column(session,  'Load_Date' 	 , 'standardizedzone.link2.l_account_customer' )	 
    atlas_create_iceberg_column(session,  'Account_HashKey' 	 , 'standardizedzone.link2.l_account_customer' )	 
    atlas_create_iceberg_column(session,  'Account_Customer_Hashkey' 	 , 'standardizedzone.link2.l_account_customer' )	 
    ##satellite
    atlas_create_iceberg_table(session,'standardizedzone.satellite2.s_account_new' , 'standardizedzone.satellite2.s_account_new' , 's_account_new', 'standardizedzone.satellite2','standardizedzone.satellite2.s_account_new')
    atlas_create_iceberg_column(session,  'Account_Status' 	 , 'standardizedzone.satellite2.s_account_new' )	          
    atlas_create_iceberg_column(session,  'Balance_LCY' 	 , 'standardizedzone.satellite2.s_account_new' )		         
    atlas_create_iceberg_column(session,  'Record_Source' 	 , 'standardizedzone.satellite2.s_account_new' )		      
    atlas_create_iceberg_column(session,  'Load_Eff_Date' 	 , 'standardizedzone.satellite2.s_account_new' )		      
    atlas_create_iceberg_column(session,  'Load_End_Date' 	 , 'standardizedzone.satellite2.s_account_new' )		      
    atlas_create_iceberg_column(session,  'Customer' 	     , 'standardizedzone.satellite2.s_account_new' )		          
    atlas_create_iceberg_column(session,  'Account_HashKey'  , 'standardizedzone.satellite2.s_account_new' )		      
    atlas_create_iceberg_column(session,  'Available_Balance_LCY' 	 , 'standardizedzone.satellite2.s_account_new' )	    
    ##curated
    atlas_create_iceberg_table(session,'curatedzone.curated2.fact_account_balance_new' , 'curatedzone.curated2.fact_account_balance_new' , 'fact_account_balance_new', 'curatedzone.curated2','curatedzone.curated2.fact_account_balance_new')
    atlas_create_iceberg_column(session,  'Available_Balance' 	    , 'curatedzone.curated2.fact_account_balance_new' )		   
    atlas_create_iceberg_column(session,  'Customer_HashKey'	   	, 'curatedzone.curated2.fact_account_balance_new' )	
    atlas_create_iceberg_column(session,  'Available_Balance_LCY' 	, 'curatedzone.curated2.fact_account_balance_new' ) 
    atlas_create_iceberg_column(session,  'Balance' 	            , 'curatedzone.curated2.fact_account_balance_new' )	               
    atlas_create_iceberg_column(session,  'cdr_dt_id' 	            , 'curatedzone.curated2.fact_account_balance_new' )	           
    atlas_create_iceberg_column(session,  'Account_HashKey' 	    , 'curatedzone.curated2.fact_account_balance_new' )	       
    atlas_create_iceberg_column(session,  'Customer_ID' 	        , 'curatedzone.curated2.fact_account_balance_new' )	           
    atlas_create_iceberg_column(session,  'Account_Status' 	        , 'curatedzone.curated2.fact_account_balance_new' )	       
					   
###atlas_create_iceberg_process(session,  qualifiedName,name, outputs,inputs ,queryText, queryId  )
    #t24_source.cdc_account_to_landingzone.corebanking2.cdc_account
    inputs = [
        {"type": "rdbms_table", "table_qualified_name": "t24_source.cdc_account"}
    ]
    outputs = [
        {"type": "iceberg_table", "table_qualified_name": "landingzone.corebanking2.cdc_account"}
    ]
    atlas_create_iceberg_process(session,  't24_source.cdc_account_to_landingzone.corebanking2.cdc_account', 'cdc_account', outputs,inputs ,"select * from t24_source.cdc_account", ""  )

    inputs = [
        {"type": "rdbms_table", "table_qualified_name": "t24_source.cdc_customer"}
    ]
    outputs = [
        {"type": "iceberg_table", "table_qualified_name": "landingzone.corebanking2.cdc_customer"}
    ]
    atlas_create_iceberg_process(session,  't24_source.cdc_customer_to_landingzone.corebanking2.cdc_customer', 'cdc_customer', outputs,inputs ,"select * from t24_source.cdc_customer", ""  )
    
    inputs = [
        {"type": "iceberg_table", "table_qualified_name": "landingzone.corebanking2.cdc_customer"}
    ]
    outputs = [
        {"type": "iceberg_table", "table_qualified_name": "standardizedzone.link2.l_account_customer"},
        {"type": "iceberg_table", "table_qualified_name": "standardizedzone.satellite2.s_account_new"},
        {"type": "iceberg_table", "table_qualified_name": "standardizedzone.hub2.h_account_new"},
        {"type": "iceberg_table", "table_qualified_name": "standardizedzone.hub2.h_customer_new"}
    ]
    atlas_create_iceberg_process(session,  'landingzone.corebanking2.cdc_customer_to_standardizedzone', 'cdc_customer', outputs,inputs ,"select ID from landingzone.corebanking2.cdc_customer", ""  )

    inputs = [
        {"type": "iceberg_table", "table_qualified_name": "landingzone.corebanking2.cdc_account"}
    ]
    outputs = [
        {"type": "iceberg_table", "table_qualified_name": "standardizedzone.link2.l_account_customer"},
        {"type": "iceberg_table", "table_qualified_name": "standardizedzone.satellite2.s_account_new"},
        {"type": "iceberg_table", "table_qualified_name": "standardizedzone.hub2.h_account_new"}
    ]
    atlas_create_iceberg_process(session,  'landingzone.corebanking2.cdc_account_to_standardizedzone', 'cdc_account', outputs,inputs ,"select ID from landingzone.corebanking2.cdc_account", ""  )
  
    inputs = [
        {"type": "iceberg_table", "table_qualified_name": "standardizedzone.link2.l_account_customer"},
        {"type": "iceberg_table", "table_qualified_name": "standardizedzone.satellite2.s_account_new"},
        {"type": "iceberg_table", "table_qualified_name": "standardizedzone.hub2.h_account_new"},
        {"type": "iceberg_table", "table_qualified_name": "standardizedzone.hub2.h_customer_new"}    ]
    outputs = [
        {"type": "iceberg_table", "table_qualified_name": "curatedzone.curated2.fact_account_balance_new"},
    ]
    atlas_create_iceberg_process(session,  'curatedzone.curated2.fact_account_balance_new', 'curatedzone.curated2.fact_account_balance_new', outputs,inputs ,"select ID from landingzone.corebanking2.cdc_account", ""  )

########atlas_create_iceberg_column_lineage(session, qualifiedName, name, outputs, inputs, query ):    

################################################landingzone.corebanking2.cdc_account###################################
    inputs = [
        {"type": "rdbms_column", "table_qualified_name": "oracle.t24_source.cdc_account.t_balance_lcy"}
        ]
    outputs = [
        {"type": "iceberg_column", "table_qualified_name": "landingzone.corebanking2.cdc_account.T_BALANCE_LCY"},
    ]
    querys = [
        {"query": "t24_source.cdc_account_to_landingzone.corebanking2.cdc_account"}
    ]
    atlas_create_iceberg_column_lineage(session,  'landingzone.corebanking2.cdc_account.T_BALANCE_LCY', 'T_BALANCE_LCY', outputs,inputs ,querys )
    
    inputs = [
        {"type": "rdbms_column", "table_qualified_name": "oracle.t24_source.cdc_account.day_id"}
        ]
    outputs = [
        {"type": "iceberg_column", "table_qualified_name": "landingzone.corebanking2.cdc_account.DAY_ID"},
    ]
    querys = [
        {"query": "t24_source.cdc_account_to_landingzone.corebanking2.cdc_account"}
    ]
    atlas_create_iceberg_column_lineage(session,  'landingzone.corebanking2.cdc_account.DAY_ID', 'DAY_ID', outputs,inputs ,querys )
  
    inputs = [
        {"type": "rdbms_column", "table_qualified_name": "oracle.t24_source.cdc_account.t_currency"}
        ]
    outputs = [
        {"type": "iceberg_column", "table_qualified_name": "landingzone.corebanking2.cdc_account.T_CURRENCY"},
    ]
    querys = [
        {"query": "t24_source.cdc_account_to_landingzone.corebanking2.cdc_account"}
    ]
    atlas_create_iceberg_column_lineage(session,  'landingzone.corebanking2.cdc_account.T_CURRENCY', 'T_CURRENCY', outputs,inputs ,querys )     

    inputs = [
        {"type": "rdbms_column", "table_qualified_name": "oracle.t24_source.cdc_account.data_date"}
        ]
    outputs = [
        {"type": "iceberg_column", "table_qualified_name": "landingzone.corebanking2.cdc_account.DATA_DATE"},
    ]
    querys = [
        {"query": "t24_source.cdc_account_to_landingzone.corebanking2.cdc_account"}
    ]
    atlas_create_iceberg_column_lineage(session,  'landingzone.corebanking2.cdc_account.DATA_DATE', 'DATA_DATE', outputs,inputs ,querys )   

    inputs = [
        {"type": "rdbms_column", "table_qualified_name": "oracle.t24_source.cdc_account.t_available_balance_lcy"}
        ]
    outputs = [
        {"type": "iceberg_column", "table_qualified_name": "landingzone.corebanking2.cdc_account.T_AVAILABLE_BALANCE_LCY"},
    ]
    querys = [
        {"query": "t24_source.cdc_account_to_landingzone.corebanking2.cdc_account"}
    ]
    atlas_create_iceberg_column_lineage(session,  'landingzone.corebanking2.cdc_account.T_AVAILABLE_BALANCE_LCY', 'T_AVAILABLE_BALANCE_LCY', outputs,inputs ,querys )   

    inputs = [
        {"type": "rdbms_column", "table_qualified_name": "oracle.t24_source.cdc_account.t_available_balance"},
        {"type": "rdbms_column", "table_qualified_name": "oracle.t24_source.cdc_account.t_available_balance_lcy"}
        ]
    outputs = [
        {"type": "iceberg_column", "table_qualified_name": "landingzone.corebanking2.cdc_account.T_AVAILABLE_BALANCE"},
    ]
    querys = [
        {"query": "t24_source.cdc_account_to_landingzone.corebanking2.cdc_account"}
    ]
    atlas_create_iceberg_column_lineage(session,  'landingzone.corebanking2.cdc_account.T_AVAILABLE_BALANCE', 'T_AVAILABLE_BALANCE', outputs,inputs ,querys )      

    inputs = [
        {"type": "rdbms_column", "table_qualified_name": "oracle.t24_source.cdc_account.t_balance"},
        ]
    outputs = [
        {"type": "iceberg_column", "table_qualified_name": "landingzone.corebanking2.cdc_account.T_BALANCE"},
    ]
    querys = [
        {"query": "t24_source.cdc_account_to_landingzone.corebanking2.cdc_account"}
    ]
    atlas_create_iceberg_column_lineage(session,  'landingzone.corebanking2.cdc_account.T_BALANCE', 'T_BALANCE', outputs,inputs ,querys )     

    inputs = [
        {"type": "rdbms_column", "table_qualified_name": "oracle.t24_source.cdc_account.t_customer"},
        ]
    outputs = [
        {"type": "iceberg_column", "table_qualified_name": "landingzone.corebanking2.cdc_account.T_CUSTOMER"},
    ]
    querys = [
        {"query": "t24_source.cdc_account_to_landingzone.corebanking2.cdc_account"}
    ]
    atlas_create_iceberg_column_lineage(session,  'landingzone.corebanking2.cdc_account.T_CUSTOMER', 'T_CUSTOMER', outputs,inputs ,querys )   

    inputs = [
        {"type": "rdbms_column", "table_qualified_name": "oracle.t24_source.cdc_account.id"},
        ]
    outputs = [
        {"type": "iceberg_column", "table_qualified_name": "landingzone.corebanking2.cdc_account.ID"},
    ]
    querys = [
        {"query": "t24_source.cdc_account_to_landingzone.corebanking2.cdc_account"}
    ]
    atlas_create_iceberg_column_lineage(session,  'landingzone.corebanking2.cdc_account.ID', 'ID', outputs,inputs ,querys )   


#################################################standardizedzone.hub2.h_account_new###################################
    inputs = [
        {"type": "iceberg_column", "table_qualified_name": "landingzone.corebanking2.cdc_account.T_STATUS"}
        ]
    outputs = [
        {"type": "iceberg_column", "table_qualified_name": "standardizedzone.satellite2.s_account_new.Account_Status"}
    ]
    query =  {"type": "iceberg_process", "table_qualified_name": "landingzone.corebanking2.cdc_account_to_standardizedzone"}
    atlas_create_iceberg_column_lineage(session, 'standardizedzone.satellite2.s_account_new.Account_Status', 'standardizedzone.satellite2.s_account_new.Account_Status', outputs, inputs, query )      
   
    inputs = [
        {"type": "iceberg_column", "table_qualified_name": "landingzone.corebanking2.cdc_account.T_AVAILABLE_BALANCE"}
        ]
    outputs = [
        {"type": "iceberg_column", "table_qualified_name": "standardizedzone.satellite2.s_account_new.Available_Balance_LCY"}
    ]
    query =  {"type": "iceberg_process", "table_qualified_name": "landingzone.corebanking2.cdc_account_to_standardizedzone"}
    atlas_create_iceberg_column_lineage(session, 'standardizedzone.satellite2.s_account_new.Available_Balance_LCY', 'standardizedzone.satellite2.s_account_new.Available_Balance_LCY', outputs, inputs, query )      
      
    inputs = [
        {"type": "iceberg_column", "table_qualified_name": "landingzone.corebanking2.cdc_account.T_BALANCE_LCY"}
        ]
    outputs = [
        {"type": "iceberg_column", "table_qualified_name": "standardizedzone.satellite2.s_account_new.Balance_LCY"}
    ]
    query =  {"type": "iceberg_process", "table_qualified_name": "landingzone.corebanking2.cdc_account_to_standardizedzone"}
    atlas_create_iceberg_column_lineage(session, 'standardizedzone.satellite2.s_account_new.Balance_LCY', 'standardizedzone.satellite2.s_account_new.Balance_LCY', outputs, inputs, query )      
    

    inputs = [
        {"type": "iceberg_column", "table_qualified_name": "landingzone.corebanking2.cdc_account.T_BALANCE_LCY"}
        ]
    outputs = [
        {"type": "iceberg_column", "table_qualified_name": "standardizedzone.satellite2.s_account_new.Balance_LCY"}
    ]
    query =  {"type": "iceberg_process", "table_qualified_name": "landingzone.corebanking2.cdc_account_to_standardizedzone"}
    atlas_create_iceberg_column_lineage(session, 'standardizedzone.satellite2.s_account_new.Balance_LCY', 'standardizedzone.satellite2.s_account_new.Balance_LCY', outputs, inputs, query )      

    inputs = [
        {"type": "iceberg_column", "table_qualified_name": "standardizedzone.satellite2.s_account_new.Balance_LCY"},
        {"type": "iceberg_column", "table_qualified_name": "standardizedzone.satellite2.s_account_new.Account_Status"},
        {"type": "iceberg_column", "table_qualified_name": "standardizedzone.satellite2.s_account_new.Available_Balance_LCY"}
        ]
    outputs = [
        {"type": "iceberg_column", "table_qualified_name": "curatedzone.curated2.fact_account_balance_new.Balance"}
    ]
    query =  {"type": "iceberg_process", "table_qualified_name": "curatedzone.curated2.fact_account_balance_new"}
    atlas_create_iceberg_column_lineage(session,  'curatedzone.curated2.fact_account_balance_new.Balance', 'fact_account_balance_new.Balance', outputs,inputs ,query )   


    inputs = [
        # {"type": "iceberg_table", "table_qualified_name": "standardizedzone.link2.l_account_customer"},
        # {"type": "iceberg_table", "table_qualified_name": "standardizedzone.satellite2.s_account_new"},
        # {"type": "iceberg_table", "table_qualified_name": "standardizedzone.hub2.h_account_new"},
        # {"type": "iceberg_table", "table_qualified_name": "standardizedzone.hub2.h_customer_new"},
        {"type": "iceberg_table", "table_qualified_name": "curatedzone.curated2.fact_account_balance_new"}    
    ]
    outputs = [
        {"type": "report", "table_qualified_name": "ba0_cao_demo_rdp@superset"},
    ]
    atlas_create_iceberg_process(session,  'REPORT_DEMO', 'REPORT_DEMO_1', outputs,inputs ,"REPORT_DEMO", ""  )

# Close the session (optional, but good practice)
session.close()
