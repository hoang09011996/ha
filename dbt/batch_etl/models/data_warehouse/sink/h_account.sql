 

{# {{ config(materialized='table') }} #}

{{
    config(
          materialized='incremental'
        , object_storage_source="standardizedzone"
        , pre_hook= "DELETE FROM {{ this }} where Load_Date =   to_date(cast(cast( {{ var('date') }} as int) as varchar), 'yyyyMMdd') " 
        
    )
}}
{# {% set table_exists= adapter.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'h_account' ") %} #}




with source as (

    SELECT distinct
        md5(concat('T24_ACCOUNT','-',ID)) AS Account_HashKey,
        ID AS Account_Number,
        md5(concat('RECORD_SOURCE','-','T24_ACCOUNT'))  AS Record_Source,
        to_date(cast(cast(DATA_DATE as int) as varchar), 'yyyyMMdd') AS Load_Date
    FROM {{ref('twt_cdc_account')}}

)

select *
from source
