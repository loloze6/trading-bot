# Skill and prompt-input files: stale-reference audit (report only)

Date of audit: 2026-11-05. Code as committed (master 2026-10-28 plus night-work doc commits).
SR = strategy-research/, RP = SR/workflow/run_phase1_research.py, RC = SR/workflow/run_campaign.py,
CFG = SR/config/campaign_config.yaml. All paths below are relative to SR unless they start with RP/RC.
No file was changed except this one. Prompt files steer the AI: this report states facts only; the operator decides any change.

## Method

- File set: every file under `workflow_artifacts/skills/` (25 md) and `workflow_artifacts/templates/` (19 files, 3 of them 0 bytes),
  plus the 4 `docs/` files the code pastes into stage prompts (`DATA_AVAILABILITY.md`, `STRATEGY_DESIGN_GUIDE.md`,
  `COMPONENT_CATALOG.md`, `DATA_DICTIONARY.md`). Total 48 files.
- Loaders found by reading the prompt builders: `_SKILL_MAP` (RP:1019-1027) read by `_build_stage_prompt` (RP:1051-1053);
  `_CLOSED_BOOK_STAGE_INPUTS` (RP:3162-3215); `STAGE_CONFIGS` handoff names (RP:156-256) read from the run's `handoffs/`
  (RP:9683-9685, RP:19824-19826), which `workflow/setup_run.py:109-118` fills by copying `templates/handoffs/*.yaml`;
  the addenda constants (RP:7735, 8143, 8591, 16772, 16789, 17299-17303, 17944); `tools/analyst_session.py:55,422-431`.
- Reached = reached under the committed defaults in CFG. Defaults that matter: `config_direct_authoring`, `grid_evaluation`,
  `analyst`, `regroup_record`, `decide_next`, `verdict_routing_retired`, `claim_tests`, `nearest_build`, `folds`, `exact_config_1b`,
  `brief_criteria` are all `enabled: false`; `data_availability_gate`, `exclusion_digest_input`, `stale_input_path_fix`,
  `variant_selection_record` are `true`. Routing facts: RP:20160 (strategy_config_authoring only if config_direct on), RP:20176-20186
  (analyst / grid route only if their flags are on), RP:20233 (validation skipped only if config_direct on), RP:9672-9677
  (backtest_specification is a tool stage only if config_direct on).
- Checks run by script: (b) every path-like token resolved against SR, repo root, trading-bot/, docs/, tools/, config/, workflow/ and the
  file's own directory, run-relative `artifacts/...` names checked against the code; every `name()`/`::name` identifier checked as a def or
  assignment in all .py files; every `file.py:NN` citation read at the cited line. (c) every `orchestrator.<key>` and `<key>.enabled`
  compared with the keys of CFG. (d) the sealed range loaded from `config/campaign_data_policy.yaml` and compared with every
  YYYY-MM-DD, YYYYMMDD, YYYY-MM and month-name date in the 48 files (only `file:line` printed; also a bare-year scan). (e) grep for `CLAUDE`.
- SR/CLAUDE.md headings now: `## 1. Objective and overview` with `### Workflow stages` (CLAUDE.md:6,18), `## 2. Behaviour rules`, `## 3. Development and test process`.
  Registry (CLAUDE.md:20-26, RP:156-256) holds 12 stages: hypothesis_generation, strategy_config_authoring, innovation_expansion, validation,
  backtest_specification, data_availability_gate, protocol_execution, verdict_interpreter, analyst, regroup_record, campaign_review, holdout_evaluation.
  "1a/1b/5a" are sub-labels of these (USER_GUIDE.md section 2) and were not counted as stale.

## Totals

| Category | Findings |
|---|---|
| a. stages not in STAGE_CONFIGS / not reached | 17 lines (of these 5 are accurate "retired/removed" notes, 3 are the regime-auditor human route; see per file) |
| b. file paths that do not exist / citations pointing at the wrong line | 17 |
| c. flags not in CFG | 0 |
| d. written-out date inside the sealed range | 2 |
| e. old CLAUDE.md sections | 1 |
| f. instruction contradicting code (clear cases) | 3 |

