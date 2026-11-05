# tools/ — inventory

`strategy-research/tools/` holds the research pipeline's deterministic helpers: the
modules the orchestrator imports (gates, record writers, claim and criteria code, the
backtest runner), the standalone command-line tools an operator runs by hand, the git
hook and holdout gate, the Kraken forward recorder (`recorder/`) and the run viewer
(`run_viewer/`). This page is a lookup table only. **The code is the source of truth**:
each module's docstring says what it does and why; when this page and the code disagree,
the code wins and this page is the thing to fix.

## How to read the table

- **RP** = `workflow/run_phase1_research.py`, **RC** = `workflow/run_campaign.py`,
  **SR** = `strategy-research/`, **TB** = `trading-bot/`. A bare `name.py:N` is a sibling
  in `tools/`.
- **Live** means the live pipeline reaches the file: an import chain from RP or RC was
  found by an AST scan of every import statement (imports inside functions included),
  or RP runs the file as a subprocess. The chain shown is one shortest chain. This is a
  grep fact, not a judgement: many live modules only run under an `orchestrator.*` flag
  that is off by default.
- **Used by** lists the non-test importers as `file:line` (lines as of the commit that
  last edited this page; they drift), then the number of test files that import it.
- A CLI tool with no importer is in its normal state: a command is run, not imported,
  so "no importer found" is not evidence that a tool is dead.
- `power_check.py` and `prescreen_signal.py` are no longer in `tools/` (see git history).

## Conventions

- Tools import each other as bare sibling modules (`import decide_next`): RC and RP put
  `tools/` on `sys.path` first (`RC:80`, `RP:83`). Heavy imports (anything that pulls in
  `core.launcher` or the agent SDK) are kept lazy, inside the function that needs them.
- Small shared-definition modules (`composition_names.py`, `protocol_refusal.py`,
  `reader_categories.py`) have no imports of their own, so any side can import them
  without weight. When two places need one rule, the rule lives in one tool and both
  import it.
- RP runs subprocess tools with the trading-bot interpreter (`TBOT_PYTHON`, `RP:1817`).
- The sealed holdout range is read only through `holdout_policy.py` from
  `config/campaign_data_policy.yaml`. No tool or doc writes its dates out.
- Two firewalls: no decision-path code may import `fragment_patterns.py`
  (`SR/tests/test_fragment_patterns_firewall.py`), and per `near_miss_scoreboard.py`'s
  docstring nothing that computes a verdict, routing or promotion may consult the
  scoreboard.
- Adding a tool: give it a module docstring whose first paragraph states its purpose,
  add a row to the table below, and test it under `SR/tests/`. A tool that touches market
  data also follows the repository's hard rules (no lookahead, a "why this can't leak"
  note, a trial-ledger row per experiment; see the repository `CLAUDE.md`).

## Inventory

### Queue, decide-next and launch

| tool | purpose | used by | CLI |
|---|---|---|---|
| `decide_next.py` | Picks the next idea when a lineage finishes: loads memory, registry and proposals, writes `decision_record.yaml` and the brief for a picked candidate (called by RC under `orchestrator.decide_next.enabled`). | **Live** (RP imports it). Imported by `RP:6443,8596`; `RC:2444,2484,5013,5229,5276,5342,5386,5422,5460,5510,5594,5694`; `analyst_session.py:995`; `config_vehicle.py:270`; `fold_confirm.py:422,497`; `SR/engineering/lane1_replay/lane1_registry_check.py:25`. Tests: 34 files. | - |
| `campaign_lock.py` | Single-writer campaign launch lock: a second launch on the same host refuses instead of racing on `campaign_state.yaml`. | **Live** (campaign_memory &larr; RP). Imported by `RC:82`; `campaign_memory.py:50`. Tests: 11 files. | - |
| `abandoned_launch.py` | Marks and recognises run dirs left by a launch that raised before `run_loop` (`status: abandoned_launch`), so scanners skip them. | **Live** (near_miss_scoreboard &larr; RP). Imported by `RC:90`; `build_exclusion_digest.py:65`; `near_miss_scoreboard.py:117`; `replay_repeat_gate.py:90`. Tests: 1 file. | - |
| `campaign_review_retired.py` | Shared constants and append-only files of campaign review under retired verdict routing (`component_requests.yaml`, `campaign_review_log.yaml`, `campaign_decision.yaml`). | **Live** (RP imports it). Imported by `RP:7723`; `RC:85`; `claim_card.py:571,605`; `claim_measure.py:375`; `explore_confirm.py:1001,1090`. Tests: 3 files. | - |
| `research_folds.py` | The fixed folds of time windows (`config/folds.yaml`) and the seeded fold draw for a child run; dates resolved from the data policy. | **Live** (RP imports it). Imported by `RP:1757`; `RC:89`; `campaign_memory.py:51`; `decide_next.py:126`; `fold_confirm.py:531`; `reader_proposals.py:488`; `run_protocol.py:2169`; `SR/engineering/FOLD-FLOORS-2/real_return_null.py:101`. Tests: 5 files. | - |
| `venue_resolver.py` | Turns a brief's (venue, product) into the protocol keys the backtest reads (`exchange`, `market_type`, venue labels). | **Live** (RP imports it). Imported by `RP:19017`; `decide_next.py:1922`; `variant_coin.py:171,648`; `SR/engineering/FOLD-FLOORS-2/real_return_null.py:102`. Tests: 1 file. | - |

