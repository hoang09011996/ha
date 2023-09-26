SELECT  
    *
    FROM "standardizedzone"."s_account"  
    where  to_date(cast(cast( {{ var('date') }} as int) as varchar), 'yyyyMMdd')  between Load_Eff_Date and Load_End_Date