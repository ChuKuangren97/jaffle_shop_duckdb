# Example output: DataHub write-back

**Trigger:** PR editing `models/stg_orders.sql`
**Live PR:** https://github.com/ChuKuangren97/jaffle_shop_duckdb/pull/8

In addition to posting a PR comment, the agent calls DataHub's `add_tags`
mutation tool to tag the changed table directly in the catalog:

```python
await client.call_tool("add_tags", {
    "tag_urns": ["urn:li:tag:break-predictor-reviewed"],
    "entity_urns": [urn]
})
```

Result, visible on the `stg_orders` entity page in DataHub itself, independent of
GitHub:

> **Tags:** `break-predictor-reviewed`

This is the "contribute back to the graph" pattern DataHub's own hackathon
materials describe — the agent doesn't just read metadata, it leaves a durable,
inspectable trace of its work inside DataHub, not only on the PR that triggered it.
