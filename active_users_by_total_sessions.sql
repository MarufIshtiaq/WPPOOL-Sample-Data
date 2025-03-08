select  top 5
	user_id,
	sum(total_sessions) as total_sessions
from
	wppool_data_sample
where activation_status = 1
group by user_id
order by total_sessions desc