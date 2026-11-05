# Test hygiene facts (2026-11-05)

Sources: `rerun_20261105_002932.log` (full fast-suite log of the final night-work commit, `run_tests.py -- -q -rs`, `CI=true`, Python 3.13), `check_final_run.out` (same run), `run_tests.log` (baseline), and a fresh clone of HEAD 704f720 (`file://` clone, scratchpad `hyg/`) used for `--collect-only -m slow` only. No test was run in the repo. All paths below are relative to the repo root.

## Totals (final run)

| Suite | passed | skipped | deselected (slow) | warnings | time |
|---|---|---|---|---|---|
| trading-bot/tests | 1432 | 16 | 74 | 2170 | 96.6 s |
| strategy-research/tests + tools/recorder/tests | 7733 | 33 | 35 | 8374 | 850.2 s |
| total | 9165 | 49 | 109 | 10544 | |

Baseline `run_tests.log` had 1 failed / 32 skipped in SR. That failure was `test_installed_hook_matches_tracked` run without `CI=true` (the test fails when `.git/hooks/pre-commit` is absent; with `CI=true` it skips, see 1.6). Skip reasons are identical between baseline and final apart from the three clone-path strings in the Kraken/Binance cache messages.

Static count of test functions (AST, `def test*`): 6469 across the three test directories. Skip sites in code (grep): `skipif(` 28 TB / 15 SR / 6 recorder; `pytest.skip(` 7 TB / 18 SR / 0 recorder; `pytest.importorskip` 25 SR / 1 recorder; `requires_cache(` 10 SR.

## 1. Skipped tests (49) with reasons

