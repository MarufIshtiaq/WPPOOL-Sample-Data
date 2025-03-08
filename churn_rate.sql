with churn_rate as (
    select sum(cast(churned as int)) as total_churned
    from wppool_data_sample
)
select 
    subscription_type,
    concat(format(sum(cast(churned as int)) * 100.0 / (select total_churned from churn_rate), '0.00'), '%') as churn_rate
from 
    wppool_data_sample
group by 
    subscription_type