# E-039 S1 — Characterise and stop: Findings

**Stage:** S1 only. No code touched (A8.6 not removed, `validation_gate` not modified, no
post-backtest gate built). Per the dispatch and `EPIC.md`'s own two-phase discipline, this
document reports and stops.

**Scope note on method:** every number below was either read from an existing artifact on
disk or produced by actually invoking `strategy-research/tools/run_protocol.py` — the same
tool and argument shape `workflow/run_phase1_research.py`'s `protocol_execution` stage uses
(`run_phase1_research.py:1160-1164`) — from `strategy-research/` with the repo's own
Windows venv (`../venv/Scripts/python.exe`, per `run_phase1_research.py:88-98`). I ran
`run_protocol.py` directly rather than through the full orchestrator, so the C7
`pass_rule_evaluation.yaml` step and campaign-state trial recording (which live in the
orchestrator wrapper, `run_phase1_research.py:1226-1284`, not in `run_protocol.py` itself)
were **not** produced by these re-runs — only the core backtest artifacts
(`protocol_summary.json`, `trade_diagnostics.json`) were, which is what's needed to answer
S1's question. No holdout data was read; every protocol used here has
`sample_split_design.walk_forward_range` ending at or before `2025-12-31`, verified
per-run before executing (see Deliverable 1 table).

All new artifacts live under `runs/<run_id>/e039_s1_rerun/` (one new sibling directory per
run, next to the untouched original stub artifacts) and are left in place.

---

## Deliverable 1 — Re-scoring the 7 prescreen-killed runs

### Finding the 7

`grep -rl prescreen_stub strategy-research/runs/*/artifacts/protocol_result.yaml` returns
**7 distinct run_ids**: `run_043`, `run_044`, `run_047`, `run_048`, `run_050`, `run_053`,
`run_060` (an 8th hit, `run_044/attempt_2_invalidated_by_f5_bug/protocol_result.yaml`, is a
superseded attempt folder for `run_044`, not a distinct run). `run_057` — the epic's own
cited precedent — is **not** in this set: it already carries a real
`protocol_summary.json`/`trade_diagnostics.json`/`results/` from a 2026-07-11 manual
override (`prescreen_override_20260711.yaml`), which is why the epic could cite its verdict
already.

### Feasibility check (config + data + protocol, before running anything)

| run_id | protocol | timeframe | walk-forward window | data present locally? |
|---|---|---|---|---|
| run_043 | `protocols/baseline_v1.json` | 1h | 2024-01 → 2024-11 (11 windows) | Yes — `BTCUSDT_1h.csv`/`ETHUSDT_1h.csv` span 2018-01-01 → 2026-07-05 |
| run_044 | `protocols/baseline_v1.json` | 1h | 2024-01 → 2024-11 | Yes, same |
| run_047 | `protocols/baseline_v1.json` | 1h | 2024-01 → 2024-11 | Yes, same |
| run_048 | `protocols/run_048_generated.json` | 1h | 2018-02 → 2025-12 (96 windows) | Yes on disk, but see below |
| run_050 | `protocols/run_050_generated.json` | 1h | 2019-09 → 2025-12 (76 windows) | Yes on disk, but see below |
| run_053 | `protocols/run_053_generated.json` | 1h | 2018-01 → 2025-12 (96 windows) | Yes on disk, but see below |
| run_060 | `protocols/funding_mr_4h_retest_v1.json` | **4h** | 2019-12 → 2023-12 (49 windows) | 4h not cached as its own file; derived/fetched |

Every run had its `candidate_strategy_config.json`, `validation_protocol.yaml`, and
`pre_registration.yaml` intact in `artifacts/`, and every protocol JSON file referenced by
`prescreen_result.yaml` still exists under `protocols/`. **On paper, all 7 looked
re-runnable.** None of the 7 protocols' windows touch 2026 — all end at or before
2025-12-31, confirmed by reading each `validation_protocol.yaml.sample_split_design` and
each protocol JSON's own `windows` list before running anything.

