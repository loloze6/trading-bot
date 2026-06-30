---
name: quant-fundamentals
description: Verified mathematical identities and confirmed code behaviors relating the
pipeline's diagnostic metrics and config semantics. Required reading before applying
diagnostic rules or proposing config changes based on metric values. Contains ONLY
statements that are always true by construction or directly verified in source — no
heuristics, no market-condition-dependent claims.
---

# Quant Fundamentals

## Mission
Provide a shared, verified reasoning base so that every pipeline stage that interprets
diagnostic metrics or authors config does so from correct mathematical relationships and
confirmed engine behavior, not pattern-matched heuristics or unverified assumptions about
how the system works. If a SKILL.md rule elsewhere in this pipeline contradicts a statement
in this file, this file is authoritative — flag the contradiction rather than silently
following the other rule.

## How to use this file
Before proposing any diagnosis or config change based on a metric value (cost_drag, corr,
sharpe, win_rate, trade_count, etc.) or any regime/strategy config, check whether this file
contains a relevant identity or confirmed behavior. If it does, your reasoning and your
output must be consistent with it.

---

## Cost drag mechanics
cost_drag_pct = (gross_pnl - net_pnl) / abs(gross_pnl) × 100
  Source: trading-bot/reporting/run_artifact.py (build_core function).
  Algebraically equivalent to: total_fees / |gross_pnl| × 100.

Decomposed: cost_drag = (n_trades × fee_per_trade) / |n_trades × avg_gross_pnl_per_trade|
                       = fee_per_trade / |avg_gross_pnl_per_trade|

