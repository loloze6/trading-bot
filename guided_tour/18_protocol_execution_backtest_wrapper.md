# Stop 18: Protocol execution, part 1: the backtest wrapper

## Speech (verbatim)

**Stop 18 of 29: Protocol execution, the backtest wrapper.** Open on the side: `run_phase1_research.py`, `tools/run_protocol.py`, `tools/venue_resolver.py`, `tools/cost_helpers.py`, `config/cost_model.yaml`, `protocols/run_102_generated.json`, run_102's `variants/base/` and `artifacts/protocol_result.yaml`.

**In one sentence.**
Protocol execution runs the real backtests: for each validated variant it calls the research backtest tool, which replays every test window in the trading engine and gathers the results into one summary, and the orchestrator records each variant as a trial (one counted attempt).

**Why it exists.**
The engine (stops 12-14) backtests one coin on one window. A run needs every variant on every window of its fold (a fixed set of test months), with the right venue and costs, gathered in one place.
Every backtest is also counted, because the more strategies are tried, the more one of them wins by luck. The count feeds the luck correction applied to profit later (stop 20).

**What comes in, what goes out.**
- In: per variant, its config and protocol (from step 5a, stop 16: coin, bar size, windows, venue).
- Out: per variant, its results folders (one per window, the 7 files of stop 14), a protocol summary, a config snapshot, trade diagnostics, and `protocol_result.yaml`; one trial row per variant in the campaign's trial ledger; the run-level `protocol_result.yaml` (a copy of the base variant's).
- Next: the three judges: the pass/fail grid (stop 19), the profit bars (stop 20), the analyst (stop 21).

**What happens here, step by step.**
1. Leftover outputs of an earlier attempt are cleared.
2. For each validated variant, separately: the orchestrator starts the research backtest tool in a separate process with the variant's config and its own protocol.
3. The tool refuses before touching any data if a window touches the holdout (the sealed final period), overlaps the validation period, or shares a day with another window.
4. It resolves the venue and the costs: for a Kraken perpetual-futures brief, prices come from Kraken spot as a stand-in, funding is not charged, and the fee comes from the engine's cost table (5 basis points per side). It prints that on every run.
5. It runs the engine on each window (with extra warm-up bars before it), then writes per-window results, a per-coin summary, trade diagnostics (edge and cost per trade) and a summary.
6. A refusal marks the variant "not tested" with no data touched and no trial counted; a crash marks it failed; the other variants go on.
7. Each graded variant's summary is saved, and one trial row is written: its id (run and variant), its Sharpe ratio (return per unit of risk), trade count, the whole-test figures, the windows' fingerprint and the bar size.
8. A conformance check then compares what ran with what was pre-registered (coins, windows, settings); a mismatch invalidates the trial and pauses the run.
9. The grid's evaluation is computed right after, in the same step (stop 19).

Example: run_102 ran 4 variants on 6 windows of fold B (six 4-month blocks across 2018-2021), 24 backtests. Its protocol says Kraken futures, prices from Kraken spot as a proxy, funding not modelled, funding feed dropped.

**What it costs and how long it takes.**
No AI call. Backtest time is not recorded in the run's audit log.
run_102: 24 window backtests, 4 trial rows (`runs/run_102/variants/*/results/`).

