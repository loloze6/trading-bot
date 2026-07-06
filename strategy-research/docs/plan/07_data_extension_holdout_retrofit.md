# Improvement 07 — Data Extension & Holdout Retrofit (IMMEDIATE — before any further run)

## Gap

Two compounding problems that no existing plan item (01–06) addresses, and that get worse with every additional run:

1. **The evaluation data is burnt.** `baseline_v1.json` covers 11 monthly windows (2024-01 → 2024-11) on BTCUSDT + ETHUSDT. The campaign has executed 36+ runs against these same windows, and every run's verdict has fed back into hypothesis generation (via `findings_carryover`, parameter brackets, altitude decisions). At the campaign level these windows are therefore **no longer out-of-sample** — the search process has adapted to them. Any metric computed on them, including the Keltner mean-reversion "confirmed edge", carries unquantified selection bias. Improvement 06's holdout enforcement is correct but scheduled last; the *data reservation* part of it cannot wait, because its cost compounds per run.

2. **Statistical power is structurally too low.** Two highly correlated symbols × 11 windows within a single calendar year ≈ far fewer than 22 independent observations. The known Keltner temporal-distribution problem (zero trades in ~30% of window-symbol slots due to regime absence in certain months) is a direct symptom: one year of one market regime cannot exercise regime-gated strategies. The current date is mid-2026; roughly 19 months of never-touched data (2024-12 onward) exists and is not used by any protocol.

This improvement is deliberately tiny in code and must land **before the next run**, independent of 01–06.

## Part A — Holdout retrofit (campaign in flight)

Improvement 06's rule "holdout fixed at campaign start" cannot apply retroactively. Replace with:

**Retrofit rule:** the holdout range must be selected from data that has never appeared in any walk-forward window of any historical run in this campaign. Given `campaign_state.instruments_tried` and all historical `protocol` definitions, compute the union of all burned date ranges per symbol/timeframe; holdout must be disjoint from that union.

Concrete assignment (adjust end date to data availability at implementation time):

```yaml
# campaign-level config, new file: config/campaign_data_policy.yaml
burned_ranges:
  BTCUSDT_1h: ["2024-01-01", "2024-11-30"]   # union of all historical protocol windows
  ETHUSDT_1h: ["2024-01-01", "2024-11-30"]
walk_forward_extension: ["2024-12-01", "2025-12-31"]   # newly available for walk-forward
holdout_range: ["2026-01-01", "2026-06-30"]            # FROZEN — never used by any stage except holdout_evaluation
holdout_consumed_by: []                                 # hypothesis_ids that have spent their single holdout shot
```

Enforcement (pull forward from Improvement 06, implement now):
- `tools/check_data.py`: fail any protocol whose windows overlap `holdout_range`. This is the only 06 code needed immediately.
- The `holdout_evaluation` stage itself (deflated Sharpe, promotion_audit) stays on 06's schedule. Only the **reservation and the overlap check** move to now.

## Part B — New baseline protocol `baseline_v2.json`

- Walk-forward: 24 monthly windows, 2024-01 → 2025-12 (the 2024 windows remain usable for walk-forward — they are burnt for *unbiased estimation*, not for *search*; the new 2025 windows restore some honest signal, and the holdout restores unbiased final estimation).
- Symbols: BTCUSDT + ETHUSDT (unchanged by default). Optionally add SOLUSDT 1h as a third baseline symbol (an escalation protocol for it already exists) to reduce the two-correlated-majors problem — but note this increases per-run compute ~50% and adds trials; acceptable only once Improvement 08 (prescreen) is cutting backtest volume.
- All new runs use `baseline_v2.json`. Historical results on `baseline_v1` remain comparable among themselves only; the campaign_knowledge_base (05) must tag findings with the protocol version.

## Part C — Recalibrate exhaustion memory

`findings_carryover.yaml` and `campaign_state.failed_families` encode conclusions drawn on 2024-only data. A family marked exhausted because its regime never occurred in 2024 (the Keltner zero-trade pattern generalized) may be viable on 2025 data. One-time action: mark all `failed_families` entries with `evidence_window: 2024_only`; campaign_review may re-open a 2024-only exhausted family **once** on baseline_v2 if its recorded root cause was regime-availability-related (not signal-quality-related).

## Acceptance criteria

1. `config/campaign_data_policy.yaml` exists; `check_data.py` rejects any protocol overlapping `holdout_range` (verified by a deliberately overlapping test protocol).
2. No stage other than a future `holdout_evaluation` can read candles inside `holdout_range` (grep-level audit of protocol files + data loader guard).
3. `baseline_v2.json` runs end-to-end on the extended range (data completeness check passes for 2024-01 → 2025-12).
4. The Keltner mean-reversion strategy is re-run on `baseline_v2` walk-forward windows (NOT holdout) as the first v2 run — this is the cheapest possible test of whether the campaign's one "confirmed" edge survives data it has never seen. Its zero-trade slot percentage on 24 windows is recorded and compared to the ~30% observed on v1.
5. Every `findings` entry written to the knowledge base from now on includes `protocol_version`.
