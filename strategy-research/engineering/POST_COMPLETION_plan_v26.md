# Post-completion report — delivery plan v26 + continuation (C4.4 + C6.5)

**Written:** 2026-10-03. **Covers:** `delivery_plan_v26.md` (slices 0–8, built behind flags) and
`delivery_plan_v26_continuation.md` (C0–C7), with the real-run evidence of C4.
**Sources:** `runs/run_065/pipeline_state.yaml`, `runs/run_066/pipeline_state.yaml` (audit_log,
halt_history; runtime files, not committed), each run's `artifacts/idea_status.yaml`,
`decision_record.yaml`, `grid_evaluation.yaml`, `campaign_record/campaign_state.yaml`
(trial rows), `engineering/OBSERVATIONS_QUEUE.md` (O-1..O-19), PRs #235–#310.

**Measured vs estimated.** Every number marked *(m)* is read straight from a file above.
*(d)* = derived from measured timestamps (start = end timestamp − `execution_time_seconds`).
*(e)* = estimate. Cost is the `cost_usd` the Claude SDK reports per call: an API-price
equivalent. The calls go through the operator's Claude account (no API key, C0.3), so it is
not an invoice; it is the right number for comparing stages and runs.

## In plain words

- The new pipeline ran end to end on real data, twice, on Kraken perp briefs: idea → base
  config → variants → backtest → profit bars → five readers → memory → decide-next.
- **run_065** (Donchian daily trend) needed two hand resumes for two bugs (CUL-379, CUL-380),
  both fixed the same day. **run_066** (vol-managed trend, 1h) ran hands-off, no pause.
- Both ideas were **refuted** by the profit bars. That is a valid outcome, not a failure of
  the pipeline.
- One AI run costs about **$0.90–1.35** and **~26–34 min** of active time *(m/d)*.
- Every stage answered in **1 turn** (CUL-336 closed-book check holds).
- What did not work: the run tested a block, not the idea's own claim (O-16/O-18), and the
  readers produced no usable next idea (O-19). That is what E-068 now redesigns.

## run_065 — `C4_donchian_daily_trend_kraken_perp` (1d bars, 3 variants)

| Stage | Calls | Turns | Tokens | Cost $ | Time |
|---|---|---|---|---|---|
| hypothesis_generation (1a) | 2 (1 lost, CUL-379) | 1 each | 144,193 | 0.389 | 321 s |
| strategy_config_authoring (1b) | 1 | 1 | 44,450 | 0.132 | 128 s |
| innovation_expansion (2) | 1 | 1 | 53,974 | 0.158 | 162 s |
| backtest_spec + data gate + backtests + reports (tools) | — | — | 0 | 0 | ~2.0 min *(d)* |
| specialist_readers (5 lenses) | 7 (regime_power ×3, CUL-380) | 1 each | 201,467 | 0.655 | 807 s |
| regroup_record + decide-next (tools) | — | — | 0 | 0 | ~3 s *(d)* |
| **Total** | **11** | | **444,084** | **1.334** | LLM 1,419 s |

- **Wall time** *(d)*: 15:52 → 19:16 UTC, 2026-10-02 = 3 h 23 min, of which **~26 min active**
  and ~2 h 57 min paused waiting for fixes.
- **Pause 1** (15:56, *(m)* `halt_history`): `Missing files: hypothesis_card.yaml`. Step 1a
  wrote the file name above its YAML fence, so the answer was dropped, and a missing
  deliverable was never retried. Fixed by **CUL-379 / PR #306**. Resumed by hand at 16:33
  (~37 min).
- **Pause 2** (16:52): `regime_power reader output invalid after one retry`. A malformed
  *advisory* proposal stopped the run before the decisive verdict was recorded (O-17). Fixed by
  **CUL-380 / D-061 / PR #307** (a bad proposal is dropped and recorded, never a stop). Resumed
  by hand at 19:12 (~2 h 20 min). Only regime_power and component_attribution re-ran.
- **Wasted spend** *(m)*: $0.210 (lost 1a answer) + $0.215 (two failed regime_power calls) =
  **$0.425**, about a third of the run.
