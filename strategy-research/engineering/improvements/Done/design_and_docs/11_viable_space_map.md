# Viable-Space Map — Layer-1 Cost Hurdle × {1h, 4h, 1d}

**Status: advisory.** This map is a prioritization aid only. It never blocks
hypothesis registration or an A8.6 power check, and it never substitutes for an
actual Layer 1 (`validation_gate`) or Layer 2 (`prescreen_signal.py`) run. Where this
map and a real prescreen result disagree, **the real prescreen result wins** — see
the reconciliation trace below, which is exactly that case.

**Rev. 3, 2026-07-04 — final. This revision is frozen; no further revisions are
planned.** From here, empirical gates (prescreen Layer 2, A8.6 power check, holdout)
own the actual research question for any specific hypothesis. This document's role
was triage — it is now closed.

## Scope header

**This map covers `indicator_library.yaml` signal classes only** — single-symbol,
single-indicator directional forecasts of the kind this campaign has tested to date
(oscillator, trend_following, volatility, volume_flow, structural_rate, sentiment,
order_book_imbalance). **It has no bearing on:**
- **Portfolio-construction hypotheses** (e.g. cross-sectional momentum across the P2
  universe) — their edge comes from cross-sectional ranking/rotation, not a single
  symbol's forecast-to-allocation signal, and basket-rebalancing cost structure isn't
  modeled here.
- **Accrual/carry strategies** (e.g. funding-rate carry, distinct from
  `funding_rate_extreme`'s *directional mean-reversion* use here) — carry harvests a
  continuous payment stream rather than trading a directional forecast, so "gross
  edge per round-trip trade" is the wrong unit of account for it.

Both would need their own Layer-1 pass if they enter the campaign's hypothesis space.

---

## Part 1 — Reconciliation trace: run_042 (real) vs. rev-2 map (projected)

The rev-2 map computed `fear_greed_index_contrarian`@1h at `edge_to_cost_ratio ≈
15.61/34.0 ≈ 0.46` (implausible). But this exact signal was actually run through Layer
2 as H-041-C (`strategy-research/results/prescreens/run_042/prescreen_result.yaml`),
which measured `edge_to_cost_ratio = 3.75` (**pass**, killed instead on IC
significance — `route: kill_no_ic`, p=0.5469, `n_eff=13`). Side by side:

| Input | run_042 (actual, measured) | rev-2 map (projected) | Ratio |
|---|---|---|---|
| `ic_active_bars` | 0.190476 | 0.19 (borrowed from the same run) | 1.00 |
| `avg_holding_bars` (τ, hours) | 28.73 (measured: `turnover_proxy`, 316 active bars / 11 implied trades) | 30.0 (indicator_library "12–48 bars" midpoint) | 0.96 |
| `sigma_bar_bps` | **62.5199** (measured: `stdev(next_return_bps)` pooled BTC+ETH, all ~17,520 bars/symbol, full baseline_v2 range) | **15.0** (`campaign_config.yaml prescreen.sigma_bar_bps_default`) | **4.17** |
| `estimated_gross_edge_bps_per_trade` | 63.83 | 15.61 | 4.09 |
| `edge_to_cost_ratio` (BTCUSDT) | **3.75 (pass)** | **0.46 (implausible)** | 8.9 |

**IC and holding-period assumptions were both essentially correct** (ratios 1.00 and
0.96 — well within any reasonable estimation noise). **`sigma_bar_bps` is the entire
divergence** (ratio 4.17, and the resulting edge ratio of 4.09 tracks it almost
exactly — the small residual is just the 0.96 holding-period ratio).

**Root cause:** `campaign_config.yaml`'s `sigma_bar_bps_default: 15.0` is commented
"fallback volatility estimate (bps) when < 5 bars available; encodes 1h crypto
mid-volatility assumption" — and `prescreen_signal.py._sigma_from_records()` (line
461–465) only *falls back* to it `if len(returns) < 5`; otherwise it computes
`statistics.stdev()` directly from real `next_return_bps` data. In every real run with
enough data (run_042 included), 15.0 is never actually used — it's a degenerate
placeholder for a data-starved edge case, not a "typical" 1h crypto volatility figure.
The real, full-sample, pooled BTC/ETH 1h return stdev over the entire 2024–2025
baseline_v2 window is ~62.5 bps (roughly consistent with ~60–65% annualized crypto
vol: `62.5 bps × √8760 hours/year ≈ 58%` annualized — a plausible figure). The rev-2
map borrowed the *fallback* constant and, incorrectly, treated it as a realistic
typical-case volatility assumption.