### What actually happened when I ran them

| run_id | prescreen kill (route, IC, p) | re-run outcome | new information vs. the stub |
|---|---|---|---|
| **run_043** | `kill_no_ic`, ic=-0.0211, p=0.588 | **Completed.** 22/22 windows (BTC+ETH × 11 months). Real verdict **`refine`**, not kill: `BTCUSDT: median_sharpe=-2.452<=0, min_trades=10<20; ETHUSDT: min_trades=12<20`. | **Different verdict.** Prescreen said "no informational content, kill." The real backtest shows a live signal that's neither dead nor working: monthly Sharpes swing wildly (-9.4 to +8.1), per-trade expectancy is flat and insignificant (mean 0.42 bps, t=0.16, n=394), and the actual failure mode is a **trade-count floor violation**, not absence of edge. A prescreen-only process would have filed this as "no edge, pivot elsewhere"; the real backtest says "underpowered/noisy, don't pivot on this evidence yet." |
| **run_044** | `kill_no_ic`, ic_all=-0.0087, ic_active=0.0167, p=0.881 | **Completed.** 22/22 windows. Verdict **`kill`**: `median_sharpe=-10.126` (BTC) / `-7.321` (ETH), both `< -1`. | **Same top-line verdict (kill), much more specific.** Per-trade expectancy is a highly significant **-15.9 bps** (t=-11.46, n=2076 trades) with drawdowns to **-20.5%** in single months. The prescreen's diagnostics block was entirely `null` (no gross pnl, no trade duration, no per-trade expectancy — "N/A (prescreen kill — no backtest)"). The real run shows this isn't merely "no edge" but **actively destructive**, with a real trade-level cost story to point at. |
| **run_047** | `kill_no_ic`, ic_all=0.0084, ic_active=`null` (degenerate), p=1.0 | **Completed.** 22/22 windows. Verdict **`kill`**: `median_sharpe=-3.354` (BTC) / `-5.577` (ETH). | **Same top-line verdict, structurally different diagnosis — the run_057 pattern repeats.** `zero_trade_slot_pct = 50.0`: half the monthly windows fired **zero trades** (the `|funding_rate| > 0.0002` threshold rarely trips at 1h). Per-trade expectancy on the windows that did trade is significant and negative (-13.9 bps, t=-3.50, n=251). This is a **regime/threshold-starvation** diagnosis — exactly the shape of `run_057`'s "Rule 6 CASE B" finding the epic cites as structurally unavailable to a prescreen, reproduced independently on a second hypothesis. |
| **run_048** | `refine_inverted_ic` (not `kill_no_ic`) — the prescreen's own IC-by-era breakdown already found a 180° sign flip (`ic_active_bars` negative 2018-2023, positive 2024-2025) and recommended flipping entry polarity | **Completed** (finished after this report's first draft — updated with the final result). 190/190 window-backtests (95 windows × 2 symbols, 2018-02 → 2025-12), **47m34s wall-clock**, surviving the same 2018-2020 CCXT gap-filling that crashed run_050/run_060 outright. Verdict **`kill`**: `median_sharpe=-5.162` (BTC) / `-3.507` (ETH), both `< -1`. | **Tests something different from what the prescreen recommended, and reaches a more decisive version of the same top-line signal.** The prescreen's own route was `refine_inverted_ic`, i.e. its recommendation was "flip entry polarity and retest" — this re-run backtested the **as-configured (non-flipped) component**, since S1's job is comparing the prescreen kill against a real backtest of the same config, not implementing the prescreen's proposed fix. On that config, the real result is unambiguous: per-trade expectancy **-22.2 bps** (t=-8.36, n=1726 trades, the largest and most statistically decisive expectancy of any of the 7), `zero_trade_slot_pct=25.26%`. Where the prescreen's IC read was marginal (`ic_active_bars=-0.040`, p=0.081 — "significant but negative," its own words), the real backtest turns that into a clean, high-n, high-significance kill of the un-inverted config. It does **not** test whether the prescreen's actual suggested fix (inverting polarity) would have worked — that would be a new hypothesis with its own trial. |
| **run_050** | `kill_no_ic`, ic_all=0.0008, ic_active=0.0178, p=0.521 | **Attempted, crashed.** 9/152 window-backtests completed (2019-09 → 2020-05, mostly BTCUSDT), then `RuntimeError: No historical data for BTCUSDT over 2020-06-01..2020-07-01` (`trading-bot/core/launcher.py:743`), raised after a live CCXT fetch for that month returned nothing. | **Re-run infeasible to complete as-is.** Not a config/data-presence problem in the "file is missing" sense — `BTCUSDT_1h.csv` nominally spans this whole range — but the engine's own data path fell through to a **live network fetch** for parts of 2018-2020 and hit a real gap. Partial results available (mostly negative Sharpes, -8.6 to -5.6, one +2.6, +1.7) but no final verdict. |
| **run_053** | `kill_no_ic`, ic_all=-0.0145, ic_active=-0.0503, p=0.292 | **Completed** (finished after this report's second draft — updated with the final result). 192/192 window-backtests (96 windows × 2 symbols, 2018-01 → 2025-12), **52m00s wall-clock**, again surviving the 2018-2020 CCXT gap-filling without crashing. Verdict **`kill`**: `median_sharpe=-6.535` (BTC) / `-4.261` (ETH), both `< -1`. | **Same top-line verdict, and the single most statistically decisive result of any of the 7.** MACD is a dense signal at 1h across 8 years: `zero_trade_slot_pct=0.0` and **11,002 trades** total — an order of magnitude more than any other run here. Per-trade expectancy is **-14.66 bps at t=-17.45** (n=11,002), the tightest confidence interval in the set by a wide margin. The prescreen's own IC read (`ic_active_bars=-0.050`, p=0.292 — not even significant on its own terms) gave no basis for this level of confidence; the real backtest converts a statistically ambiguous IC into an unambiguous, high-n kill. |
| **run_060** | `kill_no_ic`, ic_all=-0.0069, ic_active=0.0162, p=0.532 | **Attempted, crashed.** 2/98 windows completed (2019-12, 2020-01: sharpe -3.74, -10.27), then `RuntimeError: No historical data for BTCUSDT over 2020-02-01..2020-03-01` (`trading-bot/core/launcher.py:743`), same failure class as run_050, on the genuinely-4h protocol. | Same infeasibility class as run_050: real config+data present, real backtest attempted, halted by a live-fetch gap rather than a design or authoring problem. |

### Headline

**Of the 7, 5 completed and gave a real, execution-verified verdict** (run_043, run_044,
run_047, run_048, run_053 — the last two finished mid-report and are updated with final
numbers in their table rows). **In every one of those 5, the real backtest produced
materially more specific information than the prescreen stub could**: one flipped the
topline verdict outright (run_043: kill → refine), and the other four kept "kill" but
replaced a null diagnostics block with a concrete, falsifiable mechanism — catastrophic,
highly significant negative expectancy for run_044, run_048, and run_053 (the last reaching
t=-17.45 on 11,002 trades, the most decisive statistic in the whole set); regime/threshold
starvation (50% and 25.3% zero-trade months) for run_047 and run_048, independently
reproducing the `run_057` pattern the epic cites twice over.

These 5 split into two very different cost profiles, both measured, not estimated:

- **run_043/044/047** (2024-only `baseline_v1.json`, 100% local cache): **~3.5-4 minutes**
  each. See Deliverable 2.
- **run_048/053** (95-96 window protocols reaching back to 2018, mixing local cache with
  live CCXT gap-fills pre-2020): **47m34s** and **52m00s** respectively — roughly **12-14×
  the clean wall-clock** for ~8.6-8.7× the window count, so genuinely more expensive per
  window too, but both *did* reach a verdict rather than crashing.

**Only 2 of the 7 (run_050, run_060) failed to reach any verdict at all.** Both hit a real
historical-data hole around 2020-06/2020-02 and raised
`RuntimeError: No historical data for BTCUSDT ...` at `trading-bot/core/launcher.py:743`.
**So the final picture is: long-lookback protocols are expensive and somewhat unreliable,
not categorically broken** — 2 of 4 protocols reaching back to 2018-2019 completed cleanly
(run_048, run_053, both at 12-14× the clean-case wall-clock), and 2 of 4 crashed outright
for the identical underlying reason (live CCXT fetches over a range the local cache doesn't
fully serve). A **50% failure rate at 12-14× the cost**, when it does work, is still a real,
previously-unmeasured risk that S3 (the post-backtest gate) and any policy of "always
backtest" needs to account for — it just isn't the "always infeasible" story the early,
partial data suggested.

---

## Deliverable 2 — Real backtest wall-clock

Measured with `time (...)` around the exact `run_protocol.py` invocation, wall-clock only
(the tool made no CPU/network split available; `user`/`sys` reported near-zero because the
Windows Git-Bash `time` builtin does not account subprocess CPU time on this platform — the
`real` figure is the trustworthy one and is what matters for a trial-slot cost anyway).

| run_id | windows × symbols | data source | wall-clock (`real`) |
|---|---|---|---|
| run_043 | 11 × 2 = 22 backtests, 1 year (2024), 1h | 100% local CSV cache, zero network calls | **3m45.482s** |
| run_044 | 22 backtests, same span | same | **3m39.221s** |
| run_047 | 22 backtests, same span | same | **3m53.802s** |
| run_048 | 95 × 2 = 190 backtests, 2018-02 → 2025-12, 1h | local cache + intermittent live CCXT gap-fills, 2018-2020 | **47m34s** (measured from `start_epoch`/`end_epoch` timestamps around the same invocation) |
| run_053 | 96 × 2 = 192 backtests, 2018-01 → 2025-12, 1h | local cache + intermittent live CCXT gap-fills, 2018-2020 | **52m00s** (same timestamp method) |

**Median ≈ 3m45s, range 3m39s–3m53s, for a clean 22-backtest (11-window × 2-symbol) 1h
protocol served entirely from local cache.** That is ≈ 10 seconds of engine wall-clock per
window-symbol backtest — consistent across all three runs despite three unrelated signal
families (EMA spread, funding-sign, funding mean-reversion), which suggests the ~10s/window
figure is dominated by the engine's own per-backtest overhead (data load + indicator warmup
+ simulation loop), not by signal complexity.

