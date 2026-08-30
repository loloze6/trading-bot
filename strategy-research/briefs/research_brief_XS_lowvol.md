# Research brief — cross-sectional low-volatility, 19-pair Kraken daily

**Status: PARKED.** Measured, promising, not pre-registered. Do not run a
campaign from this file until the "Before this runs" section is satisfied.

**Raised:** 2026-08-29, from a direct measurement, not from the pipeline.

---

## Why this exists

Every one of the 35 recorded runs was single-indicator TA on 2–4 USDT symbols
at 15m–4h. At those timeframes the cost arithmetic requires an information
coefficient of **0.13–0.54**. Real signals in liquid crypto produce **0.02–0.05**.

Those runs could not have succeeded at any signal quality. The search was not
wrong about the market; it was run in a cell of the grid where the arithmetic
forbids success.

Cross-sectional, 19 pairs, weekly hold is an **empty cell**. Nothing has ever
been tested there.

---

## The measurement

Panel: 19 `kraken_*_1d.csv` daily caches, train window **2018-01-01 → 2023-12-31**.
Signal: `-stdev(last 30 daily returns)` — rank low-vol high.
Metric: cross-sectional Spearman rank IC against forward return.

| horizon | IC | t |
|---|---|---|
| 1d | +0.058 | +6.7 |
| 3d | +0.058 | +6.6 |
| 7d | +0.063 | +7.4 |
| 14d | +0.075 | +9.0 |

Momentum also present but weaker: 14d signal / 14d hold, IC +0.042 (t +5.4).

### Three attacks, all survived

**Thin cross-section?** No. Requiring 6/8/10/12/14 symbols per day gives
IC 0.057–0.070 throughout.

**Just "BTC/ETH beat the alts"?** *Partly — this is the honest haircut.*
Dropping BTC+ETH cuts IC from 0.062 to **+0.032 (t +2.9)**; dropping four
majors gives **+0.036 (t +3.0)**. Roughly half the effect is a majors tilt,
but a real residual survives among alts alone.

**Era stability?** Passes. Positive in all three eras:
2018-20 **+0.045** (t 2.2) · 2021-22 **+0.099** (t 7.7) · 2023 **+0.064** (t 2.9).

### Economics

`edge_per_trade = IC × sigma_bar × sqrt(bars_held)`, measured
`sigma_1d = 358.6 bps` (verified to scale as √t against real data).

At a **7-day hold**:

| universe | IC | edge | vs Binance spot 17bps | vs Kraken perp 10bps |
|---|---|---|---|---|
| all 19 pairs | 0.062 | 59 bps | 3.5× | **5.9×** |
| ex BTC+ETH | 0.032 | 30 bps | 1.8× | **3.0×** |
| ex 4 majors | 0.036 | 34 bps | 2.0× | **3.4×** |

Hurdle is 2.0× (`cost_model.yaml` `safety_factor`). Every variant clears it on
Kraken perps. Rough gross Sharpe via IC×√breadth: **0.89 to 1.74**.

---

## What is NOT established

- **Exploratory, not pre-registered.** 9 signals × 4 horizons = **36
  combinations** tested; the best is reported. N=36 must enter the
  deflated-Sharpe count.
- **IC is not P&L.** No turnover, weighting scheme, or rebalance slippage.
- Low-vol may still proxy liquidity or size even among the alts.
- **Validation (2024–2025) is untouched.** Deliberately. Peeking spends it.
- The exploratory run touched market data and therefore **owes a
  `research/TRIALS.csv` row** that has not been written.

---

## The mechanism question — answer before promoting

The research protocol requires three answers before code runs. Current state:

**Who is on the other side?** *Unanswered.* The equity low-vol anomaly is
usually attributed to leverage-constrained investors bidding up high-beta
assets. Whether that transfers to crypto — where leverage is abundant and
retail is lottery-seeking — is a real question, not a formality. A plausible
crypto version: retail preference for high-volatility "lottery" alts
systematically overprices them. That needs to be argued, not assumed.

**Why does it survive costs at our size?** Partly answered — the edge/cost
table above, at a weekly hold on Kraken perps. Weak point: turnover is not
yet modelled, and turnover is what kills cross-sectional strategies.

**Why has it not been arbitraged away?** *Unanswered.*

---

## Before this runs

1. Re-measure independently. A disagreement is the finding, not a nuisance.
2. Answer the three mechanism questions above.
3. Write `HYPOTHESIS.md` with pre-registered thresholds and kill criteria,
   declaring **N=36**.
4. Write the owed `TRIALS.csv` row.
5. Re-cost against Kraken perps (`cost_model.yaml` `perp` block, 10 bps round
   trip) rather than the spot default.
6. Consider whether `safety_factor: 2.0` is the right bar — it is a project
   choice, not physics, and it has probably killed more candidates than any
   strategy flaw.

Only then: validation window.

---

## Reproduction

Not committed as a tool. Rebuild it: load the 19 daily caches into a
date → {symbol: close} panel, restrict to the train window, compute
`-stdev` of the last 30 daily returns per symbol per date, and take the
cross-sectional Spearman IC against the forward return at each horizon.
Require a minimum universe size per date and report how the result moves
with it — that check is what rules out the thin-cross-section artifact.
