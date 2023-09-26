{{ config(
      materialized='table'
    , object_storage_source="standardizedzone"
    
    )
 }}

SELECT distinct
    md5(concat('CDC_ACCOUNT','-',ID)) AS Account_HashKey,
    md5(concat('RECORD_SOURCE','-','CDC_ACCOUNT')) AS Record_Source,
    to_date(cast(cast(DATA_DATE as int) as varchar), 'yyyyMMdd') AS Load_Eff_Date,
    TO_DATE('24000101','yyyymmdd') AS Load_End_Date,
    T_CUSTOMER AS Customer,
    T_STATUS AS Account_Status,
	T_AVAILABLE_BALANCE_LCY AS Available_Balance_LCY,
	T_AVAILABLE_BALANCE AS Available_Balance,
    T_BALANCE_LCY AS Balance_LCY,
	T_BALANCE AS Balance,
	T_CURRENCY AS Currency,
    DAY_ID AS DAY_ID
FROM {{ref('twt_cdc_account')}}