### Stages, protocol and routing

| tool | purpose | used by | CLI |
|---|---|---|---|
| `protocol_resolution.py` | The one shared resolver of which protocol file a run uses (with the promotion guard `assert_promotion_ratified`). | **Live** (RP imports it). Imported by `RP:11045,18491,18599,19337`; `RC:87`; `claim_tests.py:1722,1816,1885,2260`; `replay_repeat_gate.py:95`; `run_protocol.py:38`; `verdict_criteria_evaluator.py:51`. Tests: 9 files. | - |
| `protocol_refusal.py` | Shared wording/exit for "run_protocol refused before any window ran, no market data touched" (no trial row recorded). | **Live** (RP imports it). Imported by `RP:1755`; `run_protocol.py:2011`. Tests: 6 files. | - |
| `stamp_protocol.py` | Version-stamps a protocol JSON and prints its structural content hash for a pre-registration's `protocol_ref_content_hash`. | CLI run by hand; no importer found. Tests: 1 file. | `python strategy-research/tools/stamp_protocol.py <protocol.json> [--version V]` |
| `novelty.py` | The one definition of "this exact thing was already tested": the exact-match key (forecast_hash, symbols, timeframe, window_set). | **Live** (RP imports it). Imported by `RP:9390,9451,19264`; `anti_adjacency_gate.py:73`; `campaign_memory.py:250,948`; `claim_findings.py:254`; `decide_next.py:124`; `replay_repeat_gate.py:94`; `research_folds.py:57`. Tests: 8 files. | - |
| `anti_adjacency_gate.py` | Step 5a repeat gate: ADMIT or REFUSE a candidate variant by the exact-match key against campaign memory. | **Live** (RP imports it). Imported by `RP:9388`; `replay_repeat_gate.py:91`. Tests: 2 files. | `python strategy-research/tools/anti_adjacency_gate.py <config> <protocol> [--memory] [--kb] [--runs-dir] [--hypothesis-id] [--exclude-run-id] [--out]` |
| `build_exclusion_digest.py` | Digest of what was already tried, per family. Its docstring calls it legacy since E-036 S2a: nothing refuses on it; decide_next records `legacy_family_lookup` as an advisory. | **Live** (decide_next &larr; RP). Imported by `anti_adjacency_gate.py:74`; `decide_next.py:1586`; `replay_repeat_gate.py:92`. Tests: 5 files. | `python strategy-research/tools/build_exclusion_digest.py [--runs-dir] [--campaign-state] [--out]` |
| `replay_repeat_gate.py` | Read-only replay of the 5a exact-match repeat gate over past `runs/run_*`, beside the retired family-grain answer. | CLI run by hand; no importer found. Tests: 2 files. | `python strategy-research/tools/replay_repeat_gate.py [--runs-dir] [--root] [--campaign-state] [--out]` |
| `variant_coin.py` | One coin per variant at step 5a: per-variant protocol files with `symbols: [<coin>]` (kinds base / design / asset). | **Live** (RP imports it). Imported by `RP:18993`; `decide_next.py:1923`; `verdict_criteria_evaluator.py:1471`. Tests: 10 files. | - |
| `forecast_rules.py` | The D-051, D-053 and D-149 config checks (no on/off classes or dead-zone ops in graded forecasts; a variant keeps the idea's classes). | **Live** (RP imports it). Imported by `RP:19001`; `catalogue_section.py:35`; `config_vehicle.py:271`. Tests: 6 files. | - |
| `forecast_size_probe.py` | Bug detector: refuses a config whose forecast is broken in size (all NaN, or largest magnitude far below a working size). Never judges trade frequency. | **Live** (subprocess from RP). Run as a subprocess by `RP:5584` (its file hash read at `RP:5568`). Tests: 1 file. | `python strategy-research/tools/forecast_size_probe.py --config C --protocol P --json-out F` |
| `nearest_build.py` | Parses step 1b's nearest-build answers into `artifacts/deviations.yaml` and component-request rows (under `orchestrator.nearest_build.enabled`). | **Live** (RP imports it). Imported by `RP:4428`; `claim_findings.py:50`; `config_vehicle.py:556`; `fold_confirm.py:449,459`. Tests: 5 files. | - |
| `json_pointer.py` | Shared RFC 6901 JSON-pointer helpers and the variant patch applier, so the orchestrator, block registry and decide_next use one implementation. | **Live** (RP imports it). Imported by `RP:18967,18976`; `analyst_session.py:996`; `block_manifest.py:54`; `block_registry.py:70`; `composition.py:75`; `config_vehicle.py:240,458,496,533,555`; `decide_next.py:123`; `fold_confirm.py:423,529`. Tests: 5 files. | - |
| `data_availability_gate.py` | E-054 Layer 2: per-window data-touch check that a variant's data can be assembled (validate / refine / decline) before the engine runs. | **Live** (RP imports it). Imported by `RP:6505,19336,19369`. Also run as a subprocess by `RP:1903,2018`. Tests: 7 files. | `python strategy-research/tools/data_availability_gate.py <config> <protocol> [--run-id] [--out-dir] [--exchange] [--gap-tolerance] [--layer1-path]` |
| `refresh_coin_start_dates.py` | Writes per-coin `earliest_ohlcv_utc` into the venue data-capability file from the header/first row of each local 1h cache. | CLI run by hand; no importer found. Tests: 1 file. | `python strategy-research/tools/refresh_coin_start_dates.py [--dry-run]` |
| `timeframe.py` | Timeframe arithmetic derived from the string (`timeframe_seconds`, bars per day) instead of a lookup table. | **Live** (structure_key &larr; RP). Imported by `RC:92`; `claim_tests.py:1871`; `composite_cache.py:85`; `composition.py:866`; `decide_next.py:1391`; `run_protocol.py:1557`; `structure_key.py:57`; `whale_footprint_evaluation.py:107`. Tests: 2 files. | - |
| `workflow_artifact_validation.py` | Opt-in JSON-Schema validation of workflow artifacts at write/read time (schema found by file stem; warn mode by default). | **Live** (RP imports it). Imported by `RP:85`; `block_registry.py:71`; `campaign_memory.py:52`; `deflate_sharpe.py:38`; `run_protocol.py:36`; `validate_regime_detector.py:54`. Tests: 5 files. | - |
| `config_vehicle.py` | Content check of a config vehicle (a side finding's complete strategy config): its `requires` list, TB `validate_config.py` rules, `forecast_rules`, and the regime-gate form. | **Live** (RP imports it). Imported by `RP:19009`; `decide_next.py:1985,2040,2749`. Tests: 4 files. | - |

### Claims, criteria and readings

| tool | purpose | used by | CLI |
|---|---|---|---|
| `claim_card.py` | The `claim` block step 1a writes (statement, kind, tests), checked by code (under `orchestrator.claim_tests.enabled`). | **Live** (RP imports it). Imported by `RP:17405`; `RC:3125`; `analyst_memory_view.py:80`; `analyst_queries.py:1058`; `analyst_session.py:97,1687`; `claim_findings.py:48`; `claim_measure.py:46`; `decide_next.py:2134`; `explore_confirm.py:631,864,917`; `fold_confirm.py:526`; `reader_findings.py:97,122`. Tests: 20 files. | - |
| `claim_tests.py` | The claim test engine: selector / outcome / baseline / statistic measured on a run's saved `bars.csv`. | **Live** (RP imports it). Imported by `RP:17496,18463`; `analyst_queries.py:139`; `analyst_session.py:584,1222,1426,1453,1465,1693`; `claim_card.py:50`; `claim_measure.py:47`; `claim_tests_calibration.py:56`; `explore_confirm.py:423`; `fold_confirm.py:285,318,527`; `window_economics.py:96`; `SR/engineering/FOLD-FLOORS-2026-10-19/fold_floor_sim.py:43`; `SR/engineering/FOLD-FLOORS-2026-10-19/regrade.py:32`. Tests: 13 files. | `python tools/claim_tests.py --run R --spec S --out F --cache-dir D [--cache-pattern] [--method] [--calibration]` |
| `claim_tests_calibration.py` | Pre-registered calibration gate for `claim_tests.py`: on simulated no-edge prices, rejection share must be about 0.05 per side. | CLI run by hand; no importer found. Tests: 2 files. | `python tools/claim_tests_calibration.py {cell,summarize,reevaluate} ...` |
| `claim_measure.py` | Measures a run's claim-card tests on each graded variant's bars after the backtests (effect sizes only, no verdict). | **Live** (RP imports it). Imported by `RP:18374`; `analyst_queries.py:138`; `analyst_session.py:818,1044`; `claim_findings.py:49`; `explore_confirm.py:422,658,710`; `fold_confirm.py:169,317`; `SR/engineering/FOLD-FLOORS-2026-10-19/fold_floor_sim.py:42`; `SR/engineering/FOLD-FLOORS-2026-10-19/regrade.py:31`. Tests: 14 files. | - |
| `claim_findings.py` | Builds the run's `finding` for campaign memory and `artifacts/findings_summary.yaml`. | **Live** (RP imports it). Imported by `RP:18638`; `reader_findings.py:57,74`. Tests: 7 files. | - |
| `fold_confirm.py` | Confirms a claim on the fold of the child run built from it (`confirm_on_fold`, under `orchestrator.folds.enabled`). | **Live** (RP imports it). Imported by `RP:18570`; `SR/engineering/FOLD-FLOORS-2026-10-19/fold_floor_sim.py:44`; `SR/engineering/FOLD-FLOORS-2026-10-19/regrade.py:33`. Tests: 6 files. | - |
| `explore_confirm.py` | Exploration / confirmation split of a run's windows; readers see exploration windows only (under `orchestrator.explore_confirm.enabled`). | **Live** (RP imports it). Imported by `RP:4438`; `RC:3130`; `analyst_memory_view.py:81`; `analyst_session.py:1392`; `fold_confirm.py:319,528`. Tests: 8 files. | - |
| `verdict_criteria_evaluator.py` | K2 kernel: resolves a run's pre-registered pass rule from its computed results, deterministically (plus the C7-EXT gates and provenance checks). | **Live** (RP imports it). Imported by `RP:2397,2615,4408,4518,5928,6012,6047,8245,8364,8378,8830,11389,12513,12772`; `RC:84`; `campaign_memory.py:283,309`; `explore_confirm.py:387`; `grid_kb_writer.py:54`; `lint_verdict_provenance.py:44`; `near_miss_scoreboard.py:510`. Tests: 39 files. | - |
| `lint_verdict_provenance.py` | Standalone G6 check: every verdict-bearing KB / queue record cites a resolvable `pass_rule_evaluation.yaml` or declares itself `ungated`. Exit 1 on an unbacked claim. | CLI run by hand; no importer found. Tests: 1 file. | `python strategy-research/tools/lint_verdict_provenance.py [--root DIR]` |
| `reader_proposals.py` | Loads and validates proposal files (`runs/<id>/artifacts/proposals/<category>.yaml`) by hand against `proposal.schema.json`. | **Live** (RP imports it). Imported by `RP:4535`; `analyst_session.py:73,1084`; `campaign_memory.py:392`; `decide_next.py:125`; `explore_confirm.py:731`; `fold_confirm.py:404,530`; `reader_findings.py:31`. Tests: 27 files. | - |
| `reader_findings.py` | Readings v3: the code-written `skipped` reading and the side-finding review (warnings only). | **Live** (RP imports it). Imported by `RP:4656`; `decide_next.py:1195,2141`; `explore_confirm.py:773`. Tests: 9 files. | - |
| `reader_categories.py` | The proposal categories as one constant: the analyst's two lens categories and the three legacy reader names. | **Live** (RP imports it). Imported by `RP:1758`; `fold_confirm.py:405`; `SR/engineering/lane1_replay/lane1_registry_check.py:24`. Tests: 7 files. | - |

### Analyst

| tool | purpose | used by | CLI |
|---|---|---|---|
| `analyst_session.py` | The analyst session's pure part: builds the prompt and checks the model's answer (citations against the query log, claim tests, holdout dates). | **Live** (RP imports it). Imported by `RP:4706`; `campaign_memory.py:433`; `reader_findings.py:85`. Tests: 18 files. | `python tools/analyst_session.py --run <copy of a run> --lens <lens>` (smoke CLI; one real model session, spends money; refuses a run under `runs/`) |
| `analyst_queries.py` | The analyst's query engine: fixed functions over one saved run's bars and trades (no SDK, no network). Its docstring still says nothing imports it yet; RP does. | **Live** (RP imports it). Imported by `RP:4714`; `claim_tests.py:380,394`. Tests: 6 files. | - |
| `analyst_memory_view.py` | What the analyst is told about earlier claims: one row per claim with status, numbers for confirmed claims only. | **Live** (RP imports it). Imported by `RP:4722`. Tests: 4 files. | - |
| `catalogue_section.py` | Renders the component and transform-op catalogue as one prompt section from `COMPONENT_CATALOG.md` and `STRATEGY_DESIGN_GUIDE.md`. | **Live** (analyst_session &larr; RP). Imported by `analyst_session.py:44`. Tests: 1 file. | `python tools/catalogue_section.py` (prints the section; no arguments) |

### Backtest and economics

| tool | purpose | used by | CLI |
|---|---|---|---|
| `run_protocol.py` | Walk-forward protocol runner: each window an independent backtest via `core.launcher.run_backtest`; writes `protocol_result.yaml` / `protocol_summary.json`. | **Live** (residual_ic &larr; composite_cache &larr; RP). Imported by `RC:2831`; `residual_ic.py:332`. Run as a subprocess by `RP:2220,2534` and `composite_cache:261`. Tests: 30 files. | `python strategy-research/tools/run_protocol.py <config> <protocol> [--validation-protocol] [--out-dir] [--cost-product {spot,perp}] [--commission-bps] [--exchange] [--drop-feeds] [--cost-bar-all-costs] [--forecast-ic-horizons] [--diagnostics-only] [--legacy-verdict-retired] [--holdout --i-understand --hypothesis-id ID]` |
| `cost_helpers.py` | One definition of per-symbol commission (bps and per-side fraction) and the realized gross-edge / cost ratio, importable without `core.launcher`. | **Live** (portfolio_whole_test &larr; RP). Imported by `portfolio_whole_test.py:92`; `run_protocol.py:37`. Tests: 2 files. | - |
| `portfolio_daily.py` | The equal-weight portfolio's daily closes and returns: one definition for the profit bars and the composition's block returns. | **Live** (RP imports it). Imported by `RP:14029`; `composition.py:76`; `curve_cost_ratio.py:52`; `portfolio_whole_test.py:93`. Tests: 10 files. | - |
| `portfolio_whole_test.py` | Whole-test (profit bars v2) portfolio functions. Its docstring says nothing in the orchestrator calls it yet; RP:14223 imports it. | **Live** (RP imports it). Imported by `RP:14223`; `deflate_sharpe.py:798`; `variant_coin.py:362`. Tests: 13 files. | - |
| `window_economics.py` | Per (coin, window) economics of one variant, read from the run's own files; shared by the analyst query and `profit_bars_evaluation.yaml`. | **Live** (RP imports it). Imported by `RP:15407`; `analyst_queries.py:140`. Tests: 2 files. | - |
| `curve_cost_ratio.py` | Curve-based gross / cost ratio for pre-registration (equity change plus costs over costs, per coin-window account). | Imported by `SR/engineering/lane1_replay/fold_c_reading.py:23`. That importer is a hand-run engineering script; not reached from RP or RC. Tests: 1 file. | - |
| `deflate_sharpe.py` | Bailey and Lopez de Prado (2014) Deflated Sharpe Ratio over the campaign's trials, with trial deduplication. | **Live** (RP imports it). Imported by `RP:14379`; `backfill_structure_hash.py:153`; `dual_writer_demo.py:39`; `killed_run_gate.py:54`. RP also keeps its own transcription of parts of it (see the comments near `RP:13017-13234`). Tests: 20 files. | `python strategy-research/tools/deflate_sharpe.py <run_id> [--campaign-state PATH] [--allow-unmerged]` |
| `structure_key.py` | D-185 structure key of a trial, (structure_hash, timeframe): sizes the deflated Sharpe's N by what was tested. | **Live** (RP imports it). Imported by `RP:12104`; `backfill_structure_hash.py:58`; `deflate_sharpe.py:197,1161`. Tests: 2 files. | - |
| `backfill_structure_hash.py` | Keys old trial-ledger rows with their (structure_hash, timeframe); dry run (counts only) by default. | CLI run by hand; no importer found. Tests: 1 file. | `python tools/backfill_structure_hash.py [--root DIR] [--write]` |
| `episode_significance.py` | IC significance by bootstrapping over episodes (runs of active bars) instead of fixed 24-bar blocks. | **Live** (RP imports it). Imported by `RP:11141`; `claim_tests.py:153,1870`; `run_protocol.py:1556`. Tests: 5 files. | - |
| `panel_backtester.py` | Research-only vectorized panel backtester for cross-sectional strategies; `gate` reproduces an archived engine run first. | CLI run by hand; no importer found. Tests: 3 files. | `python strategy-research/tools/panel_backtester.py gate` / `... xs [--lookback] [--rebalance] [--min-n]` |
| `validate_regime_detector.py` | Deterministic regime-detector validation (persistence, transitions, sensitivity, activation) and a confidence grade. | **Live** (subprocess from RP). Imported by `retune_regime_detector.py:45`. Run as a subprocess by `RP:10172` and `retune_regime_detector:544`. Tests: 1 file. | `python strategy-research/tools/validate_regime_detector.py [--config] [--symbols] [--start] [--end] [--out]` |
| `retune_regime_detector.py` | One-shot grid search over regime-detector parameters, scored on intrinsic criteria only (no PnL). | CLI run by hand; no importer found. Referenced by path in `TB/tests/test_tbot_python_resolver.py:81`. | `python strategy-research/tools/retune_regime_detector.py [--symbols] [--start] [--end] [--skip-validate]` |
| `killed_run_gate.py` | Synthetic proof that a completed KILL backtest lands one trial row and is counted by both deflated-Sharpe N paths. | CLI run by hand; no importer found. Tests: 1 file. | `python strategy-research/tools/killed_run_gate.py` (no arguments) |
| `dual_writer_demo.py` | Synthetic end-to-end demo of the two-writer trial-ledger contract (union merge, no DSR until merged). Writes no live record. | CLI run by hand; no importer found. Tests: 1 file. | `python strategy-research/tools/dual_writer_demo.py` (no arguments) |
| `dual_writer_demo_fixtures/` | Two fabricated writer ledgers (`master_ledger.yaml`, `fork_ledger.yaml`) for the demo. | Read by `dual_writer_demo.py:41` (`FIXTURE_DIR`). | - |

### Blocks and composition

| tool | purpose | used by | CLI |
|---|---|---|---|
| `block_registry.py` | `campaign_record/block_registry.yaml`: validated blocks, append-only; written by the `regroup_record` stage. CLI appends a status record. | **Live** (RP imports it). Imported by `RP:5313,5844,6140,8884`; `composite_cache.py:442`; `decide_next.py:120`; `SR/engineering/lane1_replay/lane1_hand_block.py:30`; `SR/engineering/lane1_replay/lane1_registry_check.py:23`; `run_viewer/loaders.py:724`. Tests: 9 files. | `python tools/block_registry.py status --block-id ID --status {voided,active} --reason R --by NAME [--registry PATH]` (from strategy-research/) |
| `block_manifest.py` | The one implementation of the `artifacts/block_manifest.yaml` contract (which part of the base config is the block). | **Live** (RP imports it). Imported by `RP:18985`; `block_registry.py:68`; `claim_findings.py:109`; `config_vehicle.py:623`; `decide_next.py:2039`. Tests: 4 files. | - |
| `composite_cache.py` | The current composite forecast series a candidate block's residual IC is measured against, per exact timeframe (under `orchestrator.composition_runs`). | **Live** (RP imports it). Imported by `RP:5843,6046`; `RC:5343`; `composition.py:73`; `decide_next.py:1287,1390`; `SR/engineering/lane1_replay/lane1_hand_block.py:31`. Tests: 9 files. | - |
| `composition.py` | Deterministic composition assembly: weights and the composed config from the registry's blocks on one timeframe. Its docstring says nothing calls it yet; RP and RC import it. | **Live** (RP imports it). Imported by `RP:6132`; `RC:5344,5387`; `decide_next.py:1212,1288`. Tests: 3 files. | - |
| `composition_names.py` | Names shared by composition, decide_next, RC and RP (one definition each, no imports). | **Live** (RP imports it). Imported by `RP:6124`; `RC:86`; `composition.py:74`; `decide_next.py:121`. Tests: 1 file. | - |
| `residual_ic.py` | Residual IC: does a candidate block hold information the current composite does not. | **Live** (composite_cache &larr; RP). Imported by `composite_cache.py:84`; `composition.py:865`. Tests: 2 files. | - |

### Records and memory

| tool | purpose | used by | CLI |
|---|---|---|---|
| `campaign_memory.py` | `campaign_record/campaign_memory.yaml`: one entry per run (full or fault-only), written by `regroup_record`; also the file lock and atomic write helpers. | **Live** (RP imports it). Imported by `RP:3802,8822,9389,9450`; `anti_adjacency_gate.py:72`; `block_registry.py:69`; `campaign_review_retired.py:25`; `claim_card.py:604`; `claim_measure.py:374`; `composite_cache.py:338`; `composition.py:689,733`; `decide_next.py:122`; `explore_confirm.py:277,533,559,1000,1089`; `grid_kb_writer.py:53`; `replay_repeat_gate.py:93`. Tests: 25 files. | - |
| `grid_kb_writer.py` | Adds one grid-based entry per run to `campaign_knowledge_base.yaml`. | **Live** (RP imports it). Imported by `RP:8885,12635`. Tests: 2 files. | - |
| `record_schema.py` | Closed (allow-list) schema for KB findings and queue entries; a verdict may live in one designated field only. | **Live** (verdict_criteria_evaluator &larr; RP). Imported by `RC:83`; `lint_verdict_provenance.py:43`; `verdict_criteria_evaluator.py:50`. Tests: 13 files. | - |
| `near_miss_scoreboard.py` | Ranked near-miss table over every tested run, raw material for idea generation. Not a promotion input. | **Live** (RP imports it). Imported by `RP:8982`. Tests: 4 files. | `python tools/near_miss_scoreboard.py [--runs-dir] [--out-dir]` |
| `fragment_patterns.py` | Ideation-only diagnostics over LIFO trade fragments (`trades.json`). Under a firewall: no decision-path code may import it. | No importer found. `SR/tests/test_fragment_patterns_firewall.py` only checks that nothing imports it. | - |

### Holdout and data policy

| tool | purpose | used by | CLI |
|---|---|---|---|
| `holdout_policy.py` | The one strict reader of `campaign_data_policy.yaml`'s `holdout_range` (strict day parsing, `windows_overlap`). | **Live** (RP imports it). Imported by `RP:1756`; `RC:88`; `analyst_queries.py:585`; `check_data.py:36`; `composite_cache.py:86`; `measure_bar_sigma.py:90,92`; `research_folds.py:56`; `run_protocol.py:2022`; `SR/engineering/FOLD-FLOORS-2/real_return_null.py:100`; `run_viewer/sanitize.py:105`. Tests: 8 files. | - |
| `seal_safe_cache.py` | Seal-safe reads of local OHLCV caches for research tools, reusing the engine's seal guards. | Imported by `measure_funding_carry.py:38`; `panel_backtester.py:58`. Both importers are CLI tools; not reached from RP or RC. Tests: 3 files. | - |
| `check_data.py` | Checks the bars a protocol needs are on disk and refuses a protocol that overlaps the sealed holdout. Exit 0 clean, 1 holdout overlap, 2 gap over a day. | CLI run by hand; no importer found. Tests: 2 files. | `python strategy-research/tools/check_data.py [--protocol P] [--policy PATH] [--skip-data-check] [--timeframe TF]` |
| `cache_gap_census.py` | Timestamp-continuity census over the local OHLCV caches (gap pairs, contiguous runs, gap-aware n_eff). Read-only. | CLI run by hand; no importer found. | `python strategy-research/tools/cache_gap_census.py [--data-dir] [--timeframe] [--warmup] [--block] [--gate-floor]` |
| `measure_bar_sigma.py` | Measures `sigma_bar_bps` (std of 1-bar returns, bps) for the recorded Kraken pairs, refusing sealed candles. | CLI run by hand; no importer found. Tests: 1 file. | `python -m tools.measure_bar_sigma [--pairs] [--start] [--end] [--local-data] [--full-history]` (from strategy-research/) |
| `measure_funding_carry.py` | Measures realized perp funding carry on the in-sample window only (window bound hard-coded in the file). | CLI run by hand; no importer found. Tests: 1 file. | `python strategy-research/tools/measure_funding_carry.py` (no arguments) |

### Forward recorder (Kraken WS)

| tool | purpose | used by | CLI |
|---|---|---|---|
| `recorder/` | Standalone Kraken WS v2 forward-recorder package (capture, journal, compaction, retrieval, whale features). See `recorder/RUNBOOK.md`. | **Live**, partly: `recorder/shard_reader`, `whale_features` and `journal` via TB/data/fetchers/whale_footprint_fetcher.py:91-92 &larr; TB/data/feed_registry.py:18 &larr; data_availability_gate (RP) and TB/core/launcher (run_protocol). Its tests (`recorder/tests/`) run via `run_tests.py`; CI installs `recorder/requirements.txt` (`.github/workflows/tests.yml:47`). | `python -m recorder.<module>` with `strategy-research/tools/` on the path (the supervisors `cd` there, e.g. `recorder/supervise.sh:130`) |
| `whale_footprint_evaluation.py` | Evaluation harness for `prereg_whale_footprint_v2.yaml`: every threshold read from the pre-registration; its docstring says it has not been run on the real capture. | CLI run by hand; no importer found. Tests: 1 file. | `python strategy-research/tools/whale_footprint_evaluation.py --prereg PATH [--run-id ID]` |

### Viewer

| tool | purpose | used by | CLI |
|---|---|---|---|
| `run_viewer/` | Read-only local web page over run folders and records (D-180); every output string passes through `sanitize.py`. Design in `run_viewer/DESIGN.md`. | Tests: `SR/tests/test_run_viewer.py`. | `python tools/run_viewer/server.py --runs runs [--root] [--host 127.0.0.1] [--port 8765]` (from strategy-research/) |

### Hooks and gates

| tool | purpose | used by | CLI |
|---|---|---|---|
| `hooks/pre-commit` | Tracked pre-commit hook: the secret scan and the holdout date gate (the test suite is deliberately not in it). | Run by git once `setup_hooks.sh` has set `core.hooksPath`. Tests: `SR/tests/test_installed_hook_matches_tracked.py`, `test_precommit_gate0_delete_allowed.py`. | Installed once per clone by `setup_hooks.sh` (sets `core.hooksPath`); git then runs it on every commit. |
| `setup_hooks.sh` | One-time per clone: points git's `core.hooksPath` at `tools/hooks/`. | CLI run by hand, once per clone (named in the header of `hooks/pre-commit`); no code or test runs it. | `sh strategy-research/tools/setup_hooks.sh [--check]` |
| `holdout_date_gate.sh` | Scans the git index for dates inside the sealed holdout range and blocks the commit unless exempted in `config/holdout_gate_exemptions.txt`. Deny by default. | Run by `hooks/pre-commit:83` and CI (`.github/workflows/tests.yml:60`). Tests: `SR/tests/test_holdout_date_gate.py`. | `sh strategy-research/tools/holdout_date_gate.sh [--self-test-only \| --report-residual]` |

### Misc

| tool | purpose | used by | CLI |
|---|---|---|---|
| `build_inventory.sh` | Regenerates the E-002 `INVENTORY.tsv` (every tracked file under strategy-research/ with bytes and git-history aggregates). | CLI run by hand; no code or test runs it. | `sh strategy-research/tools/build_inventory.sh` (no arguments; cds to the repo root) |
| `gen_user_guide_toc.py` | Generates `docs/USER_GUIDE.md`'s table of contents from its headings. | `--check` is run by `SR/tests/test_user_guide_toc.py`. | `python tools/gen_user_guide_toc.py [--check]` |
| `README.md` | This file. | Documentation; no test reads it. | - |

### Package members

`recorder/` (standalone; imports nothing from `trading-bot/`; its data is reserved,
see `config/campaign_data_policy.yaml:kraken_ws_forward_recorder`):

| file | purpose | used by | CLI |
|---|---|---|---|
| `__init__.py` | Package marker; states the reserved-data rule. | Loaded by every `recorder.<module>` import. | - |
| `record_kraken_ws.py` | The capture daemon: verbatim `book` (depth 10), `trade`, `instrument`, `status`, `heartbeat` from Kraken WS v2 for the 19 pairs. | Run by `supervise.sh:117` and `supervise.ps1:107`. Imported by `coverage_report.py:75,80`; `journal_mark.py:39,42`; `liveness.py:53,56`; `retrieval_manifest.py:62,65`. | `python -m recorder.record_kraken_ws run [--out] [--depth] [--book-mode] [--snapshot-interval] [--roll] [--no-compress] [--min-free-gb] ...` |
| `shard_writer.py` | Verbatim NDJSON shard writer (frame bytes spliced, never re-serialised). | Imported by `record_kraken_ws.py:76,85`. | - |
| `book_state.py` | Local depth-N book behind the lossy SNAPSHOT cadence mode. | Imported by `record_kraken_ws.py:69,78`. | - |
| `compaction.py` | Hourly zstd compaction of shards, verified before the raw file is deleted. | Imported by `record_kraken_ws.py:70,79`; `shard_writer.py:77,79`. | - |
| `disk_guard.py` | Free-space floor checked while recording; a breach writes `DISK_GUARD_ABORT` and exits 3. | Imported by `record_kraken_ws.py:71,80`. | - |
| `journal.py` | Coverage journal: attests what was captured, since the book channel has no sequence numbers. | **Live** (shard_reader &larr; TB whale fetcher, see above). Imported by `coverage_report.py:72,77`; `journal_mark.py:38,41`; `liveness.py:50,55`; `record_kraken_ws.py:75,84`; `retrieval_manifest.py:61,64`; `shard_reader.py:82,91`. | - |
| `journal_mark.py` | Supervisor-side journal writer (`RESTART_BOUNDARY` records). | Run by `supervise.sh:182` and `supervise.ps1:169`. | `python -m recorder.journal_mark restart --out DIR --exit-code N [--attempt] [--backoff] [--reason]` |
| `shard_reader.py` | The read side: frames in timestamp order across pairs, with journal gaps interleaved, never interpolated. | **Live** (TB/data/fetchers/whale_footprint_fetcher.py:91). Imported by `whale_features.py:195,197`; `whale_persistence.py:109,119`; `whale_report.py:47,57`. | - |
| `whale_features.py` | Whale-footprint features from public trades, aggregated to bars (no forward return, no IC). | **Live** (TB/data/fetchers/whale_footprint_fetcher.py:92). Imported by `whale_persistence.py:110,120`; `whale_report.py:48,58`. | - |
| `kraken_crc.py` | Kraken WS v2 L2 book CRC32 checksum verifier, replayable over the shards. | No importer found (listed in `__init__.py`'s `__all__`); tests only (`tests/test_kraken_crc.py`, `test_cadence_modes.py`). | - |
| `coverage_report.py` | Report of the intervals NOT captured over the capture's life, and why. | CLI run by hand. | `python -m recorder.coverage_report [--out] [--journal] [--start] [--end] [--symbol] [--channel] [--fail-on-gap]` |
| `liveness.py` | Operator health check; exit 0 healthy, non-zero down or degraded. | CLI run by hand (printed as a next step by `install_systemd_unit.sh:142`). | `python -m recorder.liveness [--out] [--window] [--expect-symbols] [--max-staleness]` |
| `retrieval_manifest.py` | Capture-host manifest (sha256 and bytes of every compacted shard and the journal). | Run over SSH by `retrieve_shards.py:132`; imported by `retrieve_shards.py:71,75,186,188`. | `python -m recorder.retrieval_manifest --out DIR` |
| `retrieve_shards.py` | Pulls shards from the capture host and verifies them against the manifest; `prune` deletes only confirmed remote files. | CLI run by hand. | `python -m recorder.retrieve_shards {pull,prune} --host H --remote-out D --local-out D [--identity] ...` |
| `whale_persistence.py` | Sign persistence (holding bars) of each whale feature. | CLI run by hand. | `python -m recorder.whale_persistence [--root] [--symbols] [--start] [--end] [--bar-seconds] ...` |
| `whale_report.py` | Descriptive statistics of the whale features (no predictive statistic). | CLI run by hand; no test found. | `python -m recorder.whale_report [--root] [--symbols] [--bar-seconds] ...` |
| `supervise.sh` | Linux restart supervisor (no relaunch after exit 0 or `DISK_GUARD_ABORT`). | Run by the systemd unit that `install_systemd_unit.sh:69` writes. Tests: `tests/test_supervisor_sh.py`. | `bash tools/recorder/supervise.sh [--out DIR] [--min-free-gb N] [--book-mode MODE] ...` |
| `supervise.ps1` | Windows restart supervisor, same policy. | Run by the scheduled task `register_scheduled_task.ps1:65` registers. Tests: `tests/test_supervisor.py`. | - |
| `install_systemd_unit.sh` | Registers `supervise.sh` as a systemd system service. | Run by hand. | `bash tools/recorder/install_systemd_unit.sh` |
| `register_scheduled_task.ps1` | Registers `supervise.ps1` as a Windows Scheduled Task. | Run by hand. | - |
| `RUNBOOK.md` | Operator runbook for the recorder. | Documentation. | - |
| `requirements.txt` | The recorder's dependencies (websockets, zstandard). | Installed by CI (`.github/workflows/tests.yml:47`). | - |
| `.gitattributes` | Forces LF line endings on `*.sh`. | git. | - |
| `tests/` | The recorder's own test suite (16 test files, a conftest and a fixture). | Run by `run_tests.py` as a sibling suite. | - |

`run_viewer/` (read-only; GET and HEAD only; binds 127.0.0.1 unless `--host`):

| file | purpose | used by | CLI |
|---|---|---|---|
| `server.py` | Stdlib `http.server` page and JSON API over the run folders; refuses to start if the sealed-window policy cannot be read. | CLI run by hand. Tests: `SR/tests/test_run_viewer.py`. | see `run_viewer/` above |
| `loaders.py` | The data layer: one JSON-able document per view, never raises on a missing or unparseable file. | Imported by `server.py:39`. | - |
| `sanitize.py` | The one output filter: masks any date inside the sealed window in every string the viewer emits. | Imported by `server.py:40`. | - |
| `DESIGN.md` | The viewer's design. | Documentation. | - |
| `SHAPES_run_099.md` | The artifact shapes the loaders are written against (`DESIGN.md:75`). | Documentation. | - |
| `static/` | The page: `index.html`, `app.js`, `style.css`, `view4.js`, `view4.css`. | Served by `server.py` (`STATIC_DIR`, `server.py:42`). | - |
| `static/vendor/` | Vendored uPlot (`uplot/uPlot.iife.min.js`, `uPlot.min.css`, `LICENSE`, `README.md`) and a `.gitattributes` (`* -text`). | Loaded by `static/index.html:9,22`. | - |
