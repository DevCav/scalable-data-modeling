{{ config(materialized='view') }}

select
    id_oid as brand_uuid,
    to_varchar(barcode) as barcode,
    brand_code,
    category,
    category_code,
    cpg_id_oid as cpg,
    top_brand,
    name

from {{ ref('brands') }}