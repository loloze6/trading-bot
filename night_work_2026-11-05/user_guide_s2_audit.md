# USER_GUIDE §2 fact-check (night work 2026-11-05)

File: `strategy-research/docs/USER_GUIDE.md` (SR = strategy-research/, RP = SR/workflow/run_phase1_research.py,
RC = SR/workflow/run_campaign.py). Line numbers in the table are the guide's lines **after** the edits.

## Section bounds

§2 "Workflow Overview" runs from line 150 (`## 2. Workflow Overview`) to line 2002, the line before
`## 3. Artifacts`, at 2003 before and after the edits. That is much longer than the "roughly 150-700"
in the brief: it holds §2.1 Stage Map, §2.2 index table and terms, §2.2.x stage blocks (research_brief,
stages 2, 15, 3, 4, 6, 14, 8, 9, regime_auditor, 11, 18, grid route, 17, 12, 13) and §2.3 routing
tables. I checked the whole section.

## Sources checked

- RP `STAGE_CONFIGS` (RP:156-245, 12 entries), `_SKILL_MAP` (RP:1019-1027, 7 entries).
- The routing functions `determine_post_validation_route` (RP:9766), `determine_post_refinement_route` (RP:9749),
  `determine_post_spec_route` (RP:19564), `determine_post_verdict_route` (RP:16117),
  `determine_post_campaign_review_route` (RP:16292), `_route_holdout_evaluation` (RP:15699),
  `_apply_circuit_breaker` (RP:15822), `_route_escalate` (RP:11906) and `_route_campaign_terminate`.
  Also the `run_loop` routing block (RP:20153-20630).
- The flag readers (`_*_enabled`, dependency raises), `config/campaign_config.yaml` (committed
  orchestrator defaults) and `config/feature_flag_register.yaml` (states).
- The handoff templates `workflow_artifacts/templates/handoffs/*.yaml`. Also the code that adds inputs to a
  handoff (`_apply_b7_mandatory_inputs`, `_apply_closed_book_inputs` / `_CLOSED_BOOK_STAGE_INPUTS` at
  RP:3161-3208, `_apply_*_context`) and `_create_remaining_handoffs` (RP:9855-9938).
- The SR/tools/ files and symbols named in §2: all exist, except `tools/build_reports.py`, which D-198 deleted.

## Statements checked

**About 175 statements checked**:

| Verdict | Count |
|---|---|
| OK | 145 |
| FIXED | 20 (19 diff hunks) |
| WRONG-NOT-FIXED | 7 |
| UNCHECKABLE | 4 |

## Non-OK statements

