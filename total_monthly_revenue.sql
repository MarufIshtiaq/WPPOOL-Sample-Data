select
	plan_type,
	sum(monthly_revenue) as total_monthly_revenue
from
	wppool_data_sample
--where plan_type is not null
group by
	plan_type