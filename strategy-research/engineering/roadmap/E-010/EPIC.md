# E-010 — Slippage and lot-size/min-notional model

**State:** new
**Owner:** Jeremy
**Updated:** 2026-08-04

## Why

Handed over by Dorian on 2026-07-31 with a decision-ready spec ("🎯 Slippage
model — decision-ready spec", Notion) — queue #4 on his board, sitting on
this side, and absent from `EPICS.md` until now. `MockExecutionHandler`
today fills every order at the exact bar close with zero slippage; the only
modelled cost is the 10 bps fee, so every backtest result produced so far is
optimistic by construction. Cost error changes WHICH strategies a generator
proposes, not merely how they score — a generator optimizing against
zero-slippage fills systematically proposes high-turnover mirages. That is
why Dorian sequenced this by irreversibility (it changes what gets selected)
rather than by severity.

## Done when

RATIFIED 2026-08-04: the operator ratified Dorian's spec as-is, with one
amendment (criterion 4 below) and two recorded limits (see "Known limits").
S0 is ticked.

NOTE for the record: ratifying accepts the spec's premise that execution-core
changes stay on Jeremy's side under single-writer. That is a
division-of-labour commitment for all of E-010, not just this spec.

Derived from the spec's own acceptance criteria (spec was reachable and read
this dispatch — not left blank per the E-004 precedent):

`MockExecutionHandler` applies flat-bps slippage against the trade direction
(buys fill above close, sells below) and lot-size/min-notional rounding
(hardcoded Binance BTCUSDT filters, no network calls in backtests), as two
independently switchable knobs (`slippage_bps`, rounding on/off), both off by
default. Verify:

1. Default (both knobs off): `python trading-bot/main.py simulate` reproduces
   byte-identical output to the existing baseline (`config_sha 5ccbec42` /
   `data_sha 5a75366c`) — a bit-identity test in the shape of
   `tests/test_warmup_prefetch_bit_identical.py` passes.
2. The same run at `slippage_bps=5` and `slippage_bps=10` produces recorded,
   differing deltas against the 0 bps baseline, with fee and slippage drag
   attributed separately in the run artifact.
3. A mutation test confirms: with the flag off, breaking the slippage code
   path is provably invisible (output unchanged); with the flag on,
   disabling it fails a test.
4. A run whose symbol is not BTCUSDT RAISES rather than falling through to
   BTCUSDT's lot-size/min-notional filters. Rationale: `config.json` has
   `symbols: ["BTCUSDT"]` so the hardcoded filters are correct today, but the
   campaign runs multi-symbol (P4_ts_trend uses BTCUSDT and ETHUSDT;
   `local_data/` holds 19 pairs). A silent fall-through would apply BTC's
   filters to ETH and produce quietly wrong numbers. Loud failure over silent
   wrongness.

**Baseline dependency:** E-012 (two-bars manifest/loop defect) will break the
`config_sha 5ccbec42` / `data_sha 5a75366c` pins in criterion 1 above — both
E-012's manifest fix and its loop fix do. Either E-010 lands while that
baseline is still stable, or its hashes are re-pinned after E-012 resolves.
Not resolved here; recorded as a dependency.

## Known limits

Accepted, not defects — recorded so nobody later cites the output beyond what
it supports:

- Flat-bps slippage is size-independent and will UNDERSTATE cost on the
  largest rebalances. Accepted for v1; the spec defers a depth-dependent
  model. Mitigating context: the engine has no drift gating and rebalances on
  every nonzero delta (`trading_bot.py:229`), so turnover is high and
  dominated by many trades rather than a few large ones — flat bps captures
  most of the effect for THIS engine.
- 5 and 10 bps are SENSITIVITY PROBES, not calibrated costs. No one has
  measured real BTCUSDT slippage. The deltas show how much apparent edge is
  cost-sensitive; they do NOT state what costs are. This wording must survive
  into the run artifact.

## Stories

- [x] S0 — Operator ratifies the spec: as-is, modified, or rejected.
      RATIFIED as-is, with the non-BTCUSDT hard-fail amendment and the two
      recorded limits above (2026-08-04).
- [ ] S1 — Implement flat-bps slippage + lot-size/min-notional rounding in
      `execution/execution_handler.py`'s `MockExecutionHandler`, both knobs
      off by default.
- [ ] S2 — Bit-identity test (default path) + mutation test (flag on/off) +
      the 0/5/10 bps comparison run, deltas recorded in the run artifact.
- [ ] S3 — Decide whether the default flips. Off-by-default is correct for
      landing safely, but a knob that is off by default does not fix "every
      result is optimistic by construction". After the 0/5/10 bps deltas are
      measured, decide whether slippage becomes on-by-default and at what
      bps. The spec is silent on this.

## Log

- 2026-08-03 — `new`. Surfaced from the fork sync (dispatch W27); spec is
  Notion "🎯 Slippage model — decision-ready spec" (handed to Jeremy
  2026-07-31). Spec was read this dispatch — reachable, so a testable Done
  when was derived from it rather than left unwritten.
- 2026-08-04 — Operator ratified the spec as-is, with the non-BTCUSDT
  hard-fail amendment (Done-when criterion 4) and two recorded limits
  (flat-bps size-independence; 0/5/10 bps as sensitivity probes, not
  calibrated costs). S0 ticked; S3 added. Baseline dependency on E-012
  (two-bars manifest/loop defect) recorded against the config_sha/data_sha
  pins in criterion 1. Next step: S1 (dispatch W31).