**This number does not generalize to every protocol.** run_048's completed 190-backtest run
took 47m34s (≈15s/backtest) and run_053's completed 192-backtest run took 52m00s
(≈16.25s/backtest) — both roughly **1.5-1.6× the clean per-backtest rate**, but **~12-14×
the clean *total* wall-clock** because each protocol has ~8.6-8.7× as many backtests as
the clean 22-backtest case. The other two protocols in this class (run_050, run_060) never
finished at all: both raised `RuntimeError: No historical data for BTCUSDT ...` at
`trading-bot/core/launcher.py:743` after a live CCXT fetch for a specific pre-2020 month
returned nothing. All four slow/failed cases trace to the same cause: live CCXT network
fetches triggered for the pre-2020 portion of the data, which is somewhat slower when it
succeeds (run_048, run_053) and fatal when the exchange has a genuine gap (run_050,
run_060) — a measured **50% outright-failure rate (2 of 4) for this protocol class**.
**So "a backtest costs ~4 minutes" is only reliably true for windows the local cache
already serves cleanly** (recent data, matching the campaign's own `walk_forward_extension`
range); a protocol that reaches into the `backward_extension` era (2018-2023, used by
several of these very hypotheses for extra sample size) reliably costs 12-14× more even in
its best observed case, and has a real, now twice-demonstrated chance of failing outright,
for reasons unrelated to the strategy being tested. This is exactly the "wall clock becomes
the binding constraint" risk `EPIC.md` names, and now has a measured shape: **it is not a
flat per-run cost, it is a data-locality-dependent one, and for the backward-extension era
it is also unreliable (50% failure in this sample), not just slower.**

