# Improvements Register

> Historical audit of completed plans, not a live tracker.

Index of the numbered improvement plans under `docs/plan/`. One row per numbered
slot. This is an **index, not a narrative** — it answers "was this built, and how
do we know?", nothing more. Built 2026-07-30 (dispatch CLEAN-4c).

## How status was determined

Three independent evidence sources, deliberately kept separate because they
disagree:

| Source | Meaning | How measured |
|---|---|---|
| **SPECIFIED** | a plan file exists at `docs/plan/NN_*.md` | `git ls-files docs/plan` |
| **IMPLEMENTED** | the improvement is referenced from the PROD corpus | `grep` over PROD corpus (below) |
| **ACCEPTED** | a dedicated acceptance test or acceptance artifact exists | filename + content search |

**PROD corpus** = 53 files: non-test `.py`/`.sh`, `config/*.yaml`, `workflow/*.yaml`,
`tools/hooks/pre-commit`. Measured with GNU grep under the Bash tool (never
PowerShell). Reference counts are *line* counts, not occurrence counts.

**Reference counts are naming-convention-dependent — see §Caveats.** A zero in the
PROD column means "no reference under the searched names", NOT "not implemented".
Where the two diverge the row says so explicitly.

## Register

| # | Title | Spec path | Status | Completed | Evidence |
|---|---|---|---|---|---|
| 00 | *(meta — not an improvement)* | `engineering/improvements/done/design_and_docs/00_overview_v2.md`, `engineering/improvements/done/design_and_docs/00_closing_state.md` | **N/A — META** | n/a | `00_overview_v2.md:3` SUPERSEDED banner; `engineering/improvements/done/design_and_docs/00_closing_state.md:3` ARCHIVED-SNAPSHOT banner. Canonical closing state is `engineering/improvements/done/IMPROVEMENTS_DONE_20260706.md` |
| 01 | Edge-Source Taxonomy & Causal Root-Cause Diagnostics | `engineering/improvements/done/design_and_docs/01_edge_source_taxonomy.md` | **IMPLEMENTED**, acceptance UNKNOWN | by 2026-07-06 | PROD 3: `config/available_feeds.yaml:6`, `workflow/run_phase1_research.py:4375,4381`; built-record `IMPROVEMENTS_DONE_20260706.md:18` |
| 02 | Regime Attribution & Detector Validation | `engineering/improvements/done/design_and_docs/02_regime_attribution.md` | **IMPLEMENTED**, acceptance UNKNOWN | by 2026-07-06 | PROD 8: `workflow/run_phase1_research.py:1438,1468,1504,1518,1537,4812,4918`, `workflow/stages.yaml:120`; built-record `IMPROVEMENTS_DONE_20260706.md:15` |
| 03 | Trade-Level Diagnostics (Entry/Exit Attribution) | `engineering/improvements/done/design_and_docs/03_trade_level_diagnostics.md` | **IMPLEMENTED**, acceptance UNKNOWN | by 2026-07-06 | **Zero `Improvement 03` hits — naming artifact, see Caveats.** Deliverable is live: `tools/run_protocol.py:1177` `# Step 03`, writes `trade_diagnostics.json` at `:1188`; consumed by `tools/verdict_criteria_evaluator.py:187,310,396`; built-record `IMPROVEMENTS_DONE_20260706.md:16` |
| 04 | Indicator Knowledge Library | `engineering/improvements/done/design_and_docs/04_indicator_library.md` | **IMPLEMENTED (slim) + ACCEPTED**; audit only *partially* closed | 2026-07-04 (partial) | PROD 1 + `config/indicator_library.yaml`; `tests/test_improvement04_acceptance.py` (7 tests). **Disagreement:** `IMPROVEMENTS_DONE_20260706.md:123` records `diversity_audit` NOT genuinely exercised; built-record `:20` marks it delivered "slim", no empirical write-back |
| 05 | Campaign Knowledge Base (Cross-Run Findings) | `engineering/improvements/done/design_and_docs/05_campaign_knowledge_base.md` | **IMPLEMENTED + ACCEPTED** | 2026-07-03 | PROD 2; `runs/run_042/artifacts/improvement_05_acceptance.yaml:2` `accepted_at: "2026-07-03"`; deliverable `campaign_knowledge_base.yaml`; built-record `IMPROVEMENTS_DONE_20260706.md:19` |
| 06 | Promotion Rigor (Multiple-Testing Correction & Holdout) | `engineering/improvements/done/design_and_docs/06_promotion_rigor.md` | **IMPLEMENTED + ACCEPTED** | by 2026-07-06 | PROD 6; `tests/test_improvement06_acceptance.py` (7 tests); built-record `IMPROVEMENTS_DONE_20260706.md:21`, calibration `:26-60` |
| 07 | Data Extension & Holdout Retrofit | `engineering/improvements/done/design_and_docs/07_data_extension_holdout_retrofit.md` | **IMPLEMENTED**, acceptance UNKNOWN | 2026-07-02 | PROD 6 (5× `Improvement 07` + `workflow/run_phase1_research.py:4144` `Improvement-07`); date from `tests/test_circuit_breaker_family_scoping.py:109` and `tests/test_campaign_review_trigger.py:7` ("tagged 2026-07-02, Improvement 07"); built-record `IMPROVEMENTS_DONE_20260706.md:14` |
| 08 | Signal Prescreen (Cheap IC Gate) | `engineering/improvements/done/design_and_docs/08_signal_prescreen.md` | **IMPLEMENTED**, acceptance UNKNOWN | by 2026-07-06 | PROD 7; built-record `IMPROVEMENTS_DONE_20260706.md:17` (recorded jointly as "08+09") |
| 09 | Cost Hurdle as Upstream Design Constraint | `engineering/improvements/done/design_and_docs/09_cost_hurdle_gate.md` | **IMPLEMENTED**, acceptance UNKNOWN | by 2026-07-06 | PROD 4 (3× `Improvement 09` + `tools/run_protocol.py:84` `Step 09`); `config/cost_model.yaml`; built-record `IMPROVEMENTS_DONE_20260706.md:17` (recorded jointly as "08+09") |
| 10 | Maker/Limit Execution — Engine Assessment | `engineering/improvements/done/design_and_docs/10_maker_execution_assessment.md` | **ASSESSMENT — implementation explicitly out of scope** | rev. 2026-07-04, updated 2026-07-28 | Self-declared at `engineering/improvements/done/design_and_docs/10_maker_execution_assessment.md:1` "(Backlog, **Not Implementation**)" and `:3-8`. Zero PROD refs is **correct and expected**, not a gap. Config-level maker assumptions already live in `config/cost_model.yaml` |
| 11 | Viable-Space Map — Layer-1 Cost Hurdle × {1h,4h,1d} | `engineering/improvements/done/design_and_docs/11_viable_space_map.md` | **ADVISORY — frozen/closed, never implementable** | Rev. 3 frozen 2026-07-04 | Self-declared at `:3` "**Status: advisory**… never blocks" and `:9-12` "frozen; no further revisions… it is now closed". Referenced as prose by `config/campaign_config.yaml:35`. Zero PROD refs is **correct and expected** |

