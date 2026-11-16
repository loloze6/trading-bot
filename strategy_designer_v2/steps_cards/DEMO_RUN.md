# Run brief: demo_run (written after the run, 2026-11-16)

This brief was written after the run, to give every named run one; its purpose is the one stated when each call was
made, its outcomes were not pre-registered.

**Purpose.** Validate the orchestration functions on real ideas, one function at a time: `run_idea` (one idea through
steps 3 to 7), then `select_next` and `loop` (the next idea chosen by its score, turn after turn, until a budget).

**Scope.** The starting idea: the 002-03 repair from 7.d (`...d1_above-average-drift-near-highs`), brief 002, six
coins (BTC, ETH, LTC, XMR, XRP, ZEC), folds A to D, daily bars. Two loop calls: budget 4 USD, then 15 USD.

**What happened.** 12 ideas tested, 18.30 USD in all: 6 confirmed, 6 inconclusive, none with a profitable book (the
checks that fail are mostly mean daily return and Calmar: real effects too small to pay). Every window ran on every
coin. Readings: `orchestration/run_idea/validation/reading.md`, `orchestration/loop/validation/reading.md`,
`orchestration/select_next/validation/reading.md`.
