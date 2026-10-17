---
# E-068 validation brief (operator, 2026-10-04; DRAFT until the operator approves it).
# Purpose: one real run with orchestrator.claim_tests.enabled on, whose idea is
# short-horizon by nature (hours on 1h bars), so the claim test has enough
# separate events (DESIGN_PROPOSAL.md section 11, scope note). Written after
# test B (O-20): the vol-managed brief was declared exhausted twice.
#
# Same test period and windows as the C4 Kraken briefs (2022-2023, six 4-month
# windows, RUNBOOK 1f): an end-to-end workflow run, not an edge verdict.
# Venue: Kraken futures costs with Kraken SPOT prices as a declared proxy;
# funding not modelled (D-057, option A). No promotion block, no pass_rule:
# criteria come from step 1a.

strategy_domain: "short_horizon_reversal"
market_universe: [BTCUSDT, ETHUSDT]
timeframe: "1h"
venue: "kraken"
product: "perp"
research_goal: >
  Test whether an unusually large 1h move on BTC or ETH is partly given back
  over the next few hours (1 to 12 hours), net of fees and slippage. The other
  side: forced flow -- liquidations and stop cascades on leveraged perps push
  price past where unforced traders would trade it, and they must trade at
  any price, so the move overshoots and partly reverts once the forced orders
  are done. Why it might survive: the effect is concentrated in rare, violent
  hours that a slow trend follower ignores and that are risky to provide
  liquidity into. Why it might not: those same hours carry the widest spreads,
  and the move may instead continue (momentum). The claim must state which
  way the next hours go and over which horizon, in hours.
constraints:
  - "End-to-end workflow run on 2022-2023 only (six 4-month windows): not an edge test. The 100-trades-per-coin and era-stability bars are not expected to be met."
  - "Funding is not modelled on this venue (Kraken spot prices as a proxy for futures): do not use the funding_rate feed."
  - "Short horizons: the claim's horizons are 1 to 12 bars (1 to 12 hours on 1h bars)."
available_data: []

criteria_from: hypothesis_generation

machine_constraints:
  protocol:
    symbols: [BTCUSDT, ETHUSDT]
    timeframe: "1h"
    start: "2022-01-01"
    end: "2023-12-31"
    window_months: 4
---

# Hourly shock reversal on BTC/ETH, Kraken perp (E-068 validation run)

The E-068 validation run needs an idea whose claim lives on short horizons, so that
`claim_tests` gets thousands of hourly bars and enough separate events (the scope note
in E-068's DESIGN_PROPOSAL.md section 11). The earlier hourly brief
(`C4_vol_managed_trend_kraken_perp`, multi-week momentum) was declared exhausted twice by
step 1a (O-20), so this brief states a different mechanism: forced flow and overshoot after
extreme hours.

The idea is stated loosely on purpose. Step 1a chooses the signal, the threshold for an
"unusually large" hour, the direction and the horizons (1-12 bars). It also writes the
claim card with its test, which this run exists to validate.