| Guide line | Statement | Verdict | Correct fact (file:line) | old -> new |
|---|---|---|---|---|
| 271 | "Under the readers/regroup flags the graph already reads protocol_execution → analyst → regroup_record → the grid's route" | FIXED | The readers flag was deleted (D-198). The grid route is keyed on `grid_evaluation` (`_grid_route_enabled`, RP:4011-4018). | "readers/regroup flags" -> "grid/regroup flags" |
| 362 | `STAGE_CONFIGS` "holds 11 entries" | FIXED | 12 entries (RP:156-245; also SR/CLAUDE.md §1) | "11 entries" -> "12 entries" |
| 468 | Stage 2 input `config/available_feeds.yaml`, "consulted by the skill" | FIXED | D-195 dropped it from `research_brief_to_hypothesis.yaml` (`tests/test_d195_skills_handoffs.py:104-113`). The hypothesis-design SKILL.md does not mention it, and no code adds it to a closed-book prompt (`_CLOSED_BOOK_STAGE_INPUTS`, RP:3161). | "consulted by the skill" -> "not an input since D-195 (dropped from the handoff; no code adds it)" |
| 474 | `hypothesis_card.yaml` read by "innovation_expansion, validation" | FIXED | The validation handoff requires only `expanded_hypothesis_card.yaml` (`innovation_expansion_to_validation.yaml:6-8`), and no code adds the card for `validation`. `hypothesis_to_strategy_config_authoring.yaml:15` requires it. | "innovation_expansion, validation" -> "innovation_expansion, strategy_config_authoring (flag on)" |
| 653 | Diversity rule lives at `innovation-expansion/SKILL.md:74-105` | FIXED | The "IMPROVEMENT 04 — Real Diversity Check" section is at SKILL.md:55-104 | ":74-105" -> ":55-104" |
| 684 | Stage 4 input includes `hypothesis_card.yaml` | FIXED | Same as line 474: not in the validation handoff or any code-added input (RP:3161-3208, RP:3088-3106) | removed "`hypothesis_card.yaml`," |
| 774 | Stage 6 input `validation_decision.yaml` | FIXED | The handoff requires `expanded_hypothesis_card.yaml` and `validation_protocol.yaml` (`validation_to_backtest_specification.yaml:10-14`) | "`validation_decision.yaml`" -> "`validation_protocol.yaml`" |
| 780 | Stage 6 output: candidate config, decision, variant_selection | FIXED (omission) | The LLM deliverables are `backtest_spec.yaml` and `decision.yaml` (template:22-24). Code writes `candidate_strategy_config.json` from `backtest_spec.yaml`'s `config` (RP:20266-20279). | added "`backtest_spec.yaml`" and "(its `config`, written by code)" |
| 842 | data gate: "the one flag in this codebase that ships on" | FIXED | The committed config also ships `exclusion_digest_input`, `stale_input_path_fix`, `variant_selection_record` and `schedulability_block` on. The gate's flag is the only one whose reader **defaults** on (`.get("enabled", True)`, RP:3702; docstring RP:3684-3698). | "ships on" -> "defaults on" |
| 886-889 | data gate design rationale: "Off by default, unlike every other stage … so it ships opt-in first" | FIXED (the requested re-check) | On by default since delivery_plan_v26 s:0.4 item 14 (RP:106-115, RP:3684-3698). Committed `data_availability_gate.enabled: true`. Register state `on`. | -> "Shipped off by default at first (2026-09-11): … so it shipped opt-in first (bit-identity discipline). delivery_plan_v26.md s:0.4 item 14 turned it on by default (2026-09-20)." |
| 951 | E-016 "not yet merged to master (branch feat/e016-…): once landed, a cost-dominated kill … is meant to feed" | FIXED | E-016 is in the code: `fee_reduction_metrics` (SR/tools/run_protocol.py:1226), `candidate_system` enum (`verdict_interpretation.schema.json:120-127`), IMPROVEMENT 10 (`verdict-interpreter/SKILL.md:740`). | -> "merged to master: a cost-dominated kill … feeds" |
| 992-993 | `--diagnostics-only` "so the category reports and the trial row keep their inputs" | FIXED | D-198 deleted the category reports (`tools/build_reports.py` is gone). | -> "so the trial row keeps its inputs" |
| 1017-1019 | C5.8: "`reports/profitability.yaml` drops verdict/… (`build_reports(legacy_verdict_retired=True)`)" | FIXED | `tools/build_reports.py` was deleted (D-198). What remains is `run_protocol.py --legacy-verdict-retired` (run_protocol.py:2365-2372, 2796-2797), passed under `_promotion_retired_enabled` (RP:1745-1752). | -> "`run_protocol.py` gets `--legacy-verdict-retired` (the legacy top-level `verdict` is recorded as null; the category reports that also dropped it were deleted with `tools/build_reports.py`, D-198)" |
| 1098 | "The `pass_rule_evaluation.yaml` step is invisible in §3 — it has no artifact entry" | FIXED | §3 has `### pass_rule_evaluation.yaml` (guide line 2788) | -> "had no §3 artifact entry; it now has [one](#pass_rule_evaluationyaml)" |
| 1258 | Stage 11: "`config/coin_universe.yaml` and `innovation_notes.yaml`, if available, feed the asset-stability gate" | FIXED | This contradicted the same paragraph ("`innovation_notes.yaml` is still not an input of this stage"). The verdict_interpreter closed-book inputs have no innovation_notes (RP:3187-3205), and neither does the vi handoff (RP:9895-9925). | -> "`config/coin_universe.yaml` feeds" |
| 1262-1265 | Stage 11: grid_evaluation/idea_status "are optional inputs … not yet wired to override this stage's own verdict … routing isn't binding yet" | FIXED | Neither file is in the vi handoff (RP:9903-9925). With `grid_evaluation` on, protocol_execution routes to analyst/regroup_record/grid route, so verdict_interpreter is unreached (RP:20177-20187), and the grid route is binding (`determine_post_specialist_readers_route`, RP:5403). | -> "are not inputs of this stage: with `orchestrator.grid_evaluation.enabled` on, the route comes from `idea_status.yaml` and this stage is unreached (D-198, "Route from the grid" below)." |
| 1280 | Stage 11 item 2: "see stage 10" | FIXED | The guide no longer numbers regime_auditor as stage 10 (its own block, line ~1174) | -> "see the `regime_auditor` block" |
| 1841 | Stage 13 output "updated campaign_data_policy.yaml (`holdout_consumed_by`, `consumed_at`)" | FIXED | The orchestrator writes only `holdout_consumed_by` (`_mark_holdout_consumed`, RP:6694-6720). `consumed_at` appears nowhere in RP; it is a `holdout_result.yaml` field (`holdout_result.schema.json:12,61`). | removed "`consumed_at`" |
| 1869 | Stage 13 item 4: "`consumed_at` is stamped, then `status` is read" | FIXED | RP:15788-15789: `_mark_holdout_consumed(policy, consumed, hyp_id)`, then status | -> "The `hypothesis_id` is added to `holdout_consumed_by`, then `status` is read." |
| 1958 | §2.3 after campaign_review: `terminate` → "write research_decision" | FIXED | `_route_campaign_terminate` writes `ROOT/campaign_decision.yaml`, sets campaign status `space_empty` and returns `completed_rejected` | -> "write `campaign_decision.yaml`" |
| 445-446, 477-480 | Stage 2: "the skill is instructed to write `edge_source` before `signal_concept`" / "A1.1–A1.3 (populate edge_source before signal_concept) … live in the skill prompt" | WRONG-NOT-FIXED | hypothesis-design SKILL.md (D-190 rewrite, 84 lines) has no `signal_concept` and no A1.x rule. `edge_source` is a field list (SKILL.md:34,75). Fixing it means rewriting the rationale paragraph and item 1. | — |
| 483-489 | Stage 2 items 2-3: `evidence_type` "chosen from `config/available_feeds.yaml`"; a signal needing a missing feed "routes to `feed_wishlist.yaml`" | WRONG-NOT-FIXED (ambiguous) | D-195 removed A1.2/available_feeds/feed_wishlist from the handoff and the skill (test_d195_skills_handoffs.py:104-133), and no code routes a card to feed_wishlist. But `hypothesis_card.schema.json:76,84` still describes the A1.2 rule. It needs an owner decision on the schema text. | — |
| 1773-1784 | Stage 17 item 16 score_provenance (b)/(c): `rubric_version` must be `<category>-reader-v2` "pinned to the five SKILL files". It also describes reader citation checks and reader retry. | WRONG-NOT-FIXED | D-198 deleted the reader skills and stage. `READER_RUBRIC_VERSIONS` still exists (tools/reader_proposals.py:56-62), but regime_power is `-v3`. Under the flag the analyst's rubric is also accepted (RP:5045-5047). This needs a paragraph rewrite. | — |
| 1563-1565 | Stage 17 item 7: "carries the route flag-off runs take in the readers' own iteration" | WRONG-NOT-FIXED (ambiguous) | The readers stage was deleted (D-198). The intended meaning (the same-iteration grid route, RP:20177-20187) is unclear, so I did not reword it. | — |
| 1946 | Circuit breaker "Same instrument/timeframe escalated 2× with no improvement → Force terminate or campaign_review" | WRONG-NOT-FIXED (ambiguous) | I found no such check: `_apply_circuit_breaker` (RP:15822-15857) has only the two breakers in the rows above. The nearest code is `_route_escalate`: once all instruments are exhausted it returns `completed_rejected` and does not return `campaign_review` (comment, RP:11906+18). Someone who owns E037-32 must decide whether to delete the row or reword it. | — |
| 1881-1883 | Stage 13 notes: "The guide's §2.2 row names gates 1 and 2 only" | WRONG-NOT-FIXED | The §2.2 row (line 323) names no gates. This is a historical note, so I left it. | — |
| 1788-1806 | Stage 12 stage input `campaign_state.yaml` | WRONG-NOT-FIXED (minor) | The campaign_review template's path `../../campaign_state.yaml` (campaign_review.yaml:11) does not resolve after the E-002 move. The real file is `campaign_record/campaign_state.yaml` (RP:93). `_STALE_INPUT_PATH_FIXES` covers only optional inputs. This is a code/template defect, not a guide error. | — |
| 607-610 | Stage 3: "139 generated, 36 tested, 103 discarded … no run has ever built more than one config" | UNCHECKABLE | These are measured run counts, and I did not open `runs/` | — |
| 633-634 | Stage 3: "of 25 unconstrained expansion runs, 21 land in [3,6]" | UNCHECKABLE | measured run data | — |
| 1639-1640 | Stage 17 item 13: `failed_families` "already holds 9 distinct families" | UNCHECKABLE | live campaign_state content | — |
| 1856-1858 | Stage 13 gate 2b: "0 of 57 briefs in the tree carry the key" | UNCHECKABLE | measured counts | — |

