# E-037 S3 — Triage

**State:** proposed — awaiting Jérémy's decisions
**Input:** the 30 findings in [`FINDINGS.md`](FINDINGS.md) — 1 closed, 29 open
**Last synced:** 2026-08-31, after S5. A mechanical completeness check confirms every finding appears below.
**What this file is for:** S3's job per the EPIC is *"each becomes a card or
issue. Jérémy decides what gets worked."* This groups them so that decision is
a handful of calls rather than twenty-five.

**Nothing here has been actioned.** No issue created, no code changed.

---

## The short version

Of 30 findings, **23 are documentation** and **7 touch code or the machinery around it**. One (E037-29) is already closed. Only the code
ones can hurt a running campaign; the documentation ones are what made the
system hard to reason about in the first place.

Three questions decide almost everything:

1. **Is `regime_auditor` supposed to run?** ([E037-16](FINDINGS.md#e037-16))
   A documented stage that is never dispatched. Design call, not a fix.
2. **Should stated rules be enforced, or restated as guidance?**
   ([E037-18](FINDINGS.md#e037-18), and the sweep it implies)
3. **Do you want a gate that stops §3 drifting again?**
   ([E037-24](FINDINGS.md#e037-24) — the audit script already exists)

---

## Group A — Code defects (5)

The only group that can affect results. Recommend these become issues.

| ID | Severity | What | Why it is not cosmetic |
|---|---|---|---|
| [E037-26](FINDINGS.md#e037-26) | **high** | The run_060 zero-data guard (`prescreen_signal.py:1320`) raises before F5c's component-error override can fire. **The suite is RED on `origin/master`.** | F5c exists to stop an engineering failure being scored as a scientific kill -- the run_044 lesson. Its component-error branch is now unreachable. Fails loud rather than silent, so no wrong verdicts today, but the error message misreports the cause: it says "no symbols requested" on a run that loaded 168 bars. **The only finding that is failing right now rather than merely wrong.** |
| [E037-10](FINDINGS.md#e037-10) | **high** | `episode_significance.py:209` hardcodes `block_24_dense_fallback` while passing a derived `block_size`. run_060 stamps that label beside `block_size: 6`. | The 2026-08-28 fix that made the label track the arithmetic covered the default path only. An artifact asserting a method it did not use is exactly what that fix existed to prevent. **Not a one-line change** — the literal is in `VALID_METHODS`, which the F4d conformance gate matches on, so label and gate move together. Also needs a decision on already-archived artifacts carrying the wrong label. |
| [E037-16](FINDINGS.md#e037-16) | **high** | `regime_auditor` is documented as an automated stage; nothing dispatches it and nothing writes `regime_audit_decision.yaml`. | Everything downstream that assumes that file exists — the A2.2 retune firewall, stage 7's `ungated_escape_eligible` write-back — is silently conditional on a human having produced it. **Design decision required:** make it a stage, or re-document it as a human step. |
| [E037-17](FINDINGS.md#e037-17) | medium | `_ensure_regime_detector_report` returns `None` silently when the config is missing or the subprocess fails. | The verdict then proceeds with no detector report and the only trace is stdout. Sits against the project's own rule that anything feeding decisions raises on degenerate inputs — the rule that produced the run_060 guards. |
| [E037-11](FINDINGS.md#e037-11) | medium | `protocol_version` is stamped as a platform-dependent path; `Path(...).name` mis-parses a Windows path on POSIX. | Does not bite within one run. Bites when an artifact crosses machines — the dual-writer model. |

**Recommendation:** **E037-26 first — the suite is red wherever the data cache exists.** Then E037-10. [E037-27](FINDINGS.md#e037-27) belongs with them: it is *why* E037-26 survived on master behind a green tick. E037-16 needs your design call before it
can be written as an issue at all. E037-17 and E037-11 are real but can wait.

---

## Group B — The guide describes things that do not exist (6)

The largest and most surprising group. All one root: **§3's field tables were
written from intended design and never reconciled with output.**

| ID | Severity | What |
|---|---|---|
| [E037-24](FINDINGS.md#e037-24) | **high** | Systemic: 5 entries have documented fields that appear in **zero** real artifacts. `escalation_request` 3 of 3, `protocol_result` 6 of 7. |
| [E037-22](FINDINGS.md#e037-22) | **high** | `verdict_interpretation.yaml` — 5 of 6 fields phantom across 39 files, 11 real fields undocumented. |
| [E037-21](FINDINGS.md#e037-21) | **high** | 5 artifacts documented as pipeline output are behind feature flags; **every flag is off**. Never produced. |
| [E037-14](FINDINGS.md#e037-14) | medium | `cost_check.required_gross_edge_bps` — a subkey no code emits. |
| [E037-23](FINDINGS.md#e037-23) | medium | `decision.yaml` documented values `approved`/`blocked` never occur; real values are `spec_ready` (38) and `validation_incomplete` (1). |
| [E037-02](FINDINGS.md#e037-02) | medium | `prescreen_result.yaml`'s route enum omits `no_signal_artifact`, which overrides every other route. |

**These are cheap to fix and were expensive to find.** S2 has already written
the correct content alongside the old, so the remaining work is deciding
whether to delete the intended-design prose or keep it marked.

**Recommendation:** one issue for the group, plus adopt
[`tools/audit_field_tables.py`](tools/audit_field_tables.py) as a gate so it
cannot recur. That second half is the durable part.

---

## Group C — Stated guarantees that nothing enforces (2)

| ID | Severity | What |
|---|---|---|
| [E037-18](FINDINGS.md#e037-18) | **high** | Stage 3's *"Must: pass real-diversity check … cosmetic = rejected"* is enforced by nothing. `library_category` appears once in all of `workflow/` and `tools/`, in a prompt string. The model self-reports its own verdict. |
| — | — | Precedent: §3's *"all artifacts are validated against JSON schemas"*, corrected 2026-08-27 after it turned out no schema is loaded by any code. |

Two confirmed instances make this a **class**. The phrasing is the tell:
"Must:" and "rejected" read as mechanical outcomes.

**Recommendation:** decide the general rule first — *does a "Must" in the guide
mean code enforces it?* — then sweep every "Must:" in §2.2 against that rule.
Cheaper as one sweep than as findings arriving one at a time.

---

## Group D — Structure and findability (6)

The original complaint, in its component parts.

| ID | Severity | What |
|---|---|---|
| [E037-19](FINDINGS.md#e037-19) | **high** | 5 real artifacts had no entry, including `pass_rule_evaluation.yaml`, the decision authority. **Fixed by S2's additions** — listed here so the pattern is visible: every one was a recent addition that shipped without an entry. |
| [E037-12](FINDINGS.md#e037-12) | medium | 14 amendment codes, 26 mentions, zero pointers to where any is defined. Related incident: C4 rule-citation confabulation. |
| [E037-20](FINDINGS.md#e037-20) | medium | Two metadata conventions coexist; `Updated by` appears on 2 of 28 entries. |
| [E037-25](FINDINGS.md#e037-25) | medium | §5 documented 3 of 22 tools, omitting the one that implements stage 7. |
| [E037-15](FINDINGS.md#e037-15) | medium | Guide numbers 13 stages, `STAGE_CONFIGS` has 10; stage 4 has two names. |
| [E037-09](FINDINGS.md#e037-09) | medium | `strategy-research/CLAUDE.md` lists a different 10-stage workflow and asserts the schema validation §3 records as false. **This is what an agent reads first.** |

**Recommendation:** these are S4's material, not separate issues — except
[E037-09](FINDINGS.md#e037-09), which is a two-minute fix with outsized effect and should
be done regardless of S4's timing.

---

## Group E — Attribution and precision (7)

Correct in spirit, wrong in detail. Low individual value; worth doing as one
pass during S4.

| ID | Severity | What |
|---|---|---|
| [E037-01](FINDINGS.md#e037-01) | medium | Stage 7's row credits the tool with the A8.6 check; it is orchestrator logic. |
| [E037-04](FINDINGS.md#e037-04) | medium | `prescreen_result.yaml`'s `Created by` is wrong on one of three creation paths. |
| [E037-05](FINDINGS.md#e037-05) | medium | "block-bootstrap" names the fallback as if it were the default; there are three methods. |
| [E037-13](FINDINGS.md#e037-13) | medium | Three sites label the ungated-escape write-back "A9.1"; A9.1 is the `keltner_163` fixture. Needs the author's confirmation. |
| [E037-03](FINDINGS.md#e037-03) | low | §3's prescreen table shows 6 of ~30 keys, unmarked as a selection. |
| [E037-06](FINDINGS.md#e037-06) | low | Trial recording credited to the tool; it is the orchestrator. |
| [E037-08](FINDINGS.md#e037-08) | low | Two significance thresholds (`0.10`, `0.05`); neither documented. |

---

---

## Group F — Raised after the first triage pass (4)

Added 2026-08-31. Three were found after S3 was written. **E037-07 was missed by
the original grouping and is high severity** — recorded as a miss rather than
quietly slotted in.

| ID | Severity | What | Disposition |
|---|---|---|---|
| [E037-07](FINDINGS.md#e037-07) | **high** | Stage 7 rewrites stage 10's `regime_audit_decision.yaml` in place, and that entry has no `Updated by` line, so a cross-stage write is invisible to any reader. | **Missed in the first pass.** Belongs with Group D and should be worked alongside E037-20 — it is the finding that motivated the `Updated by` normalisation. |
| [E037-29](FINDINGS.md#e037-29) | **high** | The pre-commit secret scan was not installed here — two gates running of three. | CLOSED 2026-08-31. Hook re-installed, `diff` silent, and `tests/test_installed_hook_matches_tracked.py` now guards recurrence. |
| [E037-28](FINDINGS.md#e037-28) | low | The glossary says "10-stage pipeline"; the guide documents 13. Ten is the size of `STAGE_CONFIGS`. | Fold into cleanup. One phrasing — "13 documented, 10 dispatched" — stays true if either number changes. |
| [E037-30](FINDINGS.md#e037-30) | low | 13 of 46 glossary terms appear nowhere else; two describe fields that live on a different artifact. | Partly addressed: the two misattributed terms are marked in §6. The rest is a cleanup decision. |

**Why E037-07 being missed is worth stating.** The first triage grouped 25
findings by hand and dropped one of the highest-severity items in the set. That
is the same failure the epic is about — a hand-maintained index drifting from
what it indexes — happening inside the document written to manage the findings.
It was caught by a mechanical completeness check (every `E037-nn` in
`FINDINGS.md` must appear here), not by re-reading.


## Proposed issue set

Seven issues, not thirty:

| # | Title | Contains |
|---|---|---|
| 1 | **F5c's component-error path is unreachable, and the tests that would catch it run in no gate** | E037-26, E037-27 |
| 2 | `block_24_dense_fallback` label does not track the derived block size | E037-10 |
| 2 | Decide whether `regime_auditor` is a stage or a human step | E037-16 |
| 3 | §3 field tables describe fields that do not exist — plus a gate to stop recurrence | E037-24, E037-22, E037-21, E037-14, E037-23, E037-02 |
| 4 | Do "Must" statements in the guide imply enforcement? Sweep §2.2 | E037-18 |
| 5 | Detector validation fails silently; `protocol_version` is platform-dependent | E037-17, E037-11 |
| 6 | `strategy-research/CLAUDE.md` contradicts the guide it points at | E037-09 |

Remaining — E037-01, E037-03, E037-04, E037-05, E037-06, E037-08, E037-12, E037-13, E037-15, E037-19, E037-20, E037-25 — fold into
S4 rather than becoming issues, since S4 is editing those exact sections
anyway. E037-13 needs one question answered by whoever wrote the A9.1 comments.

---

---

## Maintenance of E-037's own output

Raised by Jérémy, 2026-08-31: *"if you mention a code line, is it really
maintainable? Should we implement a hook or a routine? If not maintainable, is
it really necessary — could we mention function or class instead?"*

### Are `file:line` anchors maintainable? No.

E-037 wrote **78 explicit line anchors**, plus 163 bare `:N` shorthands inside
stage blocks. Evidence that they rot:

- **Nine of roughly forty were wrong when first written** and were corrected by
  hand during S2. Not after a refactor — on the day they were written.
- Any edit above a line shifts every anchor below it. `run_phase1_research.py`
  is over 6,000 lines and changes often.

An anchor that is confidently wrong is worse than no anchor: it sends a reader
to the wrong place and they trust it.

### Function/class names are the better form — agreed

`run_phase1_research.py::_route_holdout_evaluation` beats
`run_phase1_research.py:5383` on every axis that matters. It survives edits
above it, it is greppable, and it tells the reader *what* to look for instead of
*where* it was on one particular day.

**Mapping is feasible:** 67 of the 78 explicit anchors resolve to a top-level
function or class, and the other 11 resolve to a module-level named constant
(`STAGE_CONFIGS`, `_SIG_THRESHOLD`, `_SKILL_MAP`, `VALID_METHODS`). Only one
points at a bare comment. **So every explicit anchor has a stable name
available.**

### Why it was not converted in this session

Two automated conversions were attempted and **both were reverted**. The blocker
is the 163 bare `:N` shorthands: resolving which file each belongs to requires
the enclosing prose context, and both attempts mis-attributed anchors — the
second run's validation gate refused to write and reported 47 unresolved, and
the first run had already produced wrong attributions in `FINDINGS.md`
(`::run_tool_worker` credited to `prescreen_signal.py`). Everything was reverted
and re-applied by hand; `git status` was verified clean afterwards.

The lesson is the same one this epic keeps producing: a mechanical rewrite of
prose needs a gate that refuses on doubt, and a half-converted document is worse
than an unconverted one.

**Recommendation:** do the migration as part of **S4**, where the sections are
being edited anyway and each anchor is converted in view of its own paragraph.
Until then, `test_doc_anchors.py` keeps the existing ones honest, and **new
anchors should be written in `file.py::symbol` form**.

### The routine, and where it belongs

Two tests now exist. Both are ratchets: green today, failing only on new drift.

| Test | Catches |
|---|---|
| `tests/test_user_guide_field_tables.py` | A documented artifact field that exists in no real artifact (E037-22/E037-24's defect class). |
| `tests/test_doc_anchors.py` | An anchor pointing past the end of a file, or naming a function/constant that no longer exists. |

Both were verified in both directions — injecting a fault fails them, and
`test_user_guide_field_tables.py` caught its own stale baseline entry on first
run.

**A git hook is the wrong home for these, and there is evidence.** See
[E037-27](FINDINGS.md#e037-27): the pre-commit hook runs only `trading-bot/tests/`, so
nothing under `strategy-research/tests/` runs on commit at all. CI runs both
suites, so **both new tests are already gated by CI** on every push and PR —
which is the right layer, because it also covers merges made through the GitHub
UI, where client-side hooks never fire.

The gap worth closing is E037-27's, not these tests': the pre-commit hook's scope,
and the fact that data-gated tests skip silently in CI. Fixing that is worth
more than any new routine, because it is what let a real regression sit on
master behind a green tick.

**No new hook is recommended.** The infrastructure already exists and already
covers these; adding a hook would be a guard on a guard.

## What I recommend doing first

**E037-09**, because it is small and it is the file an agent reads before anything
else. Then **issue 3's second half** — adopting the audit script as a gate —
because it is the only item that stops a whole class of finding from returning.
Then **E037-16**, because it is a design question and everything about stage 10
stays ambiguous until it is answered.

E037-10 is the most serious *defect*, but it affects a label rather than a
computation, and the run it misdescribes is already killed. It should be an
issue; it does not need to be today.
