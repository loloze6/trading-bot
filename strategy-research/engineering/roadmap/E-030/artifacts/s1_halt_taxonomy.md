# E-030 S1 — halt taxonomy

**Scope:** characterization only, no code (operator approval 2026-08-22, EPIC.md Log).
**Sources:** `campaign_record/campaign_log.md` (129 lines, the append-only primary
record), the 14 halts already measured in `artifacts/measured_halt_cost.txt`, all 58
`runs/run_*/pipeline_state.yaml` files, `docs/RUNBOOK.md` §3/§4, the halt-raising code
in `workflow/run_campaign.py` / `workflow/run_phase1_research.py`, `SESSION_LOG.md`,
`engineering/improvements/done/IMPROVEMENTS_DONE_20260712.md` (ledger A10–A14),
`session_reports/20260719_close.md`, and `git log` for 2026-07-01 → 2026-07-25.

---

## The conclusion

Of the 127.0 h of recorded downtime, **37.2 h (29%) is automatable today and still
live** — 20.4 h retry, 16.8 h quarantine. Another 21.9 h was retry-safe and is
**already fixed** (the A11 SDK rider). **21.0 h is correctly must-escalate and should
never be automated.**

The remaining **46.9 h — 37% of all downtime, the single largest halt in the record —
cannot be classified at all, because the system did not keep the error that caused
it.** That is the finding that should shape S2. A retry/quarantine policy decides on
`last_error`; `last_error` is truncated to 300 characters when the halt is written
(`run_campaign.py:874-875`) and set to `null` when the human resumes. For halt #7 the
300-character window captured a pandas `FutureWarning` and nothing else, and `run_054`'s
`last_error` reads `null` today. **Making the halt record durable is a prerequisite for
S2, not a follow-up.**

Second finding, same weight: **the reason code on a halt line is not reliable evidence
of what went wrong.** One of the 14 (#8) is a confirmed misreport — RUNBOOK §4 documents
it by date: a fresh `component_execution_error` pause was reported as `no_signal_artifact`
because a stale flag from a resolved 2026-07-07 pause was never cleared. `_classify_human_pause`
reads a sticky `flags` dict in fixed priority order, and `update_state` merges rather than
clears. `run_053` still carries `flags.kb_reactivation_violation: true` and two
`kb_reactivation_violations` records on disk today, six weeks after that pause was
resolved. **S2 must not key retry-vs-escalate on the reason code.**

Third: **12 of 14 halts were cleared with no production-code commit inside the halt
window.** The two exceptions are #12 (`9bf2a4cf`, the SDK retry rider) and #13
(`2529f5b5`, the `CandleBuilder._align()` tz fix). #11's in-window commit `996f4325`
is a 6-line edit to `briefs/H-041-C-v2.md` — no code. So most of the 127 h is
**latency-to-a-human-noticing, not repair time.** That is precisely the cost an
automatic policy removes. *Caveat, stated because it is real: an absence of an
in-window commit does not prove no code changed — this repo bundles work (`d9fc4e7e`,
2026-07-13, carried six days of changes including `run_protocol.py` and
`strategy_components.py`). The claim is about commit timing, which is verified; it is
evidence for, not proof of, "no code was needed."*

### Class totals (denominator = 14 halts / 127.0 h)

| Class | Halts | Downtime | Note |
|---|---|---|---|
| retry-safe | 3 of 14 | 42.3 h | 21.9 h of it (2 halts) already fixed by A11 |
| quarantine-safe | 7 of 14 | 16.8 h | all still live |
| must-escalate | 3 of 14 | 21.0 h | never automate |
| **undecidable** | **1 of 14** | **46.9 h** | cause not recoverable from the record |

Reason-code counts, for reconciliation against the epic's own breakdown:
`unhandled_exception` 6, `component_execution_error` 3, `no_signal_artifact` 2,
`kb_reactivation_violation` 2, `component_gap` 1 — 14 of 14, and the epic's 106.6 h
"plumbing" figure reproduces exactly. **My classification is not the same partition.**
The epic counted 10 of 14 as plumbing by reason code; by *resolution* it is still 10,
but membership changes twice: #3 moves out (its reason code says `unhandled_exception`;
its actual resolution was a research-integrity discard) and #8 moves in (its reason code
says `no_signal_artifact`; it was a `component_execution_error`).

