{{ config(materialized='view') }}

select
    id_oid as receipt_uuid,
    bonus_points_earned,
    -- bonus_points_earned_reason is intentionally excluded per prior requirements
    create_date_date as create_date,
    date_scanned_date as date_scanned,
    finished_date_date as finished_date,
    modify_date_date as modify_date,
    points_awarded_date_date as points_awarded_date,
    points_earned,
    purchase_date_date as purchase_date,
    purchased_item_count,
    rewards_receipt_status,
    total_spent,
    user_id
from {{ ref('receipts') }}
