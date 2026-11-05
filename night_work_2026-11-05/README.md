# Night work, round 4 (2026-11-05)

The operator asked for more background work ("doc, cleaning, refacto, standardization and
organisation, structure"). The same rules as the previous night apply (`COMMON_RULES.md`): docs and
reports only; no code, config, skill or tour file changed; nothing taken from the sealed post-tour
reports; docs describe the committed code and its defaults. One commit per piece, on the session
branch `ccr-fd96c37b-b5lc87`. Round 1-3 summary: `../night_work_2026-11-04/README.md`.

## First, for the direction session
**The campaign review stage cannot read its two required inputs.** Its handoff template
(`workflow_artifacts/templates/handoffs/campaign_review.yaml:9-15`) points to
`../../campaign_state.yaml` and `../../campaign_knowledge_base.yaml`; both files live under
`campaign_record/`. A missing required input raises (`run_phase1_research.py:1066-1067`). The code's
own comment (`run_phase1_research.py:3826-3843`) records this as a known defect: "guaranteed to
crash if ever triggered live", fix left to the stage's next owner. The committed review log still
shows three completed reviews, so the live path may route differently (the retired-routing review
route). This was not verified and not fixed. It is a lead for tour stop 26.

## Changed (docs only)
| Commit | What | Tests |
|---|---|---|
| `56493a20` | `docs/RUNBOOK.md`: 62 commands checked against the CLIs: 54 OK, 5 fixed (two `campaign_record/` paths, moved code citations, `--resume` sets `in_progress`, the PowerShell exception named), 3 wrong but ambiguous (left), 1 uncheckable. Audit: `runbook_commands_audit.md`. | 550 passed (12 files reading RUNBOOK) |
| `6114734b` | `tools/README.md` rebuilt as an inventory of all 81 entries: purpose, importers, CLI, grouped by area; 55 reached by the live pipeline, 19 CLI-only, 1 with no user found. Two deleted tools removed. Notes: `tools_inventory_notes.md`. | No test reads it |
| `f79a0ffc` | `docs/USER_GUIDE.md` section 2 (lines 150-2002): about 175 statements checked: 145 OK, 20 fixed, 7 wrong but needing a rewrite or a decision, 4 uncheckable. Audit: `user_guide_s2_audit.md`. | 407 passed (10 files reading the guide) |

## Reports only
| Commit | File | Headline |
|---|---|---|
| `9484a687` | `skills_stale_references.md` | 48 prompt-input files, 40 stale references: removed stages, missing paths, 11 stale code citations in the brief template's `scope:` block (copied into every brief), 2 written-out sealed dates (file:line only), 3 statements that contradict the code. Prompt text steers the AI, so any change is the operator's call. |
| `d68bbc00` | `test_hygiene.md` | 41 tests always skip even in GitHub CI (untracked runs/ artifacts and caches, missing base commits in a depth-1 checkout). 109 slow tests, none of which needs the network by the code (strategy-research/CLAUDE.md says "live market data, network"). 39 warning sites in test code. |

## Also found, not acted on
- `tools/hooks/pre-commit:47` writes the sealed dates out in a comment (root hard rule). It is a hook
  file, so it was left; the fix is to replace the comment with a pointer to the policy key.
- `--resume` writes the queue before it takes the campaign lock (`run_campaign.py:6010` vs `:6021`).
  The `retry-analyst` lock refusal prints `--retry-analyst` although it is a subcommand (`:2710`).
- Three tool docstrings say nothing calls the module, but RP or RC imports it (`analyst_queries.py`,
  `composition.py`, `portfolio_whole_test.py`). Several docstrings still name the deleted
  `prescreen_signal.py` and `power_check.py`.
- USER_GUIDE section 3 (`holdout_result.yaml`, line 2736) said the orchestrator "marks consumed_at";
  it does not (it updates `holdout_consumed_by`). Fixed afterwards in `e7c3607c`; 408 guide tests pass.
- In the "Not reached" column of `skills_stale_references.md`, "reached under the committed defaults" is
  not the operator's live flag set: under the live set the config-direct, claim-tests, decide-next,
  analyst and retired-routing addenda are reached.

## How this round influences the tour
- **No tour file changed.** The tour resumes at stop 21b; remarks on 21a to 29 are still to come.
- **Line numbers moved in docs the stops cite.** RUNBOOK lines after line 16 moved by +1. The
  USER_GUIDE section 2 edits shifted lines by a few. A stop's reading map cites the old lines; content
  is unchanged except for the fixes listed in the audits.
- **Facts that touch stops:**
  - Stop 00: USER_GUIDE section 2 is its reading source; 20 statements are now corrected.
  - Stops 04, 23 and 29 (RUNBOOK): `--resume` sets `in_progress`; the `campaign_log`/`campaign_summary`
    paths are under `campaign_record/`.
  - Stop 26 (campaign review): the input-path defect above.
  - Stop 28 (registered but not reached): `tools/README.md` was cited for its STATUS column; that
    column is replaced by the "used by" inventory.
  - Stop 29 (operator surface, CI): `test_hygiene.md`.
  - Stops 07, 10, 15, 21 and 26 (skills): `skills_stale_references.md`.
- **For the post-tour analysis:** the two reports and the "left" items in each audit are inputs next to
  the sealed verification reports. None settles a design question.

## Test status
Full fast suites as CI runs them (`run_tests.py`, `CI=true`, no slow tests) on `f79a0ffc` (all round-4 doc
edits): **ALL SUITES PASSED**. trading-bot PASS; strategy-research 7733 passed, 33 skipped, 0 failed;
holdout date gate PASS; validate_config exit 0.
