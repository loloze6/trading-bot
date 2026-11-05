# Round 3 clean-up fixes: review note

Scope: three approved doc/cleaning fixes. Working tree only; nothing staged or committed.
Every date from the holdout policy or the RUNBOOK passage is written below as `<DATE>`.
All reading of those passages went through a script that masks dates before printing.

Files changed (working tree):

- `strategy-research/docs/RUNBOOK.md` (FIX 1, FIX 3)
- `strategy-research/docs/USER_GUIDE.md` (FIX 1, FIX 2, FIX 3)
- `strategy-research/config/holdout_gate_exemptions.txt` (FIX 1)
- `strategy-research/DOC_INDEX.md`: deleted (FIX 3)
- `strategy-research/docs/HALT_RECOVERY.md`, `strategy-research/docs/VERIFICATION_DOCTRINE.md`,
  `strategy-research/docs/TIMEFRAME_CHANGE_PLAYBOOK.md`, `trading-bot/DOC/USER_GUIDE.md` (FIX 3)
- `strategy-research/tests/test_e059_6c_s2a_route_retirement.py`,
  `strategy-research/tests/test_e059_6c_s2d_holdout_unlock.py`: one tuple element removed in each (FIX 3)

---

## FIX 1: sealed holdout dates written out in live docs

**Method.** A script loaded `holdout_range` from `config/campaign_data_policy.yaml`, searched for
both bounds (ISO, compact and slash forms), and printed only path, line number and hit count.
The surrounding text was read through a date-masking filter. The edits were string
replacements built from the loaded values. Each one asserted exactly one match.

**Changes.**

- `strategy-research/docs/RUNBOOK.md:1115-1117` ("Standing rules")
  - old: ``Holdout (<DATE> to <DATE>) is untouchable outside `holdout_evaluation`, once per hypothesis.``
  - new: ``The sealed holdout period (dates in `config/campaign_data_policy.yaml`, key `holdout_range`) is untouchable outside `holdout_evaluation`, once per hypothesis.``
- `strategy-research/docs/USER_GUIDE.md:2771` (the `pre_registration.yaml` field table, `sample_split_design` example).
  This doc was count-pinned in the registry for the same reason as RUNBOOK: a live doc quoting the
  `holdout_range` value. So the same fix applies.
  - old: ``{holdout_range: ["<DATE>", "<DATE>"], holdout_note: "..."}``
  - new: ``{holdout_range: ["<start>", "<end>"], holdout_note: "..."}`` followed by
    ``(`<start>`/`<end>`: the sealed holdout period, dates in `config/campaign_data_policy.yaml`, key `holdout_range`)``
- `strategy-research/config/holdout_gate_exemptions.txt`
  - retired the line `strategy-research/docs/RUNBOOK.md<TAB>1` (old line 115)
  - retired the `strategy-research/docs/USER_GUIDE.md<TAB>1` entry and its 10-line explanation (old
    lines 272-282). The explanation itself quoted the `holdout_range` value.
  - The registry's own pin went from `7` to `6`, with a 3-line comment (no dates) saying why. This follows the
    file's existing "N -> M" convention. The measured count of holdout-date lines in the file is now 6.
    The older "5 -> 6 ... the docs/USER_GUIDE.md entry above ..." comment was left as written (history).
  - All other entries were kept.

**Evidence.** After the edit, a working-tree simulation of the gate's own `PATTERN` and
`AUTHORSHIP_KEYS` (extracted from `tools/holdout_date_gate.sh` at runtime) counts 0 lines for
RUNBOOK.md and USER_GUIDE.md and 6 for the registry. Before the edit, line 2771 had exactly 2
in-window matches, both of them the bounds. Its other date is outside the window.

**Gate.** `sh strategy-research/tools/holdout_date_gate.sh` scans the git index, not the
working tree.

- Run against the real index as it stands: BLOCKED. The index still holds the old RUNBOOK and
  USER_GUIDE text (1 line each, now unregistered) and the old registry (7 lines vs the new pin of 6).
  This is expected until the lead stages these files.
