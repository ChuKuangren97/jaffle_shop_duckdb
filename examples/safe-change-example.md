# Example output: no risk detected

**Trigger:** PR editing `models/customers.sql` (a terminal table with no downstream dependents)
**Live PR:** https://github.com/ChuKuangren97/jaffle_shop_duckdb/pull/6

Agent-posted comment:

> ✅ **Cross-Domain Break Predictor**: No downstream dependents found for `customers`.
> This change looks low-risk.

This confirms the agent distinguishes genuine risk from no risk, rather than
always returning a warning regardless of actual impact.
