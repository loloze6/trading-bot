# Daily-breadth loop: flag set, brief, commands (D-130)

Prepared 2026-10-14. The operator applies the edit and launches every run; nothing here touches
the operator's checkout. All scripts run from the operator checkout's `strategy-research/`
(`../venv/Scripts/python.exe`).

## 1. The flag edit (one script, both files)

`apply_flagset.py` (plan by default, `--write` to apply). It checks the value it expects on every
line and stops without writing if any differs.

Changes in `config/campaign_config.yaml` (5 flags):

| flag | from -> to | why |
|---|---|---|
| `variant_loop` | false -> true | the loop: one coin per variant (card C), the unit decide-next and the analyst work on |
| `composition_runs` | false -> true | composition is the designed way to pass branch 3 (a single block rarely clears 20% drawdown) |
| `analyst` | false -> true | the idea source (D-092..D-098); `model: claude-haiku-5-5` and the caps are untouched (code defaults 40 turns, 3.0 USD, 15 min) |
| `brief_criteria` | false -> true | decide-next fold children copy their source run's criteria (D-121) |
| `deviation_gate` | true -> false | D-104 pauses any step-1b answer whose deviations are not exact; in the loop 1b builds nearest versions by design |

Changes in `config/feature_flag_register.yaml` (`tests/test_feature_flag_register.py` fails on drift):
the `state` of the five flags above, and `folds` (already `enabled: true` in the operator's config,
still `off_incomplete` in the register: the test fails today).

Every orchestrator flag after the edit:

| flag | value | why |
|---|---|---|
| `halt_policy.quarantine_enabled` | off | its DONE path also calls decide-next; every halt stays a human stop |
| `exclusion_digest_input` | on | step 1a/2 read what was tried (tried_ideas) |
| `stale_input_path_fix` | on | step 1a gets the real knowledge base |
| `variant_selection_record` | on | legacy path only, inert under config-direct |
| `variant_anti_adjacency_gate` | on | the 5a exact-match repeat check |
| `schedulability_block` | on | diagnostic file, no decision reads it |
| `grid_evaluation` | on | branch 1: each idea graded on its own criteria |
| `profit_bars_file` | on | branch 3: the signed bars file |
| `profit_bars_every_backtest` | on | branch 3 on every backtest (profit-bar flag) |
| `profit_bars_v2` | on | whole-test bars as signed (D-118..D-120, D-127) |
| `category_reports` | on | required by specialist_readers |
| `data_availability_gate` | on | per variant, before any backtest |
| `config_direct_authoring` | on | 1b writes the config; variants are patches |
| `variant_loop` | **on** | see above |
| `specialist_readers` | on | the analyst replaces its reader lenses (prerequisite) |
| `regroup_record` | on | writes memory and registers validated blocks (branch 1) |
| `score_provenance` | on | requires specialist_readers |
| `decide_next` | on | picks the next run after each one |
| `verdict_routing_retired` | on | the grid and the bars decide, no refine/pivot/kill route |
| `composition_runs` | **on** | see above; prerequisites decide_next, variant_loop, profit_bars_every_backtest, verdict_routing_retired are all on |
| `forecast_size_probe` | on | per-config diagnostic |
| `claim_tests` | on | prerequisite of reader_findings and the analyst's claims |
| `reader_findings` | on | analyst prerequisite (D-091/D-092) |
| `observable_backtest` | off | not asked for |
| `zero_trade_windows_not_computed` | off | not asked for |
| `analyst` | **on** | see above |
| `folds` | on | child runs draw a fold at random (D-123); analyst prerequisite |
| `operator_approval` | on | every decide-next pick waits for `--approve` |
| `nearest_build` | on | 1b builds the nearest expressible version and records deviations |
| `deviation_gate` | **off** | see above; `nearest_build` stays on |
| `config_replay_gate` | on | acts only on a brief with an exact config (this brief has none) |
| `exact_config_1b` | on | same: only for an exact-config brief |
| `brief_criteria` | **on** | see above |
| `explore_confirm` | off | D-093 |
| `cost_bar_all_costs` | on | declared output change already in force |

Other consequences, read from the code:
- `refold` (D-122) refuses while `variant_loop` is on; it is not involved.
- With the registry holding one active daily block, composition (R1) needs two forecast blocks on a
  timeframe (`tools/decide_next.py:1362`), so it stays quiet until a second daily block validates.
- The orchestrator's analyst caps are the code defaults (`run_phase1_research.py:5087`); the
  `orchestrator.analyst` block is unchanged apart from `enabled`.

## 2. The first brief

`briefs/daily_breadth_fold_a.md` (template `research_brief_new_pipeline.md`): daily bars, Kraken
perp on spot prices, base BTC, fold A through the protocol's `fold: "A"` key
(2022-01-01 .. 2023-12-31, 4-month windows), no criteria in the brief (`criteria_from:
hypothesis_generation`), step 1a to extract several ideas (card M).

Cached daily Kraken coins covering fold A with a 250-day warm-up and no missing day
(`daily_cache_coverage.py`, bounded: dates only, nothing else printed):
AAVE, ADA, BTC, DOGE, ETH, LINK, LTC, TRX, UNI, XMR, ZEC. XRP: 2 missing days. SOL: 52 missing
days in the warm-up (fold itself covered). AVAX, INJ, NEAR, SUI, ONDO, TAO start too late.
Asset variants must come from a category other than BTC's (`store_of_value`, which also holds
ETH): AAVE, UNI, LINK (defi), ADA, ZEC, XMR, LTC, TRX (`altcoin_l1_verified_kraken`), DOGE (memecoin).

## 3. Commands, in order (campaign stopped; the brief PR merged and master merged into c4/flag-set)

1. Retire the held and paused entries (plan first, then `--write`):
   `../venv/Scripts/python.exe engineering/flagset_daily_breadth/retire_queue_entries.py --write <ids>`
   (ids in the D-130 row / the hand-off message).
2. Apply the flag edit: `.../apply_flagset.py` (plan), then `--write`; then
   `.../preflight_check.py` (the launch flag pre-flight, expects ACCEPTED).
3. Register: `PYTHONUTF8=1 ../venv/Scripts/python.exe workflow/run_campaign.py register --brief briefs/daily_breadth_fold_a.md --priority 1 --notes "daily breadth, fold A (D-130)"`
4. Dry run: `PYTHONUTF8=1 ../venv/Scripts/python.exe workflow/run_campaign.py --dry-run` (expects `=== DRY RUN PASSED ===`).
5. One step: `PYTHONUTF8=1 ../venv/Scripts/python.exe workflow/run_campaign.py --once`.
6. When decide-next holds its first pick (log: `awaiting operator approval: <id>`), stop and report
   it; the approval command is `PYTHONUTF8=1 ../venv/Scripts/python.exe workflow/run_campaign.py --approve <entry_id>`.
