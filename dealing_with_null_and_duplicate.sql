with duplicaterecords as (
    select
        user_id,
        install_date,
        last_active_date,
        subscription_type,
        country,
        total_sessions,
        page_views,
        download_clicks,
        activation_status,
        days_active,
        pro_upgrade_date,
        plan_type,          
        monthly_revenue,
        churned,
        row_number() over (
            partition by 
                user_id,
                install_date,
                last_active_date,
                subscription_type,
                country,
                total_sessions,
                page_views,
                download_clicks,
                activation_status,
                days_active,
                pro_upgrade_date,  
                plan_type,          
                monthly_revenue,
                churned
            order by install_date desc
        ) as row_num
    from 
        wppool_data_sample
)
select 
    user_id,
    install_date,
    last_active_date,
    subscription_type,
    country,
    total_sessions,
    page_views,
    download_clicks,
    activation_status,
    days_active,
    monthly_revenue,
    churned,
    coalesce(convert(varchar, pro_upgrade_date, 23), 'Not Upgraded') as updated_pro_upgrade_date,  
    coalesce(plan_type, 'Free') as updated_plan_type
from duplicaterecords
where row_num > 1