**What is switched off or not used here.**
- The old verdict (promote, kill, refine) is not computed: the summary says so.
- The research cost table `config/cost_model.yaml` is used only for diagnostics when the protocol carries a venue block; the engine's fee comes from `trading-bot/config/cost_model.json`.
- The old pass-rule evaluation file is not binding under the grid.
- The panel backtester (`tools/panel_backtester.py`) is not in this chain.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Tool branch | `run_phase1_research.py:1823-2514` | Entry clears (`:1823-1844`) |
| Per variant | `run_phase1_research.py:2135-2329` | Subprocess (`:2219-2231`), refusal / failure (`:2232-2265`), `protocol_result.yaml` (`:2285`), trial (`:2301`, `_record_backtest_trial` `:12221`), run-level copy (`:2325`) |
| After the loop | `run_phase1_research.py:2331-2514` | Index save (`:2336-2347`), bridge file (`:2382-2393`), pass-rule file (`:2412-2426`), grid (`:2439-2499`) |
| Conformance | `run_phase1_research.py:20453-20520`; `:11107`, `:11263`; invalidate `:11511` | What ran vs what was registered |
| Trial ledger | `run_phase1_research.py:12221-12376` | `campaign_state.yaml` trial rows |
| Backtest tool | `tools/run_protocol.py:2346-2425` (`main`), preflights `:2454-2489`, venue and cost `:2497-2579`, holdout mode `:2586-2642`, windows loop `:2674-2747`, diagnostics `:2750-2768`, summary `:2774-2853`; readers `:173-182`, `:538`, `:621`; refusals `:2014-2178` | One variant, all windows |
| Venue | `tools/venue_resolver.py:117-137` | Spot price proxy, funding dropped |
| Cost helpers | `tools/cost_helpers.py:92-113` | Diagnostics costs |
| Research cost table | `config/cost_model.yaml` | Diagnostics only with a venue block |
| Examples | `protocols/run_102_generated.json`; `runs/run_102/variants/base/{config.snapshot.json,protocol_summary.json,trade_diagnostics.json}`; `artifacts/protocol_result.yaml`; `artifacts/variants/base/protocol_result.yaml` | Fold B, venue block, summaries |
| Schema | `workflow_artifacts/schemas/protocol_result.schema.json` | Checked at write |

Remarks: send them as "stop 18: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

## Inspector notes

### (1) Design and mechanism

1.1 The wrapper is sound where it matters. One subprocess per variant (`RP:2219-2230`), each window through the same `run_backtest` the engine exposes with `warmup_prefetch=True`, `holdout_start` guard and the per-window `commission_rate` (`run_protocol.py:2682-2688`); the config is hashed and snapshotted before any window runs so what ran is what was stamped (`:2497-2498`, `:2576-2579`). The refusal/failure ladder is complete: every `continue` branch either records a `backtest_failed` row or is a pre-data refusal with none (`RP:2147-2318`), and an earlier attempt's failure is carried (`RP:2331-2335`). The trial row is replaced in place on a re-run with the old attempt kept (`_record_backtest_trial RP:12364-12370`). Good for the goal: the luck-correction count cannot silently lose a look.

