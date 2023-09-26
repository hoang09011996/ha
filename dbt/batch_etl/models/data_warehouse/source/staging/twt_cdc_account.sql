

select *
FROM  "sourceimage-corebanking"."cdc_account"
where DATA_DATE = '{{ var("date") }}'
 