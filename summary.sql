-- total number of sessions
select count(total_sessions) as total_sessions
from wppool_data_sample

-- count of distinct users
select count(distinct user_id) as distinct_users
from wppool_data_sample;

-- average, minimum, and maximum total_sessions
select 
    avg(total_sessions) as average_sessions,
    min(total_sessions) as minimum_sessions,
    max(total_sessions) as maximum_sessions
from wppool_data_sample

-- distribution of free vs. pro users
select 
    user_id,
    count(*) as user_count,
    format(count(*) * 100.0 / (select count(*) from wppool_data_sample), '0.000') + '%' as percentage
from wppool_data_sample
group by user_id