# Stop 20: Branch 3, the profit bars

## Speech (verbatim)

**Stop 20 of 29: Branch 3, the profit bars.** Open on the side: `config/profitability_bars.yaml`, `run_phase1_research.py`, `tools/portfolio_daily.py`, `tools/portfolio_whole_test.py`, `tools/deflate_sharpe.py`, `tools/structure_key.py`, `tools/window_economics.py`, `docs/DATA_DICTIONARY.md` (§10).

**In one sentence.**
The profit bars are the campaign's one fixed definition of "profitable enough": a short list of thresholds, signed by the operator, that every tested variant is graded against after its backtests, and the only door to the holdout (the sealed final period of market data).

**Why it exists.**
The grid (the pass/fail table of criteria written before the run, stop 19) asks whether the run's own idea held. It does not ask whether the strategy makes money worth trading. One campaign-wide list answers that, the same way for every run, so the bar cannot move to fit a result.
It also prices in luck: the more strategies tried, the more one looks good by chance. The deflated Sharpe ratio (the Sharpe ratio, return per unit of risk, discounted for the number of attempts) corrects for that.
A variant that clears every bar stops the run for the operator. Nothing else leads to the holdout.

**What comes in, what goes out.**
- In: the bars file (thresholds and signature); each variant's backtest results (stop 18): equity bar by bar, trades, the protocol's windows; the campaign's trial ledger (every counted attempt so far).
- Out: `profit_bars_evaluation.yaml`: per variant, each bar's threshold, actual value and result; the list of passing variants.
- Next: campaign memory (stop 22), the analyst's book (stop 21), decide-next for combination runs (stop 24), the run viewer, the route (stop 23).

**What happens here, step by step.**
1. Right after the backtests, the bars file is loaded and checked. A missing or mistyped value stops the step: no threshold is ever guessed.
2. Each variant tested in this attempt is graded. One that failed or was not tested is listed with no rows.
3. Its coins form one portfolio, equal money in each. Each window's daily values are chained end to end into one whole-test curve. Missing days for some coins make a row "not evaluable", never a flattering number.
4. Eight rows are measured under today's values:
   - Sharpe ratio above 0;
   - deflated Sharpe at least 0.5, counted only against the campaign's trials of the same strategy shape (same components and bar size, parameters ignored);
   - Calmar ratio (yearly return over the worst fall) above 0.75;
   - worst fall at most 20%, shown but not deciding;
   - average daily return at least 0.05%;
   - Sharpe above equal-weight buy-and-hold on the same days (buy-and-hold charged one round trip);
   - trades on at least 1% of bars, forced end-of-window closes not counted;
   - Sharpe still above 0 with any one 4-month block left out.
5. A variant covering only part of the test period has its time-dependent limits scaled to its share.
6. A variant passes when every deciding row passes. A deflated Sharpe that cannot be computed is a warning, not a fail.
7. Beside the rows, for information only: the forecast's shape and, with the analyst on, each window's economics (gross, fees, net, turnover).
8. The file is written and the run goes on. Nothing pauses yet.
9. After the record-keeping stage, if any variant passed, the run pauses for the operator. The grid's status is not changed.
10. The operator writes a holdout decision: "continue" (the run ends as the grid says) or "spend" on one passing variant. A spend is refused unless that variant still passes, the bars file is unchanged, the trial ledgers are merged, the hypothesis never used the holdout, and the deflated Sharpe, recomputed on today's ledger, still clears 0.5.

run_102's `profit_bars_evaluation.yaml` is not in this checkout.