**Verdict: the map's model needed the fix, not the prescreen formula.**
`prescreen_signal.py`'s Layer 2 formula and its data-driven sigma estimation are
correct and internally consistent (this is exactly what a `statistics.stdev()` over
17,520 real bars should produce). The map's error was reusing a documented,
data-starved fallback constant as if it were a general-purpose volatility assumption.
No change to `cost_model.yaml`, `prescreen_signal.py`, or `campaign_config.yaml` is
made here — this is a map-only correction (the `sigma_bar_bps_default: 15.0` naming
and comment, while a latent readability trap, is out of scope for this pass; noted for
awareness, not touched).

**Consequence for the map:** rev-2's F&G verdict was wrong in the *other* direction
from rev-1 — not from a scaling artifact this time, but from a wrong constant. Rev-3
below uses the real measured `sigma_bar_bps = 62.52` (source: `run_042`) uniformly,
and F&G reverts to matching the real, already-on-record result: cost-plausible,
power-insufficient. This was already documented in `improvements/IMPROVEMENTS_DONE_20260706.md`'s epistemic
state section ("H-041-C ... cost ratio 3.75 ...") before this map existed — the map
was, briefly, out of sync with the campaign's own existing record. It is not new news.

---

## Part 2 — τ semantics fix: `strategy_holding_hours` vs. `typical_lag_bars`

`indicator_library.yaml`'s `typical_lag_bars` describes how long the *indicator takes
to register/trigger* — e.g. "5–20+ bars" for a moving-average crossover to complete.
For mean-reversion/oscillator archetypes, the position closes on the same cycle that
triggered it, so detection lag ≈ holding period is a reasonable proxy. For
**trend-following archetypes, this is the wrong number**: a trend-following position
is designed to be held from one trend-flip to the next, which for a genuine
long-lookback trend system is governed by trend persistence, not indicator-registration
lag. Conflating the two (as rev. 1 and rev. 2 both did) silently assumes a
short-term, high-turnover implementation of "trend following," not what the term
usually means.

`strategy_holding_hours` (distinct field, per archetype):

| Archetype | strategy_holding_hours (τ) | Source |
|---|---|---|
| Oscillator / mean-reversion (rsi_mean_reversion, stochastic_oscillator, keltner_channel_mean_reversion, bollinger_bands) | = `typical_lag_bars` (unchanged) | `indicator_library.yaml`: entry and exit are governed by the same reversion cycle, so detection lag is a reasonable holding-period proxy |
| Oscillator / momentum filter (rsi_momentum) | = `typical_lag_bars` (unchanged) | `indicator_library.yaml` describes this as a short-term momentum filter, not a long-lookback trend system — its own notes give no basis for a longer hold |
| Volume flow (on_balance_volume) | = `typical_lag_bars` (unchanged) | Divergence resolves on the same timescale as its own detection lag per `indicator_library.yaml` notes |
| Structural rate (funding_rate_extreme) | = `typical_lag_bars` (post-settlement resolution, unchanged) | Event-driven mechanism (8h settlement cycle), not lag-driven; already treated specially for feasibility (see rev-2 footnote, retained below) |
| Sentiment (fear_greed_index_contrarian) | **28.73h (measured)**, not 30h (library midpoint) | `run_042` `turnover_proxy.avg_holding_bars` — real measured data supersedes the declarative library range wherever it exists |
| **Trend-following** (moving_average_crossover, keltner_channel_trend, macd) | **1,440h (~2 months)**, representative of a 1–3 month range | General trend-following/CTA convention, **not** `indicator_library.yaml`'s lag figures: Moskowitz, Ooi & Pedersen (2012) "Time Series Momentum," *J. Financial Economics* (1–12 month formation/holding); Hurst, Ooi & Pedersen (2017) "A Century of Trend Following," AQR (1–12 month lookback blends). A genuine trend-following implementation holds until the trend reverses, not until the crossover/indicator itself registers. |

Recomputed with `sigma_bar_bps = 62.52` (Part 1 fix) applied uniformly:

| Indicator | τ (h) | gross edge (bps) | vs. required (34–41) |
|---|---|---|---|
| rsi_mean_reversion | 5.0 | 4.19 | implausible |
| rsi_momentum | 4.0 | 3.75 | implausible |
| stochastic_oscillator | 6.5 | 4.78 | implausible |
| keltner_channel_mean_reversion | 1.0 | 1.88 | implausible |
| bollinger_bands | 2.0 | 3.54 | implausible |
| on_balance_volume | 6.5 | 7.97 | implausible |
| funding_rate_extreme | 1.0 | 0.88 | implausible |
| fear_greed_index_contrarian | 28.73 | **63.83** (= run_042 exact) | **plausible (cost-only)** |