## Summary table

Counts are a/b/c/d/e/f. "Used by" gives the loader file:line. "Reached?" is under the committed defaults.

| File | Used by (loader) | Reached? | a | b | c | d | e | f |
|---|---|---|---|---|---|---|---|---|
| skills/hypothesis-design/SKILL.md | RP:1020 -> RP:1051; stage hypothesis_generation (RP:157-161) | yes | 0 | 0 | 0 | 0 | 0 | 0 |
| skills/hypothesis-design/BRIEF_HYPOTHESES.md | RP:8591, `_apply_brief_hypotheses_context` RP:8621 | no (decide_next off) | 1 | 0 | 0 | 0 | 0 | 0 |
| skills/hypothesis-design/DECIDE_NEXT_CANDIDATES.md | RP:8143, `_apply_decide_next_context` RP:8462 | no (decide_next off) | 1 | 0 | 0 | 0 | 0 | 0 |
| skills/hypothesis-design/PREFILLED_CLAIM.md | RP:17302, `_apply_claim_tests_context` RP:17409-17445 | no (claim_tests off) | 1 | 0 | 0 | 0 | 0 | 0 |
| skills/hypothesis-design/CLAIM_TESTS.md | RP:17299, RP:17429, copy source RP:17958; tools/analyst_session.py:429 | no (claim_tests off) | 0 | 0 | 0 | 0 | 0 | 0 |
| skills/hypothesis-design/CLAIM_TESTS_TRADE.md | RP:17303, RP:17437; tools/analyst_session.py:429 | no (needs claim_tests and analyst) | 0 | 0 | 0 | 0 | 0 | 0 |
| skills/hypothesis-design/CLAIM_TESTS_EXECUTION.md | tools/analyst_session.py:429 only (no RP loader) | no (analyst off) | 0 | 0 | 0 | 0 | 0 | 1 |
| skills/strategy-config-authoring/SKILL.md | RP:1021 -> RP:1051; stage strategy_config_authoring (RP:170-174) | no (config_direct off) | 0 | 0 | 0 | 0 | 0 | 0 |
| skills/strategy-config-authoring/CLAIM_NOTE.md | RP:17300, RP:17421 | no | 0 | 0 | 0 | 0 | 0 | 0 |
| skills/strategy-config-authoring/NEAREST_BUILD.md | RP:16772, `_apply_nearest_build_context` RP:16779 | no | 1 | 0 | 0 | 0 | 0 | 0 |
| skills/strategy-config-authoring/START_FROM_CONFIG.md | RP:16789-16790, `_apply_start_config_context` RP:16813 | no | 1 | 0 | 0 | 0 | 0 | 0 |
| skills/innovation-expansion/SKILL.md | RP:1022 -> RP:1051; stage innovation_expansion (RP:175-183) | yes | 0 | 0 | 0 | 0 | 0 | 1 |
| skills/quant-validation/SKILL.md | RP:1023 -> RP:1051; stage validation (RP:184-196) | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| skills/backtest-engineering/SKILL.md | RP:1024 -> RP:1051; stage backtest_specification (RP:197-201), LLM stage when config_direct off (RP:9672-9680) | yes | 0 | 0 | 0 | 0 | 0 | 0 |
| skills/verdict-interpreter/SKILL.md | RP:1025 -> RP:1051; stage verdict_interpreter (RP:216-220) | yes (grid off, analyst off) | 4 | 0 | 0 | 1 | 0 | 1 |
| skills/campaign-review/SKILL.md | RP:1026 -> RP:1051; stage campaign_review (RP:246-250) | conditional (review trigger, RP:12977-13000, RP:16276) | 1 | 0 | 0 | 0 | 1 | 0 |
| skills/campaign-review/RETIRED_ROUTING.md | RP:7735, `_apply_retired_routing_review_context` | no (verdict_routing_retired off) | 0 | 0 | 0 | 0 | 0 | 0 |
| skills/quant-fundamentals/SKILL.md | `_CLOSED_BOOK_QUANT_FUNDAMENTALS` RP:3162-3165, used RP:3192, 3196, 3209, 3213 | yes (via backtest_specification, verdict_interpreter, campaign_review) | 0 | 0 | 0 | 1 | 0 | 0 |
| skills/claim-revision/SKILL.md | RP:17944 `CLAIM_REVISION_SKILL`, RP:18061 (skill_file_name=) | no (claim_tests off) | 0 | 0 | 0 | 0 | 0 | 0 |
| skills/analyst/SKILL.md | tools/analyst_session.py:423 (`build_prompt`); stage analyst (RP:231-235) | no (analyst off) | 0 | 1 | 0 | 0 | 0 | 0 |
| skills/analyst/forecast.md | tools/analyst_session.py:423 (`{lens}.md`) | no | 0 | 0 | 0 | 0 | 0 | 0 |
| skills/analyst/trade_efficiency.md | tools/analyst_session.py:423 | no | 0 | 0 | 0 | 0 | 0 | 0 |
| skills/regime-auditor/SKILL.md | none found (human procedure, docs/USER_GUIDE.md:236, 1205) | no loader | 1 | 0 | 0 | 0 | 0 | 0 |
| skills/research-system-evolution/SKILL.md | none found | no loader | 0 | 0 | 0 | 0 | 0 | 0 |
| templates/handoffs/research_brief_to_hypothesis.yaml | STAGE_CONFIGS RP:158 | yes | 0 | 0 | 0 | 0 | 0 | 0 |
| templates/handoffs/hypothesis_to_strategy_config_authoring.yaml | STAGE_CONFIGS RP:171 | no | 0 | 0 | 0 | 0 | 0 | 0 |
| templates/handoffs/hypothesis_to_innovation_expansion.yaml | STAGE_CONFIGS RP:176 | yes | 0 | 0 | 0 | 0 | 0 | 0 |
| templates/handoffs/innovation_expansion_to_validation.yaml | STAGE_CONFIGS RP:185 | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| templates/handoffs/validation_to_backtest_specification.yaml | STAGE_CONFIGS RP:198 | yes | 0 | 0 | 0 | 0 | 0 | 0 |
| templates/handoffs/backtest_spec_to_protocol_execution.yaml | STAGE_CONFIGS RP:213 (tool stage) | yes | 0 | 0 | 0 | 0 | 0 | 0 |
| templates/handoffs/protocol_to_verdict_interpreter.yaml | STAGE_CONFIGS RP:217 | yes | 0 | 0 | 0 | 0 | 0 | 0 |
| templates/handoffs/campaign_review.yaml | STAGE_CONFIGS RP:247; copied RP:16280 | conditional (as campaign-review) | 0 | 3 | 0 | 0 | 0 | 0 |
| templates/handoffs/holdout_evaluation.yaml | STAGE_CONFIGS RP:253 (tool stage) | conditional (promote route) | 0 | 0 | 0 | 0 | 0 | 0 |
| templates/backtest_spec.yaml | no loader | no | 0 | 1 | 0 | 0 | 0 | 0 |
| templates/decision.yaml | no loader | no | 0 | 0 | 0 | 0 | 0 | 0 |
| templates/handoff.yaml | no loader | no | 0 | 0 | 0 | 0 | 0 | 0 |
| templates/hypothesis_card.yaml | no loader | no | 0 | 0 | 0 | 0 | 0 | 0 |
| templates/pipeline_state.yaml | no loader (workflow/setup_run.py:70-91 builds its own state) | no | 5 | 0 | 0 | 0 | 0 | 0 |
| templates/research_brief.yaml | no loader (named by campaign-review/SKILL.md:178) | no | 0 | 0 | 0 | 0 | 0 | 0 |
| templates/research_brief_new_pipeline.md | operator copy; RC:725 names it; its `scope:` block becomes part of research_brief.yaml, which stage prompts paste | yes (every brief) | 0 | 11 | 0 | 0 | 0 | 0 |
| templates/run_manifest.yaml, validation_decision.yaml, validation_protocol.yaml | no loader; all 0 bytes | no | 0 | 0 | 0 | 0 | 0 | 0 |
| docs/DATA_AVAILABILITY.md | RP:3181 (validation, refine only), RP:3188 (backtest_specification, optional); template hypothesis_to_strategy_config_authoring.yaml:22 | yes (conditional on refine / timeframe change) | 0 | 1 | 0 | 0 | 0 | 0 |
| docs/STRATEGY_DESIGN_GUIDE.md | RP:9084 and template hypothesis_to_strategy_config_authoring.yaml:17 | no (config_direct off) | 0 | 0 | 0 | 0 | 0 | 0 |
| docs/COMPONENT_CATALOG.md | template validation_to_backtest_specification.yaml:16 (optional); RP:9090; analyst via catalogue_section | yes (optional input of backtest_specification) | 0 | 0 | 0 | 0 | 0 | 0 |
| docs/DATA_DICTIONARY.md | tools/analyst_session.py:428 | no (analyst off) | 0 | 0 | 0 | 0 | 0 | 0 |

