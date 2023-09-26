

select *
FROM  "sourceimage-corebanking"."cdc_customer"
where DATA_DATE = '{{ var("date") }}'
 