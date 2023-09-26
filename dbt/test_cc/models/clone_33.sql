{{
    config(
          materialized='table'
        , object_storage_source="standardizedzone"        
    )
}}


select *
FROM  "sourceimage-corebanking"."cdc_account"
 