Outside §2 (not edited, for the lead): §3 `holdout_result.yaml` (line 2736) says
"orchestrator (marks consumed_at)". The orchestrator does not write `consumed_at` (see line 1841 above).

## data_availability_gate default: consistency across the guide

All mentions now say on by default with an explicit `false` to skip: lines 206-209 (map), 313 (§2.2 table),
829 (stage 6 routes), 840-848 (stage 14 Runs), 886-889 (rationale, fixed tonight), and 1910 (§2.3).
`grep -n -i 'data.availability' USER_GUIDE.md` shows no other default statement.

## OK statements (summary, not listed one by one)

These matched the code:
- Every stage's `default_next` and handoff name.
- The engine tags. `_SKILL_MAP` has 7 entries. `_build_stage_prompt` raises when a stage has no skill (RP:1046-1049).
- The `validation` alias for validation_gate.
- Flag defaults and dependencies:
  - `config_direct_authoring`, `variant_loop`→`config_direct_authoring`, `analyst`→`folds` only,
    `regroup_record`→`grid_evaluation`, `decide_next`.
  - `verdict_routing_retired`→`decide_next` + `profit_bars_every_backtest`.
  - `composition_runs`→four flags, `nearest_build`→`config_direct_authoring` + `claim_tests`,
    `profit_bars_v2`→`profit_bars_every_backtest`, `score_provenance` with no dependency.
  - `exclusion_digest_input` on, `variant_anti_adjacency_gate` off.
