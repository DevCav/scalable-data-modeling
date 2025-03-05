{{ config(materialized='table') }}

select
    brand_uuid,
    barcode,
    brand_code,
    category,
    category_code,
    cpg,
    top_brand,
    name

from {{ ref('stg_seeds__brands') }}