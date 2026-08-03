# E-010 — Slippage and lot-size/min-notional model

**State:** new
**Owner:** Jeremy
**Updated:** 2026-08-03

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

## Stories

- [ ] S1 — Implement flat-bps slippage + lot-size/min-notional rounding in
      `execution/execution_handler.py`'s `MockExecutionHandler`, both knobs
      off by default.
- [ ] S2 — Bit-identity test (default path) + mutation test (flag on/off) +
      the 0/5/10 bps comparison run, deltas recorded in the run artifact.

## Log

- 2026-08-03 — `new`. Surfaced from the fork sync (dispatch W27); spec is
  Notion "🎯 Slippage model — decision-ready spec" (handed to Jeremy
  2026-07-31). Spec was read this dispatch — reachable, so a testable Done
  when was derived from it rather than left unwritten.
