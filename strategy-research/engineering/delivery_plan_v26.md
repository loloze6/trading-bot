# Delivery plan — from today's code to roadmap v27

**Status:** draft, reviewed once by the operator (2026-09-19/20); four corrections applied
(composition is its own new epic, not E-044; no E-048 gate on composition; `verdict_interpreter`
is deleted, not kept as a narrator; a block is usable on any coin once validated anywhere).
Nothing in Linear has been changed yet. Companion documents: `engineering_roadmap.html` (v27,
the target — cards A–N and the 14-step walkthrough) and `roadmap_review_2026-09-18.md` (the
code-verified findings and the decisions record). The board is the source of truth for *what*;
this file is the source of truth for *in which order, touching which code, proven how*.

Written for implementation agents. Every seam names a file and a function; line numbers are
approximate (measured 2026-09-16 on branch `fix/cul-275-mark-close-positions-tests-slow`) and
must be re-grepped before editing.

---

## 0. Rules every slice obeys

1. **Two-phase.** Every slice that touches more than one function starts with a
   *characterize-and-STOP* dispatch (S1): file:line evidence, the exact artifacts read and
   written today, what changes, what breaks. The operator nods, then the build dispatch (S2)
   runs. S1 findings go to `engineering/roadmap/<EPIC>/S1_FINDINGS.md` and a paste-ready
   section for the Linear project.
2. **Off by default, bit-identical when off.** New behaviour ships behind
   `orchestrator.<name>.enabled` in `config/campaign_config.yaml`, read by a matching
   `run_phase1_research._<name>_enabled()` / `run_campaign._<name>_enabled()`, registered in
   `config/feature_flag_register.yaml` (test-enforced by `tests/test_feature_flag_register.py`).
   Each flag ships with a flag-off byte-identity test on the artifacts it could touch (pattern:
   `tests/test_e030_s4_bit_identity_and_replay.py`, `tests/test_exclusion_digest_input.py`).
   Two slices are **declared behaviour changes** that cannot be bit-identical once switched on
   (slice 3: config written at 1b; slice 6c: verdict routing retired). They still ship off by
   default; switching them on is an operator decision recorded in the flag register with a
   before/after artifact diff.
3. **Run budget.** Each slice names the real hypothesis runs that ship with it. "Real" means a
   full `protocol_execution` on market data, recorded in `campaign_state.trial_sharpes`. No
   run ever opens `local_data/holdout_sealed/`.
4. **Legacy is legacy.** The 60 existing run directories and the 15 existing trial rows are
   never rewritten. New artifacts are additive. Old verdicts get a `legacy: true` marker where
   a new reader could otherwise mistake them for new-design verdicts.
5. **Measurement channel.** Counts quoted in findings name the shell and the command (Git Bash
   for grep/python on this Windows machine).
6. **Dispatch header.** Every dispatch states NEW AGENT or CONTINUE <agent>, the slice and
   phase, the read-only or write scope, and "never open the holdout."
7. **Docs move with code.** A slice is not done until `docs/USER_GUIDE.md` §2.1/§2.2, the
   stage list in `strategy-research/CLAUDE.md`, `docs/RUNBOOK.md` and `DOC_INDEX.md` (strategy-research root) say
   what the code now does. `tests/test_guide_covers_the_code.py` and
   `tests/test_doc_anchors.py` exist for this.

---

## 1. Where each target step lives in today's code

| Target step (v26) | Today's seam | What changes (slice) |
|---|---|---|
| 0 · idea intake | `run_campaign.py::_materialize_run` (≈L288), `register_hypothesis` (≈L381); `run_phase1_research.py::_handle_hypothesis_generation_multi_card_split` (≈L3611) | multi-hypothesis briefs to the queue, brief status (6b) |
| 1a · hypothesis + criteria | stage `hypothesis_generation`, skill `hypothesis-design/SKILL.md`; pass rule copied by `run_campaign.py` ≈L304-324 / ≈L484 | criteria from the menu at 1a; pass-through (3) |
| 1b · config + manifest | stage `backtest_specification`, skill `backtest-engineering/SKILL.md` → `backtest_spec.yaml.config` → `candidate_strategy_config.json` (run_loop ≈L6050-6080) | config written at 1b under the design guide (3) |
| 2 · variants as patches | stage `innovation_expansion`, skill `innovation-expansion/SKILL.md`; `_record_variant_selection` (≈L1828) | patches; three variants (3, 4) |
| 3 · data per variant | `data_availability_gate` stage, `_E054_GATE_ENABLED` (≈L98), `tools/data_availability_gate.py` | on by default, per variant, park not pause (0, 4) |
| 4 · exact-match repeat | `tools/anti_adjacency_gate.py`, `tools/build_exclusion_digest.py`, `_route_post_variant_selection` (≈L1974), both flags off | hash match (8) |
| 5a · validate + assemble | run_loop `backtest_specification` branch: `validate_config.py` subprocess (≈L6060) | patch application, component-existence check, manifest check (3) |
| 5b · protocol windows | `run_tool_worker` `protocol_execution` (≈L1168-1260) → `tools/run_protocol.py`; `_ensure_protocol_from_constraints` (≈L2803) | loop over variants (4) |
| 6 · the grid | `tools/verdict_criteria_evaluator.py::evaluate_pass_rule_criteria` (≈L725), `_evaluate_one_criterion` (≈L217), `_lookup_metric_value` (≈L188); written at ≈L1256 as `pass_rule_evaluation.yaml` | reducers, pooled family, floors, unanimity (2) |
| 7 · reports + readers | stage `verdict_interpreter`, skill `verdict-interpreter/SKILL.md`; `_inject_regime_context_into_handoff` (≈L2490) | five reports (code) + five readers (5) |
| 8 · profit bars | `_write_promotion_audit` (≈L4771), per-protocol `promotion` blocks, `protocol_resolution.assert_promotion_ratified` | one file, every backtest, stop rule (0) |
| 9 · regroup + record | `_write_kb_findings_entry` (≈L4321), `_auto_generate_findings_carryover` (≈L4474), `_record_backtest_trial` (≈L4070), `tools/near_miss_scoreboard.py` (unwired) | one stage (6a) |
| 10 · decide next | `determine_post_verdict_route` (≈L5470), `_dispatch_verdict_route` (≈L5411), `_route_refine/_pivot/_escalate/_kill` (≈L3769-3995), `_should_trigger_campaign_review` (≈L4665), `determine_post_campaign_review_route` (≈L5634) | decide-next step, routing retired (6b, 6c) |
| 11 · queue | `run_campaign.py::_select_entry` (≈L152), `process_once` (≈L2042), `_LINEAGE_CONTINUATION_STAGES` (≈L102), `tools/record_schema.py::QUEUE_ENTRY_SCHEMA` (≈L195), `_QUEUE_STATUS_RE` (≈L107) | E-031 S3 (6b) |
| 12 · holdout | `_route_holdout_evaluation` (≈L5054) | reads the profit-bars file (0) |
| composition | nothing | slice 7 |
| runbook | `docs/RUNBOOK.md` §3 (hard pauses) §4 (resume); `run_campaign.py::_classify_human_pause` (≈L831), `resume_paused_entry` (≈L1322) | new rows and states (6c) |