## Caveats — read before trusting the PROD column

1. **The reference counts are naming-convention-dependent.** Searching only the
   literal string `Improvement NN`, case-sensitively, yields
   `01×1 02×7 04×1 05×2 06×6 07×5 08×7 09×3` and zero for 03/10/11. That
   measurement is reproducible but **undercounts**, because the codebase uses at
   least three conventions: `Improvement NN`, `IMPROVEMENT NN` (all-caps),
   `Improvement-NN` (hyphen), and `Step NN`. Case-insensitive + `Step NN` raises
   01→3, 02→8, 03→**0→4**, 07→6, 09→4. The table above uses the wider measurement.

2. **Improvement 03 is the cautionary case.** It has zero references under any
   `Improvement 03` spelling, yet is fully implemented — `tools/run_protocol.py`
   calls it "Step 03" and emits the exact artifact (`trade_diagnostics.json`) that
   `03_trade_level_diagnostics.md` specifies. Absence of a reference is not
   evidence of absence of implementation.

3. **10 and 11 are not implementable documents.** Both self-declare as
   assessment/advisory. Grouping them with 03 as "specified but unbuilt" conflates
   a naming artifact (03), a deliberate backlog assessment (10), and a frozen
   advisory triage aid (11). Only the third category — none of these — would be a
   genuine gap.

4. **"12 improvements" is a file count, not an improvement count.** Slot 00 is
   meta (overview + closing state). The real improvement set is **01–09 (nine)**;
   `IMPROVEMENTS_DONE_20260706.md:6` scopes the plan as "Plan docs (01–09,
   amendments, this file)". 10 and 11 were added later (both dated 2026-07-04) as
   cost-structure work, outside the 01–09 plan.

5. **Acceptance coverage is thin and its true extent is UNKNOWN.** Only three
   improvements have a dedicated acceptance artifact (04, 06 via test files; 05 via
   `improvement_05_acceptance.yaml`). But `IMPROVEMENTS_DONE_20260706.md:3` claims
   "All acceptance tests pass (**23/23**)", while the two named acceptance test
   files contain **14** test functions total (7 + 7). The remaining 9 are
   unlocated. *Resolving this requires the run that produced the 23/23 figure, or
   a pytest collection over whatever suite it referred to.*

6. **Git history cannot date these.** All 11 plan docs were added in a single bulk
   commit on 2026-07-06, so `git log --diff-filter=A` gives no per-improvement
   completion date. Every date above comes from document self-dating.

7. **No completion date is precisely determinable for 01, 02, 06, 08, 09.** Each is
   recorded as built in the closing state's §1 table, which carries no per-row date;
   "by 2026-07-06" is an upper bound from the P1b closure, not a measurement.
   *Resolving these requires per-improvement commit provenance that this repo's
   squashed history does not retain.*

## Related

- `engineering/improvements/done/IMPROVEMENTS_DONE_20260706.md` — canonical closing state for the
  01–09 plan build (P1a closed 2026-07-04, P1b closed 2026-07-06)
- `engineering/improvements/done/IMPROVEMENTS_DONE_20260712.md` — later run_057 pipeline ledger
- `engineering/sessions/HANDOFF_20260724.md` — archived session handoff, superseded by `engineering/roadmap/EPICS.md`
- `engineering/roadmap/E-009/EPIC.md` — carries the 5 items formerly in `BACKLOG_DEFERRED.md` (deleted)
- `engineering/improvements/done/design_and_docs/AMENDMENTS_01-06.md` — amendments that override plans 01–09 on conflict
- `archive/improvements/` — six superseded `NEXT_SESSION_*` handoffs