Rows add up to the totals above (a: 17 = 1+1+1+1+1+1+4+1+1+5+1; b: 17 = 1+3+1+11+1; d: 2; e: 1; f: 3).

## Findings per file

Only files with at least one finding, plus the uncounted notes where they matter. Dates are masked as `<date>`.

### skills/campaign-review/SKILL.md (used by campaign_review; conditional)

- :184-186 | a | "The hypothesis still enters through FULL pre-registration -- validation_gate, screening_backtest, walk_forward_validation, the works" |
  `screening_backtest` and `walk_forward_validation` are not in STAGE_CONFIGS (RP:156-256); `validation_gate` is the docs name of the code stage `validation` (CLAUDE.md:30-31).
- :187 | e | "(see `strategy-research/CLAUDE.md`'s Workflow stages)" | the heading exists (CLAUDE.md:18, under section 1), but it lists the 12 registry stages (CLAUDE.md:20-26) and none of the three names the sentence expects.
- Uncounted: :17 lists campaign_state.yaml and research_brief.yaml as required inputs; the handoff template also requires the KB (templates/handoffs/campaign_review.yaml:14-15).

### skills/verdict-interpreter/SKILL.md (used by verdict_interpreter; reached)

- :324, :331, :655 | a | "route to regime-auditor", "The orchestrator will pause the pipeline and route to regime-auditor", "route back to regime-auditor" |
  regime_auditor is not in STAGE_CONFIGS; USER_GUIDE.md:236 calls it "a human procedure the orchestrator never dispatches"; the code pauses for a human (RP:16160-16172, message "consult regime-auditor skill").
