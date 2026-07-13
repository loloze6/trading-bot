---
# SUPERSEDED (2026-07-06). source: agent (authored by the agent this session, never
# committed to git, never launched to completion). Superseded by a user-delivered
# brief specifying a single registered hypothesis (SMA(100)-daily, long-only,
# next-day-open execution, no parameter sweep) — see config/campaign_queue.yaml's
# P4_ts_trend entry for the current status and where the authoritative file should
# land. Kept here only as a record of the open-mechanism (three-candidate) framing
# that was rejected as a design: one registered hypothesis per brief, not a menu for
# hypothesis_generation to choose from. Do not launch this file's content — it is
# not the current brief for this queue entry.
#
# research_brief.yaml fields — this frontmatter block is extracted verbatim by
# workflow/run_campaign.py and written to runs/<run_id>/artifacts/research_brief.yaml.
# Schema: templates/research_brief.yaml.
strategy_domain: trend_following
market_universe: [BTCUSDT, ETHUSDT]
timeframe: "1h"
constraints:
  - "Must not propose ideas that require replacing the whole existing bot architecture."
  - "Do not write code."
  - "Keep the mechanism explicit and interpretable."
  - "POST-A2.3: no regime-gated hypotheses in the run queue. Ungated formulations only."
  - >
    KB EXHAUSTED-CHECK (A5.1): the 2024-2025-only ungated EMA-crossover cell
    (moving_average_crossover, run_043, EMA_SPREAD_TREND_CONTINUATION_V1) is already
    exhausted — no_edge_observed, root_cause already_priced_in. The Keltner
    trend-breakout cell (keltner_channel_trend) is likewise dismantled (signal_inversion /
    no informational content on TRENDING-labeled bars; see KB keltner_root_cause_reattribution).
    A valid P4 hypothesis must be a structurally different claim than either exhausted
    cell — e.g. the same mechanism re-evaluated over the backward-extended 2018-2025
    window (a materially larger, multi-cycle sample the original tests did not have),
    or a genuinely untested trend_following family member (macd has
    campaign_empirical_results: [] in indicator_library.yaml — never tested). Do not
    resubmit the identical exhausted formulation.
  - >
    MODEL-BLIND CAVEAT (docs/plan/11_viable_space_map.md, rev. 3): moving_average_crossover,
    keltner_channel_trend, and macd were flagged model_blind in that advisory Layer-1
    cost-hurdle projection — a linear-IC model cannot price a convex trend-following
    payoff, so that projection neither passed nor failed them. This is a planning note,
    not a gate; it does not block registration, A8.6, or prescreen (which uses the
    actual Layer-2 formula, not the advisory projection). backtest_specification should
    be aware that a trend-following payoff may be a poor fit for a pure-IC framing and
    should consider whether the hypothesis's expectancy claim is better expressed as
    per-trade expectancy over average holding period than as a raw correlation claim.
available_data: [price_volume_only]
research_goal: >
  Test whether a time-series trend-following mechanism (moving-average crossover,
  Keltner-channel breakout, or MACD) produces a real, cost-surviving edge on
  BTCUSDT/ETHUSDT 1h once evaluated over the full backward-extended data range
  (2018-01-01 to 2025-12-31, ~8 years, multiple bull/bear/chop cycles) rather than
  the single 2024-2025 era the two already-exhausted trend cells were tested on.
  OHLCV-only mechanism: no funding_rate or fear_greed dependency, so there is no
  era-availability gap anywhere in the backward-extended range (see
  config/campaign_data_policy.yaml — BTCUSDT/ETHUSDT 1h OHLCV verified back to
  2018-01-01; holdout_range 2026-01-01 to 2026-06-30 stays untouched).
existing_context:
  - use_existing_backtest_framework
  - prefer_minimal_code_changes
  - use_existing_strategy_architecture
optional_focus:
  - new_sub_strategy_component

# --- Pre-registration / machine_constraints (F4d) ---
# Consumed directly by the orchestrator: run_campaign.py copies this block into
# runs/<run_id>/artifacts/pre_registration.yaml at launch time. From there,
# workflow/run_phase1_research.py's _ensure_protocol_from_constraints() generates
# protocols/<run_id>_generated.json (monthly windows, 2018-01 -> 2025-12) and a
# run_context.yaml override (run_type: forced_diagnostic) BEFORE hypothesis_generation
# starts — so this run cannot silently fall back to a stale campaign_state.last_escalation
# protocol (the still-open orchestrator gap noted in docs/00_closing_state.md section 8).
# significance_methodology is intentionally omitted: trend-following signals are dense
# (fire on most/all bars), so the existing 24-bar block method's density_fallback applies —
# episode_blocked_a851a is for sparse signals only (see config/campaign_config.yaml
# episode_significance.density_fallback_pct).
machine_constraints:
  protocol:
    symbols: [BTCUSDT, ETHUSDT]
    timeframe: "1h"
    start: "2018-01-01"
    end: "2025-12-31"
    holdout: {start: "2026-01-01", end: "2026-06-30"}
---

# Research brief: P4 — time-series trend-following, backward-extended window

**Status:** ready — runnable on backfilled data (P1b backward extension, 2026-07-05).
**Queue id:** `P4_ts_trend`

## Why this brief

`docs/00_closing_state.md` (Open Items table) flags the viable-space map as
de-prioritizing OHLCV trend-following retests "at coarser timeframes for P4" — this
brief is that phase. Two of the three trend_following cells in
`config/indicator_library.yaml` are already exhausted on the original 2024-2025-only
window (moving_average_crossover: `no_edge_observed` / `already_priced_in`;
keltner_channel_trend: `signal_inversion`, no informational content on TRENDING-labeled
bars). The backward extension (`config/campaign_data_policy.yaml`) makes 2018-01-01
onward walk-forward-eligible for OHLCV specifically — nearly 8 years versus the
original ~2. That is a materially different statistical claim (more episodes, more
regime diversity, spans multiple full market cycles), not a re-run of an exhausted
cell, provided the hypothesis is framed against the full range rather than repeating
the exact 2024-2025 formulation.

## What this brief does NOT decide

This brief scopes the assignment; it does not pre-select the mechanism, the exact
indicator parameters, or the evaluation framing. `hypothesis_generation` still must:
run the KB exhausted-mechanism check itself, choose which trend_following family member
(and which window framing) is genuinely novel, and populate `power_parameters` for the
A8.6 pre-flight gate. `backtest_specification` still decides how to operationalize the
model-blind caveat above.

## Data availability (verified, not assumed)

Per `config/campaign_data_policy.yaml`: BTCUSDT/ETHUSDT 1h OHLCV fetch-verified
2018-01-01 → present (spot market). Full walk-forward-eligible span for this brief:
`backward_extension` (2018-01-01 → 2023-12-31) + `burned_ranges` (2024-01-01 →
2024-11-30) + `walk_forward_extension` (2024-12-01 → 2025-12-31) = 2018-01-01 →
2025-12-31 continuous. `holdout_range` (2026-01-01 → 2026-06-30) is frozen and
untouched by this or any run in this brief's lineage, per the campaign's standing rule.

## Standing rules that apply unchanged

Taker-only cost model (`config/cost_model.yaml` `verdict_execution_style: taker`),
episode/trial recording always on, holdout single-use, all conformance and
pre-registration gates active. Nothing in this brief overrides any of these.