- Run against a scratch copy of the index with every working-tree change in this note staged into it:
  **PASS** (8616 files examined, no unregistered holdout-range dates). Blobs went to a scratch object
  directory, and `.git/index` was checksummed as unchanged.
- **Once the lead stages the three FIX 1 files together, the gate passes.**

**Other live docs that write the holdout bounds out** (line numbers only; not changed, because
none is exempted for the same reason):

- `FORK_CHANGES.md:18,109`: registry PROSE (running narrative)
- `research/ledger/win.md:92,251,313,485`: registry PROSE (ledger)
- `strategy-research/engineering/sessions/lessons.md:17,51,142`: count-pinned (4), no stated reason; a lessons log
- `strategy-research/briefs/FUNDING_MR_DAILY_RETEST.md:191,366`, `briefs/H-041-C-v2.md:184,331`,
  `briefs/research_brief_P4_ts_trend.md:169`: research briefs (registered with counts)
- `strategy-research/workflow_artifacts/skills/quant-fundamentals/SKILL.md:115`,
  `workflow_artifacts/skills/verdict-interpreter/SKILL.md:506`: skills (prompt scope, not changed)
- History (engineering findings, done improvements, session reports, handoffs) also carries them. It is not listed
  line by line here and stays as written.

**Tests.** `tests/test_holdout_date_gate.py`, `tests/test_precommit_gate0_delete_allowed.py`
(the only SR tests that reference the gate or registry, besides a comment in `conftest.py`). Both build
their own temporary registry, so they don't depend on the real entries. They passed within the run below.
The trading-bot test `tests/test_no_sealed_date_literals.py` also passed.

---

## FIX 2: `data_availability_gate` default in USER_GUIDE

**Truth: ON by default.**

- `strategy-research/workflow/run_phase1_research.py:3684-3720`: `_data_availability_gate_enabled()`
  reads `dag_cfg.get("enabled", True)`. Its docstring calls it "the ONE flag in this module that
  defaults ON". A non-bool value raises.
- `strategy-research/config/campaign_config.yaml:463-464`: `data_availability_gate: enabled: true`.
- `strategy-research/config/feature_flag_register.yaml:236-244`: `state: "on"`, "the ONE flag in this
  register whose default is true".
- The guide's own §2.1 map (line 206), stage 14 block (lines 840-848) and routing tables (lines 829, 1910)
  already said on by default.

**Change.** `strategy-research/docs/USER_GUIDE.md:313` (§2.2 Stage Objectives table, stage 14 row):

- old: `Off by default (E-054). Check, per window ...`
- new: ``On by default (E-054 Layer 2, `orchestrator.data_availability_gate.enabled`, default `true` in `run_phase1_research.py::_data_availability_gate_enabled`; only an explicit `false` skips it). Check, per window ...``

This follows the style of the neighbouring stage 15 row, which cites its config key in parentheses.
Line 848 ("the gate's original <DATE> off-by-default (env-var) behavior") is accurate history and was left as is.

---

## FIX 3: delete `strategy-research/DOC_INDEX.md`

**Changes.**

- `strategy-research/DOC_INDEX.md`: deleted (313 lines, tracked).
- `strategy-research/tests/test_e059_6c_s2a_route_retirement.py:201`: `"DOC_INDEX.md"` removed from the tuple.
  The test name `test_flag_documented_in_guide_runbook_and_index` was left unchanged, as instructed.
- `strategy-research/tests/test_e059_6c_s2d_holdout_unlock.py:627`: `"DOC_INDEX.md"` removed from the tuple.
- `strategy-research/docs/USER_GUIDE.md:3`, `strategy-research/docs/RUNBOOK.md:3`, `strategy-research/docs/HALT_RECOVERY.md:3`
  - old: ``Not sure this is the doc you need? See [`DOC_INDEX.md`](../DOC_INDEX.md) first.``
  - new: ``Not sure this is the doc you need? See [`CLAUDE.md`](../CLAUDE.md) §1, "Where to read", first.``
