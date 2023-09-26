{{ config(
      materialized='table'
    , object_storage_source="standardizedzone"
    
    )
 }}

SELECT distinct
    md5(concat('CDC_CUSTOMER','-',ID)) AS Customer_HashKey,
    md5(concat('RECORD_SOURCE','-','CDC_CUSTOMER')) AS Record_Source,
    to_date(cast(cast(DATA_DATE as int) as varchar), 'yyyyMMdd') AS Load_Eff_Date,
    TO_DATE('24000101','yyyymmdd') AS Load_End_Date,
	T_SEGMENT_CODE   as Segment_Code           ,
    T_COMPANY_BOOK   as Company_Book            ,
	T_CUST_STATUS    as Customer_Status        ,
	T_FRAUD          as Fraud_flag             ,
	T_CREATE_DATE    as Customer_Created_date  
FROM {{ref('twt_cdc_customer')}}