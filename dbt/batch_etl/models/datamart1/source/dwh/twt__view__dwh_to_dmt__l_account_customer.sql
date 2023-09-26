SELECT  
    *
    FROM  {{ ref('l_account_customer') }} 
    where Load_Date =  to_date(cast(cast( {{ var('date') }} as int) as varchar), 'yyyyMMdd')  