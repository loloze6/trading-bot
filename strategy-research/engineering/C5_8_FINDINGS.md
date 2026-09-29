# C5.8 — Stop the legacy label reaching readers; retire base-only `pass_rule_evaluation.yaml` (Phase A, characterize and STOP)

Continuation plan row C5.8 (`engineering/delivery_plan_v26_continuation.md:136`), review finding C13 (`engineering/review_*/DELIVERY_REVIEW.md:79`, from `A2_cards_A-G.md:95-96`).
Base: `origin/master` at `5816dced`. No production code changed, no LLM call, no backtest.
All paths are under `strategy-research/` unless they start with `trading-bot/`. `rpr` = `workflow/run_phase1_research.py`, `rp` = `tools/run_protocol.py`, `br` = `tools/build_reports.py`, `vce` = `tools/verdict_criteria_evaluator.py`, `e2e` = `tests/test_e061_end_to_end_wiring.py`. Line numbers are from this checkout.

**How the "measured" rows were measured.** A throwaway test (never committed, deleted after use) ran one full run through the e2e harness (`_v2_harness`, i.e. `V2_FLAGS` = `TARGET_FLAGS` + `profit_bars_v2`, `e2e:186-203, 2065`) and copied `runs/run_001/artifacts/` and the five reader prompts (`h.prompts`, stage `specialist_readers`) to the scratchpad. `score_provenance` was OFF in that run: the harness's reader stub writes `rubric_version: profitability-reader-v1` (`e2e:691`), which the strict set refuses. `score_provenance` does not change what a reader is given: it only stamps `model_id`, enforces the rubric set and records citations against the same three files (`rpr:3969-4000`). The harness's run_protocol stub writes a reduced per-window `core` (no `post_backtest_route*` keys), so those keys are derived from code below, not measured. No run on disk carries them (`grep -rl post_backtest_route runs/` in the main checkout: 0 files).

---

## Plain-words summary

1. **The promote/kill/refine label no longer reaches readers as a value under the target flags.** The review read master at `e623531d`, before two later merges: E-061 C1.3 (`--diagnostics-only`: no validation protocol, so `hypothesis_verdict.verdict` is null) and C5.6 (`--legacy-verdict-retired`: the top-level verdict is null). Measured under the target flags: every variant's `profitability.yaml` block carries `verdict: null` and `verdict_reason: '--diagnostics-only: no validation protocol, no rule set -- diagnostics only, no verdict'`. What is left is the two **keys** (null value and a reason string). They are delivered verbatim in the profitability reader's prompt, and the profitability-reader SKILL still documents them in the report shape. Separately, the per-window `core` blocks and the diagnostics block carry a **second** legacy label family, the cost-check route codes `kill_no_ic` / `refine_inverted_ic` / `kill_cost_hurdle` / `refine_cost_hurdle` (with rationale strings). C13 does not name them, and no reader SKILL reads them.
2. **`pass_rule_evaluation.yaml` has no binding consumer under the target flags.** Every reader of the file is a legacy route (verdict_interpreter, `determine_post_verdict_route`, the campaign-review continue branch, the KB provenance stamp, the C7 conformance check). None of them is reachable once `specialist_readers` and `verdict_routing_retired` are on. The one consumer that is still reachable is advisory only (anti-adjacency Layer 1). Under the target flags the file's content is also never a verdict: 1a's pass_rule has no `outcomes`, so the evaluator returns `legacy_not_evaluable` or `VERDICT_BLOCKED`. The probe measured `VERDICT_BLOCKED`.
3. **Trial accounting does not change if the file is not written in the variant loop.** Every trial row (`run:variant`, `backtest` or `backtest_failed`) is written inside the per-variant loop, before the C7 block. The C7 block is isolated: it never raises and never records a row. The trial writer does not read the file, and neither does anything that counts N or computes the DSR. The single-run branch is different: there, a C7 exception records a `backtest_failed` row and re-raises (pinned by a test). So S2 must leave that branch alone. It is not reached under the target flags anyway.
4. **Recommended gate:** the existing C5.6 predicate `_promotion_retired_enabled()` (config_direct_authoring AND verdict_routing_retired). No new flag. It is already read once per variant loop (`rpr:1768`).
5. **S2 size:** small. It touches 2 production functions plus 1 new pure helper, 3 doc/skill lines, 1 new test file and 1 e2e extension.
6. **One operator question:** should the kill_/refine_ cost-check route codes also be withheld from readers under the flag? Recommendation: yes. Strip the codes and rationales and keep the numbers.

