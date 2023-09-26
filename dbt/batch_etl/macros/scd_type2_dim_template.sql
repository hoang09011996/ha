-- SELECT ON TYPE2
{% macro scd_type2_select_new_table(table) %}
    SELECT * FROM {{ ref('twt__table__dwh_to_dmt__new__' ~ table) }} b
{% endmacro %}


-- DELETE ON TYPE2
{% macro scd_type2_dim_delete_rows(schema, condition , keysID) %}
DELETE FROM {{ schema }}.{{ condition }} a
WHERE EXISTS (
    SELECT 1 FROM {{ ref('twt__table__dwh_to_dmt__new__' ~ condition) }} b
    WHERE a.{{ keysID }} = b.{{ keysID }}
)
{% endmacro %}



-- GET NEW ON TYPE2
{% macro scd_type2_dim_template(all_columns, keysID, system_date, except_col, table) %}
 
{% set all_columns = adapter.get_columns_in_relation(ref('twt__view__dwh_to_dmt__' ~ table)) %}

with 
source as (
    SELECT  
    {%- for col in all_columns  %}  
    {{ col.name }}          {%- if not loop.last %}           ,{{ '\n  ' }}        {% endif %}
    {%- endfor %}
    FROM {{ ref('twt__view__dwh_to_dmt__' ~ table) }}
),

twt as (
    SELECT 
    {%- for col in all_columns  %}  
    {{ col.name }}          {%- if not loop.last %}           ,{{ '\n  ' }}        {% endif %}
    {%- endfor %}
    FROM {{ ref('twt__table__dwh_to_dmt__query_from_source__' ~ table) }}
),

existed_new as (
    select  
        {%- for col in all_columns %}
        a.{{ col.name }}  {%- if not loop.last %}           ,{{ '\n  ' }}        {% endif %}
        {%- endfor %}
    from twt a
    join source b  ON (
        {%- for col in keysID %}
        a.{{ col }} = b.{{ col }}  {%- if not loop.last %}  AND   {% endif %}
        {%- endfor %}
    )
    and (
        {%- for col in all_columns if col.name not in except_col and col.name not in keysID  and col.name not in system_date %}
        a.{{ col.name }} <> b.{{ col.name }}   or ( a.{{ col.name }}  is null and b.{{ col.name }}  is not null) or (a.{{ col.name }}  is not null and b.{{ col.name }}  is null )      {%- if not loop.last %} OR {{ '\n  ' }}{% endif %}
        {%- endfor %}
    )
),
day_new as (
    select 
        {%- for col in all_columns %}
        a.{{ col.name }}  {%- if not loop.last %}   ,{{ '\n  ' }}  {% endif %}
        {%- endfor %} 
    from twt a 
    where not exists ( 
        select 1 
        from source b where  
        {%- for col in keysID %}
        a.{{ col }} = b.{{ col }}  {%- if not loop.last %}  AND   {% endif %}
        {%- endfor %}
        )
),
old_update as (
    select  
        {%- for col in all_columns %}
        {% if col.name == "Load_End_Date" %}
            a.Load_Eff_Date as Load_End_Date
        {% else %}
            b.{{ col.name }}  {%- if not loop.last %}           ,{{ '\n  ' }}        {% endif %}
        {% endif %}
        {%- endfor %}
    from twt a
    join source b  ON (
        {%- for col in keysID %}
        a.{{ col }} = b.{{ col }}  {%- if not loop.last %}  AND   {% endif %}
        {%- endfor %}
    )
    and (
        {%- for col in all_columns if col.name not in except_col and col.name not in keysID  and col.name not in system_date %}
        a.{{ col.name }} <> b.{{ col.name }}   or ( a.{{ col.name }}  is null and b.{{ col.name }}  is not null) or (a.{{ col.name }}  is not null and b.{{ col.name }}  is null )      {%- if not loop.last %} OR {{ '\n  ' }}{% endif %}
        {%- endfor %}
    )
)
select * from existed_new
UNION ALL 
select * from day_new
UNION ALL 
select * from old_update
{% endmacro %}