1.2 Three cost figures in one record, two of them wrong for the venue. run_102 base, every window: `post_backtest_cost_check.cost_bps_per_trade: 18.5` (the Binance-spot `default` round trip from `config/cost_model.yaml:114`, computed inside the engine's artifact writer), `real_round_trip_cost_bps: 10.0` (2 x 5 bps from `cost_model.json` via the venue block), and per trade `cost_paid: 10.0` plus `cost_paid_all: 15.0` (`trade_diagnostics.json:22,33`). The 18.5 figure yields `pass: false` on all six windows and `edge_to_cost_ratio 0.12-0.67` beside the "real" `pass: true` on four. Both blocks are information only under the grid, but they are what the analyst reads (stop 21). `_load_cost_model :2581` always loads the yaml; with a venue block it is bypassed for the fee (`resolve_fee_bps`, `cost_helpers.py:87-89`) but not for the engine-side check.

1.3 Readiness of the per-window "Sharpe": `core.sharpe` is the trade-exit Sharpe with `sqrt(365)` annualisation (`protocol_result.yaml:67`), nulled below 5 trades (`_SPARSE_TRADE_FLOOR :55`, `:2694-2696`); the trial row carries the median of those (`RP:12305-12308`, run_102 `-0.5675`) while `whole_test.sr_daily` on the same row is `-0.0176` (`campaign_state.yaml:2373,2389`). The DSR N and the ranking read the first; the profit bars read the second. Two Sharpes for one trial in one row, neither labelled by basis on the row itself. Carries stop 14 note on three Sharpe definitions.

1.4 Exit-reason diagnostics are a default label. `_classify_exit_reason :530-535` returns `"signal_flip"` for every exit that is not end-of-window; run_102 shows `signal_flip_pct 97.94` with `inferred_classification_pct 97.94` (`protocol_result.yaml:521-525`). A sized reduction (stop 13: the band fires on sizing changes too) and a real forecast flip are indistinguishable in the diagnostic, so `fee_reduction_metrics.trade_less_often` has no way to say which trades to remove.

1.5 `pnl_concentration` divides by total net pnl: `pct_pnl_from_top_decile_trades: -684.26` / `worst_decile 614.63` (`:518-519`) when the book is near flat. No guard for a near-zero denominator; the number is noise shaped like a finding.

1.6 Trade records: the first two trades of the first window both enter at bar index 0 with different exits (`trade_diagnostics.json:4-11, 36-43`): the lot-split accounting of stop 14. `holding_period_distribution p50 27 bars` and `n 2374` therefore count lots, not positions; `per_trade_expectancy_bps` is per lot. Not checked how the grid's trade minimum treats this.

1.7 Conformance (`RP:20453-20520`, `_check_protocol_execution_conformance :11107-11260`, `_per_coin_conformance :11263-11303`) compares `protocol_file`, symbols, range, content hash and `episode_blocked_significance_by_symbol` against `pre_registration.machine_constraints`. Sound and per-variant. Not checked: which of those keys run_102's pre-registration actually carries; a constraint block without `significance_methodology` skips that half silently (`:11131-11132`).

1.8 Failed-row accounting contradicts itself in the docstring: `_record_failed_backtest_trial` says a failed row "is EXCLUDED from today's DSR N" (`RP:12411-12414`) and then that recording it "OVER-counts N" as the conservative choice (`RP:12426-12430`). The code excludes (`statistic_valid: failed`); the rationale for the over-count is stale.

1.9 Re-runs accumulate window folders: `_runs_root = out_dir/"results"` (`:2653`) and each `run_backtest` creates a new timestamped dir; nothing in `run_protocol.py` clears `results/`, and the orchestrator's clears (`RP:1823-1844`) touch artifacts only. `protocol_summary.json` is overwritten, the folders are not (`_window_results` is used to detect "no new window", `RP:1800-1810`). Not checked: whether `run_backtest`/`new_run_dir` prunes.

1.10 Verdict on the goal: the wrapper is reliable and well-accounted; its weaknesses are in what it writes, not how it runs. Cost (1.2), Sharpe (1.3) and exit reasons (1.4) each carry two or three bases in one record, and the retired route labels (`post_backtest_route: kill_no_ic` on every window, `hypothesis_verdict.diagnostics.post_backtest_route_real`) are still computed and written. A reader that trusts the record must know which field is live; nothing in the record says so.

### (2) Legacy or simplifiable

2.1 Dead budget: `prior_runs = 0` / "Budget used 0/20" (`:2647-2651`) never reads anything; the WARNING branch is unreachable in effect.

2.2 Prescreen residue: `prescreen_backtest_cross_check` (`:2805-2807`, always `null` since E-039 removed the stage), `_build_extended_summary`/`extended_for_cross_check` kept only to produce `episode_blocked_significance_by_symbol` for the conformance check (`:2839-2848`). The legacy verdict path (`promotion` block refusal `:2478-2488`, `legacy_top_level_verdict :2799`, `--validation-protocol`/`evaluate_against_decision_rules :2810-2815`, `hypothesis_verdict` shape) is retired on the live path via two flags and three CLI switches (`--legacy-verdict-retired`, `--diagnostics-only`); the record still carries `verdict`, `verdict_reason`, `hypothesis_verdict.verdict/criteria_results` as nulls and explanatory prose (`protocol_result.yaml:467-475`). The schema still enumerates `promote|refine|kill` (`protocol_result.schema.json:11,76`).

2.3 Orchestrator side: `pass_rule_evaluation.yaml` block (`RP:2412-2437`) is skipped under `legacy_label_retired`; the flag-off single-config branch (`RP:2522+`) and `determine_post_spec_route` are reachable only with `variant_loop` off. `post_backtest_route*` fields (engine side) and `cost_dominated_real`, `post_backtest_route_real_tied` are the retired verdict-interpreter's inputs (`schema:106-116` cite verdict_interpreter), computed on every run.

2.4 Holdout mode (`:2586-2642`) shares `main()` with the walk-forward loop; it is never reached from the live loop (`verdict_routing_retired` makes `holdout_evaluation` unreachable, `SR/CLAUDE.md:67-73`). A separate entry point would shorten `main()` (500 lines) and remove `--holdout/--i-understand/--hypothesis-id` from the research tool's surface.

2.5 `dds` at `:2778-2781` builds a one-key dict inside a comprehension to read it back; it is `abs(r["core"].get("max_drawdown_pct") or 0)`.

2.6 `config/cost_model.yaml` (280 lines): the `execution_style` block is "NOT yet read by any code path" by its own words (`:193`), the `perp.funding` block is "off by default; no re-cost run" (`:177-178`), the retired-gate formulas at `:259-279` are documentation. What is live: `fee_rate_bps`/`round_trip_cost_bps` (engine-side check, 1.2) and `perp.fee_rate_bps` under `--cost-product perp` (not passed by the orchestrator: `RP:2219-2227` passes no `--cost-product`; the venue block sets `commission_bps` instead). So on the live path the yaml's only effect is the stale 18.5 figure.

2.7 Not checked: `tools/panel_backtester.py` (speech says not in chain; grep not done), `_cross_check_prescreen_vs_backtest`'s body, and whether `tests/` pin the legacy verdict path.

### (3) Disagreements between speech and element

3.1 "The research cost table `config/cost_model.yaml` is used only for diagnostics when the protocol carries a venue block; the engine's fee comes from `cost_model.json`." Reversed on the first half: with a venue block the yaml is bypassed for the trade diagnostics (`cost_paid 10.0` from `commission_bps`), but the engine's own artifact writer still prices `post_backtest_cost_check` from it at 18.5 bps on every window (1.2). Without a venue block the yaml sets the engine fee too (`_resolve_commission_rate` -> `commission_rate_for_symbol`).

3.2 "A refusal marks the variant 'not tested' with no data touched and no trial counted" (step 6). True, with the detail that the refusal is recognised only when all three hold: exit code, the stderr token on the first line, and no new window folder (`RP:1800-1810`). A refusal whose first stderr line is something else (a warning printed first) becomes a `backtest_failed` row.

3.3 "The run-level `protocol_result.yaml` (a copy of the base variant's)". A copy of the first graded variant when base fails (`RP:2379-2393`); readers of the singular file cannot tell which.

3.4 "Backtest time is not recorded in the run's audit log." The record holds it implicitly: `protocol_run_id` and the six window `run_id`s are UTC timestamps (`protocol_result.yaml:1,17,96,168,240,312,391`), about 40 s per window, about 4 min for the base variant.

3.5 "Leftover outputs of an earlier attempt are cleared" (step 1). Artifacts are (`RP:1823-1844`); the per-window `results/` folders are not (1.9).

3.6 "Trade diagnostics (edge and cost per trade)" (step 5). Per lot, not per trade (1.6), and the exit reason is a default (1.4).

3.7 Reading map `:538` is `_cost_paid_bps` and `:621` is `_full_precision_closes`, not "readers"; `:173-182` is right. Example claim "4 trial rows" matches `campaign_state.yaml:2371, 2393` (base and split_stretch_weight seen; the other two not read).

3.8 Example "Its protocol says Kraken futures, prices from Kraken spot as a proxy, funding not modelled, funding feed dropped": confirmed (`protocols/run_102_generated.json:5-18`, `protocol_result.yaml:4-13`), and `cost_components_measured: {fees: true, funding: false, slippage: false}` (`:548-551`) while `cost_paid_all` does include slippage; the summary flag and the per-trade field disagree about whether slippage is measured.