- Routes:
  - Validation: approve/conditional_approve, refine with `implementation_allowed`, refinement limit 2, reject.
  - Stage 6 spec routes, including fail-closed on an unknown status.
  - Data gate: validate/refine/decline, plus parking under the retired-routing flag.
  - Holdout gates, in order: DSR → single-use → research_only → pause → consume → pass/fail/inconclusive.
  - Campaign-review routes: continue/reframe/escalate_*/terminate, with `escalate_component` → human pause.
  - Breakers 1, 2 and 4. The 1,800,000 token budget and `_load_token_budget`.
- Regime detector: the 30-day freshness check, silent `None` returns, the retune firewall terms and its raise.
- The `--unpark` CLI and `holdout_decision.yaml`.
- Every `file::symbol` anchor I sampled in §2 resolves: about 40 RP/tools symbols.
- Analyst lens/category names, audit-log key and handoff.
- regroup_record lock file and 30 s wait, schemas, and tool files.
- 5% gap tolerance and the `"binance"` fallback.
- 15 indicator library entries, `review_every_n_runs` 6 and `dsr_min_same_basis_trials` 10.

## Tests

Run from SR/ with `CI=true PYTHONDONTWRITEBYTECODE=1 <venv>/bin/python -m pytest -q`, covering every SR/tests file that
reads USER_GUIDE.md:

- test_guide_covers_the_code.py
- test_user_guide_field_tables.py
- test_user_guide_toc.py
- test_doc_anchors.py
- test_e059_6c_s2a_route_retirement.py
- test_e059_6c_s2b_campaign_review.py
- test_e059_6c_s2d_holdout_unlock.py
- test_e059_s2b_briefs.py
- test_e059_s2b_review_fixes.py
- test_e068_4_approval_cap_warnings.py

Result: **407 passed, 3 skipped**, no failures. No edited string was pinned by a test (I grepped SR/tests and
TB/tests for each old string). No fix was withheld because of a test.

Only `strategy-research/docs/USER_GUIDE.md` was edited, and it was clean against HEAD before the edits. The other
uncommitted diffs in the tree (`docs/RUNBOOK.md`, `tools/README.md`) are not from this task.