Compare against the epic's own LLM-cost baseline (median 8 minutes of *model* time,
$0.36 median cost per run, `EPIC.md` lines 25-26): a clean local-cache backtest (≈3.75 min)
is now measured to be **cheaper in wall-clock than the median LLM interpretation time**, in
the case the epic already expected. The long-lookback case is the one that can flip that
relationship, and does so via infrastructure, not via the backtest itself being
intrinsically expensive.

---

## Deliverable 3 — Where does pre-registration live today?

**Short answer: it already lives outside `validation_gate`, for the piece that matters
most (`pass_rule`) — but the A6.1 holdout-range declaration is still written by the
`validation` stage's LLM skill, not at registration time.** These are two different
"pre-registration" duties conflated in `EPIC.md`'s phrasing, and they currently live in two
different places.

### `pass_rule` (the C7 evaluator's binding criterion)

**Already a field materialized before any pipeline stage runs — not written by
`validation_gate` at all.**

- `pre_registration.yaml` is written by **`workflow/run_campaign.py::_materialize_run()`**,
  specifically the `orch.save_yaml(artifacts / "pre_registration.yaml", pre_registration)`
  call at **`run_campaign.py:343`**, sourced directly from the campaign-queue brief's own
  `brief["evaluation"]["pass_rule"]` field (line 312) — i.e. from the human/LLM-authored
  idea itself, before `hypothesis_generation` even starts.