---

## Q1. Where the legacy label reaches the readers (full target flag set)

### 1a. What the readers are handed

| Step | Site | What happens |
|---|---|---|
| Reader handoff | `rpr:3861-3883` `_reader_handoff` | Required inputs are exactly three files: `artifacts/reports/<category>.yaml`, `artifacts/grid_evaluation.yaml`, `artifacts/registry_summary.yaml`. No `protocol_result.yaml`, no `pass_rule_evaluation.yaml`, no `idea_status.yaml`. |
| Prompt build | `rpr:4050-4051` `_build_stage_prompt("specialist_readers", ..., skill_file_name=_reader_skill_dir(category))`; `rpr:3763-3765` | Skill `workflow_artifacts/skills/readers/<category>-reader/SKILL.md` plus the handoff's files inlined. |
| Proposal validation | `tools/reader_proposals.py:148` `load_proposals`; `workflow_artifacts/schemas/proposal.schema.json:8,26,39` (`additionalProperties: false`) | Validates what a reader writes. It plays no part in what a reader reads. A proposal cannot carry a `hypothesis_verdict`/`status` field (closed schema). |

`reader_proposals.py` does not read or carry any label (`grep -n -i "verdict\|promote\|kill\|refine" tools/reader_proposals.py`: only rubric-version comments).

### 1b. The chain that produced the label, and its state today

