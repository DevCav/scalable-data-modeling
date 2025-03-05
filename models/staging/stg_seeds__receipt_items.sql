{{ config(materialized='view') }}

select
    receipt_uuid,
    user_id,
    purchase_date,
    points_earned,
    purchased_item_count,
    rewards_receipt_status,
    total_spent,
    to_varchar(barcode) as barcode,
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
    user_flagged_quantity
from {{ ref('receipt_items') }}