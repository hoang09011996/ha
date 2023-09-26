
{{
    config(
          materialized='incremental'
        , object_storage_source="standardizedzone"
        , pre_hook= "UPDATE {{ this }} a
                    SET Load_End_Date =  to_date(cast(cast( {{ var('date') }} as int) as varchar), 'yyyyMMdd')
                    WHERE EXISTS
                        ( 
                        SELECT 1 FROM {{ref('twt_new_s_customer')}} b
                        where   a.Customer_HashKey = b.Customer_HashKey
                            and a.Record_Source   = b.Record_Source
                        )
                    " 
    )
}}

SELECT  *
FROM {{ref('twt_new_s_customer')}}
