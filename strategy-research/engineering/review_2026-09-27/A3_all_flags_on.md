# A3: walking one run through with every flag on

Checkout: `C:\Users\alauz\Documents\Projects\trading-bot` at master `e623531d` (read only).
All file:line references are at that commit. SR = `strategy-research/`, RPR = `SR/workflow/run_phase1_research.py`, RC = `SR/workflow/run_campaign.py`.

**How I checked things**
- By reading the code.
- With one scratch reproduction, `scratchpad/review/repro_handoffs.py`. It sets `rpr.ROOT` to a temp dir and uses the real `setup_run` templates. It turns on `config_direct_authoring` and `variant_loop` and leaves the data gate at its default (on). It then calls the real `run_loop` at three stages. No LLM, no backtest, no network; `git status` was unchanged afterwards.
- By running one targeted test: `pytest tests/test_e060_s3b_composition_wiring.py -k end_to_end`, which passed (1 test, 150 s).

Anything marked **(inference)** was not executed.

---

## 1. Flag map

The flags live under `orchestrator:` in `SR/config/campaign_config.yaml`. The descriptions come from `SR/config/feature_flag_register.yaml`.

**Column meanings**
- "strict" means the reader raises on a value that is not a bool. The non-strict readers use `bool(x)`, so a quoted `"false"` reads as ON.
- "Enforced when" says whether the `requires` check runs before any LLM spend ("pre-flight") or only when a later call site first reads the flag ("lazy").

| flag | default | register state | requires / blocked on | how the code enforces it | reader (RPR / RC line) |
|---|---|---|---|---|---|
| exclusion_digest_input | **true** | on | none | not strict | RPR:2535 |
| stale_input_path_fix | **true** | on | none | not strict | RPR:2636 |
| variant_selection_record | **true** | on | none. Legacy LLM backtest_specification path only; inert under config-direct | not strict | RPR:6335 |
| schedulability_block | **true** | on | none | (RC) | RC:2279 |
| data_availability_gate | **true** (absent reads as true) | on | none | strict; the only flag that defaults on | RPR:2451 |
| halt_policy.quarantine_enabled | false | (not in register) | none | RC:1467 | RC:1467 |
| grid_evaluation | false | off_incomplete | blocked on E-046b (stale, see §4) | not strict | RPR:2272 |
| category_reports | false | off_incomplete | blocked on slice 5b | not strict | RPR:2293 |
| profit_bars_file | false | off_incomplete | blocked on bar ratification + avg_daily_return definition | not strict; **ratification is not checked by code** (`_load_profitability_bars` accepts `ratified_by: null`, RPR:2393-2394) | RPR:2312 |
| config_direct_authoring | false | off_incomplete | blocked on an E-056 real-LLM proof | strict | RPR:2697 |
| variant_loop | false | off_incomplete | requires config_direct_authoring | strict; raises on read, but **lazy**: first read is at 5a / data gate / protocol_execution, after 1a/1b/2 have spent | RPR:2728 |
| specialist_readers | false | off_incomplete | requires grid_evaluation + category_reports | strict; raises in **run_loop pre-flight** (RPR:11774-11785) | RPR:2798 |
| regroup_record | false | off_incomplete | requires specialist_readers | strict; pre-flight (RPR:11791-11798) | RPR:3359 |
| profit_bars_every_backtest | false | off_incomplete | requires profit_bars_file + regroup_record | strict; pre-flight (RPR:11801-11808) | RPR:2332 |
| decide_next | false | off_incomplete | requires regroup_record + config_direct_authoring | strict; checked on every `process_once` step before launch (RC:2560) | RPR:3388 |
| verdict_routing_retired | false | off_incomplete | requires decide_next + profit_bars_every_backtest | strict; pre-flight (RPR:11812-11819) and every `process_once` (RC:2563) | RPR:3485 |
| composition_runs | false | off_incomplete | requires decide_next + variant_loop + profit_bars_every_backtest + verdict_routing_retired | strict, but **lazy**: first read after 1a (RPR:12121 / 5698), at the grid (RPR:1673), and at DONE (RC:3068) | RPR:3534 |
| variant_anti_adjacency_gate | false | off_incomplete | needs regroup_record, but only when `campaign_memory.yaml` is absent; the legacy site also needs variant_selection_record | not strict; the dependency raises only at 5a, **after 3 LLM stages** (RPR:6580-6586) | RPR:6533 |

Two engine flags come from the same register: `bar_equity` (on, passed by `run_protocol.py`) and `model_funding` (off, blocked on E-014).

**When flags are read.** Only `specialist_readers`, `regroup_record`, `profit_bars_every_backtest` and `verdict_routing_retired` are snapshotted once per `run_loop`. Every other flag is re-read from the YAML at each call site. `config_direct_authoring`, for example, is read at RPR:6818, 12150, 12205, 12208 and RC:3416. So editing `campaign_config.yaml` while a run is going changes that run's routing partway through.

### Target v26 flag set (set these in place in `config/campaign_config.yaml`, leaving comments and other keys alone)