- The refinement/reactivation path has its own writer, **`_materialize_refinement_run()`**,
  which does the equivalent copy-through at **`run_campaign.py:501`**, again from
  `brief["evaluation"]["pass_rule"]` (line 457), for an operator-authored refinement brief.
- `validation` (the `validation_gate` stage) never writes this file. It only **reads** it —
  `pre_registration.yaml` is one of the two B7 "mandatory input" paths
  (`run_phase1_research.py:1317`) unioned into `validation`'s own required inputs
  (`_apply_b7_mandatory_inputs`, `run_phase1_research.py:1334-1351`) specifically so that a
  pre-registered `pass_rule` "outranks any stage-generated card on any conflict" — i.e. the
  validation stage is deliberately barred from overriding it, not the author of it.
- This is confirmed directly in `docs/USER_GUIDE.md`'s own artifact reference: **"Created
  by: `workflow/run_campaign.py` `_materialize_run()` (alongside `research_brief.yaml`)"**,
  **"Updated by: (none — write-once...)"** (`docs/USER_GUIDE.md:1927-1928`).

So for `pass_rule` specifically, **Jérémy's Decision #1 ("success criteria are written
together with the idea, not in a separate step... no separate stage survives for it") is
already true today, mechanically**, and has been since before this epic — `validation_gate`
was never the writer.

### The A6.1 holdout-range declaration

**Currently NOT in `pre_registration.yaml`. It is written into `validation_protocol.yaml`
by the `quant-validation` skill, at the `validation` stage, as-needed by an LLM prompt.**

