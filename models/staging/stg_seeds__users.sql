{{ config(materialized='view') }}

select
    id_oid as user_id,
    state,
    created_date_date as created_date,
    last_login_date as last_login,
    role,
    active,
    sign_up_source
    
from {{ ref('users') }}