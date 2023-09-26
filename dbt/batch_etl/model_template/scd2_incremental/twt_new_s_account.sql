

-- models/my_model.sql

{% set keysID=['Account_HashKey' , 'Record_Source' ]%}
{% set system_date=['Load_Eff_Date', 'Load_End_Date' ] %}
{% set except_cols=[ ] %}


{{ scd_type2_s_l__NEW__template(all_columns, keysID, system_date, except_cols, 's_account') }}
