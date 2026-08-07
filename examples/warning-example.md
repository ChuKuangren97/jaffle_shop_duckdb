# Example output: risk detected

**Trigger:** PR editing `models/stg_orders.sql`
**Live PR:** https://github.com/ChuKuangren97/jaffle_shop_duckdb/pull/4

Agent-posted comment:

> ⚠️ **Cross-Domain Break Predictor**: `stg_orders` has 3 downstream dependent(s):
> - **customers** (owner: DataHub)
> - **orders** (owner: DataHub)
> - **jaffle_shop.main.stg_orders** (duckdb platform sibling)
>
> Please confirm with the listed owners before merging this change.

This was generated from a live `get_lineage` call against a self-hosted DataHub
instance with real dbt-derived lineage from the `jaffle_shop_duckdb` project —
not mocked or hand-written.