**What is switched off or not used here.**
- Two bars are off, so they have no row: the minimum trade count and the edge-to-cost ratio, with their floors.
- The first-version definitions (median per-coin Sharpe, worst-window drawdown) are not reached under the current flags: version 2 returns first at `run_phase1_research.py:15123-15131`.
- The check on the old "promote" route is not reached under the current flags: the grid route ends the run before it, at `run_phase1_research.py:5448-5449`.
- The coin list in the bars file (BTC, ETH) is required non-empty by the loader; my grep found no other reader.
- In this checkout the committed switchboard has the four switches of this stop off (`campaign_config.yaml:349-350`, `:388-389`, `:422-423`, `:1034-1035`); the tour's current flag set, the operator's uncommitted edit, has them on.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Bars file | `config/profitability_bars.yaml:1-328` (header: decisions, readers, v1 and v2 definitions, partial coverage `:316-328`), `:330-348` (values; signature `:338-339`) | The thresholds |
| Loader | `run_phase1_research.py:3572` (`_load_profitability_bars`), `:3558` (`_bar_is_off`), `:3643-3645` | Loud schema check; null bar = off; coin list non-empty |
| Call site | `run_phase1_research.py:20640-20642` | After `protocol_execution`; bars sha recorded under routing retired |
| Evaluation | `run_phase1_research.py:15413-15554` (`_evaluate_profit_bars_every_backtest`) | Writes `artifacts/profit_bars_evaluation.yaml` |
| Candidates | `run_phase1_research.py:13878` (`_profit_bars_backtest_candidates`) | This attempt's variants; NOT_TESTED / INVALIDATED |
| Grading | `run_phase1_research.py:15105-15144`, `:15029-15102` (`_grade_profit_bars_v2`), `:14192-14218` (basis, comparators) | Rows; advisory drawdown (D-188) and DSR (D-119) |
| Row values | `run_phase1_research.py:14801-15002` (`_whole_test_profit_metrics`), `:14383` (`_whole_test_chain`), `:14742` (`_calmar_row`), `:15005` (`_trade_frequency`), `:14222` | Chain, drawdown, Calmar, mean return, Sharpe, leave-one-out, buy-and-hold |
| Window portfolio | `tools/portfolio_daily.py:38` (0.9 coverage floor), `:65`, `:134`, `:164`; `:185` (first version only) | Equal-weight curve per window |
| Whole-test tools | `tools/portfolio_whole_test.py:416` (`chain_windows`), `:761`, `:835`, `:857`, `:882`, `:914`, `:1031`, `:1127`, `:1195` (edge/cost, off) | Pure functions |
| Deflated Sharpe | `run_phase1_research.py:13131` (N, `_promotion_dsr_context`), `:14466-14491` (`_whole_test_dsr_context`), `:14591`; `tools/deflate_sharpe.py:836` (`compute_dsr_whole_test`), `:1055`, `:1132` | N trials, K same-basis Sharpes, benchmark |
| Same structure | `run_phase1_research.py:15461`, `:15490-15498`, `:14517`; `tools/structure_key.py:128` (`compute_structure_hash`), `:282` | DSR counted per (structure, timeframe), D-185 |
| Partial coverage | `run_phase1_research.py:15253-15296`, `:15478-15505` | Scaled limits (D-047) |
| Information only | `run_phase1_research.py:15318-15374` (forecast shape), `:15377-15410` → `tools/window_economics.py:295` | Beside the rows |
| Stop | `run_phase1_research.py:15570-15623` (`_profit_bars_stop_route`), called `:20584-20585` | Pause, flag `profit_bars_reached` |
| Unlock | `run_phase1_research.py:7515-7557` (`_holdout_unlock_route`), `:7414-7488` (checks), `:7106` (file reader), `:7281`, `:7318` (DSR recheck), `:7491` (refusal), `:7679` (resume pre-check) | `holdout_decision.yaml`: spend or continue |
| Not reached | `run_phase1_research.py:14069-14176` (`_portfolio_profit_metrics`), `:15132-15143`, `:13727` (`_evaluate_profit_bars`) | First version; promote route |
| Readers | `tools/campaign_memory.py:474`, `:580`; `tools/analyst_session.py:292`; `tools/decide_next.py:1305-1310`; `tools/run_viewer/loaders.py:672`, `:1229` | Memory, book, combination runs, viewer |
| Dictionary | `docs/DATA_DICTIONARY.md:465-553` (§10) | `window_economics` fields (`:473-478` ties them to this file); the rest is the analyst's tools (stop 21) |
| Switches | `campaign_config.yaml:349`, `:388`, `:422`, `:1034` | Bars file, every backtest, version 2, same structure |

Remarks: send them as "stop 20: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Deflated sharp -- i honestly would challenge the need and complexity it brings knowing that we control we do not test an idea already generated before in the workflow.. plus if not claculated it is already a warning, why would it be blocking when calculated. 

Here the branch should be simple: testing profitability over the tested variants. Step 3 / 5 / 7 (why information if not deciding, what does it add). Step 10 could persist but i do not care about mechanics checking for me: if i want to test on holdout, i would test on holdout.

## Inspector notes

