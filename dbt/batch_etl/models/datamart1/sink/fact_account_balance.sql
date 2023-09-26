{{
    config(
          materialized='incremental'
        , object_storage_source="curatedzone-curated"
        , pre_hook= "DELETE FROM {{ this }} where cdr_dt_id =     {{ var('date') }}   "             
        
    )
}}

SELECT 
    {{ var('date') }}  as cdr_dt_id
    ,a.Account_HashKey
    , a.Customer_HashKey
    , c.Customer as Customer_ID
    , c.Account_Status as Account_Status
    , c.Available_Balance_LCY 
    , c.Available_Balance
    , c.Balance
    , c.Currency
    , b.Segment_Code
    , b.Company_Book as Branch_Code
    , b.Customer_Status
    , b.Fraud_flag
    , to_date(cast(cast( c.DAY_ID as int) as varchar), 'yyyyMMdd')  AS DAY_ID
From {{ref('twt__view__dwh_to_dmt__l_account_customer')}} a 
inner join {{ref('twt__view__dwh_to_dmt__s_account')}} c 
	on c.Account_HashKey = a.Account_HashKey
inner join {{ref('twt__view__dwh_to_dmt__s_customer')}} b 
	on b.Customer_HashKey = a.Customer_HashKey
where a.Load_Date =  to_date(cast(cast( {{ var('date') }} as int) as varchar), 'yyyyMMdd')