- :736 | a | "`signal_prescreen`'s own `_resolve_ungated_escape`, was removed" | accurate historical note; the stage and function no longer exist.
- :506 | d | "Threshold is PROVISIONAL (set <date>)" | the written date lies inside the sealed range of `config/campaign_data_policy.yaml` (holdout_range). File:line only, per the rules.
- :51-63 | f | "`grid_evaluation.yaml`, `idea_status.yaml` ... REQUIRED when present ... It is NOT yet wired as a second MACHINE-AUTHORED VERDICT authority ... until a later slice repoints routing through it directly" |
  Code: with `grid_evaluation` on, `protocol_execution` no longer leads to this stage (RP:20176-20180), verdict_interpreter is "unreached (not deleted)" (RP:20170-20173, STAGE_CONFIGS comment RP:226-230) and the post-run route comes from the grid's `idea_status.yaml`. The files are written only when the flag is on (CFG `grid_evaluation.enabled: false`, key `grid_evaluation`), i.e. only when this stage is not run.
- Uncounted: :430 "across all 22 windows" and quant-fundamentals/SKILL.md:126 "standard 22-window protocol (2 symbols x 11 walk-forward windows)": the window count is read from the protocol (RP:10522-10640; folds give six blocks, RP:10616); no code line fixes 22.