(Checkout note: no `SR/runs/run_102/`, so `profit_bars_evaluation.yaml` and every run_102 figure are not checkable. The committed `campaign_config.yaml` here has `profit_bars_file`, `profit_bars_every_backtest`, `profit_bars_v2` and `dsr_same_structure` off (`:349-350`, `:388-389`, `:422-423`, `:1034-1035`, confirmed); the notes judge the mechanism under the tour's flag set, as the speech does.)

### (1) Design and mechanism

1. This is the best-guarded judge in the pipeline, and it is built to refuse rather than flatter: the loader raises on any missing or mistyped key (`RP:3572-3647`, `ProfitabilityBarsSchemaError :3566`), every row records its `basis` and `comparator` (`_BASIS_V2 :14192`, `_COMPARATOR_V2 :14211`), the whole-test chain is built once for the rows, the ledger and the DSR (`_whole_test_chain :14383-14389`), a thin or mismatched coin set is `NOT_EVALUABLE` never a number (`portfolio_daily.py:38`, `:60-63`), a ruined account is a FAIL never an unknown (`:14902-14921`, D-101), the bars file's sha is stamped at grading and compared byte-for-byte at spend (`:15448-15452`, `:15548`, `_evaluation_under_current_bars :7159`), and a spend recomputes the DSR on today's ledger (`:7485`, `:7318-7335`). For "without fooling ourselves" this element does its job.
2. What "profitable enough" means today, in one line (`profitability_bars.yaml:330-348`): whole-test daily Sharpe > 0, DSR >= 0.5, Calmar > 0.75, mean daily return >= 0.05% (about 18% a year simple), Sharpe above equal-weight buy-and-hold on the same days, trades on >= 1% of bars, and Sharpe > 0 with any one 4-month block removed; drawdown <= 20% advisory. Eight rows, all must pass (`:15093-15094`). Against stop 14's base window (net +1.4%, cost drag 56%, 383 trades) the Calmar and mean-return rows are the binding ones; the file calls `avg_daily_return_min` "the deliberate single magnitude bar" (`:34`). The bar is the operator's; the mechanism applies it the same way to every variant, which is what the speech promises.
3. The DSR's N is "the same shape on the same bar size" (D-185): `_same_structure_view` restricts N and K to rows with the candidate's `(structure_hash, timeframe)` (`:14517-14530`; `structure_key.py:1-40`: class, op names, weight signs, sizing kind, no parameter values), and a keyed candidate that is alone in its key is graded with no selection correction at all (`n1_no_selection`, `deflate_sharpe.py:866-874`, SR0 = 0). With D-149 making every idea a weighted mean of standardised indicators (stop 10 note 1.3, stop 11 note 1.3), most trials share a few keys, which is the intended effect; the cost is the other side: the first trial of a new shape is corrected for nothing, although the campaign chose that shape among the others it tried. The luck correction counts repetition of a shape, not the search across shapes. The campaign-wide N stays in `dsr_basis` for the reader (`:14501-14506`).
4. Branch 3 and branch 1 do not talk to each other, by design, and the holdout door is branch 3's alone. `_profit_bars_stop_route` reads `idea_status.yaml` only to print it (`:15599`, `:15618-15619`); `_validate_holdout_decision` (`:7414-7488`) reads no idea status; `_holdout_unlock_route` sends a `spend` to `holdout_evaluation` whatever the grid said (`:7552-7557`). So a `refuted` idea (its IC criterion failed) whose base variant clears every profit bar pauses the run and can be spent on the holdout by the operator. The speech's "the grid's status is not changed" is true and the converse is the finding: the grid's status does not gate the spend. Consistent with D-021 ("the bars are the only door"); the operator is the only check that the money and the belief point the same way.
5. The stop is the one place in the loop where autonomy ends on purpose: a pass pauses the run (`:15621-15623`) and, with quarantine off (stop 03a note 1.2), the campaign process, until a hand-written `holdout_decision.yaml` is read (`_read_holdout_decision :7106`). The stop is raised once per evaluation (`:15594-15598`), after regroup so memory already holds the result (`:15571-15573`), and is skipped when a component error pauses first (`:20584`). Sound. In 102 runs it has never fired as far as the committed records show (the registry's one active block, stop 22, is the candidate to check).
6. The buy-and-hold row makes the bar era-dependent. Equal-weight buy-and-hold on the same chained days, one round trip charged (`portfolio_whole_test.py:1127-1145`), compared by Sharpe (`:14985-14988`). On a fold whose years are one long rise, buy-and-hold's Sharpe is a high bar; on a falling fold, a trivial one. With folds A and D contiguous years (stop 06 note 1.3), the same strategy passes or fails this row by which fold decide-next drew. The row is a sound question ("does the strategy beat holding?"); its answer is not comparable across folds, and nothing in the evaluation says which regime the fold was.
7. The partial-coverage rules are heuristics stated as such: drawdown limit times sqrt(f), Calmar over sqrt(f), trade floors times f (`_normalised_profit_bars :15253-15296`, file `:316-328`), each recorded in `detail.normalisation` (`:15299-15309`). An asset variant on a late-listed coin is therefore graded on a square-root guess; honest because written down, and only for asset variants.
8. What is graded is read from files at grading time: per variant the chain reads every window's `portfolio_states.csv`, the trade counts `trade_diagnostics.json`, the buy-and-hold `bars.csv` closes, the forecast shape every `bars.csv`, the window economics `bars.csv` + `trades.json` + `metrics.json` (`:14834`, `:14899`, `:14976-14981`, `:15318-15374`, `:15377-15410`). Four variants times six windows, three to five passes over each: unrecorded compute, as every tool step (stop 05a note 1.4).
9. Readers of the result beyond the stop: memory (`campaign_memory.py:474` `profit_bars_block`, `:580` `base_book_block`: the base variant's five figures become the `base_*` book 1a sees in `tried_ideas`, stop 07 note 1.4), the analyst's book (`analyst_session.py:292-297`), decide-next only for a composition run's `NOT_EVALUABLE` rows (`decide_next.py:1305-1310`), the viewer. So on the live loop the bars inform the next choice through five numbers of the base variant in memory; the per-row verdicts of the other variants reach no decision.
10. `trade_frequency_min` was set "AFTER seeing lane 1's trade frequencies" (`profitability_bars.yaml:18-19`), and the file says so; the DSR threshold was moved from 0.95 to 0.5 (`:33-34`, D-118). Bars chosen after seeing results are the operator's prerogative and are signed; recorded here because the sha stamp protects against a silent move, not against a signed one, and nothing records how many trials were graded under each signature.

### (2) Legacy or simplifiable (leads)

1. The v1 path: `_grade_profit_bars` (`:13613`), `_evaluate_profit_bars` (`:13727`, the promote route), `_portfolio_profit_metrics` (`:14069-14176`), `_cap_partial_coverage_bars` (`:15168`), the `dsr_candidate` closure and `DSR_THRESHOLD = 0.95` inside `_promotion_dsr_context` (`:13131-13160`; under v2 only its `n_dsr_total`/`campaign` are read, `:15454`), `_dsr_on_current_ledger`'s v1 branch (`:7281-7316`), `portfolio_daily.py:185` and the file header's v1 definitions (`:80-174`, 95 lines) and "Read by" section (`:55-78`, which still describes the promote path and the legacy holdout gate's 0.95). Unreached with v2 on.
2. Off bars kept as keys and code: `trade_count_min`, `cost_edge_ratio_min`, `cost_edge_min_trades`, `trade_count_min_floor` (all null, `:333`, `:342-345`), their rows (`:14843-14853`, `:14871-14894`), `pooled_edge_to_cost_ratio` (`portfolio_whole_test.py:1195`), `normalised_trade_minimum`, the `cost_bar_all_costs` keyword inside the off cost row (`:14879-14881`; the flag's grid half is stop 19's), `_PROFIT_BARS_OFFABLE` (`:3541`) as a second off-list beside `_PROFIT_BARS_OPTIONAL_V2` (`:3545`). D-118 turned them off; the file carries four nulls and the loader checks their pairing (`:3647`).
3. `target_instrument_set` (`:335-337`, BTCUSDT and ETHUSDT): "consumed by neither" (`:166-171`), required non-empty (`:3643-3645`), naming a Binance-era pair set for a Kraken campaign. Delete the key and the check.
4. Three flags for one feature (`profit_bars_file`, `profit_bars_every_backtest`, `profit_bars_v2`; stop 03a lead 2.5) plus `dsr_same_structure`: the v2 keyword plumbing (`v2_kw`, `_grid_v2_kw`, `**({...} if v2 else {})` at `:15447`, `:15489`, `:15528`, `:15533-15537`) exists to keep the flag-off call byte-identical. With one path, `_evaluate_profit_bars_every_backtest` loses a third of its branches.
5. The two overlays, `campaign_record/trial_sharpe_basis_recompute.yaml` (`_load_trial_sharpe_basis_overlay :14443`) and `trial_structure_key_overlay.yaml` (`:14481-14483`, `structure_key.py:282`): backfills for ledger rows written before each flag. Once every counted row carries native fields, both files and their precedence rules go (stop 25).
6. `_variant_forecast_shape` (`:15318-15374`, D-150) duplicates the analyst's `describe` cells (`abs_mean`, `share_at_cap`; its own docstring says so, `:15326-15327`) for a reader that already has the query tool; `window_economics` beside it is computed once more by the analyst's query (`DATA_DICTIONARY.md:473-478`). Two copies of each figure per run.
7. The file is 348 lines for 19 values, with the decision history inline (D-118, D-119, D-120, D-127, D-129, D-188 at `:1-48`); the same pattern as the switchboard (stop 03a note 1.5).

### (3) Disagreements between the speech and the element

1. Step 10, "A spend is refused unless ...": correct for the five listed; also refused when the variant's trial is now invalidated (`:7289-7291`), when another spend is unfinished (`:7480-7484`), when the evaluation's Sharpe basis is not the current one (`:7331-7335`), and when the decision file names another run or stop (`:7420-7432`). Omission.
2. Step 9, "if any variant passed, the run pauses for the operator": only when no component-error pause came first (`:20584`) and only once per evaluation (`:15594-15598`). Detail.
3. Step 4, "deflated Sharpe at least 0.5, counted only against the campaign's trials of the same strategy shape": correct; not stated that a shape with one trial gets no correction (SR0 = 0, `deflate_sharpe.py:866-874`; note 1.3), nor that a shape-less (unkeyed) row keeps the campaign-wide N (`:14600-14603`).
4. "In: ... the campaign's trial ledger": the ledger is read twice, through `_promotion_dsr_context` and `_whole_test_dsr_context`, and the two dedup counts must agree or grading raises (`:14485-14488`). Fine; a fact.
5. "Out: `profit_bars_evaluation.yaml`" only: the stop also writes `profit_bars_reached` and `profit_bars_stop_evaluation` into `pipeline_state.yaml` (`:15621-15622`), and the unlock writes the decision record and refusal keys there (`:7497-7502`, `:7543-7545`). Omission.
6. Section 6, "The check on the old promote route is not reached ... `:5448-5449`": correct (`routing_retired` returns before the inconclusive branch). "my grep found no other reader" of the coin list: confirmed (`target_instrument_set` in `RP` is the loader only; not grepped in `tools/`).
7. Section 6, the committed switches off in this checkout: confirmed (`:350`, `:389`, `:423`, `:1035` all `enabled: false`), and so is every other flag of the tour's set but `exclusion_digest_input`, `stale_input_path_fix`, `variant_selection_record`, `schedulability_block`, `data_availability_gate` and `config_replay_gate` (6 of 34 on; `git status` clean on `config/`). The guide's note "the same code the earlier stops read" holds for the code, not for the config: stop 03a's counts (30 on, 4 off) describe the operator's uncommitted working tree.
8. Reading map: `_bar_is_off :3558`, `_load_profitability_bars :3572`, `:3643-3645`, `:13878`, `:15029-15102`, `:15105-15144`, `:14192-14218` (the two constants run to `:14220`), `:14801-15002`, `:14383`, `:14742`, `:15005`, `:14466-14491`, `:14591`, `:14517`, `:15253-15296`, `:15318-15374`, `:15377-15410`, `:15413-15554`, `:15570-15623`, `:7414-7488`, `:7491`, `:7515-7557`, `:7106`, `:7281`, `:7318`, `:7679`, `:20584-20585`, `:20640-20642`, `:14069`, `:13727`; `portfolio_daily.py:38`, `:65`, `:134`, `:164`, `:185`; `portfolio_whole_test.py:416`, `:761`, `:835`, `:857`, `:882`, `:914`, `:1031`, `:1127`, `:1195`; `deflate_sharpe.py:836`, `:1055`, `:1132`; `structure_key.py:128`, `:282`; `window_economics.py:295`; `campaign_memory.py:474`, `:580`; `analyst_session.py:292`; `decide_next.py:1305-1310`; `DATA_DICTIONARY.md:465-553`: verified. `run_viewer/loaders.py:672`, `:1229` and `:15461`, `:15490-15498` not opened beyond the grading loop.