---

## 2. The slices, in order

Dependencies are stated per slice. Slices 0, 1 and the report half of 5 can start now, in
parallel. The order below is the recommended one when work is serial.

### Slice 0 — Independent guards and files (ship now)

Four small, independent pieces. Each is its own dispatch. Run budget total: 2.

**0.1 CUL-267 — fail loud on an unmatchable or non-scale-free criterion.**
- Seam: `tools/verdict_criteria_evaluator.py::_evaluate_one_criterion` returns `SPEC_ERROR`
  today when a metric resolves to nothing (≈L217-296); `run_campaign.py::_materialize_run`
  lints the pass rule at registration via `orch._lint_pass_rule_total_mapping` (≈L348) and
  `_lint_machine_constraints_protocol_selection` (≈L361).
- Build: a registration-time lint that refuses a criterion whose `metric` is not in the
  evaluator's resolvable set (today: `per_symbol_summary` keys and
  `trade_diagnostics_summary` / `hypothesis_verdict.diagnostics` keys — enumerate them from
  a real `protocol_result.yaml`, e.g. `runs/run_059/artifacts/protocol_result.yaml`), or whose
  comparator is not in `_VALID_COMPARATORS`, or that lacks `null_handling`. Refuse at
  `_materialize_run` and `_materialize_refinement_run`, not at evaluation time. Once slice 2
  lands, extend the same lint to the menu's `scale_free: true` rule.
- Correction to the ticket text: the keyword matcher in `tools/run_protocol.py` (≈L639-659)
  is informational only since July; do not fix it, note it as legacy.
- Tests: new `tests/test_cul267_criterion_lint.py` (refuses the three cases; admits run_058's
  real dict-shaped rule). Flag: none needed — a lint that fires only on newly registered
  briefs cannot change any existing artifact; state that in the dispatch.
- Run budget: 0.

**0.2 Item 2 — `config/profitability_bars.yaml` and the branch-3 stop.**
- New file, hand-written by the operator, schema-checked by a small loader:
  `sharpe_min`, `max_drawdown_pct_max`, `avg_daily_return_min`, `trade_count_min`,
  `deflated_sharpe_threshold` (today hard-coded `DSR_THRESHOLD = 0.95` in
  `_write_promotion_audit`), `target_instrument_set` (list of symbols, or a universe name),
  `ratified_by`, `ratified_at`.
- Seam: `_write_promotion_audit` (≈L4771) reads the candidate's numbers from
  `protocol_result.yaml`; extend it to evaluate every bar from the file and write
  `artifacts/profit_bars_evaluation.yaml` (`{bars: [...], result: PASS|FAIL, reasons}`).
  `_route_holdout_evaluation` (≈L5054) step 1 reads `passes_deflated_threshold`; make it read
  the file's threshold. `protocol_resolution.assert_promotion_ratified` and the per-protocol
  `promotion` blocks stay in place until slice 6c retires routing; add a one-line note there.
- The stop: when `profit_bars_evaluation.result == PASS`, write
  `pipeline_state.flags.profit_bars_reached = true`, set `status: paused_for_human`, and add a
  new branch in `run_campaign.py::_classify_human_pause` (≈L831) returning
  `profit_bars_reached` with a RUNBOOK §3 row (what to read: the run's grid and reports; what
  to decide: spend the holdout or continue; what to update: `holdout_result.yaml`,
  `campaign_data_policy.yaml.holdout_consumed_by`; resume: `--resume`, re-enters the
  decide-next step once slice 6b exists, the verdict route until then).
- Flag: `orchestrator.profit_bars_file.enabled` (off: nothing read, nothing written).
- Tests: loader validation; evaluation on run_058/run_059 artifacts; flag-off byte-identity
  on `promotion_audit.yaml`; the pause classification row.
- Run budget: 0.

