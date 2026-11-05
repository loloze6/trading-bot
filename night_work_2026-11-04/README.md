# Night work, 2026-11-04 to 2026-11-05

The operator asked for autonomous work overnight ("doc, cleaning, refacto, standardization and
organisation, structure"), chosen wisely, with a summary of how it influences the ongoing tour.
Everything is on the session branch `ccr-fd96c37b-b5lc87`, one commit per piece, never on master,
nothing merged. Each commit can be reverted on its own.

## Choice of work
Taken only from the operator's own tour remarks, plus facts found on the way. Nothing here acts on
the sealed post-tour reports (`guided_tour/_post_tour/`) or on the inspector's notes. Nothing settles
a design question the direction session has not ruled on.
- No code refactor: without the PC's state (31 flags on, unpushed branch, live records) and before
  the post-tour rulings, a refactor could collide with unpushed work or pre-empt a decision.
- No change to `campaign_config.yaml`, `feature_flag_register.yaml` or `criterion_menu.yaml`: the PC
  holds uncommitted edits to the switchboard.

## Changed (docs and two test tuples)
| Commit | What | Tests |
|---|---|---|
| `d2a1ac3e` | `strategy-research/CLAUDE.md` restructured into the operator's three categories (stop 00): objective and overview, behaviour rules, development and test process. Stage list corrected to the 12 `STAGE_CONFIGS` keys. Broken doc pointers fixed. Prose guidance added to the brief template, with no field changed (stop 01). Every old rule is mapped in `docs_cleanup.md`. | Full fast suite on this commit: see "Test status" |
| `c891e8e1` | Sealed holdout dates removed from RUNBOOK and USER_GUIDE, now a pointer to the policy key (root hard rule), with their gate exemptions retired. USER_GUIDE corrected on `data_availability_gate` (on by default). `DOC_INDEX.md` deleted (stop 00, the operator's preference), with the two test tuples updated. Details in `round3_fixes.md`. | 771 targeted tests passed; holdout gate PASS |

## Proposed only (no code or config change)
| Commit | File | Answers |
|---|---|---|
| `0319353e` | `flag_register_proposal.md` | Stops 03a/03b: 36 switches classified: 21 core (hard-wire), 7 modular, 3 unused, 2 duplicate, 1 dead-off, 2 unsure. Also a cleaned-register sketch and a migration checklist. |
| `f8ad2e34` | `criterion_menu_audit.md` | Stop 08 "overloaded by comment lines": 171 of 306 lines are comments, and they are pasted into step 1a's prompt. Some are stale, and one restriction exists only as prompt text. |
| `8a6ef199` | `backtest_outputs_gap.md` | Stop 14 (sent as "Stop15"): a bar line holds 10 of 18 elements and a trade record 9 of 12. The per-window `trades.json` is what post-backtest steps read; nothing reads the shared one. |
| `25271c00` | `ai_step_inputs_map.md` | Stops 07 and 11: 7 AI calls, with each one's inputs and sizes. The indicator library is pasted into 1a (~17% of its prompt) for an information-only lookup. |
| `ded8a491` | `brief_restructure_proposal.md` | Stop 01: 33 brief fields and 63 code readers, the `criteria_from`/`constraints` behaviour from code, an Ideas / Trading parameters sketch, and the impact list. |
| `584e96ff` | `test_baseline_aeb86e0a.md` | Health of the code before tonight's changes: 0 real failures. |

## How this influences the tour
- **Tour files: untouched tonight.** Stops, remarks, inspector notes and the sealed `_post_tour/`
  reports are as committed in `aeb86e0a`. The tour resumes at stop 21b, with remarks on 21a to 29 to come.
- **Stops whose described element changed tonight.** A speech is never rewritten. Where a speech now
  differs from the files, the tour's rule is a dated "Correction" paragraph once the operator or
  direction rules:
  - Stop 00 (orientation) described `strategy-research/CLAUDE.md` and `DOC_INDEX.md`. The first is
    restructured, the second deleted.
  - Stop 01 (the brief) described the brief template. Prose guidance was added; no field changed.
  - Stops 03a/03b (switchboard): no change. The proposal is input for the post-tour analysis.
  - Stop 17 (data availability gate): USER_GUIDE now agrees that the gate is on by default.
  - Stop 27 (holdout): RUNBOOK and USER_GUIDE no longer write the sealed dates out, and two gate
    exemptions are retired.
- **Operator remarks answered with facts (no ruling):** stops 01, 03a/03b, 07, 08, 11 and 14, by
  the proposal files above. They are inputs for the direction session's post-tour analysis, next to
  the sealed verification reports.
- **Operator remarks implemented:** stop 00 (CLAUDE.md restructure, DOC_INDEX deletion), and stop 01
  (prose guidance only).

## Found, not acted on (for the operator)
- **GitHub reports 1 critical Dependabot alert on the default branch.** It was not inspected: no
  access to alert details from this session.
- **Live docs still writing holdout dates out, under other exemptions:** FORK_CHANGES.md,
  research/ledger/win.md, engineering/sessions/lessons.md, three briefs, and two skills (prompt text).
  Listed with line numbers in `round3_fixes.md`.
- **`campaign-review/SKILL.md:187`** cites the old CLAUDE.md stage list, with stages that no longer exist.
  This is prompt text, so it was left.
- **Test fixtures `strategy-research/tests/fixtures/d201_run_102/`, `d203_run_102/`** hold partial
  run_102 copies. They could supply examples for stops 20 to 29.

## Test status
See the last section, added when the full fast suite on the final branch head finished.