KEY IDENTITY: cost_drag is invariant to position size and leverage. Scaling forecast-to-
allocation mapping (e.g. changing a sizing divisor or scaling_factor's magnitude only)
scales both fees and gross_pnl by the same factor, leaving the ratio unchanged. A "sizing
fix" is not a coherent response to high cost_drag — sizing changes cannot move this ratio.

The only variables that change cost_drag:
1. fee_per_trade — fixed by exchange fee schedule, not a pipeline tuning lever.
2. avg_gross_pnl_per_trade — driven by (a) signal strength on entries that fire (does this
   bar's forecast direction match the actual subsequent price move), and (b) trade
   duration — a longer hold captures more price movement before the position closes,
   raising avg_gross_pnl_per_trade for the same fee cost. avg_trade_duration_bars is now
   tracked in protocol_result.yaml core metrics (added in STEP_02) — use it to test cause
   (b) directly rather than assuming.
3. n_trades does not appear in the simplified ratio — it affects TOTAL net_pnl but not the
   cost_drag RATIO itself, since fees and gross_pnl both scale with n_trades together,
   UNLESS the added trades have systematically different avg_gross_pnl_per_trade than
   existing trades (e.g. relaxing a regime gate admits lower-conviction bars with smaller
   average price moves) — in that case cost_drag changes because avg_gross_pnl_per_trade
   changes, not because n_trades changed per se. Always check whether newly-admitted trades
   have a different forecast magnitude distribution before attributing a cost_drag change
   to "more trades."

---

## Position rebalancing behavior (CONFIRMED)
The engine does NOT submit a new order on every bar a regime is active. Rebalancing is
gated: a position change only executes when |allocation_change| >= 0.20 (config field
min_allocation_change.threshold; enforced in risk_manager.py, _ctrl_min_allocation_change).
A forecast shift smaller than this threshold does not trigger a trade.

Implication: high trade counts within a single regime activation are NOT generally caused
by per-bar rebalancing. If a window shows an unexpectedly high trade count, check the
regime gate configuration first (see "default_regime trap" below) before assuming an
execution-layer cause.

---

## The default_regime trap (CONFIRMED bug pattern, contaminated 5 historical runs)
A regime detector config has a `default_regime` field — the label assigned to any bar that
does not match an explicit rule. If `default_regime` is set to the same label as an active,
signal-bearing regime (e.g. `default_regime: trending` when `trending` is also a rule-based
regime with its own ER/VR thresholds), then EVERY bar that fails the explicit threshold
check still gets classified as `trending` via the default — making the regime gate
functionally inert. The strategy will trade on every bar regardless of ER/VR values,
producing trade counts far above what the stated thresholds would predict, and cost_drag
will reflect an unfiltered signal, not the gated one the config claims to specify.

GENERAL PRINCIPLE: any fallback/default classification must use a label that is NOT also
used by an explicit, conditional rule in the same config. Before trusting any run's
diagnostics, verify default_regime is set to a genuinely neutral label (e.g. "unknown") and
is never equal to any regime name appearing in the `rules` or `regimes` block.

CONFIRMED HISTORICAL IMPACT: run_016, run_021, run_022, run_023, run_034 all had
default_regime: trending and produced trade counts and cost_drag figures that do not
reflect the stated ER/VR gate. Any conclusion drawn from these runs about regime
selectivity or threshold sensitivity should be treated as unverified unless independently
confirmed by a clean-config rerun.

---

## Sample size and statistical claims
Two distinct reliability gates apply in this pipeline. They measure different things and
must not be conflated:

GATE A — Regime bar count (n_bars):
  n_bars counts the number of bars classified into a given regime label across a window.
  This controls the reliability of the regime_validity forward_return_mean.
  Operative threshold (from verdict-interpreter/SKILL.md Rule 4): n_bars < 20 means the
  forward_return_mean for that regime is not reliable enough to declare the regime
  "uninformative" — route to Rule 5 (sample problem) instead of Rule 4 (label problem).
  Source: verdict-interpreter/SKILL.md Rule 4. Use n_bars=20 only for this purpose.

GATE B — Trade count (executed trades):
  Trade count is the number of position changes that actually executed within a window.
  This controls the reliability of per-window Sharpe, win_rate, and forecast_return_corr.
  A regime may activate on many bars (high n_bars) while generating few trades, because
  the rebalancing gate requires |allocation_change| >= 0.20 to trigger an execution
  (see "Position rebalancing behavior" above).
  No operative minimum trade count is defined anywhere in this pipeline.
  quant-validation/SKILL.md lists `min_trade_count` as an available decision criterion
  but assigns no specific number. This is an unresolved gap requiring a human decision —
  do not substitute n_bars=20 or any other number as a proxy. Flag it as an open gap if
  you encounter a situation where trade count appears too low to trust a point estimate.

WORKED EXAMPLE (confirmed clean data, Keltner mean-reversion / TRENDING regime / 1h /
BTCUSDT+ETHUSDT, run_017 and clean replications run_024, run_027, run_033):
- ER>=0.50 AND VR>=1.20 gate: ~2.5 trades/window/symbol, corr=0.214 (signal strong, trade count thin)
- ER>=0.35 AND VR>=1.20 gate: ~10 trades/window/symbol, corr=0.041 (trade count adequate, signal weak)
- ER>=0.30 AND VR>=1.20 gate: ~11 trades/window/symbol, corr=0.082 (trade count adequate, signal weak)
The ~2.5 and ~10/~11 figures are TRADE counts, not bar counts. The regime fires on many
more bars than that — the low trade count at ER>=0.50 is a consequence of the 0.20
allocation-change gate, not of the regime firing rarely. This distinction matters when
diagnosing whether to relax the regime threshold (would increase bar count) vs. relax the
rebalancing gate (would increase trade count for the same regime activation).
This shows signal strength and trade-count sample size trading off sharply across this
specific threshold range for this specific signal — there is no threshold tested that
delivers both an adequate per-window trade count AND a strong correlation. This is a
property of THIS signal under THIS regime definition, not a general law — do not
generalize this specific tradeoff to other signals or regimes without re-verifying.

A regime's "informative: true/false" label (in regime_validity blocks) should always be
read alongside n_bars for that regime. The reliability minimum for this classification is
n_bars=20 (Gate A above, from verdict-interpreter/SKILL.md Rule 4).

---

## Regime firing frequency vs. regime quality
These are different failure modes and require different fixes:
- Regime label is "uninformative" (forward returns near zero with n_bars above the
  reliability minimum of 20) → the regime DEFINITION doesn't capture a real market state
  distinction. Fix: redefine the regime (different indicators/thresholds).
- Regime fires on too few bars to produce a stable estimate (n_bars below 20) → this is a
  SAMPLE SIZE problem, not a label quality problem. Do not conclude the regime concept is
  wrong from a small-n result.
- Regime appears to fire on far more bars than the stated thresholds should allow → check
  default_regime configuration first (see above) before concluding the signal lacks
  selectivity.
Conflating these is a confirmed historical failure mode (STEP_01 Rule 4/6 audit; the
default_regime contamination of 5 runs). Check n_bars, forward_return_mean, AND
default_regime configuration before attributing any result to regime quality.
