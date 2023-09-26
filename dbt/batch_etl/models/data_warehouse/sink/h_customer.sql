
{# {{ config(materialized='table') }} #}

{{
    config(
        materialized='incremental',
        object_storage_source="standardizedzone",
        pre_hook= "DELETE FROM {{ this }} where Load_Date =   to_date(cast(cast( {{ var('date') }} as int) as varchar), 'yyyyMMdd') " 
        
    )
}}

with source as (

    SELECT distinct
        md5(concat('CDC_CUSTOMER','-',ID)) AS Customer_HashKey,
        ID AS Customer_Number,
        md5(concat('RECORD_SOURCE','-','CDC_CUSTOMER'))  AS Record_Source,
        to_date(cast(cast(DATA_DATE as int) as varchar), 'yyyyMMdd') AS Load_Date
    FROM  {{ref('twt_cdc_customer')}}

)

select *
from source
