# Docs clean-up, night of 2026-11-04: review note

Scope: the operator's remarks at guided-tour stops 00 (strategy-research `CLAUDE.md`,
`DOC_INDEX.md`) and 01 (the research brief template's people-only prose), plus a
broken-pointer pass over the live docs. Working tree only; nothing staged or committed.
No code, config, schema, test or template field was changed.

Files changed:
- `strategy-research/CLAUDE.md` (rewritten, 120 -> 84 lines)
- `strategy-research/DOC_INDEX.md` (pointer fixes only; NOT deleted, see (b))
- `strategy-research/docs/RUNBOOK.md` (4 pointer fixes)
- `strategy-research/docs/USER_GUIDE.md` (3 pointer fixes)
- `strategy-research/docs/CAMPAIGN_PROGRAM.md` (1 pointer fix)
- `strategy-research/workflow_artifacts/templates/research_brief_new_pipeline.md` (guidance comments only)

## (a) strategy-research/CLAUDE.md: old section/rule -> where it went

New layout, in the categories the operator named: **1. Objective and overview**
(with a short "Workflow stages"), **2. Behaviour rules**, **3. Development and test
process**. It opens with one line saying the root `CLAUDE.md` hard rules (secrets,
no lookahead, trial ledger, sealed holdout) and working rules apply and are not repeated.

| Old section / rule (old line) | Now |
|---|---|
| Header: "Start with `DOC_INDEX.md`" (3-4) | Replaced by a direct "Where to read" list in §1 (USER_GUIDE, RUNBOOK, CAMPAIGN_PROGRAM + queue, EPICS, DECISION_LOG). The pointer to DOC_INDEX was dropped because the operator wants it retired (it still exists, see (b)). |
| `## Project`: research-only strategy factory (6-7) | Kept, §1 |
| `## Objective`: generate, expand, validate, backtest, analyze, decide (9-10) | Kept, §1 |
| Global rule: use structured artifacts for all handoffs (13) | Kept, merged into §3: "Prefer structured YAML/JSON artifacts over prose for anything a stage or tool reads" (the pipeline already enforces it through the handoff templates). |
| Global rule: never pass full transcript/history by default (14) | Kept, §2 (minimal-context bullet) |
| Global rule: load only the files needed (15) | Kept, §2 (minimal-context bullet) |
| Global rule: innovation happens before validation (16) | Dropped: it describes the stage order, which `STAGE_CONFIGS` and the routing functions set; it is not an agent behaviour (operator: keep only behaviour rules). |
| Global rule: validation is falsification-first (17) | Dropped. Operator stop 00: it "led to unexpected behavior"; it is a stage persona trait (the `quant-validation` skill), not an agent behaviour. |
| Global rule: screening, then walk-forward, then holdout (18) | Dropped: workflow, and stale (there is no screening stage; the holdout is reached only from the `profit_bars_reached` stop plus an operator unlock, `docs/OPERATOR_UNLOCK_HOLDOUT.md`, RUNBOOK §3). The behaviour rule on the holdout stays in the root `CLAUDE.md` hard rules, which §0 of the new file says apply. |
| Global rule: large outputs to files, not inline (19) | Kept, §2 |
| Global rule: after each stage, write a short summary artifact (20) | Dropped: workflow; the pipeline writes each stage's artifacts and handoffs in code. |
| Schemas block (22-34) | Block removed (operator: does not belong here). Its one rule is kept as a single §3 line: schemas only warn (blocking only under `WORKFLOW_ARTIFACT_VALIDATION=raise`), so a rule that must stop a run is written in code where the value is read. The history (E037-09 correction, C5.7a list) is dropped; the mechanism is documented in `tools/workflow_artifact_validation.py`'s docstring and USER_GUIDE stage 17. Nothing to move to RUNBOOK: it is not an operating procedure. |
| `## Workflow stages`: "USER_GUIDE §2.2 is authoritative" (38-40) | Kept, reworded: the code is the source of truth (`workflow/run_phase1_research.py::STAGE_CONFIGS` + the `determine_post_*` functions), USER_GUIDE §2 describes them. |
| 12-stage list (42-48) | Corrected (operator: "Pipeline stages are wrong"). It listed `research_brief` (an input), `regime_detector_validation` (a helper) and `regime_auditor` (never dispatched), and missed `strategy_config_authoring`, `analyst` and `regroup_record`. Now: the 12 `STAGE_CONFIGS` keys, read from the code: hypothesis_generation, strategy_config_authoring, innovation_expansion, validation, backtest_specification, data_availability_gate, protocol_execution, verdict_interpreter, analyst, regroup_record, campaign_review, holdout_evaluation. |
| Caveat paragraph (52-98): specialist_readers deleted (D-198), route keyed on `grid_evaluation`, analyst/regroup_record flags, verdict_routing_retired, data_availability_gate default on, no prescreen, regime_* not dispatched, no refinement_planner, config-direct flow | Dropped as workflow description: each point is in USER_GUIDE §2.1 (config-direct and verdict-routing-retired variants), §2.2 (stage table) and "Route from the grid". One example kept in §1: "with `orchestrator.verdict_routing_retired.enabled` on, a run ends after `regroup_record`" (also required: `tests/test_e059_6c_s2a_route_retirement.py::test_flag_documented_in_guide_runbook_and_index` asserts this key is in `CLAUDE.md`). |
| Convention inside the caveat: a new stage is registered unconditionally and routed only when its flag is on (88-98) | Kept as a §3 rule (it is a development convention; `tests/test_e056_config_direct_authoring.py` cites it). |
| Stage 4 is `validation_gate` in docs, `validation` in code (99-100) | Kept, §1 |
| Context policy: default to minimal context (103) | Kept, §2 |
| Context policy: max 3 required reads per stage unless justified (104) | Kept, §3 (it constrains how a stage's inputs are designed) |
| Context policy: prefer YAML/JSON over prose (105) | Kept, §3 (merged with the handoff rule above) |
| Tests: interpreter paths, run from `strategy-research/` (108) | Kept, §3 |
| Tests: `TBOT_PYTHON` first; never junction a venv into a worktree (109) | Kept, §3 |
| Tests: while developing, run only touched files and neighbours (110) | Kept, §3 ("seconds to a minute" dropped) |
| Tests: CI runs the fast suite on every push; read `gh pr checks`; do not also run locally before every push (111) | Kept, §3 (CI durations "~8 / ~14 min" dropped as detail) |
| Tests: slow tests never in CI; `python run_tests.py --slow` when touching data fetching or regression backtests (112) | Kept, §3 |
| Tests: local fast suite only when CI cannot be used or for a large refactor, `-n 4` not 8 (113) | Kept, §3 (the timing measurements dropped; the reason for 4, crashed workers on memory, kept) |
| Tests: never re-run a full suite for a test-only/doc-only follow-up; say so in the PR (114) | Kept, §3 |
| Tests: one test process at a time (115) | Kept, §3 |
| Runtime records: `runs/` ignored, never stage; back up outside git; run_0001..run_060 tracked (118) | Kept, §2 |
| Runtime records: `campaign_record/` committed once per session as a docs PR; `composite/` ignored cache (119) | Kept, §2 |
| Runtime records: nothing staged between sessions; never `git clean` in the main checkout (120) | Kept, §2 |

Moved to RUNBOOK: nothing. No part of the old file was an operating procedure that
RUNBOOK lacks: the long chapters were workflow description (covered by USER_GUIDE) or
behaviour/test rules (kept here, condensed).

Pointers removed from the file (each checked): `DOC_INDEX.md` (exists; operator wants it
retired), `engineering/roadmap/E-037/FINDINGS.md#e037-09` (exists; history of the schemas
block), `delivery_plan_v26.md` s:0.4 item 14 (exists; history), `feature_flag_register.yaml`
(exists under `config/`; part of the dropped caveat), `E054_DATA_AVAILABILITY_GATE` (an env
var the code removed: legacy). Every pointer left in the new file was checked to exist.

Approval and launch rules: the old file carried none; they are in the root `CLAUDE.md`
working rules (unchanged) and RUNBOOK §0b.

Two live references to the old file's content were adjusted or checked:
- `docs/RUNBOOK.md:281` cited `strategy-research/CLAUDE.md` for the config-direct flow,
  which the file no longer describes; the citation now names only `docs/USER_GUIDE.md` §2.1/§2.2.
- `workflow_artifacts/skills/campaign-review/SKILL.md:187` cites "`strategy-research/CLAUDE.md`'s
  Workflow stages". Not changed (a skill is a stage prompt input, out of scope); the heading
  "Workflow stages" was kept so the citation still resolves. The same sentence also names stages
  that no longer exist (`screening_backtest`, `walk_forward_validation`): for a later skill review.

## (b) DOC_INDEX.md: NOT deleted

Two tests read the file and would fail with `FileNotFoundError` if it were deleted:
- `strategy-research/tests/test_e059_6c_s2a_route_retirement.py:201`
  (`test_flag_documented_in_guide_runbook_and_index`: asserts `orchestrator.verdict_routing_retired.enabled` is in `DOC_INDEX.md`)
- `strategy-research/tests/test_e059_6c_s2d_holdout_unlock.py:627`
  (`test_schema_documented_and_no_not_built_leftovers`: reads `DOC_INDEX.md`)

No CI step, `run_tests.py` or tool reads it. Deleting it needs those two tests changed first
(drop `"DOC_INDEX.md"` from the two tuples): a test change, for the lead.

Since it stays, it was treated as a live doc for (c). References to it were left in place
(they resolve): `trading-bot/DOC/USER_GUIDE.md:3`, `strategy-research/docs/RUNBOOK.md:3`,
`strategy-research/docs/USER_GUIDE.md:3` (the last two had a broken relative link, fixed in (c)).
Only one reference was removed: the opening line of `strategy-research/CLAUDE.md` (see (a)).
References in history (`SESSION_LOG.md`, `DECISION_LOG.md` rows, `engineering/` findings and
session logs, `tasks/o3_inventory.md`) were not touched.

If DOC_INDEX is deleted later, the live references to repoint are exactly:
`trading-bot/DOC/USER_GUIDE.md:3`, `strategy-research/docs/RUNBOOK.md:3`,
`strategy-research/docs/USER_GUIDE.md:3` (the "Not sure this is the doc you need?" line;
suggested replacement: `strategy-research/CLAUDE.md` §1 "Where to read"), plus the two tests above.

## (c) Broken pointers

Method: a scan of relative markdown links and backticked paths in `FORK_CHANGES.md`,
`strategy-research/*.md`, `strategy-research/docs/*.md`, `trading-bot/README.md` and
`trading-bot/DOC/*.md`, each resolved against the doc's folder, `strategy-research/`,
the repo root and `trading-bot/`. After the fixes, every relative markdown link resolves.

Fixed (file:line, old -> new):

| Where | Old | New |
|---|---|---|
| `strategy-research/DOC_INDEX.md:22` | link text `HANDOFF_CURRENT.md` (no such file; the link target was right) | `HANDOFF_20260724.md` |
| `strategy-research/DOC_INDEX.md:42` | `[RUNBOOK.md](RUNBOOK.md)` | `[docs/RUNBOOK.md](docs/RUNBOOK.md)` |
| `strategy-research/DOC_INDEX.md:100` | `[campaign_summary.md](campaign_summary.md)` | `campaign_record/campaign_summary.md` |
| `strategy-research/DOC_INDEX.md:104` | `[campaign_log.md](campaign_log.md)` | `campaign_record/campaign_log.md` |
| `strategy-research/DOC_INDEX.md:242` | `[RUNBOOK.md](RUNBOOK.md) section 3` | `docs/RUNBOOK.md` |
| `strategy-research/DOC_INDEX.md:268` | `skills/{name}/SKILL.md` | `workflow_artifacts/skills/{name}/SKILL.md` |
| `strategy-research/DOC_INDEX.md:281` | `docs/plan/` | `engineering/improvements/done/design_and_docs/` (per `docs/RESTRUCTURE_MAPPING.tsv`) |
| `strategy-research/DOC_INDEX.md:299` | `[SESSION_LOG.md](SESSION_LOG.md)` | `engineering/sessions/SESSION_LOG.md` (per `docs/RESTRUCTURE_MAPPING.tsv`) |
| `strategy-research/DOC_INDEX.md:313` | "Cross-linked from the top of `RUNBOOK.md`, `docs/USER_GUIDE.md`, and `CLAUDE.md`" | `docs/RUNBOOK.md`, `docs/USER_GUIDE.md` and `../trading-bot/DOC/USER_GUIDE.md` (CLAUDE.md no longer links it) |
| `strategy-research/docs/RUNBOOK.md:3` | `[DOC_INDEX.md](DOC_INDEX.md)` | `(../DOC_INDEX.md)` |
| `strategy-research/docs/RUNBOOK.md:229` | `(engineering/improvements/done/IMPROVEMENTS_DONE_20260712.md)` | `(../engineering/improvements/done/IMPROVEMENTS_DONE_20260712.md)` |
| `strategy-research/docs/RUNBOOK.md:281` | `(strategy-research/CLAUDE.md, docs/USER_GUIDE.md §2.1/§2.2)` | `(docs/USER_GUIDE.md §2.1/§2.2)` |
| `strategy-research/docs/RUNBOOK.md:696` | `trading-bot/PIPELINE_IMPROVEMENTS_20260712_v4.md` | `engineering/improvements/done/IMPROVEMENTS_DONE_20260712.md` (renamed in commit `c78f6578`; the A12/A13/C11/D4 ids are that ledger's) |
| `strategy-research/docs/USER_GUIDE.md:3` | `[DOC_INDEX.md](DOC_INDEX.md)` | `(../DOC_INDEX.md)` |
| `strategy-research/docs/USER_GUIDE.md:3614` | glossary "Schema": `schemas/` | `workflow_artifacts/schemas/` |
| `strategy-research/docs/USER_GUIDE.md:3615` | glossary "Skill": `skills/` | `workflow_artifacts/skills/` |
| `strategy-research/docs/CAMPAIGN_PROGRAM.md:38` | "committed as `docs/ROADMAP.md`" | adds "(since renamed `docs/CAMPAIGN_PROGRAM.md`, this file)" (renamed in commit `0f07e331`) |

Left as they are (why):

| Where | Pointer | Why left |
|---|---|---|
| `FORK_CHANGES.md` (all rows) | `.omc/`, `.claude/commands/`, `venv/`, `.venv/`, `/pyrightconfig.json`, `strategy-research/requirements-mac.txt` (now `config/requirements-mac.txt`), `workflow/stages.yaml:54`, `run_phase1_research.py:4885` and similar | A dated record of divergences: each path is what existed when the row was written (several are machine-local or gitignored by design). Treated as history. |
| `strategy-research/docs/RUNBOOK.md:620` | `docs/00_closing_state.md` section 7 | Ambiguous: the name now has two homes (`engineering/improvements/done/IMPROVEMENTS_DONE_20260706.md`, "formerly 00_closing_state.md", and the archived snapshot `engineering/improvements/done/design_and_docs/00_closing_state.md`), and the sentence is historical. |
| `strategy-research/docs/USER_GUIDE.md:2030` | `schemas/research_brief.schema.json` | No such schema exists anywhere (`workflow_artifacts/schemas/` has none for the brief). Needs a content decision, not a path fix. |
| `strategy-research/docs/VERIFICATION_DOCTRINE.md:192, 194` | `strategy-research/tests/test_prescreen_degenerate_signal_gate.py`, `.../test_turnover_proxy.py` | Neither file exists; no successor is identifiable (shallow clone, no history). The doctrine cites them as examples. |
| `strategy-research/DOC_INDEX.md:273` | skill `refinement-planner` | The skill folder does not exist (the stage was removed, E-039 S4). Stale content rather than a path; left for the DOC_INDEX decision. Same for "required input for ... `refinement-planner`" at line 79. |
| `strategy-research/DOC_INDEX.md:59-61`, `docs/DATA_DICTIONARY.md:69`, `docs/USER_GUIDE.md:1344, 1387, 1428, 3742` | `DATA_DICTIONARY_READERS.md`, `tools/data_dictionary.py`, `tools/build_reports.py`, `tests/test_near_miss_scoreboard_firewall.py`, `campaign_record/reader_skips.yaml` | Each sentence says the file was deleted. Correct as written. |
| `strategy-research/DOC_INDEX.md:261`, `docs/USER_GUIDE.md:86, 160, 3424, 3559` | `workflow/stages.yaml` | Each says it is archived. Correct as written. |
| `docs/USER_GUIDE.md:1764, 1988`, `docs/RUNBOOK.md:739`, `DOC_INDEX.md:221` | `campaign_record/trial_sharpe_basis_recompute.yaml`, `campaign_record/compositions.yaml` | Runtime files the code writes when the feature runs; absent until then. |
| `docs/USER_GUIDE.md:784, 898, 944, 1598` | `handoffs/config_direct_*.yaml`, `../../campaign_record/campaign_memory.yaml` | Per-run paths (inside `runs/<id>/`), not repo paths. |
| `docs/USER_GUIDE.md:2691` | `config/detector_wishlist.yaml` | An example value of a legacy field in run_039's file, quoted as it was. |
| `docs/USER_GUIDE.md:3646-3647` | `strategy-research/results/protocols/...` | Quoted historical finding. |
| `docs/RUNBOOK.md:17, 26` | `trading-bot/strategy-research/` | "trading-bot" is the checkout folder's name here, not the `trading-bot/` subfolder; correct for a clone named that way, ambiguous otherwise. |
| `docs/RUNBOOK.md:124`, `docs/USER_GUIDE.md` (several) | `quant-fundamentals/SKILL.md`, `strategy-config-authoring/SKILL.md`, `innovation-expansion/SKILL.md` | Shorthand inside a sentence that already names `workflow_artifacts/skills/` (or quotes an error message). Resolves. |
| `trading-bot/DOC/STRATEGY_FRAMEWORK.md:61` | `trading-bot/docs/STRATEGY_FRAMEWORK.md` | Provenance note naming a stale copy that no longer exists, on purpose. |
| Bare file names (`run_protocol.py`, `metrics.py`, `bars.csv`, ...) | many | Unqualified names of files that exist, or of run artifacts; not paths. |

Not in scope, seen in passing (for the lead):
- `strategy-research/docs/RUNBOOK.md`, "Standing rules" (about line 1115), writes the sealed
  holdout's date range out literally, against the root hard rule (refer to it only through
  `config/campaign_data_policy.yaml`). It is registered in `config/holdout_gate_exemptions.txt`
  (count 1, as is a line in `docs/USER_GUIDE.md`), so the gate passes. Not changed: the task did not
  ask for it, and the exemption entry should be retired in the same change.
- `docs/USER_GUIDE.md` §2.2's table says `data_availability_gate` is "Off by default (E-054)",
  while the §2.1 map says "ON BY DEFAULT since 2026-09-20". A content inconsistency, not a pointer.

## (d) Research brief template, people-only prose (operator stop 01)

File: `strategy-research/workflow_artifacts/templates/research_brief_new_pipeline.md`
(the template that `workflow/run_campaign.py` and `RUNBOOK.md` §1e name for new briefs).

Change: below the frontmatter, after the existing "Prose below the closing `---`..." paragraph
(left as is), one HTML comment block of guidance: the context (who writes the prose and when,
direction adds the Ratification section), the purpose in one line (let a later reader see in
under a minute what idea is tested and why it deserves a run; do not repeat the fields), what to
write in order (why this idea and why now, what the result would change, anything without a field),
how to write it (plain words, short sentences, no jargon, keep the idea as stated), and a
suggested maximum of about 200 words. Under the Ratification heading, two one-line comments: what
PURPOSE holds (the roadmap item and the question), and how pre-registered outcomes are written
(A., B., ..., before the run, so the review names which happened, as the root working rules ask).

Not changed: the frontmatter (every field, comment and placeholder), the title line, the three
headings (`## Ratification (direction; people only)`, `### PURPOSE`, `### Pre-registered outcomes`).
No field was added, renamed or made optional; the operator's field-design questions at stop 01
(optional fields, claim and fold guidance in separate docs, `criteria_from`/`constraints` naming,
the scope block) are left for the design work.

Parser and test check:
- `workflow/run_campaign.py::_parse_brief_frontmatter` reads only the leading `---` block; the
  prose is never parsed. Its placeholder check scans parsed frontmatter data only.
- `tools/run_viewer/loaders.py::parse_outcomes` looks for "Pre-registered outcomes" in the
  frontmatter `constraints` list, not in the prose.
- `tests/test_e061_c1_7_first_run_kit.py` reads the template: it parses the frontmatter and
  requires each of 11 placeholder lines (e.g. `\nvenue: "<FILL IN>"\n`) to appear exactly once in
  the whole text. The added text contains no `<FILL IN` (the file still has 15 occurrences, all
  pre-existing), so the counts are unchanged.
- `tests/test_d121_brief_criteria.py:199-202` asserts the text contains "D-121" and
  `whole_test_sharpe_positive` and not "do not add one here": still true.
- No other code or test reads the template (grep of `workflow/`, `tools/`, `tests/` for the
  path and the headings).

## Checks run

No pytest is installed in this container, so the suite was not run. Checked by hand against the
tests that read the edited files: the flag key is present in `CLAUDE.md`, `DOC_INDEX.md`,
`docs/RUNBOOK.md` and `docs/USER_GUIDE.md`; no "S2d, not built" text was added; the one
`file.py::symbol` anchor in `CLAUDE.md` (`workflow/run_phase1_research.py::STAGE_CONFIGS`, read by
`tests/test_doc_anchors.py`) resolves, and the anchor count is unchanged (the old file had the
same single anchor). Line endings stay LF. Suggested targeted run:
`tests/test_e059_6c_s2a_route_retirement.py tests/test_e059_6c_s2d_holdout_unlock.py
tests/test_doc_anchors.py tests/test_e061_c1_7_first_run_kit.py tests/test_d121_brief_criteria.py
tests/test_user_guide_toc.py tests/test_guide_covers_the_code.py tests/test_user_guide_field_tables.py`.
