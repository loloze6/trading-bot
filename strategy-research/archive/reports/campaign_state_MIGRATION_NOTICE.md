# MIGRATION NOTICE — campaign_state.yaml, 2026-07-15

`last_escalation` gained two new fields, `claimed_by_run: run_049` and
`claimed_at: '2026-07-06'`, as a one-time, operator-authorized migration
required by the K3 kernel (B10, protocol pinning + stale-escalation
hard-fail — see `docs/design/K3_protocol_pinning_design_20260714.md`
section 9, amendment A5).

**Why this was necessary:** K3's Phase B ships a hard-fail (`RuntimeError`)
for any run that falls back to `campaign_state.last_escalation.protocol_path`
without being that escalation's own claimed consumer (`claimed_by_run`
must equal the run's own `run_id`). Before this migration, the field did
not exist on this record at all — it is Phase B's own addition. Without
retroactively stamping the CURRENT `last_escalation` record with the run
it was actually scaffolded for, `run_049`'s own still-pending resumption
would hard-fail under the new B10 logic the very next time it is
attempted, even though `run_049` is exactly the run this design's
protected-consumer exception exists to preserve.

**Value applied:** `claimed_by_run: run_049`. This is the run
`_route_escalate`'s timeframe-escalation branch scaffolded when it wrote
this `last_escalation` record (`target: timeframe, detail: 15m,
protocol_path: protocols\escalation_tf_15m.json`) — confirmed by the
lineage this record documents, not inferred.

**`claimed_at` sourcing (checked, not assumed):** `campaign_state.yaml`'s
single, whole-file `updated_at` field (`2026-07-12T16:13:05.628746+00:00`
at the time of this migration) does NOT date `last_escalation`
specifically — that field has been overwritten by many unrelated writes
since the escalation was actually recorded, and `campaign_log.md` has no
entry for the run_049/escalation event at all (grepped, none found — the
log's curated format post-dates this event). `claimed_at: '2026-07-06'`
is instead sourced from `00_closing_state.md` section 8's own dating of
the P1b closure — the session in which run_047's timeframe escalation to
run_049 was recorded — per the K3 design note's own §9 A5 ruling.

**No other field in `campaign_state.yaml` was touched by this migration.**