### skills/innovation-expansion/SKILL.md (used by innovation_expansion; reached)

- :197-200 | f | "The exact-match check at step 5a (`tools/anti_adjacency_gate.py`) refuses an exact repeat ... downstream, deterministically" |
  Both call sites of that check return before doing anything unless `orchestrator.variant_anti_adjacency_gate.enabled` is on (RP:9485, RP:9583, reader RP:9351-9358); CFG:247-248 sets it `false`. Under the committed defaults no repeat is refused.

### skills/quant-fundamentals/SKILL.md (closed-book input of 4 stages; reached)

- :115 | d | "PROVISIONAL MINIMUM -- set <date>" | the written date lies inside the sealed range of `config/campaign_data_policy.yaml`.

### skills/quant-validation/SKILL.md (used by validation; reached)

- :11 | a | "`refinement_planner` retired as a separate pipeline stage" | accurate: no such entry in STAGE_CONFIGS; retirement comment RP:187-190.

### skills/regime-auditor/SKILL.md (no loader)

- :80 | a | "this regime-auditor stage" | not a STAGE_CONFIGS entry and nothing loads the file; USER_GUIDE.md:236, 1205 describe it as a human procedure.

### skills/hypothesis-design/BRIEF_HYPOTHESES.md (decide_next only)

- :47 | a | "against each other and against reader proposals" | the five readers' stage (specialist_readers) was deleted (D-198; RP:226-230, DATA_DICTIONARY.md:9-10); proposals now come from the analyst's two lenses (tools/analyst_session.py:48 `LENS_CATEGORY`). `tools/reader_categories.py` and `tools/reader_proposals.py` still carry the word.

### skills/hypothesis-design/DECIDE_NEXT_CANDIDATES.md (decide_next only)

- :17 | a | "The candidate comes from a specialist reader's proposal after an earlier run" | same fact as above (deleted readers; analyst lens proposals).

### skills/hypothesis-design/PREFILLED_CLAIM.md (claim_tests only)

- :3 | a | "from a reader's side finding: something a reader noticed" | same fact as above.

### skills/hypothesis-design/CLAIM_TESTS_EXECUTION.md (analyst only)

- :3-4 | f | "This page is shown to no prompt yet. It is the text the analyst's guide (E-077 PR-5) will add to CLAIM_TESTS.md's 'claim kind' table once that guide exists" |
  `tools/analyst_session.py:429` pastes this file into the analyst prompt (section "Claim-test vocabulary: CLAIM_TESTS_EXECUTION.md"), and `skills/analyst/SKILL.md:35-36` lists it as part of the analyst's inputs. (No RP loader exists, so step 1a never sees it: `tools/claim_card.py:64` and tests/test_e077_pr2_confirm.py:266 still say "shown to no prompt yet" about step 1a.)

### skills/strategy-config-authoring/NEAREST_BUILD.md (nearest_build only)

- :28 | a | "shows the deviations first in the run's finding and in the readers' inputs" | the readers are deleted (see above).

### skills/strategy-config-authoring/START_FROM_CONFIG.md (reader-finding briefs only)

- :3 | a | "a claim a reader noticed in an earlier run's evidence" | same fact as above.

### skills/analyst/SKILL.md (analyst only)

- :167 | b | "the run_096 smoke copy's `analyst_queries/trade_efficiency.yaml`" | no such file in this checkout (runs/ ends at run_060); the code's log path is `artifacts/analyst_queries/<lens>.yaml` (tools/analyst_session.py:56,65).

### templates/handoffs/innovation_expansion_to_validation.yaml (validation; reached)

- :16 | a | "refinement_planner retired as a separate stage; this is that stage's former job" | accurate (see quant-validation above).

### templates/handoffs/campaign_review.yaml (campaign_review; conditional)

