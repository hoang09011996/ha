
{{
    config(
          materialized='incremental'
        , object_storage_source="curatedzone-curated"
        , pre_hook= "DELETE FROM {{ this }} a
                     WHERE EXISTS ( SELECT 1 FROM  {{ref('twt__table__dwh_to_dmt__new__dim_customer')}} b 
                    WHERE a.CUSTOMER_DIM_ID = b.CUSTOMER_DIM_ID ) 
                    "    
            
    )
}}

     {# pre_hook= scd_type2_dim_delete_rows('"curatedzone-curated"', 'dim_customer', 'CUSTOMER_DIM_ID')   #}

        {# , pre_hook= "DELETE FROM {{ this }} a
                     WHERE EXISTS ( SELECT 1 FROM  {{ref('twt__table__dwh_to_dmt__new__dim_customer')}} b 
                    WHERE a.CUSTOMER_DIM_ID = b.CUSTOMER_DIM_ID ) 
                    "    #}

{{ scd_type2_select_new_table('dim_customer') }}