**0.3 Item 3 — cost-survival criterion from the trade records.**
- Seam: `tools/run_protocol.py::_aggregate_trade_diagnostics` (≈L514) already computes
  per-trade cost (`cost_paid`, A3.2) and gross P&L per trade; `hypothesis_verdict.diagnostics`
  carries `per_trade_expectancy_bps` `{mean, se, t_stat, n}` and `median_cost_drag_pct`.
- Build: add `edge_to_cost_ratio` = mean gross edge per trade (bps) / mean round-trip cost per
  trade (bps), and `survives_cost_multiple` = that ratio (so "survives 2× costs" is
  `edge_to_cost_ratio >= 2`), into `trade_diagnostics_summary` so the evaluator's existing
  pooled lookup (`_lookup_metric_value`, ≈L188) can address it with no evaluator change.
  Record the cost components present (fees, funding, slippage) in a `cost_basis` field so the
  criterion's evidence says what it includes. E-053 (sub-daily funding) is open: note it in
  `cost_basis.caveats`.
- Tests: `tests/test_cost_survival_criterion.py` on a fixture of trades; the new fields are
  additive → byte-identity of every existing field in `protocol_result.yaml`.
- Run budget: 1 legacy run re-read (no re-run needed: read `trades` under
  `runs/run_059/results/` and compare the ratio with its recorded `median_cost_drag_pct`).

**0.4 Item 14 — E-054 on by default, registered, per variant, park not pause.**
- Seam: `run_phase1_research.py` ≈L98 (`_E054_GATE_ENABLED` env var), run_loop routing
  ≈L6085 (`if _E054_GATE_ENABLED: next_stage = "data_availability_gate"`), the
  `data_availability_gate` branch ≈L6095-6125 (`refine` → `paused_for_human`).
- Build: replace the env var by `orchestrator.data_availability_gate.enabled` (default
  **true** — this is the one flag that ships on, and the register entry must say why:
  E-054 is complete and the brief requires the control); register it. Change the `refine`
  outcome from a loop pause to "variant not tested" once slice 4 exists; until then keep the
  pause but add the RUNBOOK row. Per-variant looping is slice 4's job; this slice only makes
  the gate run.
- Tests: extend `tests/test_e054_stage_wiring.py` for the config flag; flag-off byte-identity.
- Run budget: 1 real run with the gate on (any brief).

### Slice 1 — Characterize the two foundations (read-only, parallel)

**1.1 E-056 S1** — dispatch brief already drafted (2026-09-17 reply), amended for card K:
- Task 3 becomes: on the 39 runs carrying both `hypothesis_card.yaml` and
  `candidate_strategy_config.json`, list every config field whose value has no source in the
  card or the expanded card — this is the scaffolding an LLM adds, which the design guide must
  constrain (denominator stated).
- Task 4 adds: list every criterion *type* found across the 10 `pre_registration.yaml`
  files and the 38 `verdict_interpretation.yaml` criteria summaries (metric, comparator,
  threshold, scale-free yes/no) — the raw material for the menu.
- New task: inventory `trading-bot/DOC/STRATEGY_CONFIG_REFERENCE.md` and
  `docs/WORKFLOW_CAPABILITIES.md` as the seed of the design guide; list what they lack for an
  LLM to write a complete config unaided (component class list vs
  `strategies/strategy_components.py`, transform ops vs `strategies/registry.py`, regime rule
  syntax, allocation settings, "none" assignment).
- New task: the pass-through rule — what a candidate must carry (config, manifest, criteria,
  source) for 1a/1b to skip authoring; where `research_brief.yaml` would carry it.
- Output: `engineering/roadmap/E-056/S1_FINDINGS.md`. STOP.

**1.2 E-046b S1** — the criterion syntax and the menu v1:
- Read `tools/verdict_criteria_evaluator.py` end to end; `tools/run_protocol.py` per-window
  `core` keys (14, measured on run_059) and `per_symbol_summary` keys (4); the pooled
  diagnostics; `campaign_data_policy.yaml.eras`.
- Propose the criterion record: `{id, metric, source: window|pooled, reducer: median|mean|min|
  max|fraction_above|sign_consistent_by_era, reducer_arg, comparator, threshold, floor:
  {min_windows|min_trades|min_n_eff}, scale_free: true, symbol_reducer: null|per_symbol_all|
  pooled}`; how it evaluates per variant; the grid record
  (`grid_evaluation.yaml`: rows criteria, columns variants, cell PASS|FAIL|INCONCLUSIVE, idea
  status by unanimity).
- Propose `config/criterion_menu.yaml` v1 with anchored thresholds per signal class, seeded
  from the A8.6 plausible-IC table in `hypothesis-design/SKILL.md` and the corpus survey of
  1.1 task 4; include `edge_to_cost_ratio` (0.3), `residual_ic` (slice 7), `gated_beats_ungated`
  (slice 7), `sign_consistent_by_era`.
- Output: `engineering/roadmap/E-046b/S1_FINDINGS.md`. STOP.

Run budget: 0. Both are read-only.

### Slice 2 — The grid (E-046b S2)

Depends on 1.2 and 0.1. Buildable before variants exist: a grid with one column is still a
grid, and the same code later takes three.

- Seam: `tools/verdict_criteria_evaluator.py`. Add `evaluate_grid(protocol_results_by_variant,
  pre_registration, research_brief, menu)` beside the existing
  `evaluate_pass_rule_criteria` (keep the old function untouched for legacy runs). Reducers
  read `protocol_result.results[*].core[metric]` per window; pooled metrics read the existing
  `trade_diagnostics_summary` / `hypothesis_verdict.diagnostics` path; era tagging reuses
  `run_protocol.py::_era_id_for_timestamp` (≈L855) via the window label.