- :9 | b | `primary_input_artifact: ../../campaign_state.yaml` | resolves to SR/campaign_state.yaml, which does not exist; the file is `campaign_record/campaign_state.yaml` (RP:93).
- :11 | b | `path: ../../campaign_state.yaml` (required input) | same.
- :15 | b | `path: ../../campaign_knowledge_base.yaml` (required input) | the file is `campaign_record/campaign_knowledge_base.yaml` (RP:12473 `_KB_PATH`).
- Code consequence (fact): a missing required input raises `FileNotFoundError` in `_build_stage_prompt` (RP:1067). `_STALE_INPUT_PATH_FIXES` (RP:3855-3860) repoints only hypothesis_generation's optional inputs; the comment at RP:3829-3843 records that campaign_review's two required paths are not fixed; `_write_retired_review_handoff` (RP:7810-7860) writes its own handoff for the flag-on case only. The legacy review (flag off, the default) copies this template (RP:16280).

### templates/backtest_spec.yaml (no loader)

- :3 | b | "validated against strategy_config.schema.json" | no file of that name exists in the repo (only a mention in engineering/roadmap/E-056/S1_FINDINGS.md); schemas are in `workflow_artifacts/schemas/` (`backtest_spec.schema.json` is there).

### templates/pipeline_state.yaml (no loader)

- :4 | a | `current_stage: research_brief` | `research_brief` is an input, not a stage (CLAUDE.md:28).
- :16 | a | `screening_results: null` | no screening stage in STAGE_CONFIGS.
- :17 | a | `walk_forward_results: null` | no such stage.
- :37 | a | `screening_passed: false` | no such stage; `workflow/setup_run.py:84` still writes the same key into new runs.
- :38 | a | `walk_forward_passed: false` | same (`workflow/setup_run.py:85`; RP:16052 sets it).
- Note: `setup_run.py:70-91` builds the state in code and never reads this file.

### templates/research_brief_new_pipeline.md (every brief; the `scope:` block at :57-65 is copied into each brief)

Citations that point at the wrong line now (the files exist):
- :62 | b | "tools/run_protocol.py:2476-2480 prints it on every run" | the price_proxy/funding_modelled print is at tools/run_protocol.py:2544-2545; 2476-2480 is the promotion-block check.
- :64 | b | "(tools/claim_tests.py:579-581)" Selector list | `SELECTORS` is at tools/claim_tests.py:719-721.
- :64 | b | "(:631-632)" Outcome list | `OUTCOMES` is at :778-779.
- :64 | b | "(:682-683)" Baseline list | `BASELINES` is at :838-839.
- :64 | b | "(:748-749)" Statistic list | `STATISTICS` is at :904-905.
- :64 | b | "check_spec refuses it before any data is read (:881)" | `check_spec` is at :1110.
- :74 | b | "(run_phase1_research.py:11642-11646)" window-start refusal | the refusal is `_generate_monthly_windows`, RP:10548-10556 (allowed list RP:10518).
- :75 | b | "(run_campaign.py:3847-3853)" launch refusal | RC:3847-3853 holds `_PREFLIGHT_TERMINAL_PREFIXES` / `_GENERATED_PROTOCOL_FIELDS`; the pre-flight copy of the generator is `_expected_generated_protocol` (RC:3884), the validation-boundary check RC:3984-3987.
- :80 | b | "(workflow/run_phase1_research.py:11720-11724)" fold D only under folds | the check is RP:10630-10634 (`_protocol_windows_from_constraints`, RP:10596-10639).
- :81 | b | "(run_phase1_research.py:11771-11772)" start/end read with a fold | RP:11771-11772 is unrelated code (escalation baseline); `_protocol_windows_from_constraints` is RP:10608-10639, start/end read at RP:10681-10682.
- :81 | b | "(its only reader is the no-fold branch, run_phase1_research.py:11715)" window_months | the reader is RP:10625.
- Verified correct (no finding): tools/variant_coin.py:725 and :681-682, tools/venue_resolver.py:57,101-102,117-137,134, trading-bot/data/fetchers/ccxt_fetcher.py:123, config/venue_data_capability.yaml:394-397,472-481,528-530,536-537, config/available_feeds.yaml:26,35-50, docs/DATA_AVAILABILITY.md:25-38, tools/research_folds.py:113,397-403.