---

## The 14 halts

Downtime figures are `measured_halt_cost.txt`'s, reproduced: each halt paired with the
next non-`[DRY RUN]` log event. **10 of 14 halts are followed by a resume record** (a
`RESUME` line, or one of the two `=== RESUME after … ===` banners at #2 and #3);
**4 of 14 — #8, #9, #11, #12 — are not**: the next event is a bare `STAGE` or
`RECONCILE` line, i.e. the human relaunched directly rather than using `--resume`. That
matches the trap RUNBOOK §4 documents as having "cost real session time twice
(2026-07-16)".

---

### #1 — 2026-07-06T14:06:15 · `unhandled_exception` · 0.18 h · run_053
**Detail:** `'NoneType' object has no attribute 'strip'`, at `pending_stage=validation`.
**What the human did:** resumed 11 minutes later. No commit in the window.
**Root cause (verified in code):** `determine_post_validation_route`
(`run_phase1_research.py:1333-1354`) — the validation skill wrote `family_status`
instead of the schema-canonical `status`, and `decision.get("status").strip()` raised.
The code carries the fix as an in-line comment naming this exact run: *"F4f (2026-07-06,
run_053)"*, now a `status or family_status` fallback with a loud `ValueError` if neither
is present.
**Class: quarantine-safe.** Not retry-safe on the evidence available: no identical retry
is recorded as having succeeded, and the failing read is of an artifact already on disk.
A retry that *re-invokes* the stage would regenerate that artifact and could well succeed
— that is a plausible retry candidate but it is **inferred**, not demonstrated. Note this
exact halt can no longer recur: F4f closed it.

### #2 — 2026-07-06T14:18:15 · `component_gap` · 1.81 h · run_053
**What the human did:** wrote the missing engine component. The log's own resume line
names it: `=== RESUME after component_gap fix (MacdHistogramCrossoverComponent) ===`.
**Class: quarantine-safe — but as `blocked_on_component:<name>`, not `done`.** The run
genuinely cannot proceed without new engine code, so no retry helps; the *queue* has no
reason to stop. `campaign_queue.yaml` already has a `blocked_on_*` status family that
`_select_entry` skips, so the mechanism exists. Discarding rather than re-queueing would
lose a hypothesis whose only defect is that the engine lacked a piece.