---

## Part 3 — Scope caveat: trend-following is `model_blind`, not scored

Plugging the corrected `strategy_holding_hours` (1,440h) into the same linear formula
for the three trend_following indicators:

| Indicator | IC used | τ (h) | naive gross edge (bps) |
|---|---|---|---|
| moving_average_crossover | 0.05 (untested, category ceiling) | 1,440 | 118.62 |
| keltner_channel_trend | 0.032 (empirical, from the short-term param actually tested) | 1,440 | 75.92 |
| macd | 0.05 (untested, category ceiling) | 1,440 | 118.62 |

Taken at face value, these numbers would read "plausible" by a wide margin (2.9×–3.5×
the required hurdle). **They are not reported as plausible.** Two independent reasons:

1. **The linear-IC model cannot price convex/skewed payoff classes.** Trend-following's
   real payoff structure is well documented (CTA/managed-futures literature) as
   convex and positively skewed — many small losses while a trend fails to form,
   occasional large gains when one runs — closer to a long-option/lookback-straddle
   payoff than a linear forecast–return correlation. A Spearman IC is a linear
   association measure; it structurally cannot represent this payoff shape, in either
   direction (it could equally understate or overstate the true edge — the point is
   that it is not the right instrument, not that it is biased one particular way).
2. **The `sqrt(τ)` term rewards patience without limit.** Nothing in the formula
   caps how large a naive "gross edge" estimate can get by simply asserting a longer
   holding period — `keltner_channel_trend`'s 75.92 bps and `MA/MACD`'s 118.62 bps
   are driven almost entirely by `√1440 ≈ 38`, not by the (modest, partly borrowed)
   IC inputs. A model where "assume a longer hold" is a free way to manufacture
   headroom against a fixed-per-trade cost hurdle is a model that has left its valid
   domain, not a discovery.

**Verdict: `moving_average_crossover`, `keltner_channel_trend`, and `macd` are marked
`model_blind` at every timeframe.** This is a distinct status from `implausible` (the
model produced a defensible negative) and from `not_meaningful` (the architecture
can't express the hold at all) — it means the model itself is not a valid pricing tool
for this payoff class, so no plausibility verdict is asserted in either direction.
`keltner_channel_trend`'s short-term-parameterization empirical result (IC = −0.032,
already dead — see `campaign_knowledge_base.yaml`) stands on its own as a separate,
already-answered question about *that specific tested config*; it is not superseded or
contradicted by the `model_blind` archetype-level note, which is about a different,
never-built long-lookback variant.

---

## Part 4 — Recomputed map (rev. 3, final)

| Indicator | Category | Feed status | 1h | 4h | 1d |
|---|---|---|---|---|---|
| rsi_mean_reversion | oscillator | available | implausible (4.19) | implausible (4.19) | not_meaningful (hb=0.21) |
| rsi_momentum | oscillator | available | implausible (3.75) | implausible (3.75) | not_meaningful (hb=0.17) |
| stochastic_oscillator | oscillator | available | implausible (4.78) | implausible (4.78) | not_meaningful (hb=0.27) |
| moving_average_crossover | trend_following | available | **model_blind** | **model_blind** | **model_blind** |
| keltner_channel_trend | trend_following | available | **model_blind**‡ | **model_blind**‡ | **model_blind**‡ |
| keltner_channel_mean_reversion | oscillator | available | implausible (1.88) | not_meaningful (hb=0.25) | not_meaningful (hb=0.04) |
| macd | trend_following | available | **model_blind** | **model_blind** | **model_blind** |
| bollinger_bands | volatility | available | implausible (3.54) | not_meaningful (hb=0.50) | not_meaningful (hb=0.08) |
| atr_volatility_filter | volatility | available | n/a — sizing input, not a directional signal; excluded | | |
| volume_ratio_momentum | volume_flow | **blocked** (mechanism-impure, A1.3; requires `liquidation_data`) | blocked | blocked | blocked |
| on_balance_volume | volume_flow | available | implausible (7.97) | implausible (7.97) | not_meaningful (hb=0.27) |
| funding_rate_extreme | structural_rate | available | implausible (0.88) | not_meaningful (hb=0.25)§ | not_meaningful (hb=0.04) |
| open_interest_divergence | structural_rate | **not testable** (OI not wired, per `available_feeds.yaml`) | not_testable | not_testable | not_testable |
| fear_greed_index_contrarian | sentiment | available | **plausible, cost-only (63.83 = run_042 exact)** | plausible, cost-only (63.83)¶ | plausible, cost-only (63.83)¶ |
| order_book_imbalance | order_book_imbalance | **not testable** (feed unavailable) | not_testable | not_testable | not_testable |

