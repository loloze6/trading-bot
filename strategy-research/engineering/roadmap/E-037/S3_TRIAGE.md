# E-037 S3 — Triage

**State:** proposed — awaiting Jérémy's decisions
**Input:** the 25 findings in [`FINDINGS.md`](FINDINGS.md)
**What this file is for:** S3's job per the EPIC is *"each becomes a card or
issue. Jérémy decides what gets worked."* This groups them so that decision is
a handful of calls rather than twenty-five.

**Nothing here has been actioned.** No issue created, no code changed.

---

## The short version

Of 25 findings, **21 are documentation** and **4 touch code**. Only the code
ones can hurt a running campaign; the documentation ones are what made the
system hard to reason about in the first place.

Three questions decide almost everything:

1. **Is `regime_auditor` supposed to run?** ([F16](FINDINGS.md#f16))
   A documented stage that is never dispatched. Design call, not a fix.
2. **Should stated rules be enforced, or restated as guidance?**
   ([F18](FINDINGS.md#f18), and the sweep it implies)
3. **Do you want a gate that stops §3 drifting again?**
   ([F24](FINDINGS.md#f24) — the audit script already exists)

---

## Group A — Code defects (4)

The only group that can affect results. Recommend these become issues.

| ID | Severity | What | Why it is not cosmetic |
|---|---|---|---|
| [F10](FINDINGS.md#f10) | **high** | `episode_significance.py:209` hardcodes `block_24_dense_fallback` while passing a derived `block_size`. run_060 stamps that label beside `block_size: 6`. | The 2026-08-28 fix that made the label track the arithmetic covered the default path only. An artifact asserting a method it did not use is exactly what that fix existed to prevent. **Not a one-line change** — the literal is in `VALID_METHODS`, which the F4d conformance gate matches on, so label and gate move together. Also needs a decision on already-archived artifacts carrying the wrong label. |
| [F16](FINDINGS.md#f16) | **high** | `regime_auditor` is documented as an automated stage; nothing dispatches it and nothing writes `regime_audit_decision.yaml`. | Everything downstream that assumes that file exists — the A2.2 retune firewall, stage 7's `ungated_escape_eligible` write-back — is silently conditional on a human having produced it. **Design decision required:** make it a stage, or re-document it as a human step. |
| [F17](FINDINGS.md#f17) | medium | `_ensure_regime_detector_report` returns `None` silently when the config is missing or the subprocess fails. | The verdict then proceeds with no detector report and the only trace is stdout. Sits against the project's own rule that anything feeding decisions raises on degenerate inputs — the rule that produced the run_060 guards. |
| [F11](FINDINGS.md#f11) | medium | `protocol_version` is stamped as a platform-dependent path; `Path(...).name` mis-parses a Windows path on POSIX. | Does not bite within one run. Bites when an artifact crosses machines — the dual-writer model. |

**Recommendation:** F10 as an issue now. F16 needs your design call before it
can be written as an issue at all. F17 and F11 are real but can wait.

---

## Group B — The guide describes things that do not exist (6)

The largest and most surprising group. All one root: **§3's field tables were
written from intended design and never reconciled with output.**

| ID | Severity | What |
|---|---|---|
| [F24](FINDINGS.md#f24) | **high** | Systemic: 5 entries have documented fields that appear in **zero** real artifacts. `escalation_request` 3 of 3, `protocol_result` 6 of 7. |
| [F22](FINDINGS.md#f22) | **high** | `verdict_interpretation.yaml` — 5 of 6 fields phantom across 39 files, 11 real fields undocumented. |
| [F21](FINDINGS.md#f21) | **high** | 5 artifacts documented as pipeline output are behind feature flags; **every flag is off**. Never produced. |
| [F14](FINDINGS.md#f14) | medium | `cost_check.required_gross_edge_bps` — a subkey no code emits. |
| [F23](FINDINGS.md#f23) | medium | `decision.yaml` documented values `approved`/`blocked` never occur; real values are `spec_ready` (38) and `validation_incomplete` (1). |
| [F2](FINDINGS.md#f2) | medium | `prescreen_result.yaml`'s route enum omits `no_signal_artifact`, which overrides every other route. |

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
| [F18](FINDINGS.md#f18) | **high** | Stage 3's *"Must: pass real-diversity check … cosmetic = rejected"* is enforced by nothing. `library_category` appears once in all of `workflow/` and `tools/`, in a prompt string. The model self-reports its own verdict. |
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
| [F19](FINDINGS.md#f19) | **high** | 5 real artifacts had no entry, including `pass_rule_evaluation.yaml`, the decision authority. **Fixed by S2's additions** — listed here so the pattern is visible: every one was a recent addition that shipped without an entry. |
| [F12](FINDINGS.md#f12) | medium | 14 amendment codes, 26 mentions, zero pointers to where any is defined. Related incident: C4 rule-citation confabulation. |
| [F20](FINDINGS.md#f20) | medium | Two metadata conventions coexist; `Updated by` appears on 2 of 28 entries. |
| [F25](FINDINGS.md#f25) | medium | §5 documented 3 of 22 tools, omitting the one that implements stage 7. |
| [F15](FINDINGS.md#f15) | medium | Guide numbers 13 stages, `STAGE_CONFIGS` has 10; stage 4 has two names. |
| [F9](FINDINGS.md#f9) | medium | `strategy-research/CLAUDE.md` lists a different 10-stage workflow and asserts the schema validation §3 records as false. **This is what an agent reads first.** |

**Recommendation:** these are S4's material, not separate issues — except
[F9](FINDINGS.md#f9), which is a two-minute fix with outsized effect and should
be done regardless of S4's timing.

---

## Group E — Attribution and precision (7)

Correct in spirit, wrong in detail. Low individual value; worth doing as one
pass during S4.

| ID | Severity | What |
|---|---|---|
| [F1](FINDINGS.md#f1) | medium | Stage 7's row credits the tool with the A8.6 check; it is orchestrator logic. |
| [F4](FINDINGS.md#f4) | medium | `prescreen_result.yaml`'s `Created by` is wrong on one of three creation paths. |
| [F5](FINDINGS.md#f5) | medium | "block-bootstrap" names the fallback as if it were the default; there are three methods. |
| [F13](FINDINGS.md#f13) | medium | Three sites label the ungated-escape write-back "A9.1"; A9.1 is the `keltner_163` fixture. Needs the author's confirmation. |
| [F3](FINDINGS.md#f3) | low | §3's prescreen table shows 6 of ~30 keys, unmarked as a selection. |
| [F6](FINDINGS.md#f6) | low | Trial recording credited to the tool; it is the orchestrator. |
| [F8](FINDINGS.md#f8) | low | Two significance thresholds (`0.10`, `0.05`); neither documented. |

---

## Proposed issue set

Six issues, not twenty-five:

| # | Title | Contains |
|---|---|---|
| 1 | `block_24_dense_fallback` label does not track the derived block size | F10 |
| 2 | Decide whether `regime_auditor` is a stage or a human step | F16 |
| 3 | §3 field tables describe fields that do not exist — plus a gate to stop recurrence | F24, F22, F21, F14, F23, F2 |
| 4 | Do "Must" statements in the guide imply enforcement? Sweep §2.2 | F18 |
| 5 | Detector validation fails silently; `protocol_version` is platform-dependent | F17, F11 |
| 6 | `strategy-research/CLAUDE.md` contradicts the guide it points at | F9 |

Remaining — F1, F3, F4, F5, F6, F8, F12, F13, F15, F19, F20, F25 — fold into
S4 rather than becoming issues, since S4 is editing those exact sections
anyway. F13 needs one question answered by whoever wrote the A9.1 comments.

---

## What I recommend doing first

**F9**, because it is small and it is the file an agent reads before anything
else. Then **issue 3's second half** — adopting the audit script as a gate —
because it is the only item that stops a whole class of finding from returning.
Then **F16**, because it is a design question and everything about stage 10
stays ambiguous until it is answered.

F10 is the most serious *defect*, but it affects a label rather than a
computation, and the run it misdescribes is already killed. It should be an
issue; it does not need to be today.
