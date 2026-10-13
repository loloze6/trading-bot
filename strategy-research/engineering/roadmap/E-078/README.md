# E-078 · Branch 3 recognises slow strategies (new metrics)

Ruling 2 item (2), operator decision 2026-10-13. Linear: project E-078.

## Items

1. **Trade-frequency bar.** Trades ÷ bars in the window ≥ X %. X is set in this epic,
   not yet decided (see "Open decision" below). It replaces the sample floor that
   `trade_count_min` gave until D-118 switched it off; until it lands, the operator's
   review reads the trade count (D-118).
2. **Leave-one-block-out bar.** FAIL if any leave-one-out whole-test Sharpe ≤ 0. A block
   is a window under interleaved folds (B, C) and a 4-month slice under contiguous
   folds (A, D); with the folds in `config/folds.yaml` every window is one 4-month
   block, so in both cases a block is a window.
3. **Buy-and-hold bar on Sharpe.** Done: D-120 (`buy_and_hold_sharpe_excess_min`,
   strategy whole-test Sharpe > basket buy-and-hold Sharpe on the same chain and cost
   convention; the return excess kept as information).

## One-time read-only numbers (ruling 2 item (2))

**Fragility condition, stated before the scripted run:** a run is fragile if **any
leave-one-block-out whole-test Sharpe ≤ 0**.

Disclosure: before this folder existed, the same numbers were computed once ad hoc in
the session (same functions, same runs, read-only). The scripted run below is the
record; it reproduces them.

- Script: `leave_one_out_and_bh.py` (read-only: reads `runs/<run>/artifacts/` and the
  trial ledger, writes nothing into the runs). Run from `strategy-research/`:
  `../venv/Scripts/python.exe engineering/roadmap/E-078/leave_one_out_and_bh.py run_084 run_088 run_089`
- Definitions: the whole-test Sharpe is `portfolio_whole_test.whole_test_sharpe` of the
  chained equal-weight daily returns (`run_phase1_research._whole_test_chain`, the
  profit bar `sharpe_min`'s chain). Leaving a block out drops that window's days from
  the chained daily returns (each window starts from its own capital, D-116, so the
  other windows' returns are unchanged). The basket buy-and-hold Sharpe is the
  `buy_and_hold_sharpe_excess_min` row's `detail.buy_and_hold_sharpe` (D-120).
- Results: `RESULTS.md` (written by the script's output, copied verbatim).

## Open decision

- X for the trade-frequency bar. Any value chosen now is chosen after seeing lane 1's
  trade counts; say so in its D-row.
