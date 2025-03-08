select
	subscription_type,
	avg(total_sessions) as avg_sessions
from
	wppool_data_sample
group by
	subscription_type