with countryranking as (
    select 
        country,
        sum(total_sessions) as total_sessions,
        sum(page_views) as page_views,
        sum(days_active) as days_active,
        sum(monthly_revenue) as monthly_revenue,
        rank() over (order by sum(total_sessions) desc) as rank_sessions,
        rank() over (order by sum(page_views) desc) as rank_page_views,
        rank() over (order by sum(days_active) desc) as rank_days_active,
        rank() over (order by sum(monthly_revenue) desc) as rank_revenue
    from wppool_data_sample
    group by country
)
select country, total_sessions, page_views, days_active, monthly_revenue
from countryranking
where rank_sessions <= 5 or rank_page_views <= 5 or rank_days_active <= 5 or rank_revenue <= 5