### #3 — 2026-07-06T16:24:46 · `unhandled_exception` · 1.98 h · run_054
**Detail:** `Missing files: ['runs\\run_054\\artifacts\\hypothesis_card.yaml']`.
**What the human did:** the log's own resume line: `=== RESUME after discarding invalid
run_054 (KB-reactivation gate re-derivation) ===`.
**Class: must-escalate — on the resolution, against its own reason code.** The reason
code is a plumbing signature (missing deliverable, `ensure_files` hard-fail). The action
actually taken was to *discard a run because its hypothesis illegally reactivated a
closed KB finding* — a research-integrity act, and the direct cause of #4 firing two
hours later on the same lineage. An automatic retry here would have re-invoked a stage
to regenerate a card for a hypothesis that should never have been running.
**This is the clearest single argument against classifying on reason codes.**

### #4 — 2026-07-06T18:23:42 · `kb_reactivation_violation` · 19.04 h · run_053
**Detail:** `run_053`'s state still carries both violation records verbatim — the
`next_research_question` reactivated H-041-A and H-041-C, whose `reactivation_condition`s
were already consumed by `run_050` and `run_048`.
**What the human did:** resolved overnight; resumed 2026-07-07T13:26:00.
**Class: must-escalate.** By the brief's standing rule and by the RUNBOOK's own
"remain human-gated" list. Never propose auto-resuming this.

### #5 — 2026-07-07T13:26:01 · `kb_reactivation_violation` · 0.02 h · run_053
**What happened:** `--resume` at 13:26:00 confirmed resolution; the campaign re-entered
the run and halted **one second later** with the identical reason. A second resume at
13:27:30 got past it — by advancing `pending_stage` to `completed_reframed`, not by
clearing the violation. Verified: `run_053/pipeline_state.yaml` today still reads
`flags.kb_reactivation_violation: true` and still carries both
`kb_reactivation_violations` records.
**Class: must-escalate** (same class as #4).
**Its real value is as evidence:** this is the live proof that *a bare retry is not a
retry*. `--resume` checks only `status` and `pending_stage`; the classifier decides on
`flags`, which nothing cleared. Any S2 retry that does not clear the state the previous
attempt set will reproduce this 1-second loop.

### #6 — 2026-07-07T13:35:52 · `no_signal_artifact` · 0.36 h · run_054
**What the human did:** resolved in 22 minutes, no commit in window. Per RUNBOOK §3, the
cure is fixing the component/config and manually setting `pending_stage: signal_prescreen`
(this pause path leaves `pending_stage` at the literal sentinel `human_pause`).
**Class: quarantine-safe.** F5c fires when a component never fired or errored on every
bar — an engineering fact, explicitly "not a scientific result." Trial accounting is
already correct here without new machinery: a prescreen outcome records an A6.2 row via
`_record_prescreen_trial` (`statistic_valid: 'neither'`, `sharpe: null`).
**The quarantine must not write `completed_rejected`** — that would launder an
engineering failure into a scientific null.

### #7 — 2026-07-07T13:58:06 · `unhandled_exception` · **46.85 h** · run_054
**Detail as recorded:** `run_protocol.py failed:` followed by a pandas
`FutureWarning` about `.fillna`/`.ffill` downcasting — the 300-character truncation
consumed the entire detail on a warning, and the actual error never made it into the
record. `run_054`'s `last_error` is `null` today (cleared on resume).
**What the human did:** unrecoverable. Resumed 2026-07-09T12:49:14. No commit in window
(the next commit, `d9fc4e7e`, is 2026-07-13 and bundles six days of work including a
289-line change to `tools/run_protocol.py` — it *may* contain the fix; that is
speculation and is labelled as such).
**Class: UNDECIDABLE. Stated plainly rather than guessed.** This is the largest halt in
the record and 37% of all downtime, and there is no evidence on disk that decides it.
What would have settled it: an untruncated, non-clearing failure record.
**One thing did change since:** this exact call site now records a trial. H4
(`_record_failed_backtest_trial`, issue #28 / E-025, 2026-08-16) fires on a non-zero
`run_protocol.py` exit — at the time of this halt, a backtest that touched market data
and crashed left **no trial row at all**, so N silently under-counted a spent look.

### #8 — 2026-07-09T13:53:37 · `no_signal_artifact` (**misreported**) · 0.91 h · run_054
**What it actually was:** `component_execution_error`. RUNBOOK §4 documents this
incident by date: *"confirmed live: a fresh `component_execution_error_flagged: true`
pause was misreported as `no_signal_artifact` because that flag was never cleared after
the original 2026-07-07 pause was resolved"* (i.e. #6's flag). `_classify_human_pause`
checks `no_signal_artifact_flagged` **before** `component_execution_error_flagged`, so
the stale higher-priority flag masked the live one.
**What the human did:** no `RESUME` line; the next log event is a `STAGE` line 55
minutes later. No commit in window.
**Class: quarantine-safe** (as the `component_execution_error` it really was — see #13
for the trial-accounting rule that class carries).
**Counted in the "1 of 14 confirmed misreports" figure above.**

### #9 — 2026-07-09T14:48:27 · `component_execution_error` · 2.13 h · run_054
The same underlying pause as #8, correctly classified once the stale flag was cleared.
No `RESUME` line; no commit in window.
**Class: quarantine-safe.**

### #10 — 2026-07-09T16:56:17 · `unhandled_exception` · 1.26 h · run_054
**Detail:** `Claude Code returned an error result: success`.
**Class: retry-safe — proven, and ALREADY FIXED.** `claude_agent_sdk==0.2.82` returns
`is_error=True` paired with `subtype: "success"`; the SDK falls back to the subtype
string as the error text. Independently verified at the time by reading the installed
package source (`_internal/query.py`), not assumed. Ledger **A11 CLOSED**, commit
`9bf2a4cf`: `_invoke_agent_with_yaml_retry` re-invokes the same stage once on an exact
string match, with three fixtures including one asserting a *second* occurrence still
raises. This is the epic's own "the system already has ad-hoc, one-defect-at-a-time
recovery" evidence.

### #11 — 2026-07-16T11:44:16 · `unhandled_exception` · 1.09 h · run_058
**Detail:** `Missing files: ['runs\\run_058\\artifacts\\innovation_notes.yaml']` — the
stage wrote 1 of 2 required deliverables.
**What the human did:** the operator ruled it a single LLM formatting fault, not
systemic, and ordered a resume with a one-variant-only constraint. The in-window commit
`996f4325` is 6 lines added to `briefs/H-041-C-v2.md` — a brief edit, no code. Filed as
ledger **A10** at watch level: *"missing-deliverable stage failures get zero retries…
filed at watch-level pending a second occurrence."*
**Class: quarantine-safe today, and an explicit operator question for S2 (see below).**
A10 itself names the retry as the natural fix "if it recurs." It has recurred — see the
cross-run scan.

### #12 — 2026-07-16T14:08:46 · `unhandled_exception` · 20.62 h · run_058
**Detail:** `Claude Code returned an error result: success` — the same SDK defect as #10.
**Class: retry-safe — proven, ALREADY FIXED.** The fix commit `9bf2a4cf` landed inside
this halt window (2026-07-17T10:45:10). On the subsequent relaunch, `validation`
succeeded on the first invocation and the retry rider was not even needed.
**#10 + #12 = 21.9 h, the epic's "already fixed" figure, reproduced.**

### #13 — 2026-07-18T05:38:24 · `component_execution_error` · 10.27 h · run_059
**What it was:** a genuine engine bug, and the most expensive kind — **silent**.
`FundingRateMeanReversionComponent` produced `avg_forecast=0.0` on all 1,568 bar-symbol
instances at 1d with `component_error_count=0` — no exception at all.
`CandleBuilder._align()` round-tripped timestamps through the local timezone, so no
daily candle ever landed on `hour=00` and the component's `hour % 8 == 0` settlement
check failed on every bar. At 1h the offset is an exact multiple of the interval and
cancels — which is why nothing caught it earlier.
**What the human did:** in-process repro against the real `DataManager`/`CandleBuilder`
chain, then the fix at the confirmed site only — commit `2529f5b5`, in-window, plus the
first 1d regression coverage. Resumed via the 4-step procedure that this arc then wrote
into RUNBOOK §3.
**Class: quarantine-safe — with a mandatory trial-accounting rule.** No retry can fix a
real engine bug, and the queue has no reason to stop. But F6's own text
(`run_phase1_research.py:4728-4737`) is binding on what quarantine must record: *"Fix
the component/config, then re-run fresh. **No trial or parameter-dimension slot is
consumed; no family is marked failed.**"* Any trial row already written for such a run
must be marked invalid (`_mark_trial_invalidated` exists) — not deleted, not counted.

### #14 — 2026-07-18T16:01:07 · `component_execution_error` · 20.43 h · run_059
**What the human did:** resumed 2026-07-19T12:26:54; the run reached its terminal
`completed_rejected` **2 minutes and 17 seconds later**, producing the campaign's first
fully mechanically-evaluated C7 verdict. **No commit exists between the halt and the
resume** (verified: `2529f5b5` at 2026-07-18T09:54 precedes the halt; the next commit is
2026-07-19T18:32, after it). The intervention was state-only.
**Class: retry-safe — conditional on the retry clearing flags, per #5.** A bounded
automatic retry would very likely have reached the same terminal verdict without the
20.4 h wait.
**Reason-code provenance: UNDECIDED.** I could not determine whether the code
`component_execution_error` was (a) a fresh F6 diagnosis by `verdict_interpreter` on its
second pass or (b) a stale-flag misreport in the shape of #8. What I could establish:
the log line reads `pending_stage=human_pause status=active`, which is the exact
fingerprint of ledger **A12** — the `verdict_interpreter` branch
(`run_phase1_research.py:5300-5303`) lacks the `if next_stage == "human_pause": …; break`
guard its `holdout_evaluation` sibling has, so a pause set by F6 gets clobbered back to
`status="active"` by the generic completion block. What I could *not* close: only 5
seconds separate `pass_rule_evaluation.yaml`'s `evaluated_at`
(`2026-07-18T16:01:02Z`, written inside `protocol_execution`) from the halt, and an LLM
`verdict_interpreter` invocation takes ~134 s (its own audit entry). The intermediate
attempt's audit record is gone: RUNBOOK §4.5's known crash-resume limitation means the
`verdict_interpreter_attempt_0` key was **overwritten**, and the surviving
`verdict_interpretation.yaml` is the 2026-07-19 post-resume version
(`root_cause: already_priced_in`). The evidence that would decide this was destroyed by
a known, documented, accepted-as-cosmetic limitation — which turns out not to be cosmetic
once a policy wants to reason about attempts.

---

## Corroboration outside `campaign_log.md`

The S1 brief asks for halts on other run families. `campaign_log.md` only covers the
`run_campaign.py` queue-driver era (run_053 onward); runs 001–052 were driven directly
and wrote no `HALT` lines. Scanning all 58 `pipeline_state.yaml` files instead (59 run
dirs; `run_0001` has no state file) found **18 runs carrying a `last_error`**, none of
them in the 14:

| Signature | Count (of 18) | Runs | Bearing on the taxonomy |
|---|---|---|---|
| unparseable LLM YAML | 6 | 006, 024, 025, 026, 030, 050 | Already has a bounded retry — F4b's YAML-repair path |
| missing/bad path | 3 | 002, 027, 031 | Deterministic; a retry re-reads the same bad path |
| unrecognized status enum | 3 | 004, 005, 009 | `Unknown validation status: Refine` / `conditional_approve`; same shape as #1's F4f |
| SDK result misclassification | 3 | 028, 043, 047 | **5 total occurrences with #10/#12** — retry-safe call confirmed |
| missing deliverable | 2 | 003, 048 | **4 total occurrences with #3/#11** |
| `NoneType` attribute access | 1 | 018 | 2 total with #1 |

**Read this as frequency evidence, not as halts.** These are `last_error` snapshots;
`last_error` is sticky and only cleared explicitly, and 12 of the 18 carry
`status: active`, meaning the run continued past the error. I cannot compute downtime
for any of them and do not claim they each stopped anything. They survived precisely
*because* nobody ran `--resume` on them — which is itself the point about the record's
durability.

Two things follow that the 14-halt sample alone could not establish:

1. **The SDK defect occurred 5 times, not twice.** The retry-safe classification of #10
   and #12 does not rest on two data points.
2. **Missing-deliverable has 4 occurrences** (`run_003`, `run_048`, #3, #11). Ledger A10
   filed it at watch level *"pending a second occurrence"* and left acceptance criteria
   undefined. That trigger is met several times over. **This is an operator call, not
   mine** — I am reporting that A10's own condition has fired, not deciding it. The
   complication is that only #11 is a clean instance of the LLM-formatting fault the
   operator classified; #3's resolution was an integrity discard (see #3).

---

## Proposed policy shape for S2 (rules, not code)

**R1 — Integrity classes never auto-anything.** `kb_reactivation_violation`,
`research_only_unverified`, `provisional_promote_awaiting_holdout`,
`provisional_promote_holdout_inconclusive`, `conformance_gate_failure`,
`pass_rule_evaluation_disagreement`, `stale_escalation_unclaimed`, `wishlist_trigger*`,
`refinement_brief_conflicts_with_existing_continuation` → escalate to a human, exactly as
today. The first four touch the holdout or tradability; the next three touch
pre-registration; the wishlist pair touches KB reactivation. No retry, no quarantine, no
queue advance.

**R2 — Retry on an exact failure signature, never on a reason code.** `unhandled_exception`
covers 6 of the 14 halts and at least four unrelated root causes. The reason code carries
no retry information. The one proven-retryable signature is an exact string match, and it
is already implemented that way.

**R3 — A retry that does not clear the previous attempt's state is not a retry.** Halt #5
is the proof: `--resume` verified `status`/`pending_stage`, re-entered, and the classifier
halted again one second later on a `flags` entry nothing had cleared. The clear-list must
be the complete, correctly-ordered flag set the classifier reads *plus* its state-key
counterparts (`conformance_violations`, `kb_reactivation_violations`) — RUNBOOK §4 already
enumerates it.

**R4 — Same reason code twice in a row on the same run ⇒ stop retrying, escalate.**
Supported by both repeat pairs in the record (#4/#5 on run_053, #13/#14 on run_059) and
consistent with the existing local precedent — the A11 SDK retry fires once and re-raises
on a second occurrence.

**R5 — One automatic retry per (run_id, stage, signature), and campaign-level retries must
not stack on stage-level ones.** `_invoke_agent_with_yaml_retry` already nests two retry
loops (F4b YAML repair × A11 SDK). A campaign-level retry layered on top silently turns
"one attempt" into four, multiplying both token spend and the number of times a stage
touches data.

**R6 — Quarantine records, it does not discard.** Minimum record per quarantined run:
run_id, queue entry id, reason code, **untruncated** failure text, `pending_stage` at
halt, the `flags` dict verbatim, retry attempts made and their outcomes, and the
trial-accounting disposition below. Without the untruncated text, S2 reproduces #7.

**R7 — Trial accounting on quarantine (the deflated-Sharpe honesty rule).** Three cases,
all with existing machinery:
- *Touched market data, backtest raised* → `backtest_failed` row via
  `_record_failed_backtest_trial` (H4, issue #28). Excluded from DSR N by the
  `statistic_neither` bucket; counted in `total_hypotheses_tested`. Deliberately
  over-counts — a larger N only deflates a candidate Sharpe further, the anti-flattering
  direction.
- *Reached prescreen, killed there* → an A6.2 prescreen row already exists
  (`statistic_valid: 'neither'`). Nothing new needed.
- *Failed before any data touch* (e.g. #11, `innovation_expansion`) → no trial row, and
  the quarantine record must carry `no_data_touched: true` so the absence is a recorded
  decision rather than a gap someone later has to re-derive.
- *`component_execution_error` specifically* → F6 is binding: no trial or
  parameter-dimension slot is consumed and no family is marked failed. Any row already
  written for that run is marked invalid via `_mark_trial_invalidated`, never deleted.

**R8 — Quarantine must never write a scientific outcome.** A quarantined run gets
`outcome: quarantined_engineering_failure` (or `blocked_on_component:<name>`, R9), never
`completed_rejected`. F5c and F6 both say in their own text that these are not research
findings. `run_058` shows what a genuine `completed_rejected` looks like — a validation
gate rejecting on stated economic grounds.

**R9 — `component_gap` / `new_component_escalation` quarantine as re-queueable.**
`blocked_on_component:<name>`, not `done`. `_select_entry` already skips `blocked_on_*`,
so the queue advances and the hypothesis survives for whoever writes the component.

**R10 — Make the halt record durable BEFORE automating anything (prerequisite).** Today
`last_error` is truncated to 300 characters at halt time and set to `null` on resume, and
a crash-resume overwrites the stage's `attempt_N` audit entry rather than appending. Those
three properties are why 46.9 h of downtime (#7) and the provenance of another 20.4 h
(#14) are unclassifiable. A policy that decides retry-vs-escalate on evidence the system
erases will make confident wrong decisions.

**R11 — Escalate on ambiguity, and record that it was ambiguous.** A stale higher-priority
flag can mask a live pause (#8, confirmed). Until R3's clearing discipline is enforced
everywhere, the policy should cross-check the `flags` dict against the pause path actually
taken and escalate — visibly — when they disagree, rather than acting on the code.

---

## What I could not decide

Stated plainly, not guessed:

1. **Halt #7's cause (46.85 h, 37% of all downtime).** The record kept a pandas
   `FutureWarning` and discarded the error. Not recoverable from anything on disk.
2. **Halt #14's reason-code provenance.** Fresh F6 diagnosis or stale-flag misreport — the
   5-second window between `pass_rule_evaluation.yaml`'s `evaluated_at` and the halt
   cannot accommodate a ~134 s `verdict_interpreter` invocation, and the intermediate
   audit entry was overwritten by the documented crash-resume limitation. The *class*
   (retry-safe, conditional on flag clearing) is decided on separate evidence — no
   in-window commit, and a 2-minute path to terminal on resume.
3. **Whether missing-deliverable should be retried.** A10's "second occurrence" trigger
   has fired four times over, but only #11 is a clean instance of the fault the operator
   classified as non-systemic. Operator call.
4. **Whether #1's class should be retry-safe rather than quarantine-safe.** A retry that
   re-invokes the stage regenerates the artifact that failed to parse and could plausibly
   succeed; no such retry is recorded as having been attempted. Held at quarantine-safe
   on the strict evidence bar (a demonstrated successful identical retry, or a fix already
   in code). Moot in practice — F4f closed this specific failure.