The `-rs` line numbers are the skip location reported by pytest (the test's decorator/def line for `skipif`, the `pytest.skip(` line for runtime skips).

### 1.1 Base commit not reachable via `git show` (9 tests) - history-dependent

| Test | Skip site | Commit probed |
|---|---|---|
| `trading-bot/tests/test_e060_block_standardisation.py::test_engine_without_block_keys_matches_pre_s3a_engine_bar_for_bar` | `_old_engine_class()` skip at :119; commit pinned at :35 | `44421b31` |
| `trading-bot/tests/test_standardise_op.py::test_every_other_op_and_min_periods_entry_is_unchanged`, `::test_component_effective_lookback_unchanged_without_standardise` (registry.py) and `::test_engine_without_standardise_matches_master_bar_for_bar`, `::test_shipped_strategy_config_required_periods_and_lookback_unchanged` (strategy_engine.py) | `_old_module()` skip at :393; commit pinned at :384 | `e981f578` |
| `trading-bot/tests/test_vol_target_transform.py::test_every_other_op_is_unchanged` (registry.py) and `::test_engine_without_vol_target_matches_master_bar_for_bar`, `::test_shipped_strategy_config_required_bars_unchanged` (strategy_engine.py) | `_old_module()` skip at :265; commit pinned at :35 | `6e0afb35` |
| `strategy-research/tests/test_e068_claim_tests.py::test_reevaluate_cli_reads_the_committed_cells_and_hashes_git_bytes` | skip at :988 ("history not available (shallow clone)") | `bc4e67f4` |

- Mapping of the 4 + 3 test names to the "[2]/[2]/[1]/[2]" counts in the log is by the `_old_module(...)` calls at `test_standardise_op.py:400,437,458,470` and `test_vol_target_transform.py:272,312,332`.
- In this clone of HEAD (`git rev-parse --is-shallow-repository` = true, 198 commits) all four commits ARE present in `/home/user/trading-bot` (`git cat-file -t` returns `commit`), so these tests would run in the working repo. They skipped in the fresh `file://` clone used for the log, whose object store did not contain them.
- GitHub CI: `.github/workflows/tests.yml` uses `actions/checkout@v4` with no `fetch-depth`, i.e. a depth-1 checkout. A depth-1 checkout has no `44421b31`/`e981f578`/`6e0afb35`/`bc4e67f4`, so on both ubuntu-latest and windows-latest all 9 skip every time. (Inference from checkout's default depth; I did not look at a CI run.)

### 1.2 Run artifacts absent (`strategy-research/runs/` is gitignored) - 20 tests

`.gitignore:130` ignores `/strategy-research/runs/`, but `git ls-files strategy-research/runs` tracks 60 run directories (`run_0001`, `run_002` ... `run_060`). `run_081`, `run_082`, `run_083`, `run_084`, `run_088`, `run_089`, `run_091`, `run_097` have 0 tracked files. So none of these can run from a checkout; they run on the operator PC or with `D113_RUNS_ROOT` / `CUL431_RUN_DIR` / `WINDOW_ECONOMICS_RUN_COPY` set.

| Tests | Skip site | Needs |
|---|---|---|
| `test_c7ext_verdict_gates.py::test_g6_live_kb_has_no_ungated_verdict_fields`, `::test_d4_bypass_c_the_live_record_passes_the_standalone_lint` (2) | `pytest.skip(RUNS_ABSENT_REASON)` at :385 and :641; reason constant :353 ("runs/ is a runtime record, not in git (#457)") | the cited run directories (skip only when the "cited ref does not exist" violation names an absent run dir, `_is_absent_run_violation` :357) |
| `test_cul431_curve_cost_ratio.py::test_run_081_every_account_lot_net_equals_equity_change`, `::test_run_081_slippage_matches_the_diagnostics_bps`, `::test_run_081_agrees_with_the_whole_test_chain_on_junction_days` (3) | `needs_run_081` skipif defined :273-274 (decorators :274, :285, :315) | `runs/run_081/trade_diagnostics.json` (env `CUL431_RUN_DIR`) |
| `test_d113_gap_coverage.py::test_fold_a_stored_chain_rows_recompute_equal[run_081|run_082|run_083]` (3) | `pytest.skip` :170; `_RUNS_ROOT` :159 | `runs/<id>/artifacts/profit_bars_evaluation.yaml` (env `D113_RUNS_ROOT`) |
| `test_d116_chain_day1.py::test_the_pipeline_chain_reproduces_d114s_with_day1_sharpe[run_084|run_088|run_089]` (3) | `pytest.skip` :152; `_RUNS_ROOT` :143 | `runs/<id>/artifacts/protocol_result.yaml` |
| `test_d117_slippage_precision.py::test_run_081_slippage_is_now_exact_on_every_lot` (1) | `skipif` :137 | `runs/run_081/trade_diagnostics.json` |
| `test_d129_drawdown_per_stretch.py::test_contiguous_stored_runs_recompute_to_the_pre_d129_number[run_081|run_082|run_083|run_091]` (4) | `pytest.skip` :126; `_RUNS_ROOT` :116 | `runs/<id>/artifacts/protocol_result.yaml` |
| `test_window_economics_run_copy.py::test_run_copy_gross_minus_fees_is_net_and_net_is_the_equity_change` (1) | `_run_copy_windows()` skip :177; default path is a Windows temp path constant at :54 (`DEFAULT_RUN_COPY`), env `WINDOW_ECONOMICS_RUN_COPY` :55 | a copy of run_097 outside git; the skip message itself says "runs/ is not in git, CI has no copy" |
| `test_user_guide_field_tables.py::test_no_new_phantom_fields[Handoff files | holdout_result.yaml | promotion_audit.yaml]` (3) | `pytest.skip` :164 (n == 0 instances); `_instances()` :111-120 globs `runs/*/artifacts/<fn>`, `runs/*/<fn>`, `campaign_record/<fn>`, `<fn>` under SR | at least one real instance file; none is tracked (`git ls-files` finds no `holdout_result.yaml`, `promotion_audit.yaml`, `handoffs/` file) |

- GitHub CI: the checkout has only the 60 tracked run directories, so all 20 skip every time on ubuntu and windows (the three `test_user_guide_field_tables` ones too: no instance is tracked). Permanent unless the files are committed or the env vars are set.
- Count check: 2 + 3 + 3 + 3 + 1 + 4 + 1 + 3 = 20.

### 1.3 Data-cache-dependent (`trading-bot/local_data` caches and captures) - 11 tests

`git ls-files trading-bot/local_data` tracks 45 files; `BTCUSDT_1h.csv`, `BTCUSDT_funding_8h.csv`, `BTCUSDT_1d.csv` are NOT among them, and nothing under `Kraken_batch/` or `recorded_reserved/` is tracked.

| Tests | Skip site | Needs |
|---|---|---|
| `trading-bot/tests/test_build_core_gap_aware_pairing.py::test_real_btcusdt_gaps_are_detected_and_counted` | skipif :197; `cache_skip_reason()` in `trading-bot/tests/_cache_guard.py:105` | `local_data/BTCUSDT_1h.csv` covering the test window |
| `trading-bot/tests/test_funding_rate_component.py::test_run_044_config_now_produces_real_active_bars` (:53), `::test_daily_bars_with_merged_funding_produce_nonzero_forecasts` (:131), `::test_data_manager_merge_attach_chain_yields_funding_column_at_1d` (:191) | skipif, reason "local_data fixtures not present" | `BTCUSDT_funding_8h.csv` + `BTCUSDT_1h.csv` / `BTCUSDT_1d.csv` (:33-34, :127-128). The extra skipif at :52 (`run_044` config, tracked) did not fire |
| `trading-bot/tests/test_kraken_archive_ingest.py::test_ingest_roundtrip_integrity` (:94), `::test_utc_roundtrip_guard_raises_on_shift` (:148) | skipif `not PILOT_SOURCE.exists()` | `local_data/Kraken_batch/master_q4/XBTUSD_60.csv` (:39) |
| `trading-bot/tests/test_kraken_cache_reachability.py::test_default_exchange_still_binance_unqualified` | skipif :148 | `local_data/BTCUSDT_1h.csv` |
| `strategy-research/tests/test_measure_funding_carry.py::test_load_bounded_read_is_bit_identical_on_the_committed_window` | skipif :51 | `BTCUSDT_funding_8h.csv` (path from `tools/measure_funding_carry.py:29`) |
| `strategy-research/tools/recorder/tests/test_shard_reader.py::test_baseline_capture_manifest_is_readable` (:393), `::test_baseline_capture_trades_parse_under_deny_by_default` (:401), `::test_baseline_capture_exposes_its_real_coverage_gap` (:416) | skipif `not BASELINE_CAPTURE.is_dir()` (:32-34) | `trading-bot/local_data/recorded_reserved/kraken_ws_v2` |

- Count: 1 + 3 + 2 + 1 + 1 + 3 = 11 (TB 7, SR 4).
- GitHub CI: the caches are untracked, so these 11 skip on both OSes (CI checkout has no `local_data` caches; `cache_skip_reason` also skips when the cache does not cover the window).

### 1.4 Platform-only - 1 test skipped on Linux, 7 skipped here for a missing host

- `trading-bot/tests/test_merge_noop_no_rewrite.py::test_noop_read_succeeds_while_another_handle_denies_write_sharing`: `skipif(sys.platform != "win32")` at :90. Skipped on Linux; runs on the windows-latest CI job, skipped on the ubuntu job.
- `strategy-research/tools/recorder/tests/test_supervisor.py` (7 tests, lines :80, :94, :106, :114, :125, :132, :146): module-level `pytestmark = skipif(POWERSHELL is None, reason="no PowerShell host on this machine")` at :30; `POWERSHELL = shutil.which("powershell") or shutil.which("pwsh")` at :28. Skipped here because neither binary is on PATH in this container. Whether the GitHub runners have them: not checked here (the workflow only uses `shell: pwsh` in the Windows-only step, `.github/workflows/tests.yml:88`); by my knowledge of the GitHub runner images, windows-latest has `powershell` and ubuntu-latest has `pwsh`, which would mean these 7 run in CI on both. Unverified.
- Test names in `test_supervisor.py` are duplicated in `test_supervisor_sh.py` (section 4), the bash counterpart.

### 1.5 Environment-conditional, did not fire as skips in the final run (listed because the code can skip)

- `strategy-research/tests/test_installed_hook_matches_tracked.py:91` `test_installed_hook_matches_tracked`: skips at :93 when `.git` is not a directory and at :95 when `CI` is set. It skipped here because the run set `CI=true`; without `CI` it failed in the baseline (no installed hook in the clone). It always skips in GitHub CI (the test's docstring states this, lines 26-33). Counted in the 49: yes (1).
- Runtime `pytest.skip(` that did not fire: `trading-bot/tests/test_validate_config.py:59` (run_043 fixture), `test_fetch_gap_guard.py:163` (kraken_BTCUSD_1h.csv), `test_fetch_since_utc_tz.py:109` (no `time.tzset`, i.e. Windows), `strategy-research/tests/test_b2_machine_trial_accounting_proof.py:293` and skipif `B2_MACHINE_PROOF != "1"` (:135-136), `test_run_protocol_exit_reason.py:234` (run_054 artifacts), `test_d119_d120.py:161` (chain_windows start values), `test_e037_records_consistent.py:55` (S3_TRIAGE.md).
- `pytest.importorskip("jsonschema")` appears 19 times in SR tests plus `yaml`, `scipy.stats`, `pandas`, `numpy`, and `zstandard` (`tools/recorder/tests/test_compaction.py:16`). None skipped here (the venv has them); not checked whether the CI install has `jsonschema` (it is not in the three requirements files named in the workflow cache paths: not verified).

### 1.6 Summary of the 49

| Group | TB | SR | Total |
|---|---|---|---|
| Base commit not in object store (1.1) | 8 | 1 | 9 |
| runs/ artifacts or instances absent (1.2) | 0 | 20 | 20 |
| local_data / capture cache absent (1.3) | 7 | 4 | 11 |
| Windows-only test (1.4) | 1 | 0 | 1 |
| No PowerShell host (1.4) | 0 | 7 | 7 |
| CI env var (1.5) | 0 | 1 | 1 |
| Total | 16 | 33 | 49 |

Always skipped in GitHub CI (both OSes), by the reasoning above: 9 + 20 + 11 + 1 (hook) = 41. Skipped only on ubuntu: 1 (win32 test). PowerShell group: unverified.

## 2. Slow tests (deselected by `-m "not slow"`): 109

Collected with `pytest --collect-only -m slow -o addopts=""` in the fresh clone (counts match the 74 and 35 in the logs).

trading-bot (74), all marked `pytest.mark.slow` at module or test level and almost all also cache-guarded by `cache_skip_reason(...)`/`skipif` (they run `run_backtest` over `local_data/` caches and skip rather than fetch when the caches are absent; see `FORK_CHANGES.md:349-353`):

| File | slow tests |
|---|---|
| `tests/test_risk_layer_bit_identical.py` | 21 |
| `tests/test_close_positions_at_end.py` | 14 |
| `tests/test_min_allocation_change_override_bit_identical.py` | 8 |
| `tests/test_model_funding_bit_identical.py` | 6 |
| `tests/test_regression_backtest.py` | 6 |
| `tests/test_bar_equity_bit_identical.py` | 4 |
| `tests/test_gap_detection_bit_identical.py` | 4 |
| `tests/test_commission_rate_param.py` | 3 |
| `tests/test_warmup_prefetch_bit_identical.py` | 3 |
| `tests/test_exchange_selection.py` | 2 |
| `tests/test_feed_dependencies.py` | 2 |
| `tests/test_e060_composite_prefetch_backtest.py` | 1 |

strategy-research (35):

| File | slow tests | What it needs |
|---|---|---|
| `tests/test_e061_end_to_end_wiring.py` | 22 | stubbed harness; its docstring (:66) says no network, no real LLM, no real backtest |
| `tests/test_c5_7a_schemas.py` | 6 (parametrized, :367) | replays the e061 scenarios with schema validation; no network, needs `jsonschema` |
| `tests/test_run_protocol_commission_bps_flag.py` | 3 | `local_data` BTCUSDT_1h/funding_8h/fear_greed caches via `requires_cache`; real backtest subprocess |
| `tests/test_d142_max_allocation_change_removed.py` | 2 | `local_data/kraken_BTCUSD_1d.csv`, `kraken_XRPUSD_1d.csv`, `fear_greed_daily.csv` |
| `tests/test_b2_machine_trial_accounting_proof.py` | 1 | also skipif `B2_MACHINE_PROOF != "1"`; real `run_protocol.py` subprocess |
| `tests/test_run_protocol_perp_cost_wiring.py` | 1 | `local_data` caches via `requires_cache` |

- recorder tests: 0 slow.
- None of the slow tests needs the network in a way the code shows: the TB ones read local caches (`test_feed_dependencies.py:406` uses a `block_network` fixture), the SR ones use fixtures or local caches. The statement in `strategy-research/CLAUDE.md:76` ("marked `slow`: live market data, network") and `night_work_2026-11-04/README.md:72` ("slow tests, which use live market data") does not match what the files do. Fact only, per the code listed above.
- When the docs say to run them:
  - `strategy-research/CLAUDE.md:76-78`: never in CI; run on purpose when a change touches data fetching or the regression backtests: `python run_tests.py --slow` from the repo root.
  - `run_tests.py:54-55` documents `python run_tests.py --slow`; `strategy-research/engineering/DISPATCH_MODEL.md:127` repeats it.
  - `trading-bot/pytest.ini:20-28`: the `--timeout=30` global limit kills `-m slow`; use `python -m pytest -m slow --timeout=0`.
  - `tasks/lessons.md:46-47`: pre-merge check when the branch touches the pipeline = full suite plus `pytest -m "slow or not slow" tests/test_e061_end_to_end_wiring.py` (about 2 min).
  - `research/ledger/win.md:73,127`: run `pytest -m slow` before any "unchanged" claim.
  - `trading-bot/DOC/USER_GUIDE.md:959`: names slow tests to run individually.
  - `CLAUDE.md` (root): no mention of slow tests. `strategy-research/docs/RUNBOOK.md`: no mention of the slow marker (the only "slow" hit is an unrelated sentence at :486).

## 3. Warnings (final run; counts are from parsing the pytest warnings summary, so +/-1 per site)

Test code (39 distinct sites: 25 in TB, 14 in SR). All but one are the same `DeprecationWarning: The 'generic' unit for NumPy timedelta is deprecated, and will raise an error in the future` raised by `pd.Timedelta(<int>, ...)`/`pd.Timedelta(hours=...)`-style expressions.

Top test-code sites:

| Count | Site | Category |
|---|---|---|
| 7440 | `strategy-research/tests/test_e060_s3a_composition.py:90` (also hit via `test_e060_s3b_composition_wiring.py`, 3240 of them in the log's grouping) | DeprecationWarning (NumPy generic timedelta) |
| 1486 | `trading-bot/tests/test_aux_feed_fill.py:84` | same |
| 300 | `strategy-research/tests/test_e060_s2_residual_ic.py:670` | same |
| 300 | `strategy-research/tests/test_e060_s2_residual_ic.py:672` | same |
| 250 | `trading-bot/tests/test_d176_sizing_block.py:73` | same |
| 150 | `trading-bot/tests/test_build_core_block_adjusted_significance.py:121` | same |
| 93 | `strategy-research/tests/test_e054_data_availability_gate.py:110` | same |
| 93 | `strategy-research/tests/test_e054_data_availability_gate.py:112` | same |
| 68 | `strategy-research/tests/test_e054_data_availability_gate.py:65` | same |
| 32 | `strategy-research/tests/test_d186_forecast_ic_horizons.py:855` | same |
| 9 | `trading-bot/tests/test_rolling_buffer_reindex.py:104` | same |
| 8 | `trading-bot/tests/test_d146_register_read_feeds_only.py:126` and `:131` (8 each) | same |
| 6 | `trading-bot/tests/test_gap_detection_bit_identical.py:239` | same |
| 5 | `trading-bot/tests/test_cul273b_reindex_wiring.py:129` | same |

Remaining test-code sites with 1-4 hits each: TB `test_aux_feed_fill.py:113,241,252,253,268`, `test_aux_feed_delay.py:34,118`, `test_gap_rule_defects_cul359.py:30`, `test_build_core_block_adjusted_significance.py:90,136`, `test_cul273b_reindex_wiring.py:130`, `test_rolling_buffer_reindex.py:36,50,63,79,84,97`; SR `test_cul259_bootstrap_fallback_timestamp.py:83`, `test_cul265_a851a_post_backtest.py:78`, `test_d186_forecast_ic_horizons.py:854,868`, `test_e060_s2_residual_ic.py:676`, `test_e068_s3_claim_measure.py:265`.

One different category in test code: `SyntaxWarning: invalid escape sequence '\.'` at `strategy-research/tests/test_d186_forecast_ic_horizons.py:761` (non-raw string `"..\..\config\criterion_menu.yaml"`). It is also reported as `<unknown>:761` once under `tests/test_cache_network_guard.py::test_no_network_marker_without_cache_guard` (that test compiles/parses test source; fact only).

Project code (already known, counts from the final run; same category as above):

| Count | Site |
|---|---|
| 59 | `trading-bot/reporting/run_artifact.py:373` |
| 52 | `trading-bot/reporting/run_artifact.py:469` |
| 52 | `trading-bot/reporting/run_artifact.py:92` |
| 51 | `trading-bot/reporting/run_artifact.py:419` |
| 22 | `strategy-research/tools/data_availability_gate.py:516` |
| 15 | `strategy-research/tools/composition.py:881` |
| 2 | `trading-bot/data/data_manager.py:1389` (this one is `datetime.datetime.utcnow()` deprecated, not the NumPy one) |

Third-party (each appears once per suite, 4 hits in all in the summary):
- `venv/.../binance/ws/websocket_api.py:4` DeprecationWarning "websockets.WebSocketClientProtocol is deprecated" (3 per suite in the log's grouping).
- `venv/.../websockets/legacy/__init__.py:6` DeprecationWarning "websockets.legacy is deprecated".

The warnings summaries show no warning of any other category (no pytest unraisable/ResourceWarning/PytestWarning).

## 4. Slowest files, duplicates

- Slowest test files: not measured. The logs were run without `--durations`, and re-running the 14-minute SR suite was not done. Whole-suite times are in the totals table (TB about 97 s, SR about 850 s).
- Duplicate test names inside one file (a later definition shadowing an earlier one): none (AST scan of all test functions and class methods, including classes).
- The same test name in more than one file: 34 names. Pairs where the name suggests the same check in two files:
  - `strategy-research/tools/recorder/tests/test_supervisor.py` and `test_supervisor_sh.py` share 6 names (`test_a_crash_is_relaunched_and_the_gap_is_attested`, `test_a_disk_guard_abort_is_never_relaunched`, `test_a_clean_exit_is_not_relaunched`, `test_repeated_crashes_hit_the_restart_cap_and_give_up`, `test_every_restart_is_logged_with_its_reason`, `test_the_guard_exit_code_literal_matches_the_python_constant`): ps1 and sh versions of the supervisor.
  - `test_flag_non_bool_raises` appears in 5+ SR files, `test_flag_off_by_default_and_in_the_shipped_config` in 4+, `test_flag_is_registered_everywhere` in 4, `test_flag_reader` in 4+, `test_flag_is_off_in_the_real_config_and_registered` in 4+ (the per-flag test pattern).
  - Pairs: `test_d127_leave_one_block_out_bar.py` / `test_d127_trade_frequency_bar.py` share `test_absent_or_null_key_has_no_row_and_grades_exactly_as_before` and `test_the_loader_checks_the_key_only_when_present`; `test_e062_s2b1_profit_bars_v2.py` / `test_profit_bars_every_backtest.py` share `test_flag_false_when_absent_or_off` and `test_run_loop_preflight_fails_before_any_spend`; `test_e068_3b_past_return.py` / `test_e074_s1_trailing_vol.py` share `test_two_windows_never_chain` and `test_event_selector_reads_it`; `test_e062_s2b2b_dsr_wiring.py` / `test_e062_s2b3b_normalisation_wiring.py` share `test_v2_loader_refuses_a_bad_floor`; `test_d178_analyst_method.py` / `test_d184_analyst_disclosure.py` share `test_an_answer_that_cites_no_query_is_refused`; `test_exact_config_1b.py` / `test_exact_config_step2.py` share `test_run_loop_flag_on_without_exact_config_calls_the_model`; `test_d051_d053_forecast_rules.py` / `test_d149_standardised_forecast_rule.py` share `test_the_regime_detector_is_not_checked`; `test_d122_refold.py` / `test_d125_block_status.py` share `test_the_cli`.
  - TB: `test_standardise_op.py` / `test_e060_block_standardisation.py` share `test_current_value_is_not_in_its_own_denominator`; `test_bar_equity_bit_identical.py` / `test_warmup_prefetch_bit_identical.py` share `test_explicit_false_matches_omitted_default`.
  - Full list of the 34 names is reproducible with an AST scan over the three test directories (script left in scratchpad: `hyg_scan.py`). Whether bodies are equal was not compared.

## 5. Leads: tests/docstrings that refer to things no longer in the code

Heuristics run: (a) every `"--flag"` string literal in the test directories (66) was searched in tracked non-test files; (b) backticked snake_case identifiers in each test module docstring were searched in tracked non-test source (py/yaml/json/sh/ps1/txt, excluding runs/, guided_tour/, night_work*, research/).

- (a) 9 flags not found in non-test source, none stale: `--abort`, `--no-edit` (git flags, `test_s4_union_merge.py`), `--max-turns`, `--max-budget-usd`, `--mcp-config`, `--permission-mode` (claude CLI flags used in `test_e075_pr5_analyst.py` / `test_cul336_closed_book_stages.py`), `--make-series` (defined in a test fixture, `tests/fixtures/d176/replay_harness.py:102`), `--criteria` and `--readers` (negative assertions at `test_d122_refold.py:268`).
- (b) 4 modules flagged, all false positives on inspection: `trading-bot/tests/test_cache_guard_predicate.py` (`cache_skip_reason` lives in `tests/_cache_guard.py:105`), `strategy-research/tests/conftest.py:71` and `test_loop_health_instrument.py:34` (`campaign_root` is a test fixture defined in `test_halt_history.py:74`, `test_halt_quarantine_policy.py:77`, `test_k4_routing_registration.py:70`), `test_validation_route_family_status.py:5` (`family_rationale`, `family_blocking_issues` are the legacy keys it documents as the bug, still frozen in `runs/run_053/artifacts/validation_decision.yaml:5,11`).
- Result: no clear case found by grep of a test whose name/docstring refers to a feature absent from the code. Intentional "removed/retired" regression tests exist (e.g. `test_d142_max_allocation_change_removed.py`, `test_e059_6c_s2a_route_retirement.py`) and were not treated as stale.

## Not checked

- Per-file and per-test durations (`--durations` not run); the slowest-files list is therefore absent.
- Whether GitHub runners actually have PowerShell/pwsh (supervisor tests) and whether the CI install has `jsonschema`, `scipy`, `zstandard` (importorskip groups): no CI run or log was read.
- Whether the 9 base-commit tests are skipped in a real CI run: inferred from `actions/checkout@v4` default depth, not observed.
- Whether bodies of same-name tests in different files are duplicates.
- Which of the 1432 + 7733 passing tests are vacuous or never assert (only skip and warning output was read).
- Windows-specific behaviour: the final log is a Linux run; no Windows run output was read, so Windows skips and warnings are not known except from the code.
- Warning counts are from parsing the summary grouping and may be off by one per site; the run was in the scratchpad `check_final` clone, which no longer exists (log only).
- Nothing outside the test directories was searched for stale references (docs, skills, configs).