- Writer: `run_tool_worker` `protocol_execution` branch (≈L1235-1258) writes
  `artifacts/grid_evaluation.yaml` next to `pass_rule_evaluation.yaml` when the flag is on and
  the pass rule is menu-shaped; writes `artifacts/idea_status.yaml`
  (`validated | refuted | inconclusive`, with the failing or under-floor cells listed).
- Routing: until slice 6c, map `validated → promote`, `refuted → kill/terminate`,
  `inconclusive → human_pause (reason: inconclusive_grid)` through the existing
  `_resolve_verdict_fields` binding path so nothing else changes.
- Registration: `_lint_pass_rule_total_mapping` learns the menu shape; 0.1's lint enforces
  `scale_free` and floors.
- Flag: `orchestrator.grid_evaluation.enabled`. Off: `grid_evaluation.yaml` never written,
  `pass_rule_evaluation.yaml` byte-identical.
- Tests: `tests/test_grid_evaluation.py` — each reducer on a synthetic per-window table;
  floor → INCONCLUSIVE; unanimity across two synthetic variants; flag-off identity on
  run_058/run_059 fixtures.
- Docs: USER_GUIDE stage 8/11 blocks; `verdict-interpreter/SKILL.md` gains
  `grid_evaluation.yaml` as a required input when present (this skill is deleted in slice 5b
  once the flag there is on — until then it stays the flag-off path's own reader).
- Run budget: re-grade 3 legacy runs (run_054, run_058, run_059) through the grid and publish
  the comparison with their recorded verdicts — calibration, history unchanged.

### Slice 3 — Config written at 1b, patches, mechanical 5a (E-056 S2 + E-057)

Depends on 1.1 and, for criteria, on 1.2's menu. **Declared behaviour change when on.**

- Design guide: new `docs/STRATEGY_DESIGN_GUIDE.md` (or a rewrite of
  `trading-bot/DOC/STRATEGY_CONFIG_REFERENCE.md` — 1.1 decides), covering: regimes and the
  detector rule syntax, sub-strategies as weighted component lists, every component class and
  its params (generated from `strategies/strategy_components.py`, kept in sync by a test),
  transform ops (`strategies/registry.py`), allocation settings, the instrument-set field,
  the "none" assignment, and the manifest contract.
- Skills: `hypothesis-design/SKILL.md` → 1a (hypothesis, criteria from
  `config/criterion_menu.yaml`, pass-through rule, the two design-guide checks that used to
  live in the validation stage — mechanism purity, daily-feed timing — as rules, not a stage);
  a new `strategy-config-authoring/SKILL.md` → 1b (writes `artifacts/strategy_config.json`,
  `artifacts/block_manifest.yaml` `{block: {kind: forecast|regime, config_paths: [...]},
  scaffolding: [...], rationale}`); `innovation-expansion/SKILL.md` → Step 2 (writes
  `artifacts/variant_patches.yaml`: base + design patch + asset patch, each `{variant_id,
  patch: [{path, value}], rationale}`); `backtest-engineering/SKILL.md` → retired as an LLM
  stage, its checks move to code.
- Orchestrator: `STAGE_CONFIGS` gains `strategy_config_authoring` (Claude) between
  `hypothesis_generation` and `innovation_expansion`; `backtest_specification` becomes a
  `tool:` stage (no LLM) that: applies each patch to the base config (JSON pointer set),
  runs `trading-bot/tools/validate_config.py` on each, checks every `class` in
  `strategies.regimes.*.components[]` and `regime_detector.components[]` exists (import
  `strategies.strategy_components` and check attribute presence — no new registry needed
  unless 1.1 finds one), checks the manifest paths exist in the config, writes
  `artifacts/variants/<variant_id>/strategy_config.json`, and on a missing component writes
  `campaign_record/component_requests.yaml` (append `{run_id, variant_id, class, description,
  requested_at}`) and marks the variant `not_tested` in `artifacts/variants/index.yaml`.
  The `validation` stage is removed from `STAGE_CONFIGS` and from `determine_post_validation_route`
  callers when the flag is on (card N: deleted; keep the code path only for flag-off runs).
- Variant selection: `_record_variant_selection` / `variants_not_pursued.yaml` (E-034) become
  legacy; under the flag every variant is pursued.
- Flag: `orchestrator.config_direct_authoring.enabled`. Off: stage graph and every artifact
  byte-identical (the new stage is simply not routed to).
- Tests: patch application; component-existence check (positive and negative);
  manifest-path check; flag-off stage-graph identity (`tests/test_e054_stage_wiring.py`
  pattern); `tests/test_design_guide_in_sync.py` (component list vs code).
- Docs: USER_GUIDE §2.1 diagram (stage 4 removed, 1b added), CLAUDE.md stage list,
  `DOC_INDEX.md`.
- Run budget: 1 real idea authored end-to-end (1a → 1b → patches → 5a) and run through
  `protocol_execution` on the base variant only (slice 4 adds the other two).

### Slice 4 — Three variants through the protocol (E-033.1)

Depends on 3 and 2.

- Seam: `run_tool_worker` `protocol_execution` (≈L1168-1260) runs `tools/run_protocol.py`
  once with `candidate_strategy_config.json`. Build: iterate `artifacts/variants/index.yaml`,
  run once per tested variant with `--out-dir RUN_DIR/variants/<variant_id>`, write
  `protocol_result.yaml` per variant, then call slice 2's `evaluate_grid` with all columns.
  Build it as an extension of this loop, not a second loop; `_resolve_protocol_path` is
  called once (same windows for every variant).
- Data gate per variant: `data_availability_gate` runs once per variant config; `refine` →
  variant `not_tested` with a data request appended to
  `campaign_record/data_requests.yaml`; `decline` → same; the run continues if ≥ 3 variants
  remain, else `idea_status: inconclusive` with reason.
- Conformance: `_check_protocol_execution_conformance` (≈L3186) runs per variant.
- Trial accounting: `_record_backtest_trial` (≈L4070) becomes per variant — `trial_id =
  f"{run_id}:{variant_id}"`, `source: backtest`, `forecast_hash` per variant config; the
  idempotency guard keys on `(trial_id, source)` as today. `_record_failed_backtest_trial`
  likewise. `_write_promotion_audit`'s dedup (`_dedupe_trials`, ≈L4733) must accept the new
  id shape. E-025 note: the fork's `run_d_NNN` prefix scheme must accommodate `:variant`.
- Flag: `orchestrator.variant_loop.enabled` (requires `config_direct_authoring`).
- Tests: three-variant fixture run on the cached BTC/ETH data through the real
  `run_protocol.py` (slow marker); three trial rows; grid with three columns; flag-off
  identity.
- Run budget: 1 real idea, three variants, three trial rows.

### Slice 5 — Reports and readers (E-046a)

5a (reports, code) depends on nothing and can start now; 5b (readers) depends on slice 3's
vocabulary.

- 5a: new `tools/build_reports.py` producing `artifacts/reports/{profitability,
  trade_efficiency, forecast_power, regime_power, component_attribution}.yaml`, each
  `category × slice` (`overall`, `per_window`, `per_regime`, `per_symbol`) as a pure
  re-projection of `protocol_result.yaml`, `trade_diagnostics.json`, `bars.csv` and
  `regime_detector_report.yaml` — zero new computation in v1 except the regime-power
  metrics inherited from E-040's decided checks (hindsight-lag comparison with its lookahead
  trap: the hindsight labeller writes only into the report, never a signal; health numbers
  from `tools/validate_regime_detector.py`). Called from the `protocol_execution` branch after
  the grid. Flag: `orchestrator.category_reports.enabled`.