```yaml
orchestrator:
  exclusion_digest_input:       {enabled: true}   # already on; switches to tried_ideas.yaml once memory exists
  stale_input_path_fix:         {enabled: true}   # already on
  variant_selection_record:     {enabled: true}   # already on; legacy path only (inert under config-direct)
  schedulability_block:         {enabled: true}   # already on
  data_availability_gate:       {enabled: true}   # already on (default true)
  config_direct_authoring:      {enabled: true}
  variant_loop:                 {enabled: true}
  grid_evaluation:              {enabled: true}
  category_reports:             {enabled: true}
  specialist_readers:           {enabled: true}
  regroup_record:               {enabled: true}
  profit_bars_file:             {enabled: true}   # ratify config/profitability_bars.yaml FIRST (code does not check)
  profit_bars_every_backtest:   {enabled: true}
  decide_next:                  {enabled: true}
  verdict_routing_retired:      {enabled: true}   # DECLARED BEHAVIOUR CHANGE
  variant_anti_adjacency_gate:  {enabled: true}
  composition_runs:             {enabled: true}   # residual_ic threshold is a placeholder (criterion_menu.yaml ratified: false)
  halt_policy:
    quarantine_enabled: false                     # leave off (its DONE path also calls decide_next)
```

**Constraints**
- Write unquoted booleans. Seven of these readers are not strict, and a quoted `"false"` reads as ON.
- Flip every flag in one edit, while no campaign is running. The dependency graph is a directed acyclic graph with `config_direct_authoring`, `grid_evaluation`, `category_reports` and `profit_bars_file` at the roots. Any partial on-set that respects the graph is legal. The two lazily enforced edges (`variant_loop` needing config-direct; `composition_runs`'s four requirements) fail only after spend.
- Do not change flags between `--resume` calls. RPR:11869-11879 and RPR:11935-11947 fail a run routed under a flag that is now off.
- Before the first run: ratify `config/profitability_bars.yaml` (today `ratified_by: null`, `ratified_at: null`) and the `residual_ic` placeholders (`criterion_menu.yaml`, `ratified: false`). Code does not enforce either; it only records `bars_ratified_by` (RPR:10505).

---

## 2. Walking one forecast-block run with this flag set

### Entry: `run_campaign.py` (CWD must be `strategy-research/`, RC:3679)

1. **`process_once`** (RC:2545):
   - `reconcile_orphans`, then `_write_schedulability`.
   - `_decide_next_enabled()` and `_verdict_routing_retired_enabled()` are resolved; a misconfiguration raises here, before any launch.
   - `_select_entry` (RC:175): in_progress first, else the ready entry with the lowest priority.
   - **Today's queue has no ready entry.** `P4_ts_trend` is `blocked_on_daily_bar_ingest`, and the other four are `done` and legacy (no `brief_status`, so R2 never fires for them). `process_once` therefore logs "Queue exhausted" and returns False (RC:2567-2569).
   - The first run needs an operator brief registered with `run_campaign.py register`. Under decide_next that writes `brief_status: open` (RC:3531).
2. **fresh_launch** (RC:2630-2643):
   - `setup_run(run_id)` copies the **9 templates** in `workflow_artifacts/templates/handoffs/` (measured). There is no `backtest_spec_to_data_availability_gate.yaml` among them.
   - `_materialize_run` (RC:413) writes `research_brief.yaml` (with `research_only` from `venue_tradability.yaml`) and, only if the brief has `machine_constraints`, `pre_registration.yaml`. Before writing it runs the B11 / CUL-267 / K3 lints; `pass_rule` = `brief.evaluation.pass_rule`, or the pending marker if `criteria_from: hypothesis_generation`.
   - `_write_brief_hypotheses_context` (RC:3384).
   - Then `orch.run_loop(run_id)` (RC:2696), **with no try/except around it**.

### `run_loop` (RPR:11727)

- **Pre-flight** (RPR:11748-11832):
  - `_ensure_protocol_from_constraints` (RPR:7441) requires a pre-registered `promotion` block: `_require_pre_registered_promotion`, RPR:7579. Alternatively `_ensure_protocol_ref_pinned` (RPR:7676).
  - The readers pre-flight needs a menu-shaped `pass_rule` unless it is deferred to 1a (RPR:5614).
  - Then regroup_record, pbe and vrr are resolved.
  - A failure writes `status=failed` before any spend.
- **Each stage** (RPR:11834-12628):
  - Token breaker at the top of the loop (1.5M weighted units, `_load_token_budget`; regroup_record is exempt).
  - `handoff_data = load_yaml(handoff)` (RPR:11966) and `ensure_files(required_inputs)` (RPR:11968). Both are **outside the `try`**, which only starts at RPR:11992.

| step | function (file:line) | reads | writes | LLM or code | can pause / park / stop | next |
|---|---|---|---|---|---|---|
| 1a hypothesis_generation | `_invoke_agent_with_yaml_retry` RPR:702 → `async_invoke_agent` RPR:6813 → `run_claude_worker` RPR:967 | brief, `available_feeds`, `indicator_library`; plus `criterion_menu` + `cost_model` (RPR:6261); tried_ideas / exclusion digest; KB / wishlist; the DECIDE_NEXT / BRIEF addenda | `hypothesis_card.yaml` (+ `queued_hypotheses.yaml`, `brief_status.yaml`) | Claude `claude-haiku-4-5` (RPR:944); +1 YAML retry, +1 SDK retry | exhausted brief → `completed_brief_exhausted`; repeat card → `completed_no_new_hypothesis`; `_write_pass_rule_from_card` (RPR:5669) raises before 1b; residual_ic added (RPR:12121) | `strategy_config_authoring` (RPR:12150) |
| 1b strategy_config_authoring | same worker; `_clear_stale_block_manifest` | card, STRATEGY_DESIGN_GUIDE, B7 pre_registration | `backtest_spec.yaml`, `decision.yaml`, `block_manifest.yaml` | Claude; manifest failure → sent back once (`_route_block_manifest_check` RPR:11445) | component_gap → **park** waiting_for_component (RPR:11516-11530); unknown status → pause | innovation_expansion |
| 2 innovation_expansion | same worker | brief, card, feeds, library, `backtest_spec.yaml` (RPR:6273) | `expanded_hypothesis_card.yaml`, `innovation_notes.yaml`, `variant_patches.yaml` (base / design / asset per the SKILL). `variant_patches.yaml` is **not** a checked deliverable | Claude | none | `backtest_specification` (RPR:12205) |
| 5a backtest_specification | `run_tool_worker` RPR:1965-2153 (tool because config-direct, RPR:6818) | `backtest_spec`, `variant_patches`, `block_manifest` | `variants/<id>/strategy_config.json`, `variants/index.yaml`, `candidate_strategy_config.json` (base), `component_requests.yaml` | code + `validate_config.py` subprocess per variant | **before any of this, run_loop's `ensure_files` on the template handoff raises; see Finding 1** | `_route_post_config_direct_backtest_specification` RPR:11604 |
| 5a exact-match repeat gate | `_gate_config_direct_variants` RPR:6722 → `_repeat_gate_context` RPR:6551 (`_resolve_protocol_path` → D-3) | `campaign_memory.yaml`, protocol, KB | `variant_anti_adjacency_result.yaml`, index.yaml (repeats → not_tested) | code | every variant a repeat → `completed_no_new_hypothesis`; none validated → park (component) / pause | data_availability_gate |
| 5a data gate, per variant | `run_tool_worker` RPR:1262-1391; route RPR:12291-12355 | each variant config + resolved protocol | `variants/<id>/data_availability/…`, `artifacts/variants/<id>/data_availability_gate.yaml`, `campaign_record/data_requests.yaml` | code (`data_availability_gate.py` subprocess; may fetch) | fewer than 3 validated left → park (all-data / all-class) or **pause `variant_gate_insufficient`** (RPR:12319-12351) | protocol_execution |
| protocol_execution | `run_tool_worker` RPR:1429-1725 | `variants/index.yaml`, protocol, `validation_protocol.yaml` (**never written in this flow**, see Finding 3) | per variant: `RUN_DIR/variants/<id>/…` (backtest outputs), `artifacts/variants/<id>/protocol_result.yaml`; singular `protocol_result.yaml` (base copy); `pass_rule_evaluation.yaml` (legacy C7, base only); `grid_evaluation.yaml`, `idea_status.yaml`, `residual_ic.yaml`, `reports/*.yaml`; one **trial row per variant** `run:variant` (RPR:1575) | code (`run_protocol.py` subprocess per variant; `validate_regime_detector.py` when the report is 30+ days old: RPR:2885, RPR:7063) | all variants fail → raise; grid / report error → stage fails **after** trials are recorded (RPR:1725); conformance violation → invalidate that variant's trial + pause (RPR:12411-12463) | then `_evaluate_profit_bars_every_backtest` RPR:10457 (per-variant `profit_bars_evaluation.yaml`, never pauses here) → `specialist_readers` |
| specialist_readers | `_run_specialist_readers_stage` RPR:3250 → `run_reader_worker` RPR:3147 ×5 | per reader: `reports/<cat>.yaml` + `grid_evaluation.yaml` | `proposals/<cat>.yaml` (validated); `data_requests.yaml` rows for `requires_feed` | Claude ×5, +1 validation retry each; budget checked before each | component errors → readers skipped; invalid output after the retry → fail; budget → `rejected_budget_exceeded` | regroup_record |
| regroup_record | `_run_regroup_record_stage` RPR:6075 | idea_status, grid, variants, proposals, trial ids (read only), pbe evaluation | `campaign_memory.yaml` (upsert); `block_registry.yaml` (validated + manifest; append-only); KB entry (`legacy_schema: false`); near-miss scoreboard | code | stale registry / KB after a fault → logged, still pauses | route RPR:12533-12563 |
| decide step | `_profit_bars_stop_route` RPR:10540 → `_holdout_unlock_route` RPR:4949 → `determine_post_specialist_readers_route` RPR:3275 → `_route_retired_idea_status` RPR:4256 → `_retired_review_route` RPR:5300 | pbe evaluation, idea_status, pipeline_state | pipeline_state (`completed_<status>`, status completed); `campaign_state.runs` via `_record_run_in_campaign_state` | code | component error → pause; any passing variant → **pause `profit_bars_reached`**; review due → `campaign_review` (Claude; handoff written by `_write_retired_review_handoff`, RPR:5251) | terminal `completed_validated`, `completed_refuted` or `completed_inconclusive` |
| DONE + decide_next | RC:2909-2928 → `_apply_idea_status_outcome` RC:2946 → `_finish_lineage_with_decision` RC:3035 → `decide_next.decide` tools/decide_next.py:1604 | `campaign_memory`, queue, proposals, source configs / manifests, registry, compositions, feed registry | `runs/<run>/artifacts/decision_record.yaml`; a minted `campaign_record/candidate_briefs/...` + queue entry (origin reader), or extra-card queued→ready, or R2 `<owner>__more_<n>`, or R1 composition; queue saved `done` last | code | `stop` → `process_once` returns False | next `process_once` picks via `_select_entry` |

**decide_next order** (tools/decide_next.py:24-59):
1. An existing in_progress or ready entry is picked; operator entries go first.
2. R1 composition: an exact timeframe holding at least 2 validated forecast blocks not yet composed. It goes ahead of agent entries.
3. Reader proposals and a brief's extra cards, gated by:
   - exact-match novelty (binding);
   - feasibility (the patch resolves, the manifest resolves, the class exists, `requires_feed` is wired).

   Candidates are ranked by `confidence_real` descending, then `distance_to_profitable` descending, then cost ascending, then id.
4. R2: an open brief gets a "more hypotheses" request. A brief goes to exhausted after 2 empty R2 requests in a row.
5. Otherwise, stop.

A picked candidate's brief carries `candidate.criteria_from: hypothesis_generation` and the source run's `machine_constraints`. The run is materialized pending at 1a and its criteria are rebuilt from 1a's card.

### Composition run (R1)

- **At DONE:** `_prepare_r1` (RC:3256) writes, in code:
  - the three variant configs (base, vol_scaled, ic_weighted) and `composition_manifest.yaml` under `campaign_record/compositions/<id>/`;
  - the `compositions.yaml` row.

  `_register_r1` (RC:3347) then writes the brief and a queue entry with origin composition. A preparation failure becomes a `paused:composition_failed` entry, and decide runs again (RC:3087-3095).
- **In the run:** 1a, 1b and 2 are code (`_run_composition_code_stage` RPR:3925, `_composition_mode` RPR:3764). The 5a exact-match gate is skipped for compositions (RPR:6758). At 5a the composition manifest is checked on every variant (RPR:2007-2021).
- **In the grid:** `profit_bars` is graded by branch 3's own grader (RPR:1679-1683). `residual_ic` is skipped as "composition run".
- **At regroup:** a composite never registers as a block. A crash is paused as `composition_failed` (RC:2731-2736).
- The same handoff breaks as a forecast run apply here: 5a still loads the `validation_to_backtest_specification.yaml` template. The only end-to-end test hides this by rewriting the handoffs (§5).

### Holdout path

1. Any variant PASSes every bar → `profit_bars_reached` pause. `pending_stage` stays at `regroup_record`, and `profit_bars_stop_evaluation` is set to the evaluation's `generated_at` (RPR:10574).
2. The operator writes `runs/<run>/artifacts/holdout_decision.yaml`. Its schema is closed: decision spend|continue, run_id, profit_bars_stop_evaluation, variant_id, trial_ledgers_merged, ratified_by, ratified_at, note.
3. `run_campaign.py --resume` → `holdout_decision_resume_blocker` (RC:1735-1745, RPR:5113).
4. `run_loop` re-enters regroup_record. The stop was already raised for this evaluation, so `_holdout_unlock_route` (RPR:4949) → `_validate_holdout_decision` (RPR:4863) runs. It refuses unless all of these hold:
   - the ledgers are attested merged;
   - this evaluation PASSes the named variant under the same bars sha;
   - DSR clears on the current ledger;
   - the hypothesis is not already in `holdout_consumed_by`;
   - no other unfinished spend exists.
5. Outcomes:
   - **spend** → `holdout_evaluation` (RPR:11880-11909 → `_unlocked_holdout_evaluation`, RPR:5062). The holdout backtest is run **by hand**; then `holdout_result.yaml` → `completed_promoted` or `completed_rejected`, or a pause.
   - **continue** → `completed_<idea_status>` → decide_next.
   - Anything else → the `holdout_unlock_refused` pause.

---

## 3. Breakage a real run would hit

### 3.1 Handoff contract not ported to config-direct (breaks_run, measured)

All three items below were measured with the scratch repro against the real templates.

1. **5a backtest_specification.** The handoff is the legacy template `validation_to_backtest_specification.yaml`. Its `required_inputs` lists `artifacts/validation_protocol.yaml` (template line 13). Only the `validation` stage writes that file, and config-direct skips that stage (RPR:12205).
   - `ensure_files` at RPR:11968 raises `FileNotFoundError`. That line is outside the `try`, so the exception escapes `run_loop`.
   - The repro produced `FileNotFoundError: Missing files: [...expanded_hypothesis_card.yaml, ...validation_protocol.yaml]`. The first file is missing only because the bare repro never ran stage 2; the second is structural.
2. **data_availability_gate.** Its handoff `backtest_spec_to_data_availability_gate.yaml` is not a template. Only `_create_remaining_handoffs` (RPR:6965) writes it, and that is called only on the legacy branch (RPR:12270). So `load_yaml` at RPR:11966 raises an uncaught `FileNotFoundError` (repro: `No such file or directory: ...handoffs\backtest_spec_to_data_availability_gate.yaml`).
3. **protocol_execution.** The template `backtest_spec_to_protocol_execution.yaml:13` requires `validation_protocol.yaml`, so `ensure_files` raises again. Even if the handoff were relaxed, `run_tool_worker` passes `--validation-protocol artifacts/validation_protocol.yaml` unconditionally (RPR:1479, RPR:1515-1520). `run_protocol.py:2289-2291` then `open()`s it **after all windows have been backtested**. Every variant would exit non-zero, be recorded as `backtest_failed` (counted, but the data is spent), and then "all variants failed" raises (RPR:1595). **(inference for this half; the file-open path was read, not executed)**

**What happens at campaign level** (RC:2696 has no try/except; `run_forever`, RC:3536, has none either):
- `process_once` crashes with a traceback.
- The campaign lock is released (RC:3714).
- No `halt_history` or `campaign_log` HALT line is written, and `status` stays `active`.
- A restart re-selects the in_progress entry and crashes at the same stage.
- 1a, 1b and 2 are not re-spent (`pending_stage` is already 5a), but the campaign cannot progress.

The test harness knows about this: `tests/test_e033_slice4b_gate_conformance_promotion.py:82-90` says run_loop's step-1 `load_yaml(handoff_path)` "raises FileNotFoundError, UNCAUGHT", and it scaffolds handoffs with empty `required_inputs`.

### 3.2 Environment: no trading-bot interpreter (breaks_run, measured)

`_resolve_tbot_python` (RPR:101-122) looks for `../venv/Scripts/python.exe`, then `../.venv/bin/python`, relative to `strategy-research/`. On this checkout it raises "No runnable trading-bot interpreter". `venv/Scripts/` has `pytest.exe` but no `python.exe` and no `pyvenv.cfg`.

`run_tool_worker` calls it on its first line (RPR:1242). So every tool stage fails before doing anything: 5a (config-direct), data gate, protocol_execution and regime validation. `run_protocol.py`, `data_availability_gate.py` and `validate_config.py` all need this interpreter, which needs the trading-bot requirements (pandas<3, ccxt, and so on). The suite's register entries already mention "no resolvable trading-bot venv in this build environment".

### 3.3 Startup and configuration failures

- **Flag misconfiguration.** Pre-flight catches the specialist_readers / regroup_record / pbe / vrr chain before spend (status `failed`). `decide_next` and vrr are also checked each `process_once`. `variant_loop` without config-direct, `composition_runs` without its four requirements, and anti-adjacency without regroup_record with no memory all raise **only after 1a (or after 1a/1b/2)**. Within the target set none of these fire.
- **The first brief must be authored for the new pipeline.**
  - Without `machine_constraints` there is no `pre_registration.yaml`, and the readers pre-flight fails (RPR:2900-2903).
  - Without a menu-shaped `evaluation.pass_rule` **or** a brief-level `criteria_from: hypothesis_generation`, the pre-flight fails: "pass_rule is not menu-shaped" (RPR:2904-2908).
  - For an operator brief with an explicit `pass_rule`, the criteria 1a writes into the card (IMPROVEMENT 07) are **ignored**, because `_write_pass_rule_from_card` returns False (RPR:5682-5683). Only candidate / reframe briefs take criteria from 1a.
- **D-3 `promotion_unratified`** (`tools/protocol_resolution.py:77-105`; RPR copy at :7564). Measured: **8 of the 13 `protocols/*.json` carry the generic promotion block with no `ratified_by`**: baseline_v1, baseline_v2, escalation_avaxusdt_4h, escalation_solusdt_4h, escalation_tf_15m, run_048/050/053_generated. The safe ones are diagnostic_btceth_4h, funding_mr_4h_retest_v1, funding_mr_daily_retest_v1, h041c_v2_backext and ts_trend_daily_v1.
  - A brief pinning any of the 8 passes materialization, because the K3 lint does not check promotion. It then raises at the first `_resolve_protocol_path`: the 5a repeat gate (RPR:6588) or the data gate (RPR:1292). That is after 1a, 1b and 2 are spent; `status` becomes `failed`.
  - A generated protocol (`machine_constraints.protocol`) must carry a **non-generic** `promotion` block (G7, RPR:7579). This legacy knob feeds only `run_protocol.py`'s top-level verdict, which the grid never reads.
  - decide_next candidates copy the source run's `machine_constraints`, so they inherit whichever of these it had.
- **Losing one variant stops the campaign.** The data-gate route needs at least 3 validated variants when there are no repeats (RPR:12319). The innovation-expansion SKILL asks for exactly base + design + asset.
  - If one variant fails `validate_config.py` on a non-V12 code, fails patch application, or gets a data refine or error, 2 remain.
  - `_variant_park_kind` (RPR:4086-4117) then returns None, and the run pauses with `variant_gate_insufficient`. That label is misleading when the cause is a config violation, and `process_once` returns False.
  - **(inference on how often this happens; the mechanism was read)**
- **Regime detector report is stale.** `regime_detector_report.yaml` says `evaluated_at: 2026-08-28T19:54`. That is 30 days before today, and freshness needs `age.days < 30` (RPR:7078). So the first run's protocol_execution runs `validate_regime_detector.py` (RPR:2885, RPR:7089). If it fails, the reports block records an error and the stage fails **after** the trial rows are written (RPR:1703-1725).

### 3.4 Silent degradation / fallback to legacy

- **Category reports see only the base variant, and lose trade and bar data under the variant loop.**
  - Variant backtests write to `RUN_DIR/variants/<vid>/` (RPR:1512-1520; `run_protocol.py:2038, 2207` write `results/` and `trade_diagnostics.json` under `--out-dir`).
  - `build_reports.load_run_sources` reads `RUN_DIR/trade_diagnostics.json` and `RUN_DIR/results/<window>/bars.csv` (tools/build_reports.py:201-215), plus the singular base-copy `protocol_result.yaml`.
  - So trade_efficiency's trade-level slice, regime_power's bar slices and component_attribution come out "unavailable" without any error. The five readers reason from base-only, partly empty reports while the grid covers every variant. **(inference on report content; paths measured by reading)**
- **Legacy machinery still runs every backtest:**
  - C7 `pass_rule_evaluation.yaml` on the base variant (RPR:1640-1655);
  - `run_protocol.py`'s promotion-block verdict (`verdict: kill|...`);
  - `evaluate_against_decision_rules`.

  Nothing on the new route reads them (checked: `campaign_memory`, `grid_kb_writer`, `block_registry` and `decide_next` do not read the top-level verdict).
- **Retired paths still reachable.** Validation and verdict_interpreter are unreached, with a guard at RPR:11996. `_dispatch_verdict_route` raises under vrr. `holdout_evaluation` without an unlock pauses (RPR:11927-11934). A legacy campaign review pauses before its LLM call (RPR:11948-11961). A legacy continuation or `refinement_brief` halts before `run_loop` (RC:2573-2583, 2675-2684). I did not find an unguarded legacy route.
- **`variant_patches.yaml` is not a checked deliverable of stage 2.** The template's deliverables are the two legacy files. An omission surfaces only at 5a as a raise (RPR:1991-1996), with no YAML-style retry.

### 3.5 Closed-book stage agents (CUL-336, pending)

`ClaudeAgentOptions(model=..., allowed_tools=[])` is used at RPR:989 and RPR:3097, with no `tools=[]` and no `setting_sources`. SESSION_LOG.md:54 records these as not closed-book: default CLI tools, and local settings allow Read across the repo including `holdout_sealed`. The fix is on another branch and is treated as pending here. Until it lands, every one of the 8+ stage-agent calls per run can in principle read files outside its handoff.

### 3.6 Keys, environment and data

| need | where | notes |
|---|---|---|
| Anthropic | `claude_agent_sdk.query` (RPR:56, 987, 3096); SDK 0.2.82 installed | The SDK drives the Claude Code CLI, which needs CLI auth or `ANTHROPIC_API_KEY` (**inference**; nothing in the repo reads that variable) |
| Gemini | `google.genai` is imported at module top (RPR:57-58), so the package must be installed | `genai.Client()` is **lazy** (RPR:1073-1083). No template assigns `gemini`, so no key is needed under this flag set |
| Exchange | `data_availability_gate.py` / `run_protocol.py` via trading-bot `DataManager` / ccxt | Public OHLCV and funding: network only when a cache is missing (**inference**: no keys on the backtest path) |
| Env vars read by code | `WORKFLOW_ARTIFACT_VALIDATION`, `WORKFLOW_ARTIFACT_VALIDATION_QUIET` (tools/workflow_artifact_validation.py:47-51) | optional |
| Shell | `PYTHONUTF8=1` (RUNBOOK:21-24); CWD = `strategy-research/` (RC:3679) | |
| Caches present | `trading-bot/local_data/`: BTC/ETH 1h, 1d, funding_8h; BTC 4h, 1m; AVAX 1h/4h/funding; fear_greed_daily; kraken_* 1h/1d | No ETH 4h. A 4h protocol on ETH needs a fetch, or the gate declines / parks |
| Campaign files | `campaign_record/campaign_memory.yaml` and `block_registry.yaml` **do not exist yet** | Fine with regroup_record on: fresh memory. With it off, the anti-adjacency gate raises |

### 3.7 Trial accounting under this set

- Each variant backtest writes `trial_id = "<run>:<variant>"` (RPR:1575). Every failure branch records `backtest_failed` (RPR:1497-1589). A conformance violation invalidates only that variant's row (RPR:12452-12457). The regroup stage writes none.
- **Not counted, by design:**
  - variants skipped before a backtest (repeat, 5a validation, data gate);
  - the regime-detector validation run;
  - the composite used for residual IC (register: "not a trial").
- **Wasted but counted:** Finding 3's scenario, where all windows run and then the tool crashes. N goes up with no usable result.
- The dual-writer merge is enforced only at holdout spend (`trial_ledgers_merged` attestation). Before that, DSR in profit bars / R1 is computed on the local ledger alone.

### 3.8 Cost per run

| stage | model | calls (min / max) |
|---|---|---|
| 1a | claude-haiku-4-5 | 1 / 4 (YAML retry × SDK retry) |
| 1b | haiku | 1 / ~6 (+1 manifest resend) |
| 2 | haiku | 1 / 4 |
| readers | haiku | 5 / 10 |
| campaign_review | haiku | 1 per 6 recorded runs |
| 5a, data gate, protocol_execution, regroup, decide | code | 0 (subprocesses: 3× `validate_config`, 3× data gate, 3× `run_protocol`, optional detector validation, residual IC) |

- A forecast-block run is at least 8 Claude calls; a composition run is 5 (readers only).
- There is one breaker: 1.5M weighted units per run (`campaign_config.yaml:92`). It is checked at the top of each stage and before each reader.
- Every stage uses `_CLAUDE_WORKER_MODEL = "claude-haiku-4-5"` (RPR:944), including all five readers.

---

## 4. Stale docs

1. `SR/config/requirements-mac.txt:13-20` and `CLAUDE.fork.md` ("importing `run_phase1_research` additionally needs the Gemini key env var") say `genai.Client()` is built at import time. The code is lazy (RPR:1073-1083).
2. `SR/config/campaign_config.yaml:330-339` (grid_evaluation) says idea_status "is NOT yet wired into any `_resolve_verdict_fields` call site". `SR/docs/USER_GUIDE.md:883` says it is "NOT yet read by any routing call site". Both are stale: `_load_idea_status` / `determine_post_specialist_readers_route` route on it (RPR:2977, 3275-3333).
3. `feature_flag_register.yaml:274` (variant_loop `blocked_on: E-033.1 slice 4b ... none of which this sub-slice builds`) and `campaign_config.yaml:544-548` are stale. Slice 4b is built: the per-variant data gate (RPR:1262), per-variant conformance (RPR:12411), and `test_e033_slice4b_gate_conformance_promotion.py` exists.
4. `campaign_config.yaml:462-465` and `feature_flag_register.yaml:236-239` say "refine → variant not tested ... deferred to a later slice that does not exist yet". Under variant_loop, a refine marks the variant not_tested (RPR:1357-1374).
5. `campaign_config.yaml:102-105` names backtest_specification and verdict_interpreter as the remaining LLM stages. Under the new set they are 1b and five readers.
6. `SR/docs/RUNBOOK.md:19` (and every command line after it) uses `../venv/Scripts/python.exe`, which is absent on this checkout (measured). `RUNBOOK.md:127` says "the prescreen finds no protocol_ref"; the prescreen was removed (E-039 step 5).
7. `SR/docs/USER_GUIDE.md:869`: protocol_execution input `validation_protocol.yaml` "stage 4 | yes" has no config-direct caveat. That missing caveat is Finding 1/3. `USER_GUIDE.md:884` puts `trade_diagnostics.json` in `artifacts/`, but `run_protocol.py:2207` writes it to `--out-dir` (the run dir, or `variants/<id>`).
8. Templates:
   - `hypothesis_to_innovation_expansion.yaml` has a duplicated `required_inputs` key (the last one wins);
   - its deliverables omit `variant_patches.yaml`;
   - `research_brief_to_hypothesis.yaml` ("before the prescreen runs") and `validation_to_backtest_specification.yaml` do not know about config-direct.
9. `SR/CLAUDE.md` says that when config-direct is on, "backtest_specification becomes a deterministic tool stage". That is true of the worker, but the stage still loads the LLM-era handoff with LLM-era required inputs (Finding 1).

---

## 5. Existing end-to-end tests

**No test runs the target pipeline end to end with real handoffs.** The closest is `tests/test_e060_s3b_composition_wiring.py::test_end_to_end_registry_change_to_graded_composite` (lines 920-1107). It passed here in 150 s, but:
- it runs a **composition** run: 1a/1b/2 are code, so there is no stubbed-LLM forecast path;
- it uses `FLAT_COMP_ON` with **`data_availability_gate: False`** and **no `variant_anti_adjacency_gate`** (lines 66-68);
- it **replaces `setup_run`** with a scaffold whose handoffs have `required_inputs: []` (lines 997-1003). That hides Findings 1-3;
- it stubs `subprocess.run` (fake `run_protocol` / `validate_config`), `_run_specialist_readers_stage`, `build_reports` and the regime refresh.

Other tests drive a single stage via `_minimal_run_at` plus `_write_handoff` scaffolds (test_e033_slice4b, test_e036_s2a:752-770, test_e059_6c_s2c).

**What a stubbed end-to-end wiring test needs (Phase B):**
1. **Sandbox:** the conftest's autouse ROOT redirect, plus `setup_run.ROOT` pointed at the sandbox, **with the real `TEMPLATES_DIR`**. Do not stub `setup_run`; the templates are what is under test.
2. **Config:** the §1 flag set written to `<root>/config/campaign_config.yaml`. Copy the real `criterion_menu.yaml`, `profitability_bars.yaml`, `available_feeds.yaml`, `indicator_library.yaml`, `cost_model.yaml`, `venue_tradability.yaml` and `campaign_data_policy.yaml` (for the holdout range), and `docs/STRATEGY_DESIGN_GUIDE.md` for the 1b handoff path.
3. **Protocol:** one small ratified or non-generic protocol JSON in `<root>/protocols/` (2 symbols, 5 or more windows so the menu floors can pass), pinned via `machine_constraints.protocol_ref`.
4. **Brief:** an operator brief with `brief_status: open` via `register`, `machine_constraints.protocol_ref`, and `criteria_from: hypothesis_generation` (or a menu-shaped `evaluation.pass_rule`).
5. **LLM stub at `run_claude_worker`** (and `_invoke_reader_llm`), keyed on stage. It writes:
   - 1a: a card with menu `criteria` ids;
   - 1b: `backtest_spec.yaml` (spec_ready + a real `validate_config`-clean config) + `decision.yaml` + `block_manifest.yaml`;
   - 2: the two legacy files + a 3-variant `variant_patches.yaml`;
   - readers: one valid proposal in one category, `[]` elsewhere.

   Assert that no gemini call happens.
6. **Subprocess stub:**
   - `validate_config.py` → 0;
   - `data_availability_gate.py` → write `data_availability_gate.yaml` outcome validate, exit 0;
   - `run_protocol.py` → `protocol_summary.json` + `results/<w>/portfolio_states.csv` + `bars.csv` + `trade_diagnostics.json` under `--out-dir` (reuse `_fake_subprocess`, test_e060 lines 892-917, extended with bars and trades);
   - `validate_regime_detector.py` → a fresh report.

   Patch `_resolve_tbot_python`. **Also assert on the argv:** there must be no `--validation-protocol` pointing at a missing file.
7. **Drive it** with `camp.process_once()` twice: run 1 (launch → `completed_<status>` → decide_next mints the reader candidate), then run 2 (the candidate: 1a criteria rebuilt, the pass-through config hash is checked at 5a, and the exact-match gate sees run 1 in memory).
8. **Assert:**
   - no uncaught exception and `last_error is None`;
   - 3 trial rows `run:variant` per run;
   - `grid_evaluation` / `idea_status` / `reports` / `proposals` / `profit_bars_evaluation` / `campaign_memory` / `block_registry` (on validated) / `decision_record` exist;
   - reports carry non-"unavailable" trade and bar slices (catches §3.4);
   - the queue entries' final statuses.
9. **Variants of the test:**
   - the profit-bars PASS path → `profit_bars_reached` pause → `holdout_decision.yaml` continue → resume → `completed_*`;
   - one variant failing `validate_config` (pins Finding 6's behaviour);
   - a protocol with the generic promotion (the D-3 raise before 5a spend).

---

## Top findings

Ranked: breaks_run first, then breaks_vision, gap, tidy.

1. **breaks_run**: 5a loads the legacy handoff `templates/handoffs/validation_to_backtest_specification.yaml:13`, which requires `validation_protocol.yaml`, and no stage writes that file under config-direct. `ensure_files` (RPR:11968, outside the try) raises. **Every forecast-block run dies at 5a after 1a/1b/2 are spent (measured in the repro).**
2. **breaks_run**: the `backtest_spec_to_data_availability_gate.yaml` handoff is written only by `_create_remaining_handoffs`, which is called only on the legacy branch (RPR:12270), and it is not a template. `load_yaml` (RPR:11966) raises. **Even with 1 fixed, every run dies entering the data gate (measured).**
3. **breaks_run**: protocol_execution's template (`backtest_spec_to_protocol_execution.yaml:13`) requires `validation_protocol.yaml`, and `run_tool_worker` always passes `--validation-protocol` (RPR:1479/1519), which `run_protocol.py:2289-2291` opens only after the backtests. **Even with 1 and 2 fixed, every variant would spend its data and then fail (the ensure_files half was measured; the post-backtest crash is an inference from reading).**
4. **breaks_run**: no trading-bot interpreter exists at `../venv/Scripts/python.exe` or `../.venv/bin/python` on this checkout. `_resolve_tbot_python` (RPR:101-122, called at RPR:1242) raises. **Every tool stage and backtest fails on this machine (measured).**
5. **breaks_run**: those exceptions escape `run_loop` and `process_once` (RC:2696, RC:3536 have no try). **The campaign process crashes with no classified halt or halt_history; `status` stays `active`, and every restart re-crashes at the same stage.**
6. **breaks_run** (inference on frequency): the variant loop requires at least 3 validated variants after the data gate (RPR:12319), but stage 2 emits exactly 3. **One `validate_config` violation, patch failure or data refine pauses the whole campaign with the misleading `variant_gate_insufficient` (RPR:12342-12351).**
7. **breaks_run** (operator setup): the queue has no ready entry, and legacy briefs never trigger R2. 8 of 13 `protocols/*.json` carry the unratified generic promotion block, and D-3 (`tools/protocol_resolution.py:96`) raises on first resolution, after 3 LLM stages. **The first run needs a newly registered brief with `machine_constraints`, a safe protocol pin, and a menu-shaped pass_rule or `criteria_from` (RPR:2904).**
8. **breaks_vision**: under the variant loop, `build_reports` reads `RUN_DIR/trade_diagnostics.json` and `RUN_DIR/results/*/bars.csv` (tools/build_reports.py:201-215), while variant backtests write to `RUN_DIR/variants/<id>/` (RPR:1512-1520). **The readers get base-only reports whose trade and bar slices are silently "unavailable".**
9. **breaks_vision**: stage agents are not closed-book yet (RPR:989, RPR:3097: `allowed_tools=[]` only; CUL-336 pending). **Every stage agent, and in principle the eight or more per run, can read repo files, including `holdout_sealed`, until that fix lands.**
10. **gap**: bar ratification (`profitability_bars.yaml` `ratified_by: null`) and the `residual_ic` placeholder (`ratified: false`) are recorded but never enforced (RPR:2393, RPR:10505). **A PASS against placeholder bars raises the real `profit_bars_reached` holdout stop.**
11. **gap**: the `variant_loop` and `composition_runs` dependencies, and anti-adjacency's regroup_record check, are enforced lazily, after LLM spend (RPR:2762, 3547, 6580). Seven flag readers use plain `bool()`, so a quoted `"false"` turns a flag ON. **A config slip costs a partial run instead of failing at start.**
12. **gap / tidy**: the only near-end-to-end test (test_e060_s3b:920-1107) swaps `setup_run` for empty-input handoffs and turns the data gate off, so Findings 1-3 are untested. Several docs are stale: the Gemini-key claim, "idea_status not read", variant_loop blocked on 4b, and the RUNBOOK python path (§4). **The suite is green while the real path is broken.**
