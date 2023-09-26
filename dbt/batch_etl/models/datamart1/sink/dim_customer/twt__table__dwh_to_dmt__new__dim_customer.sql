{{ config(
      materialized='table'
    , object_storage_source="standardizedzone"
    
    )
 }}

{% set keysID=['CUSTOMER_DIM_ID' ]%}
{% set system_date=['Load_Eff_Date', 'Load_End_Date' ] %}
{% set except_cols=[ ] %}


{{ scd_type2_dim_template(all_columns, keysID, system_date, except_cols, 'dim_customer') }}

