# Vectorized panel research path — XS_momentum

Dispatch: build a research-only vectorized panel backtester, validate it reproduces an
archived single-symbol engine run (gate), then run XS-momentum on the ratified 19-pair
Kraken universe. Precondition manifest e7c8749 / clean: CONFIRMED.

## Scope boundary (hard)
- Research-only. NO edits to core/backtester.py, main_strategy.py, RollingBuffer, or any
  production engine path. New code lives in strategy-research/tools/ only.
- Engine gap = ledger blocker: single-symbol load (backtester.py:92,:359),
  unpartitioned RollingBuffer (main_strategy.py:44), zero netting hooks. Same blocker
  class as P4_ts_trend's daily-bar gap.

## Reproduction target (gate)
Archived run: run_054 (P4_ts_trend, SmaTrendLongOnlyComponent L=100, daily, long-only,
regime always `unknown`). 30 window-symbol slots (BTC+ETH x 15 semi-annual windows),
Binance daily data (local_data/*_1d.csv), DEFAULT commission 10 bps, initial 1000 USDT.
Recorded headline metrics per window in runs/run_054/protocol_summary.json.

Signal (exact): forecast_T = 10 if close[T-1] > SMA100(close)[T-1] else 0; identity
transform; standardization skipped; alloc = forecast/10 (binary 0/1). Trades = signal
flips; fill at close[T]; final open position force-closed at window end.

## PRE-REGISTERED TOLERANCE (declared before seeing any comparison)
- trade_count: EXACT integer match, all 30 slots. (Strongest diagnostic: any mismatch =
  signal / execution-timing / rebalance-gating divergence.)
- net_return_pct: |Δ| <= 0.5 pp OR <= 2% relative, whichever larger, per slot.
- sharpe: |Δ| <= 0.10 absolute per slot (engine rounds to 3dp).
- max_drawdown_pct: |Δ| <= 0.5 pp absolute per slot.
- gross_pnl / net_pnl / fees_paid: <= 2% relative per slot.
Rationale: mechanics are deterministic; a faithful reimplementation on identical data
must match to rounding. These bands absorb float/rounding + the documented one-bar-lag /
fill-at-close approximation, but a real return/cost/Sharpe bug blows past them.
GATE PASSES only if ALL 30 slots pass ALL bands. Any failure => STOP + report (no
tolerance widening, no target swap).

## Cost model reuse (no fork)
- Gate: 10 bps default (what run_054 used) to reproduce.
- XS run: cost_model.yaml `perp` block, 5 bps taker / 10 bps round-trip, per dispatch
  step 4. Funding NOT modeled (valid: XS is price-based). Read the YAML directly; do not
  re-derive.

## XS-momentum mechanics (each a STOP if violated)
- (a) no forward-fill into ranking — exclude asset at that bar
- (b) dollar-neutral long-top / short-bottom
- (c) pointwise entry, no lookahead on listing dates
- (d) rank at bar t uses data through t; positions taken at t+1
- Universe: 19 pairs; effective start 2017-05-18; min viable n=6; ~75,200 bars.

## Steps
- [x] Confirm manifest
- [x] Read engine: backtester, run_protocol, forecast_manager, components, metrics,
      build_core, launcher, portfolio_info, execution_handler
- [x] Locate data (Binance daily; 19 Kraken 1h)
- [x] Pre-register tolerance
- [x] Build panel_backtester.py (verbatim metric fns + sequential sim + SMA + XS)
- [x] Run gate vs run_054 (30 slots), side-by-side
- [x] GATE DECISION: PASS — all 30 slots reproduce net_return/sharpe/max_dd/trade_count
      EXACTLY to 3dp (tighter than pre-registered bands); fees/gross/net within 2%.
- [x] XS run on 19-pair panel: net Sharpe 1.325 / gross 1.665; DD -62% (200% gross);
      turnover 423x; NOT cost-dominated; no-lookahead confirmed; decays post-2021
      (net 0.77) -> 2025 (net ~0.07). Cross-section n>=6 first at 2017-05-26.
- [x] C7-style verdict: REFINE (positive lean). median/overall net Sharpe > 0 (promote
      bar cleared) but DD > 30% bar (leverage-convention-dependent) => not clean promote;
      well above kill; not cost-dominated. Fork to research path VINDICATED.
- [ ] Register (venue, research-only, research-path flag); ledger; KB finding; commit;
      read-back after each write
