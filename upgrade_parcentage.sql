select
    concat((sum(case when subscription_type = 'pro' then 1 else 0 end) *100 /20000), '%') as upgraded_to_pro
from
    wppool_data_sample