- `trading-bot/DOC/USER_GUIDE.md:3-4`
  - old: ``... See [`strategy-research/DOC_INDEX.md`](../../strategy-research/DOC_INDEX.md) first — that file maps every doc in this monorepo by the question you arrived with.``
  - new: ``... See [`strategy-research/CLAUDE.md`](../../strategy-research/CLAUDE.md) §1, "Where to read", which lists the research-side docs by purpose.``
- `strategy-research/docs/VERIFICATION_DOCTRINE.md:277`
  - old: ``Cross-linked from `strategy-research/DOC_INDEX.md` and `workflow_artifacts/skills/verdict-interpreter/SKILL.md`.``
  - new: ``Cross-linked from `workflow_artifacts/skills/verdict-interpreter/SKILL.md`.``
- `strategy-research/docs/TIMEFRAME_CHANGE_PLAYBOOK.md:5`: `Read strategy-research/DOC_INDEX.md first ...` became
  ``Read `strategy-research/CLAUDE.md` §1 ("Where to read") first ...``.
- `strategy-research/docs/TIMEFRAME_CHANGE_PLAYBOOK.md:19`: the row "Checklist addition (doc-index maintenance) | folded into
  DOC_INDEX.md's own header" now reads "retired with `strategy-research/DOC_INDEX.md` (file deleted)".

**Not changed (history; stays as written).** Grep of the whole repo (excluding `.git/`, `runs/`,
`archive/`, `guided_tour/`, this folder, SESSION_LOG.md and DECISION_LOG.md) still finds DOC_INDEX in:

- `tasks/o3_inventory.md:62`
- `engineering/sessions/HANDOFF_*.md:17`
- `engineering/sessions/session_reports/*` (close, venue_survey and margin_funding reports)
- `engineering/roadmap/E-035/S1_FINDINGS.md:485`, `E-056/S2_FINDINGS.md:382`, `E-058/S1_FINDINGS.md:323`,
  `E-059/S1_FINDINGS_6B.md:530`, `E-059/S1_FINDINGS_6C.md:394`, `E-060/S1_FINDINGS.md:366`
- `engineering/improvements/done/restructure-planning-E-002/` (CLEANUP_PLAN.md, REFERENCE_MAP.tsv, INVENTORY.tsv)
- `engineering/delivery_plan_v26.md:49,272,486`
- `engineering/review_*/A1_*.md`

**Skills/prompt templates.** No file under `strategy-research/workflow_artifacts/` mentions DOC_INDEX.
No code (`.py`) other than the two tests reads it.

---

## Tests run

Interpreter: scratchpad venv (python 3.13), `CI=true PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`.

- From `strategy-research/`: **734 passed, 3 skipped, 0 failed** (23 files). These are every SR test
  that mentions DOC_INDEX, `USER_GUIDE.md` or `RUNBOOK.md`, plus the gate tests: test_doc_anchors,
  test_e030_s4_bit_identity_and_replay, test_e059_6c_s2a_route_retirement, test_e059_6c_s2b_campaign_review,
  test_e059_6c_s2b_review_fixes, test_e059_6c_s2c_parked_states, test_e059_6c_s2c_review_fixes,
  test_e059_6c_s2d_holdout_unlock, test_e059_s2b_briefs, test_e059_s2b_review_fixes,
  test_e061_c1_7_first_run_kit, test_e061_c2_s2c_variant_shape, test_e068_4_approval_cap_warnings,
  test_guide_covers_the_code, test_halt_history, test_halt_quarantine_policy,
  test_holdout_research_only_gate, test_profit_bars_every_backtest, test_stage_attempt_counter,
  test_user_guide_field_tables, test_user_guide_toc, test_holdout_date_gate,
  test_precommit_gate0_delete_allowed.
- From `trading-bot/`: **37 passed, 0 failed**. Files: test_build_core_all_bars_corr (the only trading-bot test that
  greps these docs) and test_no_sealed_date_literals.

## Notes for the lead

- Stage the three FIX 1 files together. The gate checks the index, so staging only the registry
  would block the commit.
- The broad scan for holdout bounds in tracked `.md` files read `trading-bot/local_data/README.md`
  (it printed line numbers only). That path was excluded from later scans and was not changed.