- 5b: five skills `readers/<category>-reader/SKILL.md`, dispatched sequentially (the
  orchestrator has no fan-out; `_invoke_agent_with_yaml_retry` is one call per stage) as one
  stage `specialist_readers` that loops; each reads only its report plus `grid_evaluation.yaml`
  and writes `artifacts/proposals/<category>.yaml`: a list of `{proposal_id, kind: patch|
  new_block, patch or block sketch in design-guide vocabulary, evidence: [numbers cited],
  scores: {confidence_real, distance_to_profitable, mechanism_plausibility} each 0–3 with
  the anchor text, model_id, rubric_version}`. The regime reader carries the retune firewall
  (`_validate_retune_firewall`, ≈L2474, re-pointed at its output). **Corrected 2026-09-20
  (operator decision):** the `verdict_interpreter` stage is **removed from `STAGE_CONFIGS`**
  under this slice's flag, not kept as a narrator — the five readers are the whole
  explanation layer. Every caller of `verdict_interpretation.yaml` must be re-pointed or
  retired: `_inject_regime_context_into_handoff`, `_auto_generate_findings_carryover`,
  `_write_kb_findings_entry`, `_check_kb_reactivation_conformance`, the
  `campaign-review/SKILL.md` required-input list, and `tools/near_miss_scoreboard.py`'s
  schema-diversity reader — enumerate the full caller list in this slice's own
  characterize-and-stop dispatch (it overlaps but is not identical to slice 6c's routing
  callers; do both surveys in the same pass since they touch the same file).
- Tests: report re-projection equals source fields (property test on run_059); proposals
  schema; firewall.
- Run budget: 2 real runs read by all five readers.

### Slice 6 — Closing the loop (items 10, 11, 12)

The largest slice; three sub-slices, each behind its own flag, in this order.

**6a Regroup and record (item 10, new epic).** Depends on 2, 5a.
- New tool stage `regroup_record` after the readers: writes `campaign_record/
  campaign_memory.yaml` (idea status + grid summary + proposals refs per run), appends
  validated blocks to `campaign_record/block_registry.yaml` (`{block_id, kind, config_fragment,
  regime_assignment, criteria_passed, variants_passed, numbers, correlation_to_composite,
  validated_by_run, registered_at}`), calls `tools/near_miss_scoreboard.py::build_scoreboard`
  (finally wiring its documented hook), and appends the trial rows if slice 4 did not.
  Keeps `_write_kb_findings_entry` writing the legacy KB in parallel (legacy readers still
  need it) with `legacy_schema: false` on new entries.
- `campaign-review/SKILL.md` gains the new memory file as a required input and cites its
  fields.
- Flag: `orchestrator.regroup_record.enabled`. Run budget: 0, verified on slices 4–5's runs.