Numbers are `gross_edge_bps_per_trade`, using `sigma_bar_bps = 62.52` (Part 1) and each
row's `strategy_holding_hours` (Part 2). Required range 34.0–41.0 bps (taker only, per
`verdict_execution_style` hard rule in `cost_model.yaml`).

‡ `keltner_channel_trend`'s empirically-tested short-term parameterization (IC=−0.032)
is separately dead; the `model_blind` label here applies to the archetype-level
long-lookback treatment only (see Part 3).
§ See rev-2's feasibility footnote (retained): `funding_rate_extreme`'s τ=1h describes
post-settlement resolution speed; feasibility at 4h/1d also fails the settlement-cycle
sampling constraint independently. Already empirically dead (IC=0.014) regardless.
¶ 4h/1d figures for F&G extrapolate the 1h empirical result via the timeframe-invariant
derivation (Part 2 of rev-2, retained: `gross_edge = IC × sigma_1h × √τ_hours`, τ fixed
in real hours). Not independently measured at 4h/1d — flagged as an extrapolation, same
caveat as before.

**IMPORTANT — what "plausible, cost-only" means for `fear_greed_index_contrarian`:**
this is not a new finding. It restates `run_042`'s actual, already-on-record result
(cost check passes at ratio 3.75) and the campaign's own existing characterization of
H-041-C as "parked (inconclusive, powered-out)" in `improvements/IMPROVEMENTS_DONE_20260706.md` — cost was
never the reason it's parked; insufficient statistical power was (`n_eff=13` vs. 35
needed, addressed by the existing backward-extension backlog item). This map cell
changes nothing about H-041-C's status; it just stops disagreeing with the number that
was already on record.

---

## Reading the map (rev. 3)

- **No OHLCV mean-reversion/oscillator/volatility/volume-flow cell clears the
  hurdle at any timeframe**, and most become architecturally `not_meaningful` at
  4h/1d (sub-1-bar holds). This conclusion is unchanged from rev. 2 and is not
  sensitive to the sigma correction — even at 4–8× the original sigma estimate, these
  indicators' modest ICs and short holds keep them 4–9× short of the hurdle, not
  borderline.
- **`funding_rate_extreme` stays dead everywhere** — mechanism is settlement-pinned,
  IC is empirically near-zero (0.014), unaffected by either correction in this
  revision.
- **`fear_greed_index_contrarian` clears the cost hurdle** — consistent with, not
  contradicting, the actual empirical Layer 2 result already on record. It remains
  parked on power grounds, not cost grounds. Nothing here reopens H-041-C or bypasses
  the single-use holdout / power-check rules.
- **Trend-following (`moving_average_crossover`, `keltner_channel_trend`, `macd`) is
  `model_blind`, not scored.** The naive numbers (76–119 bps) would look attractive,
  which is itself the tell that a linear IC-based model is being asked to price a
  payoff shape it cannot represent. A real assessment of trend-following viability on
  this venue needs a different methodology (e.g. an actual long-lookback backtest with
  convexity-aware metrics), not a bigger `τ` plugged into this formula.

## What this does NOT say

- It does not reopen, promote, or change the status of any hypothesis, including
  H-041-C — see the boxed note in Part 4.
- It does not clear any cell for `backtest_specification` on its own authority — only
  actual Layer 1 (`validation_gate`) and Layer 2 (`prescreen_signal.py`) runs do that,
  per `09_cost_hurdle_gate.md`'s acceptance criteria. This map is advisory triage.
- It does not resolve whether `sigma_bar_bps_default: 15.0`'s comment in
  `campaign_config.yaml` ("encodes 1h crypto mid-volatility assumption") is misleading
  given the real measured value is ~62.5 bps — flagged as an observation from the
  reconciliation trace, left untouched, out of scope for this map.
- It does not attempt to price trend-following archetypes at all — `model_blind` is a
  refusal to score, not a disguised verdict.
- It does not cover portfolio-construction or accrual/carry hypotheses (Scope header).
- **This document is frozen as of this revision.** Any future question about a
  specific hypothesis's cost feasibility goes through the actual Layer 1/Layer 2 gates,
  not a future rev. 4 of this map.
