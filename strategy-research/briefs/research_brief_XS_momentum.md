---
# research_brief.yaml fields — placeholder, not yet finalized. This brief is
# blocked_on_P2 (see below); do not launch until the blocker clears. When P2
# completes, review and complete this frontmatter (market_universe in particular)
# before flipping the queue entry to `ready`.
strategy_domain: cross_sectional_momentum
market_universe: [BTCUSDT, ETHUSDT]   # PLACEHOLDER — a cross-sectional signal needs
                                       # more than 2, highly-correlated symbols; see
                                       # "What P2 must deliver" below.
timeframe: "1h"
constraints:
  - "Must not propose ideas that require replacing the whole existing bot architecture."
  - "Do not write code."
  - "Keep the mechanism explicit and interpretable."
  - "POST-A2.3: no regime-gated hypotheses in the run queue. Ungated formulations only."
  - >
    DO NOT LAUNCH until the P2 instrument-universe-expansion prerequisite (see below)
    is closed and this queue entry's status is flipped from blocked_on_P2 to ready.
available_data: [price_volume_only]
research_goal: >
  Test whether a cross-sectional momentum ranking (rank instruments by trailing
  return, go long top-ranked / short or flat bottom-ranked) produces a real,
  cost-surviving edge across a broader crypto instrument set than the campaign's
  current BTC/ETH pair.
existing_context:
  - use_existing_backtest_framework
  - prefer_minimal_code_changes
  - use_existing_strategy_architecture
optional_focus:
  - new_sub_strategy_component
---

# Research brief: XS-momentum — cross-sectional momentum

**Status:** blocked_on_P2 (not runnable yet).
**Queue id:** `XS_momentum`

## Why this is blocked

Cross-sectional momentum is defined by ranking *across* instruments at each bar — it
is not meaningful with the campaign's current two-symbol universe. Per
`campaign_state.yaml`, `instruments_tried` is currently `[BTCUSDT, ETHUSDT]`, and
`config/campaign_config.yaml`'s `symbol_correlation.btc_eth_return_correlation_1h`
(0.82) means this pair's `n_eff_symbols` (A8.6 formula:
`n / (1 + (n-1)*rho)`) is ≈1.10 — statistically closer to trading one instrument
than two. A cross-sectional rank across a 2-asset, rho=0.82 universe is not a
meaningful cross-section; it would just be a relabeled pairwise signal, and the KB
already treats "current feeds... power-limited on 2 years x 2 correlated symbols" as
a structural finding (`docs/00_closing_state.md` section 3).

`coin_universe.yaml` already lists a broader candidate set (`smart_contract_infra`:
SOLUSDT/AVAXUSDT/DOTUSDT; `defi`: UNIUSDT/AAVEUSDT/LINKUSDT; `payment`; others) but
every one of them currently has `data_cached: false` — no OHLCV has been fetched or
verified for any of them yet, unlike the P1b backward-extension effort that verified
BTC/ETH back to 2018-01-01 by real fetcher calls before it was used as evidence.

## What P2 must deliver before this brief can run

1. Fetch and verify (real fetcher calls, gap-checked — same standard as
   `docs/p1b_fetch_manifest.md`) OHLCV for a candidate cross-sectional set from
   `coin_universe.yaml` (at minimum enough instruments, at low-enough pairwise
   correlation, to give `n_eff_symbols` materially above the current ≈1.10 — this is
   a measurement to make when P2 runs, not an assumption to pre-register here).
2. Update `coin_universe.yaml`'s `data_cached` flags and `campaign_data_policy.yaml`
   with the new instruments' verified availability windows and holdout treatment,
   mirroring how the P1b backward extension was recorded.
3. Re-measure pairwise correlations for the actual chosen set (the existing
   `symbol_correlation` block only has a BTC/ETH pair; a 4+ instrument cross-section
   needs its own `rho_bar` or full correlation matrix for the A8.6 power check to be
   valid).

## Unblock procedure

When P2 (instrument-universe expansion) is complete: fill in this brief's
`market_universe` with the verified cross-sectional set, decide `machine_constraints`
(protocol start/end per the new instruments' verified availability), and flip this
queue entry's `status` in `config/campaign_queue.yaml` from `blocked_on_P2` to `ready`.
Do not flip it without completing steps 1-3 above — this is a hard prerequisite, not
a priority note.