**6b Decide-next and the queue (E-031 S3 + item 11's selection half).** Depends on 6a.
- `tools/decide_next.py` (pure, testable): inputs `campaign_memory.yaml`,
  `block_registry.yaml`, `campaign_queue.yaml`, `proposals/*.yaml`, open briefs; gates:
  novelty (slice 8's hash check; until then the existing digest at family grain, advisory
  only), feasibility (data gate result, component requests), rule R1 "registry changed since
  last composition → composition next" (slice 7 supplies the brief writer; until then R1 is a
  no-op), rule R2 "queue empty → for each brief with `status: open`, enqueue a 1a request for
  more hypotheses; stop only when every brief is `exhausted`"; ranking: `confidence_real`
  desc, `distance_to_profitable` desc, cost estimate asc (cost by protocol class: window
  count × variant count × E-039's measured per-backtest median). Writes
  `artifacts/decision_record.yaml` (`{picked, why, ranked_candidates, gates_applied}`) and
  appends the picked candidate as a queue entry via `register_hypothesis` (the existing
  single writer; `source: agent`, `status: ready`).
- Queue changes (`tools/record_schema.py`): `QUEUE_ENTRY_SCHEMA` is closed — add
  `brief_status` (TEXT, `open|exhausted`), `origin` (TEXT: `brief|reader|composition|
  campaign_review|external`), `proposal_ref` (REF), `parked_reason` (TEXT). Statuses
  `paused:waiting_for_component` and `paused:waiting_for_data` already match
  `_QUEUE_STATUS_RE` — no regex change. `_select_entry` (≈L152) unchanged: ready-by-priority.
- Multi-hypothesis briefs (card M): `_handle_hypothesis_generation_multi_card_split` (≈L3611)
  under the flag enqueues cards 2..k via `register_hypothesis` with `origin: brief` instead of
  creating child runs; sets the brief's `brief_status`.
- `run_campaign.py::process_once`: when the finished run's `pending_stage` is a terminal
  status and the flag is on, call `decide_next` before `_select_entry`, ignoring
  `continuation_child` (6c removes it).
- Flag: `orchestrator.decide_next.enabled`. Tests: pure-function tests on synthetic memory
  and queue; R2 on an open brief; schema tests for the new fields; flag-off identity of
  `campaign_queue.yaml`.
- Run budget: 2 consecutive real runs where the second was chosen by `decide_next`, with the
  decision record on disk.

**6c Retire verdict routing; runbook; parked states (item 11, new epic).** Depends on 6b.
**Declared behaviour change when on.**
- Under the flag: `determine_post_verdict_route` returns `completed_<idea_status>` after
  `regroup_record` and never calls `_dispatch_verdict_route`; `_route_refine/_pivot/
  _escalate/_kill`, `_apply_circuit_breaker`, `_create_escalation_protocol`,
  `_create_timeframe_protocol` and `continuation_child` are unreachable (keep the code for
  flag-off runs; mark each with a `# legacy routing (v26 card G)` comment). Campaign review
  keeps `reframe` (writes a brief, `origin: campaign_review`, to the queue via
  `register_hypothesis`) and `terminate`; `continue`/`escalate_*` no longer route.
  `verdict_interpreter` is deleted (decided in slice 5b, not folded in — see the correction
  there); this slice's own S1 must independently confirm every remaining caller of
  `verdict_interpretation.yaml` is re-pointed before the flag can go on.
- Parked states: `_classify_human_pause` gains no new *pause* rows for component/data; instead
  `process_once` marks the entry `paused:waiting_for_component|data`, appends a
  `campaign_log.md` PARKED line, and continues. `resume_paused_entry` (≈L1322) learns
  `--unpark <entry_id>` after the operator has built the component or fetched the data.
- Runbook: `docs/RUNBOOK.md` §3 gains rows `profit_bars_reached`, `queue_exhausted_with_
  open_briefs`, `campaign_review_terminate`; §4 gains the parked-state procedure; every row
  states what to read, what to decide, which artifact to update, and the resume command.
  `docs/HALT_RECOVERY.md` cross-referenced.
- Flag: `orchestrator.verdict_routing_retired.enabled`. Tests: the K2 verdict-machinery
  tests (`tests/test_k2_verdict_machinery.py`, `tests/test_e018_mechanical_routing.py`,
  `tests/test_k4_routing_registration.py`) must still pass flag-off; new tests prove
  flag-on never scaffolds a child run.
- Run budget: the two runs of 6b, re-checked with the flag on.

### Slice 7 — Composition (new epic, not E-044; E-048 is not a gate)

**Corrected 2026-09-19/20, operator review of this plan.** Three changes from the first
draft: (1) composition is its **own new Linear epic**, not a re-scope of E-044 — E-044
("run several proven strategies at once") is a different, live-portfolio idea and is left
untouched; (2) **no E-048 gate** — combining forecasts on a comparable scale is expected to
already be achievable with the transform pipeline's existing standardisation op, so the
design guide (slice 3) is simply told to apply it when assembling a composite; E-048 is
only promoted out of backlog into real work if a specialist reader's finding from a real
composite result says the existing transforms are not enough — that is an ordinary queue
proposal, not upfront engineering; (3) **cross-coin eligibility is decided**: any validated
block is usable in a composite for any instrument, not only the coins it was tested on —
the composite's own grading against the profit bars (slice 0.2) is the check, not an
upfront filter. This removes the former "S1 characterisation question" on eligibility.

Depends on 3, 4, 6b. Run budget: 1 (the first composition run, as soon as the registry
holds two blocks — no longer split into a before/after standardisation pair).

- 7.1 Registry consumers: `residual_ic` criterion in `tools/verdict_criteria_evaluator.py`
  (regress the candidate's per-bar forecast from `bars.csv` on the current composite's
  forecast, IC of the residual with effective sample size — reuse
  `trading-bot/performance/signal_statistics.py`); the composite forecast series is produced
  by running the last composition config once per registry change (cached under
  `campaign_record/composite/<registry_hash>/`).
- 7.2 Composition brief writer in `tools/decide_next.py` rule R1: writes a
  `research_brief.yaml` with `origin: composition`, listing every block's fragment from the
  registry (any instrument, per the decision above), the three weighting schemes as the
  three variants, criteria = the profit-bars file, and the instrument set from that file.
- 7.3 1a passes it through; 1b's skill gets a "composition mode" section in the design guide
  (assemble the listed fragments into regimes/sub-strategies, apply the scheme, **apply the
  transform pipeline's existing standardisation op to each block's forecast before
  combining** — verify in slice 1.1/3 which op this is and that it is sufficient; invent
  nothing else); 5a's manifest check verifies every listed block is present and the scheme
  applied (weights match the scheme's formula within tolerance).
- 7.4 Regime blocks: lift the A2.3 "no regime-gated hypotheses" rule in
  `hypothesis-design/SKILL.md` and `innovation-expansion/SKILL.md` for composition briefs;
  criterion `gated_beats_ungated` compares variant B vs A on the profit bars plus the
  regime-power health metrics.
- 7.5 Feedback path: if the forecast-power or component-attribution reader (slice 5b) flags
  the composite's combined signal as poorly scaled from a real result, its proposal routes
  through `decide_next.py` like any other finding; only then does a genuine E-048 build get
  scheduled (its own S1/S2, unblocked by this slice).
- Flag: `orchestrator.composition_runs.enabled`. Tests: brief writer on a synthetic registry;
  residual IC on synthetic series (independent → high, duplicate → ~0); manifest/scheme
  check.

### Slice 8 — Exact-match repeat check and outside ideas (E-036, E-035)

- 8.1 E-036: replace the fingerprint by `sha256(canonical_json(strategy_config) + instrument +
  timeframe + window_set_ref)` computed at 5a per variant and stored in
  `campaign_record/exclusion_digest.yaml` entries; `anti_adjacency_gate.layer2_digest_check`
  returns REPEAT only on hash equality, NEIGHBOUR (same family/instrument/timeframe) with the
  neighbours' run ids and idea statuses attached, NOVEL otherwise; legacy entries carry
  `legacy: true` and can never produce REPEAT. Then switch on `variant_anti_adjacency_gate`
  and retire `anti_adjacency_retry` (it fired before a config existed). Run budget: replay
  over the corpus, publish refuse/admit counts before/after.
- 8.2 E-035: S1 as filed; plus the feed-acquisition lane: `campaign_record/data_requests.yaml`
  (slice 4) becomes the lane's intake; a reader proposal with `requires_feed` routes there.
  Run budget: 1 externally-sourced idea reaching a grid verdict.

---

## 3. Cross-cutting work (owned by the slice that first needs it)

| Concern | Owner slice | Notes |
|---|---|---|
| `legacy: true` markers on KB findings, digest entries, scoreboard rows | 6a, 8.1 | never rewrite; add the marker on read where the file is closed-schema |
| Trial accounting per variant and per composition run | 4, 7 | `E-025` must accept `run_NNN:variant` ids in its union merge |
| Flag register entries | every slice | one entry per flag, `state`, `criterion`, `blocked_on` |
| Skill files: rewrite `hypothesis-design`, `innovation-expansion`; new `strategy-config-authoring`, five readers; retire `quant-validation`, `backtest-engineering` (as LLM), `regime-auditor` (kept as spec only until 5a inherits its metrics); **delete `verdict-interpreter`** (5b, decided 2026-09-20 — not reduced, removed) | 3, 5 | each skill change ships with its handoff template under `workflow_artifacts/templates/handoffs/` |
| Schemas under `workflow_artifacts/schemas/` | 3, 5, 6 | declared, not enforced today (CLAUDE.md); add `grid_evaluation`, `idea_status`, `block_manifest`, `variant_patches`, `proposals`, `decision_record`, `block_registry` for documentation and the optional validator |
| USER_GUIDE §2.1/§2.2, CLAUDE.md stage list, RUNBOOK §3/§4, DOC_INDEX, WORKFLOW_CAPABILITIES | every slice | `tests/test_guide_covers_the_code.py` gates it |
| Retirement of per-protocol `promotion` blocks and `assert_promotion_ratified` | 6c | only after the profit-bars file is the sole reader |

---

## 4. Linear artifacts to create or change (nothing done yet)

Convention: epics are Linear *projects* named `E-NNN · title`; stories are milestones `S1 ·`,
`S2 ·`; tickets are `CUL-` issues. Next free epic number is **E-058**. Project descriptions
carry the relevant v27 cards verbatim (cards are quoted, not paraphrased).

**Corrected 2026-09-19/20** (operator review of this plan): composition is **not** a re-scope
of E-044 — it is its own new epic, **E-060** below. E-044 is left untouched. E-048 is **not**
promoted into a build — it stays in the backlog, referenced only as a possible later trigger.

| Action | ID | Title | Content to carry | Milestones |
|---|---|---|---|---|
| update | CUL-267 | (as is) | add: prerequisite of the grid; fix goes in `verdict_criteria_evaluator.py`, keyword matcher is legacy; scale-free lint after slice 2 | — |
| create issue | CUL-new | Profitability bars file, campaign-wide, and the branch-3 stop | card B (bars half), card L row `profit_bars_reached`; slice 0.2 seams; `target_instrument_set` | — |
| create issue | CUL-new | Cost-survival criterion from trade records | card E; slice 0.3; E-010 done, E-053 open caveat | — |
| create issue | CUL-new | E-054 follow-up: on by default, registered, per variant, park not pause | slice 0.4 + slice 4's per-variant part; absorbs E-054.1 | — |
| create issue (under E-033) | CUL-new | E-033.1 — test all three variants, each counted | card D, D2; slice 4 seams; per-variant trial ids | — |
| update project | E-033 | (as is) | note D1 superseded by card D; link the new issue | — |
| update project | E-056 | Step 1b writes the bot config directly, under a design guide, with a manifest | cards B (criteria half), K, N; slice 1.1 brief; slice 3 scope | S1 · Characterize (config scaffolding, criterion types, design-guide gaps, pass-through) · S2 · Build (1a/1b skills, design guide, tool-stage 5a, flag) |
| update project | E-057 | State each variant as a named patch on the base config | card D; `variant_patches.yaml` | S1 · Patch contract · S2 · Build with E-056 S2 |
| update project + move issue | E-046b | The grid, and the criterion menu it grades against | cards B, C; slice 1.2 and 2; **move CUL-298 under it** and close it as merged into S2 | S1 · Criterion syntax + menu v1 (exists, re-scope) · S2 · `evaluate_grid`, `grid_evaluation.yaml`, `idea_status.yaml` · S3 · Menu anchors from the legacy re-grade |
| update project | E-046a | Give each backtest a focused report, one per specialist reader | card I (scores), E-040's measurements absorbed; slice 5 | S1 · Reports as re-projection · S2 · Five readers + proposals contract · S3 · Retune firewall on the regime reader |
| create project | E-060 | Block registry and composition runs | cards A, F (corrected 2026-09-19: not E-044, no E-048 gate, any-coin eligibility); slice 7 | S1 · Characterize (composite forecast cache, residual IC, which transform op standardises) · S2 · Registry + residual-IC criterion · S3 · Composition brief writer + 1b composition mode + 5a checks · S4 · First composition run |
| create project | E-058 | Regroup and record — one stage that writes memory before anything is decided | card H; slice 6a; near-miss scoreboard hook; campaign-review skill inputs | S1 · Characterize the four writers today · S2 · Build the stage + `campaign_memory.yaml` + registry writer |
| create project | E-059 | Retire verdict routing; retire verdict_interpreter; decide-next; the operator runbook | cards G, I, L, M; slices 5b, 6b, 6c (verdict_interpreter deletion folded in here since it shares the same caller survey as routing retirement) | S1 · Characterize every caller of the routing table, every pause path, and every reader of `verdict_interpretation.yaml` · S2 · `decide_next.py` + queue fields (with E-031) · S3 · Routing retired + `verdict_interpreter` deleted, behind flag, with runbook rows + parked states · S4 · Two-run proof |
| update project + create sub-issue | E-031 | The queue: let more than one good idea wait its turn, and pick from it | card M; slice 6b; correct "called once" → twice | S3 re-scoped: return edge = `decide_next` + `register_hypothesis`; **new sub-issue** "Brief-sourced entries and brief status open/exhausted" |
| update project | E-036 | Repeat check = exact match on the full backtest setup | card K (repeat half); slice 8.1; legacy tagging | S1 · reopened: hash contract · S2 · Build + corpus replay |
| update project | E-035 | Pull in outside ideas automatically, and open a feed-acquisition lane | card I (manual path exists); slice 8.2 | S1 (exists) · S2 (exists) · S3 re-scoped: feed lane intake = `data_requests.yaml` |
| update project | E-048 | (as is, stays in backlog) | note added: no longer a gate on composition (corrected 2026-09-19) — promoted to real work only if a slice-7 specialist reader's finding says the transform pipeline's existing standardisation op is insufficient | — |
| close as superseded | E-040 | — | comment: measurements absorbed by E-046a S1/S3 and the `gated_beats_ungated` criterion; judgment stage retired (card F, walkthrough note) | — |
| update project | E-049 | (as is) | escalation files disappear with E-059; `sample_split_design` gone with the deleted validation stage | — |
| update project | E-025 | (as is) | per-variant and composition trial ids in the union merge | — |
| update project | E-053 | (as is) | referenced by the cost-survival criterion's caveat | — |
| update project | E-041 | (closed) | note: the E-054 env-var flag was outside the register's coverage; slice 0.4 fixes it | — |
| doc | — | `engineering/roadmap/E-018/EPIC.md` or Linear E-018 | note: scoreboard hook wired by E-058 | — |

Decision cards A–N are pasted, verbatim, into E-056 (B, K, N), E-046b (B, C), E-046a (I),
E-060 (A, F), E-058 (H), E-059 (G, I, L, M), E-057 (D), E-036 (K).

---

## 5. Recommended dispatch order for the next two weeks

1. Now, in parallel: **0.1 CUL-267**, **0.3 cost criterion**, **1.1 E-056 S1**, **1.2 E-046b S1**,
   **5a reports** (all read-only or additive). One dispatch each.
2. After the operator reads 1.1 and 1.2: **2 grid build**, then **0.2 profit bars**,
   **0.4 E-054 on**.
3. After 2: **3 config-direct** (the first declared behaviour change; run budget 1).
4. After 3: **4 variants** (run budget 1), then **5b readers** (run budget 2).
5. After 5: **6a → 6b → 6c** (run budget 2), then **7 composition** (run budget 1, no
   E-048 wait), then **8**.

Each dispatch brief is written from the slice text above plus the rules in §0. The first
one is ready: the E-056 S1 brief from the 2026-09-17 reply, with the four amendments listed
under slice 1.1.
