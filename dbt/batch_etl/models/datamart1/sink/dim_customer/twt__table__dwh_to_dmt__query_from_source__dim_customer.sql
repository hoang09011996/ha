{{ config(
      materialized='table'
    , object_storage_source="curatedzone-curated"
    
    )
 }}

SELECT distinct
	md5(concat(hc.Customer_HashKey, '-',  {{ var('date') }}   )) AS CUSTOMER_DIM_ID,
	hc.Customer_HashKey AS Customer_Hashkey,
	sc.Segment_Code AS SEGMENT_CODE,
	sc.Customer_Created_date AS OPEN_DATE,
	sc.Customer_Status AS CUSTOMER_STATUS ,
	sc.Fraud_flag AS FRAUD_FLAG,
	to_date(cast(cast({{ var('date') }} as int) as varchar), 'yyyyMMdd') AS Load_Eff_Date,
	to_date('24000101', 'yyyyMMdd') AS Load_End_Date
FROM
	 {{ref('twt__view__dwh_to_dmt__h_customer')}} hc
INNER JOIN {{ref('twt__view__dwh_to_dmt__s_customer')}}    sc
    ON  sc.Customer_HashKey = hc.Customer_HashKey
