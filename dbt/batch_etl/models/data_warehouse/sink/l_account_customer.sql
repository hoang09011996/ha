


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
	MD5(concat('ACCOUNT_CUSTOMER_-',a.ID,'-',b.ID)) AS Account_Customer_Hashkey,
	MD5(concat('CDC_ACCOUNT-',a.ID)) AS  Account_HashKey,
	MD5(concat('CDC_CUSTOMER-',b.ID)) AS Customer_HashKey,
	'CDC_ACCOUNT' AS Record_Source,
	to_date(cast(cast(a.DATA_DATE as int) as varchar), 'yyyyMMdd') AS Load_Date
FROM  {{ref('twt_cdc_account')}} a
INNER JOIN {{ref('twt_cdc_customer')}}  B ON A.T_CUSTOMER = B.ID

)

select *
from source