- **Outcome** *(m)*: `idea_status: refuted` — "at least one criterion FAILed with sufficient
  data". 3 trial rows (`run_065:base`, `:donchian_period_14_reactive`,
  `:donchian_solusdt_crossasset`), memory upserted, decision record written, holdout untouched
  (`holdout_reserved: false`).

## run_066 — `C4_vol_managed_trend_kraken_perp` (1h bars, 4 variants)

| Stage | Calls | Turns | Tokens | Cost $ | Time |
|---|---|---|---|---|---|
| hypothesis_generation (1a) | 1 | 1 | 66,638 | 0.177 | 131 s |
| strategy_config_authoring (1b) | 1 | 1 | 42,989 | 0.126 | 129 s |
| innovation_expansion (2) | 1 | 1 | 53,132 | 0.160 | 155 s |
| backtest_spec + data gate + backtests + reports (tools) | — | — | 0 | 0 | ~19.1 min *(d)* |
| specialist_readers (5 lenses) | 5 | 1 each | 140,267 | 0.437 | 452 s |
| regroup_record + decide-next (tools) | — | — | 0 | 0 | ~2 s *(d)* |
| **Total** | **8** | | **303,026** | **0.900** | LLM 867 s |

- **Wall time** *(d)*: 19:56 → 20:30 UTC = **33.7 min, no pause**. The 19 min of tool time
  is the hourly backtests (24 bars a day against run_065's one).
- **Outcome** *(m)*: `idea_status: refuted`. 3 graded trial rows (`base`,
  `keltner_extended_momentum`, `sol_infra`). `xrp_payment` was **not tested**: the data gate
  skipped it for 1.7 % missing bars in one month (within its 5 % tolerance). It never validates
  the idea (card D, as designed), but skipping on a gap that small is the CUL-367 / CUL-344
  item 8 problem: tell data quality apart from missing windows.
- **Decide-next** *(m)*: rule R2 fired and queued `…__more_1` for both briefs (ask 1a for
  another hypothesis). Those entries are held `blocked_on_e068` (see below).

## Cost and time per run

| | run_065 | run_066 |
|---|---|---|
| LLM cost (m) | $1.33 (of which $0.43 wasted on bugs) | $0.90 |
| Clean-run cost (e) | ~$0.91 | $0.90 |
| Tokens (m) | 444k | 303k |
| Active time (d) | ~26 min | ~34 min |
| Hand interventions | 2 | 0 |

- **Where the money goes** *(m)*: readers ~49 % of a clean run, 1a ~20 %, 1b + step 2 ~32 %.
  Backtests cost no LLM money; on 1h bars they are the longest step.
- **C4 as a whole** *(m)*: the four earlier attempts (run_061–064, stopped by the O-1..O-12
  bugs) cost $0.63 + $0.34 + $0.44 + $0.47 = $1.88. **C4 total ≈ $4.12** for six runs.
- **D-063 (PR #310) adds inputs to the readers** after these runs: about +20k tokens per reader
  call, **+$0.13 per run (e)**. To be measured on the next run.

## What worked

- **The joined-up path.** C1.1's end-to-end wiring test (#238) plus C1.2–C1.7 (#241–#243):
  the first real run did not crash at setup, as the review predicted it would before C1.
- **Closed-book stages** (CUL-336, #235): 19 of 19 calls, `num_turns: 1`.
- **One coin per variant, per-variant reports, crashed variant never validates**
  (#248, #251–#253): visible in run_066 (xrp untested → idea cannot validate).
- **Profit bars v2** (E-062: #236, #240, #254–#259, #261, #265–#267, #269): whole-test portfolio Sharpe/drawdown, DSR on the
  same basis, signed bars; both runs graded on it.
- **Score provenance** (#263–#264): every reader call stamped with the observed model
  (`claude-haiku-4-5-20251001`); readers that self-reported "claude" were flagged
  `self_report_differs`, not trusted.
- **Memory + decide-next**: `campaign_memory.yaml` upserted per run; decide-next wrote a decision
  record each time and R2 minted the next step without a human.
- **Trial counting**: every graded variant landed a `run:variant` row, including the refuted
  ones.
- **Holdout**: never touched by either run.

## What broke (and where it went)

| Id | What, in plain words | Status |
|---|---|---|
| O-1 | "Long-only" component check at the wrong level (run_061) | fixed (#280) |
| O-2 | Step 2 sending the brief back to 1a | working as intended; prompt gap |
| O-3 | 1a declaring a brief exhausted on a cost argument | fixed: cost vetoes deleted (#292) |
| O-4 | Step 2 invented a component class name | fixed: catalogue given to step 2 (#280) |
| O-5 | Asset variants evicted, not re-windowed | SOL as intended; XRP a design gap |
| O-6 | Park reason said "component" when failures were data | fixed (#291) |
| O-7 | Breakout (threshold) idea in a linear-forecast design | fixed: graded forecasts only (#280–#282) |
| O-8 | Data gate blocked every version over small gaps | partly fixed: D-060 / CUL-374 (#305); target design CUL-367 |
| O-9 | Nothing before the backtest says which windows run | partly: `window_months` D-059 (#303); check parked CUL-372 |
| O-10 | `base` made 0 trades: forecast shrunk ~1,000,000× | fixed: size probe D-056 (#295) |
| O-11 | Grading stopped on two faults (run_064) | mostly fixed: CUL-369 (#300), CUL-370 (#302, ticket still open), CUL-368 partly (#298) |
| O-12 | Brief's venue/product never reached the backtest | fixed: D-057 (#298) |
| O-13 | Size check passes two "zero" cases | by design (#295) |
| O-14 | Binance spot fee + margin slippage mix | parked: Kraken is the venue |
| O-15 | Whole-test chain skips each window's first day | parked: monthly-restart artifact |
| O-16 | run_065's grid did not test run_065's claim | open → E-068 |
| O-17 | Advisory reader proposal halted the run | fixed: D-061 / CUL-380 (#307) |
| O-18 | A run should prove a written finding, not only score a block | open → E-068 |
| O-19 | Readers produced no usable next idea | partly: CUL-381 (#309), D-063 (#310); rest in E-068 |

| Ticket | What | PR |
|---|---|---|
| CUL-369 | Consecutive windows shared a day | #300 (D-058) |
| CUL-373 | Conformance compared spellings, not coins, on a venue protocol | #304 |
| CUL-374 | Data gate paused on gaps the engine already ignores | #305 (D-060) |
| CUL-375 | Prepare C4 on Kraken perp (new briefs, 4-month windows, dry run) | briefs + dry run |
| CUL-376 | Launch both C4 Kraken briefs to a graded result | run_065, run_066 |
| CUL-379 | Stage answer with its file name above the YAML fence was lost; no retry | #306 |
| CUL-380 | Reader new_block shape not stated; a bad proposal stopped the run | #307 (D-061) |
| CUL-381 | Readers fed another run's detector report | #309 (D-062) |

Still open from C4: CUL-367 (data quality vs missing windows; would have kept `xrp_payment`),
CUL-368 (Kraken asset-variant cost entry, partly fixed), CUL-370 (report size, in progress),
CUL-372 (window check, parked), CUL-377/378 (window boundaries, warm-up check).

## Verdict on the plan

- **C0–C3: done.** **C4: done with caveats** (run_065 needed two hand resumes; run_066 clean).
- **C5:** C5.1, C5.6, C5.7, C5.8 done; C5.2 superseded by E-068 (composable claim tests);
  C5.3/C5.4/C5.5 become backlog decision tickets; C5.9 (CUL-335) moves to E-067;
  C5.10 (E-035) stays parked.
- **C6:** C6.1, C6.2 done; C6.3 two of three one-pagers written (`docs/OPERATOR_START_CAMPAIGN.md`,
  `docs/OPERATOR_UNLOCK_HOLDOUT.md`), "read a run's results" waits for E-068 (readers change);
  C6.4 (roadmap v28) deferred until after E-068; C6.5 is this file.
- **C7** becomes the parked epic E-070 (legacy clean-up).

## Decisions now open for the operator (C4.4)

1. **Models per stage.** Today every stage runs on Haiku 4.5. Readers are half the cost and
   produced nothing usable (O-19), but the cause was missing inputs and a wrong job, not only
   the model. Recommendation: keep Haiku until E-068's readers v3 exist, then compare on one
   run (E-069 holds the per-stage model setting).
2. **Continue the campaign?** Recommendation: not before E-068 slice 1. Another run today would
   again score a block without testing the idea's claim; the R2 entries stay `blocked_on_e068`.
