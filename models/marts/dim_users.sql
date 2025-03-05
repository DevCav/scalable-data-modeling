{{ config(materialized='table') }}

select
    user_id,
    state,
    to_timestamp(created_date / 1000) as created_at,
    last_login,
    role,
    active,
    sign_up_source,
    datediff(month, created_at::date, current_date) as user_account_age_months
    
from {{ ref('stg_seeds__users') }}