- `workflow_artifacts/skills/quant-validation/SKILL.md:54-71` ("IMPROVEMENT 06 — Holdout
  Range Declaration") instructs the LLM: *"Before finalizing `validation_protocol.yaml`,
  read `../../config/campaign_data_policy.yaml` and record the campaign holdout range in
  `sample_split_design`"*, with a hard rule that `validation_protocol.yaml.sample_split_design`
  must contain `holdout_range` or the deliverable check fails.
- Every one of the 7 runs' `validation_protocol.yaml` confirms this in practice —
  `sample_split_design.holdout_range` is present and reads `[2026-01-01, 2026-06-30]` (or
  equivalent prose) in all 7, verified directly while checking feasibility for Deliverable
  1.
- This is a **purely mechanical fact** — the holdout dates come straight from
  `config/campaign_data_policy.yaml` and require no LLM judgment — but it is currently
  produced by an LLM-driven stage rather than at materialization time alongside
  `pass_rule`.

### What's left in `validation`/`determine_post_validation_route` once A8.6 is removed

A8.6 lives at exactly two call sites, neither of which is the LLM skill itself — both are
orchestrator routing code that runs *after* the `validation` LLM stage produces its
`validation_decision.yaml`:

- `determine_post_validation_route()`, `run_phase1_research.py:2341-2360` — blocks
  `approve`/`conditional_approve` before `backtest_specification` if
  `_run_a86_power_check()` says `insufficient_power_a_priori`.
- The `signal_prescreen` pre-flight branch, `run_phase1_research.py:6284-6300` — a second,
  earlier a-priori check with the same verdict function.

Removing both (S2's job, not this one) leaves `determine_post_validation_route()` doing
only status-based routing (`approve`/`conditional_approve` → `backtest_specification`,
`refine` → `refinement_planner` with a refinement-counter cap, `reject` → terminate), and
leaves the `quant-validation` **skill itself** doing everything A8.6 never touched: the
devil's-advocate pressure test (falsifiable statement, null expectation, ≥5 failure modes,
bias risks, the Improvement-09 cost-feasibility Layer-1 check) **plus** the A6.1
holdout-range write described above. That pressure-test role is exactly what `EPIC.md`
already says overlaps `refinement_planner`.

### Answer to the design question

**No separate stage needs to survive for pre-registration.** One of its two components
(`pass_rule`) already lives outside `validation_gate` today, at brief-materialization time.
The other (A6.1's holdout-range) is the one piece still tied to the `validation` stage, and
it is a mechanical copy from `campaign_data_policy.yaml` with no judgment content — nothing
stops it from moving into `_materialize_run()`/`_materialize_refinement_run()` alongside
`pass_rule`, written by `run_campaign.py` itself rather than prompted from an LLM. Once that
one field moves, `validation_gate` retains zero scientific-integrity duties, and merging it
into `refinement_planner` (S4) removes no safeguard — the two duties EPIC.md worried about
losing (pre-registered pass_rule, pre-registered holdout split) are both satisfiable
without any stage surviving in `validation_gate`'s current form.

**This is a recommendation, not a decision** — the call on whether/when to move the A6.1
write is Jérémy's, per the dispatch.

---

## Open questions for Jérémy

1. **Where should the A6.1 holdout-range write live once `validation_gate` merges away?**
   My finding: it's a mechanical field (no LLM judgment required) that could move into
   `run_campaign.py::_materialize_run()`/`_materialize_refinement_run()` alongside
   `pass_rule`, completing the same migration `pass_rule` already made. My recommendation
   is to make that move as part of S4 (stage consolidation) so `validation_gate` disappears
   with zero net loss of pre-registration integrity — but this is your call, not mine.
2. **How should S2/S3 treat the long-lookback data-availability gap found in Deliverable
   1?** Four of the seven runs I re-ran (`run_048`, `run_050`, `run_053`, `run_060`) all use
   protocols whose windows reach back before ~2020 and all made live CCXT calls to fill
   gaps in that range. `run_048` and `run_053` both completed, but at 12-14× the clean
   wall-clock (47m34s and 52m00s vs. ~3.75 min); `run_050` and `run_060` hit a real
   historical gap and crashed outright with `RuntimeError` at
   `trading-bot/core/launcher.py:743`, never reaching a verdict. That's a measured **50%
   outright-failure rate (2 of 4) for this protocol class**, on top of the surviving half
   costing an order of magnitude more wall-clock. This is separate from A8.6/the prescreen
   and outside this dispatch's scope to fix, but "always backtest" (the epic's proposed
   shape, item 1) assumes every hypothesis *can* be cheaply and reliably backtested — for
   anything using the campaign's `backward_extension` range, that assumption is currently
   false often enough to matter. Worth a decision on whether this blocks S2/S3 or is
   tracked as a separate ticket.