### docs/DATA_AVAILABILITY.md (pasted into validation refine / backtest_specification)

- :85 | b | "(`episode_significance.py:209`)" | the label `block_24_dense_fallback` is at tools/episode_significance.py:70; line 209 is in `episode_block_bootstrap`.

## Category c

No finding. Every `orchestrator.*` flag named in the 48 files exists in CFG: cost_bar_all_costs, zero_trade_windows_not_computed, analyst, profit_bars_v2, forecast_size_probe, verdict_routing_retired, claim_tests, decide_next, folds, brief_criteria, exact_config_1b, exclusion_digest_input, config_direct_authoring, nearest_build, variant_selection_record, grid_evaluation.

## Code-side facts met on the way (not file findings)

- STAGE_CONFIGS names three handoff files that do not exist in `templates/handoffs/`: `backtest_spec_to_data_availability_gate.yaml` (RP:209; written by `_create_remaining_handoffs`, RP:9842-9868), `protocol_to_analyst.yaml` (RP:232; `_ensure_analyst_handoff`) and `specialist_readers_to_regroup_record.yaml` (RP:243; `_REGROUP_RECORD_HANDOFF`, written by code, RP:8837). The last name still carries the deleted stage name.
- `skills/hypothesis-design/SKILL.md:24` says "When `CLAIM_TESTS_EXECUTION.md` is among your inputs"; no step 1a loader adds it (see the CLAIM_TESTS_EXECUTION finding), so that condition cannot occur at 1a.
- `templates/hypothesis_card.yaml:24-29` shows five `statement` keys; `hypothesis-design/SKILL.md:40,79` lists six (adds `predicts_kind`). The template has no loader.
- DATA_DICTIONARY.md:69 cites `tools/build_reports.py` and says it was deleted in D-198; DATA_DICTIONARY.md:9-10, 433 describe the removed readers' sections. Both are accurate, not counted.

## Not checked

- Semantic accuracy of the numeric thresholds, table values and behaviour descriptions inside the long skills (verdict-interpreter rules 1-6 and thresholds, strategy-config-authoring and innovation-expansion body text, analyst SKILL.md body, CLAIM_TESTS.md and CLAIM_TESTS_TRADE.md rules, quant-fundamentals identities) against the code. Only the items named above were compared; a test keeps CLAIM_TESTS.md's block list equal to tools/claim_tests.py.
- The body of docs/DATA_DICTIONARY.md, docs/STRATEGY_DESIGN_GUIDE.md and docs/COMPONENT_CATALOG.md (about 150 KB) against the code; only the scripted checks (a-e) were run on them, and file:line citations were checked only where listed.
- The run-relative artifact names (`artifacts/...`) were checked only for being mentioned somewhere in RP, RC or tools/*.py, not for being written by the stage the skill says.
- Whether each `reason:` text in the handoff templates matches what the stage's code now adds or removes (closed-book, B7, exclusion-digest, config-direct unions).
- Config files pasted as data (config/cost_model.yaml, config/coin_universe.yaml, config/criterion_menu.yaml, config/indicator_library.yaml, campaign_record/*) and the JSON schemas under workflow_artifacts/schemas/: not part of this scope.
- Prompt text built inside the .py files themselves (objective, constraints, stop_conditions written by code, e.g. RP:9842-9945) and the gemini worker's copy of the loader (RP:1580-1590, dead per the note at RP:3844-3849).
- Written-out dates in other forms (e.g. "Q4 2026", week numbers) and dates split across lines; the scan covered YYYY-MM-DD, YYYY/MM/DD, YYYYMMDD, YYYY-MM and month-name forms, and found only the two lines reported.
- Whether research-system-evolution/SKILL.md and regime-auditor/SKILL.md are loaded by an operator-side tool outside the repo (no .claude/skills directory exists in the checkout).
- guided_tour/ and everything sealed by COMMON_RULES.md were not opened.
