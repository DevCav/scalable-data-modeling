{{ config(materialized='table') }}

select
    receipt_uuid,
    user_id,
    purchase_date,
    points_earned,
    purchased_item_count,
    rewards_receipt_status,
    total_spent,
    barcode,
    description,
    final_price,
    item_price,
    needs_fetch_review,
    partner_item_id,
    prevent_target_gap_points,
    quantity_purchased,
    user_flagged_barcode,
    user_flagged_new_item,
    user_flagged_price,
    user_flagged_quantity,

    date_trunc('month', purchase_date) as purchase_month,

    case 
        when purchase_month = date_trunc('month', current_date) 
            then true
        else false
    end as is_recent_month,

    case 
        when purchase_month = date_trunc('month', dateadd(month, -1, current_date)) 
            then true
        else false
    end as is_previous_month

from {{ ref('stg_seeds__receipt_items') }}