| Hop | Site | Target-flag state (measured unless marked) |
|---|---|---|
| run_protocol top-level `verdict` (promote/kill/refine from the protocol's `promotion` block) | `rp:1818-1866` `legacy_top_level_verdict`; switch `rp:2548-2551` | `null`, reason `LEGACY_VERDICT_RETIRED_REASON` (`rp:1812-1815`). The orchestrator passes `--legacy-verdict-retired` when `_promotion_retired_enabled()` (`rpr:1467-1475`, read once at `rpr:1768`, used at `rpr:1881`). Measured: `variants/base/protocol_result.yaml` top-level `verdict: None`. This field is **not** re-projected into any report. `br` reads only `hypothesis_verdict` (`br:352-361`), and C5.6 pinned that (`tests/test_c5_6_no_promotion_for_config_direct.py:547-551`). |
| run_protocol `hypothesis_verdict.verdict` (promote/kill/refine from `evaluate_against_decision_rules`, `rp:1655-1659`) | `rp:2561-2572` | `null`. Config-direct never writes `validation_protocol.yaml` (the validation stage is unreached, `rpr:8244-8257`), so `_validation_protocol_args` passes `--diagnostics-only` (`rpr:1453-1465`) and `diagnostics_only_hypothesis_verdict` returns `verdict: None` with `DIAGNOSTICS_ONLY_VERDICT_REASON` (`rp:1782-1798`). Measured: `hv verdict None` in every variant. |
| `profitability.yaml` re-projection | `br:349-363` `build_profitability_report`: `overall = {source, diagnostics, verdict: hv.get("verdict"), verdict_reason: hv.get("verdict_reason")}` | Measured: `reports/profitability.yaml` has `verdict: null` 3 times (asset/base/design), each followed by the diagnostics-only `verdict_reason`. |
| Reader prompt | `rpr:4050` | Measured: the profitability reader's prompt carries the same six lines (`verdict: null` + `verdict_reason: '--diagnostics-only: ...'`, x3). No other reader prompt carries a `verdict:` line. |

**The second label family (route codes), derived from code.**
`trading-bot/reporting/run_artifact.py:565-571` puts `post_backtest_route`, `post_backtest_route_rationale`, `post_backtest_route_real` and `post_backtest_route_real_rationale` in every window's `core`. They are set whenever the IC, the block-adjusted p-value, sigma and trade duration are all non-null (`run_artifact.py:426-450`). The values come from `trading-bot/performance/signal_statistics.py:348-456` `determine_route`: `kill_no_ic`, `refine_inverted_ic`, `kill_cost_hurdle`, `refine_cost_hurdle`, `proceed_to_interpretation`, `inconclusive_insufficient_data`. The rationales contain advice such as "flip polarity" and "Fix: wider threshold or longer holding".
They reach `profitability.yaml` three ways: `per_window[].core` verbatim (`br:371-375`), `per_symbol[<sym>][]` with `**core` spread (`br:385-389`), and the run-level mode in `overall.diagnostics.post_backtest_route_real`, `post_backtest_route_real_tied` and `cost_dominated_real` (`rp:1712-1721, 1756-1758`, re-projected verbatim at `br:359`).
Measured in the probe: the three diagnostics keys are present (`null`, because the stub core has no routes). The per-window keys are absent there only because the stub omits them.
The other four reports do not carry either family. `forecast_power` copies only `forecast_return_corr(_pvalue)` from `core` (`br:461-467`), and `trade_efficiency` copies `trade_diagnostics_summary` (`rp:1086-1136`: no label field). Measured: `grep -i "verdict|kill|refine|promote|lineage|terminate"` over `grid_evaluation.yaml` and `registry_summary.yaml` gives 0 hits, and over the five reports only the `profitability.yaml` lines above plus `*_source` strings naming the `hypothesis_verdict.diagnostics` path.

### 1c. Does any reader SKILL tell the reader to use it?

No.
- `profitability-reader/SKILL.md:56` **documents** the keys in the report shape (`overall: {source, diagnostics: {...}, verdict, verdict_reason}`). No rule, score anchor or example reads them. Rules 1 and 5 read `diagnostics.median_cost_drag_pct`, `median_gross_pnl`, `win_rate_vs_sharpe` and `median_forecast_return_corr` (`:174-205`).
- All five SKILLs forbid emitting the words: profitability `:268-279`, forecast_power `:231`, regime_power `:257`, component_attribution `:278`, trade_efficiency `:245`.
- None references the route codes: `grep -rn "post_backtest_route\|cost_dominated\|route_real\|verdict_reason" workflow_artifacts/skills/readers` gives only `profitability-reader/SKILL.md:56`.

### 1d. A guard that looks like it covers this, but does not

C5.6's prompt guard `_assert_no_promotion_or_verdict_in_prompts` (`e2e:1616-1631`) checks `re.findall(r"(?m)^(verdict|verdict_reason):", prompt)`. It matches only a key at column 0. The profitability report nests the keys (8 spaces of indentation), so the guard passes while every profitability prompt carries them (measured above). A green C5.6 guard is therefore not evidence for C13.

### 1e. Outside the target set (context only)

`specialist_readers` requires only `grid_evaluation` and `category_reports` (`rpr:3602-3635`), not `config_direct_authoring`. With `specialist_readers` on and `config_direct_authoring` off, the validation stage writes `validation_protocol.yaml`, `--validation-protocol` is passed, and `hypothesis_verdict.verdict` is promote/kill/refine. That value then reaches the profitability reader as a live label. The same happens with a stale `validation_protocol.yaml` left from a pre-flag attempt of the same run (`_validation_protocol_args` keys on `validation_path.exists()`, `rpr:1463`). A3 §1's "switch flags with no campaign running" makes that second case unlikely. The gate recommended in Q3 implies config_direct, so it cannot fix the first case, and it does not need to (it is not the target design).

---

## Q2. Every writer and consumer of `artifacts/pass_rule_evaluation.yaml`

### 2a. Writers (exhaustive: `grep -rn "pass_rule_evaluation" --include=*.py strategy-research trading-bot | grep -i "save_yaml|write|dump"`)

| # | Site | Branch | Isolation |
|---|---|---|---|
| W1 | `rpr:2063-2079` (evaluate at `:2064`, write at `:2068`) | Variant loop (`rpr:1717`, `_variant_loop_enabled()`). Evaluates only the **representative** summary: base, else the first graded variant (`rpr:2030-2031`). | Own `try/except`. Logs and never re-raises (`rpr:2072-2079`). Runs **after** the per-variant loop (`rpr:1796-~1975`) has written every trial row. |
| W2 | `rpr:2296-2316` (evaluate at `:2307`, write at `:2311`) | Single-run branch (`rpr:2214`). | Inside the post-success accounting `try` (`rpr:2272`). A raise records a `backtest_failed` row and re-raises (`rpr:2399-2408`). The trial row is written at `rpr:2426-2427`. |

Under the target flags `variant_loop` is on, so only W1 runs. `verdict_routing_retired` does **not** require `variant_loop` (`rpr:4415-4435`: it requires decide_next and profit_bars_every_backtest). So W2 stays reachable in a legal, non-target configuration.

What W1 writes under the target flags: 1a writes a pass_rule of `{"criteria": [...]}` only (`rpr:6782`; `_write_pass_rule_from_card` `rpr:6811-6827`), with no `outcomes`. So `_resolve_pass_rule` returns `legacy_not_evaluable` (`vce:953-957`), or the precondition gate returns `VERDICT_BLOCKED` first (`vce:875-890`). Neither carries `hypothesis_verdict`/`lineage_routing`. Measured in the probe: `result: VERDICT_BLOCKED`.
Exception: an operator brief's hand-written `evaluation.pass_rule` is copied verbatim (`workflow/run_campaign.py:800`). The C5.1 menu lint (`vce:1721-1755`) does not forbid `outcomes`. So such a brief could make W1 write PASS/FAIL with a promote/kill/terminate pair taken from the base variant alone. That is the literal C13 residue, and the new-pipeline brief template does not do it (`workflow_artifacts/templates/research_brief_new_pipeline.md:66-77,172`: `criteria_from: hypothesis_generation`, "do not add one here").

### 2b. Consumers, and whether each is reached under the full target flag set

| # | Consumer | Site | Reached under target flags? | Evidence |
|---|---|---|---|---|
| C1 | verdict_interpreter stage input (`after_backtest` required input) | `rpr:2823-2827` | **No** | Under `specialist_readers`, protocol_execution routes to `specialist_readers` (`rpr:15253`), and a run found at verdict_interpreter raises before any call (`rpr:15074-15079`). |
| C2 | `determine_post_verdict_route`: binding status override, `_resolve_verdict_fields(pre_eval=...)`, C7 conformance, then `_write_kb_findings_entry` | `rpr:13593-13604, 13685-13705, 13719` | **No** | Called only from the verdict_interpreter branch of run_loop (`rpr:15609-15614`). See C1. |
| C3 | `_check_pass_rule_evaluation_conformance` (the "~L13419" check) | `rpr:13419-13457` | **No** | Called only from C2 (`rpr:13697`) and C4 (`rpr:13863`). With the file absent it returns `[]` (`rpr:13433-13434`). Its flag `pass_rule_evaluation_disagreement` is a halt reason in `run_campaign.py:1476-1477`, set only by C2/C4. |
| C4 | `determine_post_campaign_review_route` continue branch | `rpr:13816-13826, 13863-13871` | **No** | Under `verdict_routing_retired` it returns at `rpr:13760-13761`, before loading anything. |
| C5 | KB provenance stamp `verdict_status: gated` + `pass_rule_evaluation_ref` (the "~L10540" logic) | `rpr:10529-10559` `_verdict_provenance_stamp`, called at `rpr:10681` inside `_write_kb_findings_entry` | **No** | This stamps **campaign_knowledge_base.yaml findings**, not the trial ledger. Its only caller `_write_kb_findings_entry` is called only from C2 (`rpr:13719`). Under the target flags the KB entry comes from `tools/grid_kb_writer.py`, which cites `runs/<id>/artifacts/idea_status.yaml` (`grid_kb_writer.py:15,27,91`). |
| C6 | Queue entry `pass_rule_evaluation_ref` | `workflow/run_campaign.py:4078-4097` `_apply_idea_status_outcome` | Reached, but reads **`idea_status.yaml`**, not this file | Ref = `runs/<run>/artifacts/idea_status.yaml`. Pinned at `e2e:1064` and `tests/test_e059_s2a_decide_next.py:751`. `vce.resolve_evaluation_ref` (`vce:677-742`) accepts any owned file with `result` PASS/FAIL. |
| C7 | anti-adjacency Layer 1: `_lineage_routing_of_run` | `tools/anti_adjacency_gate.py:212-226`, via `_branches_closed_by_lineage_routing` `:229-268` and `layer1_advisory` `:413-430`; caller `rpr:7740` | **Yes, advisory only** | Layer 1 "NEVER refuses" (`anti_adjacency_gate.py:28-34, 413-420`). A missing file returns `None` (`:219-221`), the same value it reads from today's target-flag content (no `lineage_routing` key; see 2a). The result is identical except in the operator-brief-with-`outcomes` case, where a later run's advisory could currently say `warn` and would say `admit`. It only ever looks at legacy KB child findings (`:262-265`). |
| C8 | `tools/lint_verdict_provenance.py`, `tools/record_schema.py:188,220`, `vce:760-850` `validate_verdict_provenance` | Validate the **refs** in KB/queue entries | Not through this file under the target flags | New entries cite `idea_status.yaml` (C5, C6). Historic entries citing old runs' files (e.g. `config/campaign_queue.yaml:355`, run_059) are untouched, because their files stay on disk. |
| C9 | `tools/near_miss_scoreboard.py` | — | Does not read it | Only its docstring mentions it (`:29`). It reads `grid_evaluation.yaml` / `verdict_interpretation.yaml` (`:554-555`). |
| C10 | `verdict-interpreter/SKILL.md`, `docs/USER_GUIDE.md:67,929,975-990,1062-1069,1205-1210,1276`, `docs/RUNBOOK.md`, `tools/README.md`, `config/campaign_config.yaml:324,337,466` (comments), `workflow_artifacts/schemas/idea_status.schema.json:5` (description) | Prose | — | Docs only. USER_GUIDE §3 should gain one sentence in S2. |
| C11 | Tests: `test_e033_slice4a_variant_loop.py:317` (exists, base-only, under config_direct + variant_loop, **without** verdict_routing_retired), `:660` (C7 crash, the file absent, trials intact); `test_trial_accounting_characterization.py:701-742` (single-run C7 raise gives exactly one `backtest_failed` row); `test_cul336_closed_book_stages.py:378-397`, `test_e018_mechanical_routing.py`, `test_c7ext_verdict_gates.py`, `test_c7ext_r2_closed_schema.py`, `test_anti_adjacency_gate.py`, `test_halt_quarantine_policy.py`, `test_loop_health_instrument.py`, `test_e059_s2b_briefs.py`, `test_guide_covers_the_code.py` | — | All run with the gate off, or test legacy functions directly. | None needs to change if S2 is gated as in Q3. |

### 2c. Trial accounting if the file is not written under the flags

**Unchanged: N, the DSR and every `run:variant` row are identical, in the variant-loop branch.**
- Rows are written inside the per-variant loop (`rpr:1951-1952` success, plus the `_record_failed_backtest_trial` branches at `rpr:1810, 1836, 1907, 1921, 1938, 1955`). All of this happens before the C7 block at `rpr:2063`.
- The C7 block cannot write or alter a row: its `except` only prints (`rpr:2072-2079`).
- `_record_backtest_trial` reads only `summary` (`hypothesis_verdict.diagnostics`, `per_symbol_summary`, `results`) and the config hash (`rpr:10349-10418`). `_record_failed_backtest_trial` likewise (`rpr:10424-10507`).
- N and the DSR are computed from the ledger (`campaign_state.trial_sharpes`) by `deflate_sharpe` / branch 3 (`_whole_test_trial_kw`, `rpr:12371`). Neither reads this file (grep: no hit in `tools/deflate_sharpe.py` or the profit-bars modules).
- Existing proof: `tests/test_e033_slice4a_variant_loop.py:618-669` (C7 raises, the file absent, all three `run_951:*` rows remain `backtest`).

**Not safe to copy into the single-run branch.** There, not running C7 would remove one of the two raisers covered by the accounting `try`. The pinned contract is: a C7 raise leads to exactly one `backtest_failed` row plus a re-raise (`test_trial_accounting_characterization.py:701-742`). Skipping C7 would turn that look into a `backtest` row with a real Sharpe. N stays 1 per look, but the row's `source`/`statistic_valid`/`sharpe` would differ. S2 therefore gates **W1 only**. Under the target flags W2 is unreachable (`variant_loop` on).

---

## Q3. Which flag gates it

**Recommendation: `_promotion_retired_enabled()` (`rpr:9027-9045`), i.e. `config_direct_authoring` AND `verdict_routing_retired`. No new flag.**

- It is the exact condition under which every binding consumer (C1-C5) is unreachable. `verdict_routing_retired` retires C4 explicitly (`rpr:13760`), and it requires `decide_next`, which requires `regroup_record` → `specialist_readers` (making C1-C3 unreachable) and `config_direct_authoring` (`rpr:4415-4435`; `rpr:4318-4330`).
- It is the predicate C5.6 already uses for the same family ("the legacy promote/kill/refine verdict is retired"). The variant loop already reads it once as `legacy_verdict_args = _legacy_verdict_args()` (`rpr:1768`). S2 can use `bool(legacy_verdict_args)`, so there is no second config read, and in the same attempt run_protocol's null verdict and the missing `pass_rule_evaluation.yaml` always agree.
- **Not `specialist_readers` / `grid_evaluation` / `variant_loop`:** with verdict routing still live, legacy code that reads the file stays reachable (C4 with `routing_retired=False`). The C5.6 precedent says exactly this: "config_direct alone is NOT enough: with verdict routing still live G7 stays required" (`rpr:9035-9036`), and `test_c5_6_no_promotion_for_config_direct.py:117-140` pins it. Gating on `variant_loop` would also break the existing pin `test_e033_slice4a_variant_loop.py:317` (the file is written under config_direct + variant_loop).
- **Not a new flag:** the semantics are identical to an existing predicate. A new flag needs its own register entry (`config/feature_flag_register.yaml`, checked by `tests/test_feature_flag_register.py`) and one more switch for C4 to remember. The target set already turns `verdict_routing_retired` on. D-043: removal waits for the post-C4 clean-up epic, so this is a gate, not a deletion. The register's `verdict_routing_retired` criterion text (`config/feature_flag_register.yaml:457+`) gains one sentence.

---

## Q4. Proposed S2 build

### Production changes (all no-ops with the gate off)

1. **`rpr` `run_tool_worker`, variant-loop branch only.**
   - Under the gate, skip the C7 `try` block `rpr:2063-2079` (`evaluate_pass_rule_criteria` + write). Keep `import verdict_criteria_evaluator as _vce` and the `_pre_reg_for_eval` / `_brief_for_eval` loads (`rpr:2045-2052`): the grid block at `rpr:2089+` uses them. Print one line stating that the file is not written and why (any emoji print must stay cp1252-guarded: `tests/test_emoji_prints_cp1252_guarded.py`).
   - Under the gate, at branch entry, unlink a stale `artifacts/pass_rule_evaluation.yaml` from an earlier attempt. This follows the same "this attempt's artifacts only" precedent as `_clear_specialist_readers_artifacts` (`rpr:3674-3700`) and the branch-3 stale clear (`rpr:1519-1528`). Otherwise a pre-flag attempt's base-only file would survive into C7's advisory reader.
   - At the variant-loop `build_reports` call (`rpr:2191-2194`), pass `legacy_verdict_retired=True` **only under the gate**, as a conditional kwarg, so the call with the gate off is unchanged (repo convention, e.g. `rpr:15612-15613`).
   - W2 (single-run branch, `rpr:2296-2316`) and its `build_reports` call (`rpr:2387`) are not touched (Q2c).
2. **`br` `build_reports`**: add a keyword-only `legacy_verdict_retired: bool = False`. When true, apply a new pure helper `_strip_legacy_verdict_fields(report)` to the `profitability` report in both shapes (single-run `slices.overall` and schema-2 `variants.<vid>.slices.overall`). It drops `verdict` and `verdict_reason` from an `overall` that is not the `{unavailable: ...}` shape. **If the operator answers OQ1 yes**, it also drops `post_backtest_route_real`, `post_backtest_route_real_tied` and `cost_dominated_real` from `overall.diagnostics`, and `post_backtest_route`, `post_backtest_route_rationale`, `post_backtest_route_real` and `post_backtest_route_real_rationale` from every `per_window[].core` and `per_symbol[<sym>][]` row. It keeps the numeric `post_backtest_cost_check(_real)` blocks and the correlation fields. Default False: the output is the same dict as today.
3. **Docs/skill (no rubric change):** `profitability-reader/SKILL.md:56` comment: "`verdict`/`verdict_reason` are absent once verdict routing is retired; an idea's status is the grid's". `rubric_version` stays `-v2` (no scoring text changes; `tools/reader_proposals.py:41-44` pins the rubric dict, not the prose). USER_GUIDE §3 C7 paragraph (`docs/USER_GUIDE.md:975-990`) and artifact table row (`:929`): one sentence on the gate. Register criterion sentence (Q3).

### Off-by-default byte-identity test (new file, e.g. `tests/test_c5_8_legacy_label_retired.py`)

- **Gate off, orchestrator:** run the variant loop with config_direct + variant_loop (no verdict_routing_retired), using `test_e033_slice4a_variant_loop.py`'s fake-subprocess pattern. Assert `pass_rule_evaluation.yaml` is written with the same content as today (compare minus `evaluated_at`), and that the spied `build_reports` call's kwargs are exactly `{write, variants, failed_variants, untested_variants}`.
- **Gate off, builder:** `build_reports(run_dir, variants=...)` output with no kwarg == output with `legacy_verdict_retired=False`, and `verdict`/`verdict_reason` present.
- **Gate on, same stubbed variants:** the file is not written. A stale one planted beforehand is removed. **The trial ledger equals the gate-off run's ledger row for row** (rows carry no timestamp: `rpr:10394-10404`). That comparison is the explicit trial-accounting proof.
- **Gate on, builder:** the stripped report equals the unstripped report minus exactly the named keys, and nothing else differs.
- **Single-run branch untouched:** a gate-on run with variant_loop off still writes W2, and `test_trial_accounting_characterization.py:701` stays green.

### e2e extension (`tests/test_e061_end_to_end_wiring.py`, rule 8)

- `_assert_no_promotion_or_verdict_in_prompts` (`e2e:1616-1631`): for `specialist_readers` prompts, match indented keys too (`(?m)^\s*(verdict|verdict_reason):`). Measured today, this is **red**: 6 lines in the profitability prompt. That makes it the S2 red test. Stage-agent prompts were not captured by the probe, so S2 must check the tightened regex against them before widening it beyond readers.
- `test_end_to_end_two_runs_with_the_real_run_setup` (`e2e:1050`) and `_assert_c5_6_run_completed` (`e2e:1634`): assert `h.art(r1, "pass_rule_evaluation.yaml") is None`, and that `reports/profitability.yaml` has no `verdict`/`verdict_reason` under any variant. The existing trial-row assertions (`e2e:1080-1084`, `:1666-1667`) stay as the accounting check.
- If OQ1 is yes: `Harness._run_protocol`'s stub `core` (`e2e:768+`) gains the four `post_backtest_route*` keys, so the strip is exercised end to end (today the stub omits them, so a pass would be vacuous).

### Pin/guard tests naming the touched modules (run all before merge)

- `build_reports` (12 files): `test_c5_6_no_promotion_for_config_direct.py` (`:547` profitability report independent of the top-level verdict), `test_e033_slice4a_variant_loop.py`, `test_e035_s2c_feed_requests.py`, `test_e046a_category_reports.py`, `test_e046a_slice5b_i_reader_skills.py`, `test_e046a_slice5b_ii_b_readers_stage.py`, `test_e046a_slice5b_ii_b_review_fixes.py`, `test_e058_s2a_regroup_record.py`, `test_e060_s3b_composition_wiring.py`, `test_e061_c2_s2e_distance_rubric.py`, `test_e061_end_to_end_wiring.py`, `test_reader_proposals.py`.
- `pass_rule_evaluation` (14 files): `test_anti_adjacency_gate.py`, `test_c7ext_r2_closed_schema.py`, `test_c7ext_verdict_gates.py`, `test_cul336_closed_book_stages.py`, `test_e018_mechanical_routing.py`, `test_e033_slice4a_variant_loop.py`, `test_e058_s2b_registry_kb_scoreboard.py`, `test_e059_6c_s2c_parked_states.py`, `test_e059_s2a_decide_next.py`, `test_e059_s2b_briefs.py`, `test_e061_end_to_end_wiring.py`, `test_guide_covers_the_code.py`, `test_halt_quarantine_policy.py`, `test_loop_health_instrument.py`.
- Trial accounting: `test_trial_accounting_characterization.py`, `test_b2_machine_trial_accounting_proof.py`, `test_dual_writer_guards.py`, `test_record_backtest_trial_expectancy_shape.py`, `test_invalidated_trial_exclusion.py`.
- Reader skills: `test_c5_7b1_model_id_stamp.py`, `test_c5_7b2_rubric_citations.py`, `test_e046a_slice5b_i_reader_skills.py`, `test_e056_1b_block_manifest.py`, `test_e059_s2b_review_fixes.py`.
- Flags and routing: `test_feature_flag_register.py`, `test_e059_6c_s2a_route_retirement.py`.
- `run_phase1_research.py` text/print guards: `test_emoji_prints_cp1252_guarded.py`, `test_run_phase1_research_cp1252.py`, `test_doc_anchors.py`, `test_user_guide_field_tables.py`. The full list of 39 files naming the file literally: `grep -rl "run_phase1_research\.py" tests`.

**Size:** 2 production functions changed (`rpr` `run_tool_worker` variant-loop branch; `br` `build_reports`) plus 1 new pure helper in `br`. Roughly 30-50 production lines, plus 1 SKILL comment line, 2 USER_GUIDE sentences and 1 register sentence. 1 new test file and 1 e2e extension (plus the stub `core` keys if OQ1 is yes). Sonnet-sized for tests/docs; the `rpr` change touches the accounting-adjacent branch, so it goes to Opus per D-044.

---

## Q5. Open question for the operator

**OQ1. Also withhold the kill_/refine_ cost-check route codes from readers under the gate?**
C13 names only the promote/kill/refine verdict, and that verdict already reaches readers as `null`. The route codes (`kill_no_ic`, `refine_inverted_ic`, `kill_cost_hurdle`, `refine_cost_hurdle`, plus rationales with fix advice) are the same retired routing vocabulary. Card G ("Refine / pivot / escalate / kill is retired") and D-009 (readers never decide) retire the routing, but neither says whether this evidence stays in the reader inputs. No reader SKILL reads the codes (1c). The numbers they summarise stay in the report either way (`forecast_return_corr*`, `post_backtest_cost_check(_real)` with edge/cost ratio, `diagnostics.median_*`).
**Recommended answer: yes.** Strip the 3 diagnostics keys and the 4 per-window route/rationale keys under the same gate, and keep every numeric field. That way the readers score from numbers, not from a verdict-shaped word. If no, S2 drops only `verdict`/`verdict_reason`.

No other operator question. The branch scope (variant loop only), the stale-file clear and the flag choice follow from the code, the C5.6 precedent and D-043.
