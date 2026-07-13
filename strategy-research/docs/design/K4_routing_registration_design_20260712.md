# K4 — Routing/Registration Kernel (A1 + A3 + B1): Design Note

**Phase:** A (design only — no code, no state, no tests written this phase)
**Author:** Implementation agent, this session, 2026-07-12
**Status:** DRAFT — awaiting operator message `DESIGN APPROVED K4` before Phase B (implementation)

---

## 0. Scope and non-goals

In scope: ledger items **A1** (lineage-continuation persistence), **A3**
(atomic-enough scaffold registration + reconciler), **B1** (first-class
refinement-brief ingestion path), designed as one coherent change to the
routing/registration layer per NEXT_SESSION.md task (1) sequencing.

Explicitly NOT designed here (context only, read for non-foreclosure):
A2 (distinct terminal strings for refine vs. pivot), A4 (`quarantined_orphan`
as a first-class recognized status), A6/A7 (`--step` stage-granular mode +
budget accounting), B2 (dry-run branch parity). Each section below states
where this design leaves a hook for those items rather than blocking them.

No campaign process is running (verified: no `campaign.pid` process
responds — operator-stated, not independently re-verified by me this
phase since that would require a shell probe of a live PID, which the
operator's context preamble already supplies and Phase A does not need to
duplicate). `campaign_state.last_escalation.protocol_path` is confirmed
stale (`protocols\escalation_tf_15m.json`, a 15-minute protocol) — nothing
in this design reads or writes `last_escalation`, so no code path here
touches it. Flagging per instructions: not consumed, not triggered.

---

## 1. Ledger items read (context, not fixed here)

A1, A2, A3, A4, A6, A7, B1, B2 — full text already on file in
`PIPELINE_IMPROVEMENTS_20260712_v4.md`; not re-quoted here to keep this
note's own size down. RUNBOOK.md sections 1/3/4 and the end-of-file custody
rule also read (see prior orientation turn this session). The one
addition from this reread worth recording: RUNBOOK's custody rule already
states the exact non-silent-substitution norm this design leans on in
§7 below (agent-authored brief superseded by user-delivered one → renamed
`..._draft_superseded.md`, never silently deleted) — B1's conflict
handling is a direct application of that existing norm, not a new one.

---

## 2. Code quotes (step 2)

### (a) `lineage_new_runs` computed from a runs/-directory diff bracketing one `process_once()` call

`workflow/run_campaign.py`:

```python
# lines 809-815
run_dir = ROOT / "runs" / run_id
before_dirs = _snapshot_run_dirs()
before_splits = _snapshot_hypothesis_splits()
orch.run_loop(run_id)
after_dirs = _snapshot_run_dirs()
after_splits = _snapshot_hypothesis_splits()
new_runs = sorted(after_dirs - before_dirs)
...
# line 847
lineage_new_runs = [r for r in new_runs if r not in split_child_ids]
# line 848
if pending in _LINEAGE_CONTINUATION_STAGES and lineage_new_runs:
```

`_LINEAGE_CONTINUATION_STAGES` itself (line 72):

```python
_LINEAGE_CONTINUATION_STAGES = ("completed_reframed", "completed_escalated")
```
— `completed_refined` (the string both `_route_refine` and `_route_pivot`
return, see (b) below) is absent, confirming A1's first symptom.

Trace confirming the two-part bug (verified against `run_phase1_research.py`,
not just asserted): `run_loop()`'s main while-loop guard is

```python
# line 3544-3547
TERMINAL_PREFIXES = ("completed", "rejected", "human_pause", "failed_validation")
if not current_stage or current_stage.startswith(TERMINAL_PREFIXES):
    print(f"🏁 Pipeline finished. Final state: {current_stage}")
    break
```

`_route_refine`/`_route_pivot` are invoked *synchronously inside* the same
`run_loop()` call, from `determine_post_verdict_route()` (line 3341-3345),
itself called from the `verdict_interpreter` stage's routing block (line
3776) within the *same* while-loop iteration that later sets
`pending_stage = "completed_refined"` (lines 3792-3797) and reloads state
(line 3800) — the loop then re-enters, sees `pending_stage` starts with
`"completed"`, and breaks. So the child directory (created by
`setup_next_run`/`_scaffold_next_run` inside `_route_refine`/`_route_pivot`,
see (b)) **is** created inside the same `process_once()` call that
observes it, *the first time through*. The bug bites on the *next*, separate
`process_once()` call: `entry["run_ids"][-1]` is still the parent run
(only appended to `run_ids` by the `CONTINUE` branch, which never fired
because `completed_refined` wasn't in the tuple — so it fell through to
`DONE` already). A fresh `process_once()` call selects that same
(now-`done`, per the bug) or still-`in_progress` entry, calls
`orch.run_loop(parent_run_id)` again — but `pending_stage` is *already*
`completed_refined`, so the while-loop breaks on its very first check
(line 3545) without doing anything. `before_dirs`/`after_dirs` for *this*
call are therefore identical (the child dir already existed before this
call started) — `new_runs` is empty regardless of whether the tuple is
fixed. This is the crash-window/cross-invocation half of A1 the ledger
describes, and it reproduces even with `completed_refined` added to the
tuple, exactly as NEXT_SESSION.md states.

### (b) Scaffold creation and registration are separate operations

`_route_refine` (lines 1933-1959), the scaffold call:

```python
next_id = _next_run_id(run_id)
print(f"\n🔄 REFINE (altitude 1): setting up {next_id} with proposed brief.")
setup_next_run(path, next_id)          # <- creates runs/<next_id>/... on disk
...
return "completed_refined"             # <- no registration write anywhere here
```

`setup_next_run` (lines 1460-1466):

```python
def setup_next_run(current_run_path: Path, next_run_id: str):
    _scaffold_next_run(next_run_id)
    proposed  = current_run_path / "artifacts" / "proposed_brief.yaml"
    next_brief = ROOT / "runs" / next_run_id / "artifacts" / "research_brief.yaml"
    shutil.copy(proposed, next_brief)
```

`_scaffold_next_run` (lines 1442-1457) shells out to `setup_run.py` as a
**subprocess**, which itself calls `create_pipeline_state()`
(`setup_run.py` lines 33-80) — the directory and its fresh
`pipeline_state.yaml` exist on disk the moment that subprocess returns.
Nothing in `_route_refine`/`_route_pivot`/`_route_escalate` writes to
`campaign_queue.yaml` or `campaign_state.yaml`'s `runs` list — that
registration happens only in `run_campaign.py::process_once()`'s
`CONTINUE`/`LAUNCH` branches, a different file, a different (wrapper)
process layer, always *after* `run_loop()` has already returned. This is
the exact separation A3 flags.

`process_once()`'s own fresh-launch path shows the same two-step split on
its own side (lines 796-805):

```python
if not entry.get("run_ids"):
    brief_path = ROOT / entry["brief_path"]
    brief = _parse_brief_frontmatter(brief_path)
    run_id = _next_new_run_id()
    setup_run(run_id)                # <- mkdir + pipeline_state.yaml on disk
    _materialize_run(run_id, brief)  # <- research_brief.yaml (+ pre_registration.yaml)
    entry["run_ids"] = [run_id]
    entry["status"] = "in_progress"
    _save_queue(queue)               # <- registration, separate write, separate file
```
A crash between `setup_run(run_id)` and `_save_queue(queue)` leaves a
fully- or partially-materialized run directory with **zero** references
in `campaign_queue.yaml` or `campaign_state.yaml` — see §4 below, where
`run_051`/`run_040` are live instances of exactly this shape.

### (c) `brief_path` is consumed only on fresh launch

Confirmed at the same lines quoted in (b): the `_parse_brief_frontmatter`
+ `_materialize_run` call is gated behind `if not entry.get("run_ids")`.
The `else` branch (line 806-807) does nothing with `brief_path` at all:

```python
else:
    run_id = entry["run_ids"][-1]
```
There is no code path anywhere in `run_campaign.py` that re-reads
`brief_path` (or any brief-like field) for an entry that already has
`run_ids` — confirms B1's stated symptom exactly.

---

## 3. Consumers of `pipeline_state.yaml`'s `artifacts` field (step 3)

Grepped `run_phase1_research.py`, `run_campaign.py`, `setup_run.py`, and
the rest of `strategy-research/` for any read of the state-dict key
`artifacts` (as opposed to the `artifacts/` *directory*, which is read
constantly and is not what's being asked about here).

**No consumer found anywhere.** `setup_run.py::create_pipeline_state()`
(line 56) is the *only* writer (`"artifacts": {}` in the initial state
dict); no code in this repo ever reads `state["artifacts"]` or
`state.get("artifacts")`, and no code ever writes a non-empty value into
it. It is dead/vestigial — every real run's `pipeline_state.yaml`
(`run_051`, `run_026`, `run_031`, `run_036`, `run_040`, and by inspection
the general shape) carries `artifacts: {}` forever regardless of how many
real files exist under `artifacts/` on disk. This fully explains the
operator's run_057 observation (`artifacts: {}` despite artifacts on
disk) as pre-existing, unrelated dead code — not a defect introduced by,
or in scope for, A1/A3/B1. No design decision below writes to or reads
this key; the new `continuation_child`/`continuation_created_by` fields
(§5) are added as sibling top-level keys, not nested under `artifacts`,
so there is no collision risk with whatever future work (if any) revives
this field.

(Aside, also out of scope, noted only because it surfaced while reading
this code: run_057's missing `signal_prescreen` `audit_log` entry is
explained by the `_skip_agent` short-circuit at line 3609-3639 — the A8.6
power pre-flight can resolve `signal_prescreen` without ever calling
`_invoke_agent_with_yaml_retry`, which is presumably the only writer of
`audit_log` entries. Not verified further; not this kernel's concern.)

---

## 4. Spot-checked run directories (step 4)

Read-only. No README/notes files exist in any of the five directories
checked (`run_051`, `run_026`, `run_031`, `run_036`, `run_040` all contain
only `artifacts/`, `handoffs/`, `pipeline_state.yaml`, and — for
026/031/036 — `protocol_summary.json`/`results/`).

| run | status | pending_stage | apparent origin |
|---|---|---|---|
| `run_051` | active | `hypothesis_generation` | Fresh scaffold, `completed_stages: []` — never actually started. Consistent with a crash or abandoned allocation right after `setup_run`/`_scaffold_next_run`, before any stage ran. |
| `run_026` | active | `completed_reframed` | Ran through `verdict_interpreter` → `campaign_review`; `last_error` shows a YAML parse failure (`mapping values are not allowed here...`, 2026-06-29T08:00) during/after `campaign_review`. Reached the reframe-terminal `pending_stage` but was never picked up by a continuation — exactly the orphan-lineage shape A3 describes: routing set the terminal string, no registration followed. |
| `run_031` | **failed** | `campaign_review` | Ran through `verdict_interpreter`; `last_error`: `[Errno 2] No such file or directory: 'runs\run_031\artifacts\proposed_brief.yaml'` (2026-06-29T21:41). Reads as an attempted refine route whose `proposed_brief.yaml` was never produced, raising inside `run_loop`'s except-block (line 3802-3805) rather than hitting `_route_refine`'s own graceful `if not proposed.exists()` guard (line 1935-1937) — meaning the missing-file access happened somewhere else in the stack, before or outside that guard. Not re-diagnosed further; out of scope for K4, flagged for the deferred-fixes list. |
| `run_036` | active | `verdict_interpreter` | Ran through `protocol_execution`; `audit_log: {}` (empty) even though `completed_stages` lists five real stages — consistent with tool-only stages (e.g. `protocol_execution`) not writing `audit_log` entries at all (no LLM invocation), not a new bug. Stalled before `verdict_interpreter` ran; no further trace of why. |
| `run_040` | active | `hypothesis_generation` | Same shape as `run_051` — fresh, unstarted scaffold. |

### Grandfather-baseline list cross-check (21 entries named in the prompt)

I cross-checked the stated 21-id list
(`run_0001`–`run_010`, `run_026`, `run_031`, `run_036`, `run_040`,
`run_045`, `run_046`, `run_049`, `run_051`, `run_052`, `run_055`,
`run_056`) against `campaign_queue.yaml` (`run_ids`:
`P4_ts_trend` → `[run_053, run_054, run_057]`, `XS_momentum` → `[]`) and
`campaign_state.yaml`'s `runs` list (33 ids, `run_011`–`run_054` minus
gaps). Naive arithmetic (57 dirs on disk − 34 ids referenced by
queue-run_ids ∪ campaign_state.runs) gives **23**, not 21 — a two-id
discrepancy against the operator-supplied list.

Investigated rather than assumed correct either way (per the standing
recomputation-over-narrative rule): `run_041` and `run_042` are **not**
in `campaign_state.yaml`'s `runs` list, but **are** referenced in
`campaign_state.yaml`'s `trial_sharpes` list
(`trial_id: run_041` / `run_042`, `source: prescreen_backfill`,
`hypothesis_id: H-041-A` / `H-041-C`). `trial_sharpes` is a legitimate,
independent registration surface that the operator's shorthand
"campaign_state" doesn't literally name but clearly should include —
folding it in reconciles the arithmetic exactly (57 − 34 − 2 = 21,
matching the supplied list). **No discrepancy to report**: the
operator-supplied list is correct; my job is to make sure the *reconciler
design* (§6) checks `trial_sharpes[].trial_id` (and, for the same reason,
`hypothesis_splits[].parent_run`/`.children`) as registration surfaces in
their own right, not just `campaign_state.runs` — otherwise a rebuilt
reconciler would falsely flag `run_041`/`run_042` as new orphans the
first time it runs. This is folded into §6.

I did not independently re-verify the apparent origin of `run_045`,
`run_046`, `run_049`, `run_052` this phase (not in the five directories
step 4 named for spot-check) — flagged as an open item before the
frozen-baseline file (§6) is actually populated in Phase B; that
population is a data-entry task, not a design decision, so it doesn't
block DESIGN APPROVAL, only the baseline file's final content.

---

## 5. Design: A1 — persisted continuation intent

**Where:** the run's own `pipeline_state.yaml` (per-run file, currently
sole-written by `run_phase1_research.py`'s `update_state()`), **not**
`campaign_state.yaml`.

**Why not `campaign_state.yaml`:** that file already has many independent
writers (`record_pivot`, `record_escalation`,
`update_campaign_state_after_run`, `_mark_campaign_status`, KB writeback,
etc.) called from scattered routing sites, and RUNBOOK.md's own standing
rules name it (alongside `campaign_queue.yaml` and the wishlist files) as
shared state with real concurrent-writer risk — the file
`incident_20260710` is about. Adding a new load-bearing field there
increases contention surface for no benefit: the information
("does *this* run have a child, which one, created by which route")
is intrinsically per-run data, and `pipeline_state.yaml` already has
exactly one writer for a given `run_id` by convention. Keeping it local
also means the write is naturally co-located (same `update_state()` call)
with the existing `pending_stage` transition — see atomicity below.
`run_campaign.py`'s own queue file (`campaign_queue.yaml`) was a third
candidate but is rejected for a stronger reason: the routing decision is
made deep inside `run_phase1_research.py`, which by explicit design
(module docstring, `run_campaign.py` lines 13-16) knows nothing about
`campaign_queue.yaml` — writing there from `_route_refine` would add a
second writer to a file `run_campaign.py` currently owns exclusively,
which the single-writer-per-state-store rule argues against introducing
without need.

**Fields (new, top-level in `pipeline_state.yaml`):**
- `continuation_child: <run_id> | null` — the run_id this run's routing
  scaffolded, if any.
- `continuation_created_by: "_route_refine" | "_route_pivot" | "_route_escalate" | null`
  — which routing function created it. This is deliberately *not* a
  rename of the terminal string itself (`pending_stage` stays
  `completed_refined`/`completed_escalated` exactly as A2 finds it) —
  it's an additive, separately-auditable field. Framed this way, it
  doubles as an early, minimal instance of A2's own proposed
  `route_taken` field; A2's later work can either keep this field as-is
  or promote/rename it, but nothing here forecloses that.

**Write site:** one line added at the end of each routing function,
*before* it returns its terminal string, in the same `update_state()`
call idiom already used elsewhere in this file (not a new file, not a
new writer — `run_phase1_research.py` already owns
`runs/<run_id>/pipeline_state.yaml`):

```python
# _route_refine, right after setup_next_run(path, next_id) succeeds:
update_state(path=path, continuation_child=next_id,
             continuation_created_by="_route_refine")
return "completed_refined"
```
(same pattern in `_route_pivot` after its scaffold+carryover copy, and in
`_route_escalate`'s `instrument`/`timeframe` branches after
`_scaffold_next_run`/brief-copy, both before `return "completed_escalated"`
— the `new_component` branch returns `"human_pause"`, not a continuation
stage, so it's untouched).

Because `update_state()` only merges keys explicitly passed as kwargs
(line 386-389: `if isinstance(value, dict) and key in state...: state[key].update(value) else: state[key] = value`),
the *later* `update_state()` call in `run_loop`'s own step 6 (line
3792-3797, which sets `pending_stage`/`completed_stages`/`status` but
does **not** pass `continuation_child`) cannot clobber the value just
set — confirmed by reading `update_state`'s merge logic directly, not
assumed.

**`run_campaign.py::process_once()` change:** replace the dir-diff
(`before_dirs`/`after_dirs`/`new_runs`/`lineage_new_runs`, lines 809-815,
847) with a direct read of the run's own persisted field:

```python
state = orch.load_yaml(run_dir / "pipeline_state.yaml")
...
pending = state.get("pending_stage") or ""
continuation_child = state.get("continuation_child")
if pending in _LINEAGE_CONTINUATION_STAGES and continuation_child:
    entry["run_ids"].append(continuation_child)
    _save_queue(queue)
    _log(f"CONTINUE {entry['id']} lineage {run_id} -> {continuation_child} ({pending})")
    return True
```
`_LINEAGE_CONTINUATION_STAGES` gains `"completed_refined"` (covers both
refine and pivot, since both currently return that same string — see
A2 note above). The `_snapshot_run_dirs`/`before_dirs`/`after_dirs`
machinery stays (still needed for split-child detection, which is an
orthogonal, already-working mechanism keyed off
`campaign_state.hypothesis_splits`, not touched by this change) but
`lineage_new_runs`/`new_runs` as inputs to the *lineage-continuation*
decision are removed; `new_runs` remains only for the split-detection
math (`split_child_ids`).

**Crash-window analysis:** the remaining window is between (i)
`setup_next_run`/`_scaffold_next_run` finishing (child directory +
child's own fresh `pipeline_state.yaml` now exist on disk) and (ii) the
new `update_state(..., continuation_child=next_id, ...)` call landing on
the *parent's* file. A crash inside that window leaves a real,
fully-scaffolded child directory with **no reference anywhere** —
structurally identical to the A3 orphan pattern (§6), and closed by the
same reconciler, not by A1 itself. This ordering (child-dir-first,
parent-record-second) is deliberate: the alternative order (record
`continuation_child` on the parent *before* the child directory exists)
produces a strictly worse failure mode — a dangling reference to a
run_id with no directory, which would crash `orch.run_loop()` on the next
`process_once()` call rather than merely sitting inert as an
undiscovered orphan. Recording second, after the scaffold is known-good,
means the only possible inconsistency is "orphan, safely ignorable until
found," never "dangling reference, actively crashes on next use."

True atomicity (single filesystem transaction covering both the child
scaffold and the parent's state write) is not attempted and is not
achievable here without much larger surgery (the child scaffold for
`_route_pivot`/`_route_escalate` goes through a `subprocess.run(...,
setup_run.py, next_id)` boundary — line 1451/1969/2010/2045 — so even a
temp-then-rename scheme on the Python side wouldn't make the subprocess's
own file writes part of the same transaction). Given the reconciler makes
the residual window loudly detectable and inert rather than
silently corrupting state, this is judged sufficient for K4; a
temp-then-rename hardening is noted as a possible future increment in
§9, not required for this kernel's acceptance criteria.

---

## 6. Design: A3 — scaffold/registration + reconciler

**Atomicity mechanism:** kept as write-order (mkdir/materialize first,
registration last) — this is already `process_once()`'s current order
(§2b) and, of the three options named in the prompt, has the safest
failure mode. Evaluated the other two explicitly:
- *registration-before-mkdir* — inverts the failure mode to "a
  campaign_queue.yaml entry references a run_id with no directory on
  disk," which crashes the next `orch.run_loop()` call outright, worse
  than an inert orphan.
- *temp-then-rename* — would remove the sub-case of a **partially**
  materialized directory being visible under its real name (e.g. a dir
  with `pipeline_state.yaml` written but `research_brief.yaml` not yet),
  which is a real (if narrower) improvement, but doesn't fully close the
  window either (the rename and the queue-file save are still two
  separate operations), and — same subprocess-boundary problem as
  §5 — doesn't compose cleanly with `setup_run.py` being invoked via
  `subprocess.run` from three call sites. Recorded as a candidate future
  hardening (§9), not adopted now: the reconciler below makes the
  residual window safe either way, so the marginal benefit doesn't carry
  its added complexity for this kernel.

**Crash window that remains:** "materialized but not yet registered" —
directly evidenced, not hypothetical: `run_051` and `run_040` (§4) are
live instances of this exact shape (fresh scaffold, `completed_stages: []`,
referenced nowhere). The reconciler's job is to make this window
*findable and inert*, never to eliminate it outright.

**Reconciler — registration surfaces (corrected per §4's arithmetic
check):** a run_id counts as referenced if it appears in **any** of:
1. `campaign_queue.yaml`: any entry's `run_ids` list.
2. `campaign_state.yaml`: the top-level `runs` list.
3. `campaign_state.yaml`: `trial_sharpes[].trial_id` (needed — see §4;
   `run_041`/`run_042` are only registered here).
4. `campaign_state.yaml`: `hypothesis_splits[].parent_run` and
   `hypothesis_splits[].children[]` (same reasoning — a split sibling's
   `run_id` may legitimately never reach `campaign_state.runs` or
   `trial_sharpes` before its own queue entry is created).
5. The new frozen baseline file (below).

**New frozen baseline file:** `config/campaign_baseline_runs.yaml`.
Proposed schema:
```yaml
version: '1.0'
frozen_at: '2026-07-12'
description: >
  Run directories that predate or fall outside this campaign's normal
  atomic registration path (pre-K4, or manually resolved). A human adds
  an entry here only after manually confirming provenance. Never
  auto-populated by the reconciler; a newly discovered, unlisted orphan
  is always reported as unexpected, never silently grandfathered in.
grandfathered_runs:
  - id: run_0001
    reason: pre-tracking (predates campaign_queue.yaml/campaign_state.yaml)
  # ... run_002 .. run_010, same reason
  - id: run_026
    reason: >
      orphaned mid-reframe; pipeline_state.yaml last_error shows a YAML
      parse failure in/after campaign_review, 2026-06-29. See step-4
      spot-check in K4_routing_registration_design_20260712.md.
  - id: run_031
    reason: >
      failed refine route (missing proposed_brief.yaml, unhandled
      exception), 2026-06-29. Same spot-check.
  - id: run_036
    reason: stalled before verdict_interpreter; no further trace found. Same spot-check.
  - id: run_040
    reason: fresh scaffold, never started. Same spot-check.
  - id: run_045
    reason: NOT YET SPOT-CHECKED -- confirm before treating as grandfathered.
  - id: run_046
    reason: NOT YET SPOT-CHECKED -- confirm before treating as grandfathered.
  - id: run_049
    reason: NOT YET SPOT-CHECKED -- confirm before treating as grandfathered.
  - id: run_051
    reason: fresh scaffold, never started. Same spot-check.
  - id: run_052
    reason: NOT YET SPOT-CHECKED -- confirm before treating as grandfathered.
  - id: run_055
    reason: >
      quarantined_orphan, pivot scaffold of the overturned run_054 kill,
      2026-07-09 (see runs/run_055/ORPHANED_README.md). Never advance,
      reuse, or copy from it (NEXT_SESSION.md state-delta).
  - id: run_056
    reason: same event as run_055.
```
Populating the four `NOT YET SPOT-CHECKED` entries is data entry, not a
design decision — flagged as a Phase-B prerequisite, doesn't block
approval of the mechanism itself.

**Reconciler logic (design, not code):**
```
def _referenced_run_ids() -> set[str]:
    referenced = set()
    queue = _load_queue()
    for e in queue["queue"]:
        referenced.update(e.get("run_ids") or [])
    campaign = orch.load_campaign_state()
    referenced.update(campaign.get("runs", []))
    referenced.update(t["trial_id"] for t in campaign.get("trial_sharpes", [])
                       if t.get("trial_id"))
    for ev in campaign.get("hypothesis_splits") or []:
        if ev.get("parent_run"):
            referenced.add(ev["parent_run"])
        referenced.update(ev.get("children") or [])
    baseline = orch.load_yaml(BASELINE_PATH) or {}
    referenced.update(r["id"] for r in baseline.get("grandfathered_runs", []))
    return referenced

def reconcile_orphans() -> list[str]:
    on_disk = {p.name for p in (ROOT / "runs").iterdir() if p.is_dir()}
    orphans = sorted(on_disk - _referenced_run_ids())
    unexpected = [o for o in orphans if not _is_quarantined_orphan(o)]
    if unexpected:
        _log(f"RECONCILE: {len(unexpected)} unreferenced run dir(s), "
             f"not in baseline: {unexpected}")
    return orphans
```
`_is_quarantined_orphan(run_id)` checks for the existing hand-set
convention (`status: quarantined_orphan` marker / `ORPHANED_README.md` in
that run's directory, per `run_055`/`run_056` precedent) — this is where
the design leaves A4's hook: A4's later work is exactly "make
`quarantined_orphan` a status selectors/reconcilers/`_next_run_id`
explicitly know about"; this reconciler already treats "known quarantined"
and "newly unexpected" as separate buckets so A4 has something concrete
to formalize rather than needing to touch this function's shape again.

**When it runs:** once, read-only, at the top of `process_once()` (or
`run_forever`'s first iteration) — cheap (a few YAML loads + one
`iterdir()`), before `_select_entry()` picks anything. Also run
(read-only, same function) inside `dry_run_verify()`, logged the same
way, so a broken baseline file or a newly-appeared unexpected orphan
shows up in the zero-footprint dry run before a real launch. `orphans`
(the full list, quarantined + unexpected) is never used to block
`_select_entry()` or `_next_new_run_id()`/`_next_run_id()` — both
already scan `runs/` on disk directly (confirmed reading
`_next_new_run_id`, `run_campaign.py` lines 127-148, and `_next_run_id`,
`run_phase1_research.py` lines 1712-1772), so an orphan's number is
already never reissued regardless of this reconciler; the reconciler's
job is purely detection/reporting, not allocation-safety (that safety
already exists, independently, via the max-scan allocator).

**`quarantined_orphan` never selected/renumbered:** already true today
by the allocator's scan-based design (it occupies a real directory, so
its number is already excluded from `existing_numbers`/`nums`); the only
gap is that `_select_entry()` only looks at `campaign_queue.yaml` entries
(never at bare `runs/` directories) so a quarantined orphan was never
selectable to begin with. No change needed there; noted for completeness
since the prompt asks for it explicitly.

---

## 7. Design: B1 — refinement_brief_path

**New queue-entry field:** `refinement_brief_path` (parallel to the
existing `brief_path`), consumed only when an entry is *already*
`in_progress` (non-empty `run_ids`) — the inverse condition from
`brief_path`'s fresh-launch-only gate, so the two fields are mutually
exclusive by construction (one fires exactly when the other's guard is
false), with an idempotency guard so the same value is never consumed
twice:

```python
if entry.get("refinement_brief_path") and \
   entry.get("refinement_brief_consumed_for") != entry["refinement_brief_path"]:
    parent_run_id = entry["run_ids"][-1]
    ...  # see below
elif not entry.get("run_ids"):
    ...  # existing fresh-launch branch, unchanged
else:
    run_id = entry["run_ids"][-1]
```

**Precedence over internal (LLM-authored) routing — the conflict case:**
if the parent run's own `pipeline_state.yaml` *already* carries a
`continuation_child` (§5 — i.e. `_route_refine`'s internal,
`proposed_brief.yaml`-driven routing already fired, before the operator
had a chance to set `refinement_brief_path`), this is a genuine conflict,
not a silent-override case: two candidate children now exist for the same
lineage step, one LLM-authored, one operator-authored. Per RUNBOOK's own
existing custody norm ("no silent substitution in either direction... an
agent-authored brief that gets superseded... renamed
`..._draft_superseded.md`, never silently deleted"), this design treats
that state as a **new hard-pause** condition
(`refinement_brief_conflicts_with_existing_continuation`) rather than
either discarding the internal child or ignoring the operator's field —
a human decides (rename the internally-scaffolded child's directory per
the existing convention, or explicitly discard the operator's override).
This is a *behavioral* design point (what must happen), not new code
against RUNBOOK's pause table this phase — flagged in §9 as a doc/table
update needed alongside the Phase-B code, since RUNBOOK.md section 3's
table is the authoritative list of pause reasons and currently doesn't
have a row for it.

**Materialization (when no conflict):**
```python
brief_path = ROOT / entry["refinement_brief_path"]
brief = _parse_refinement_brief_yaml(brief_path)   # NEW helper, see below
child_id = _next_new_run_id()
setup_run(child_id)
_materialize_refinement_run(child_id, brief, brief_path)
entry["run_ids"].append(child_id)
entry["refinement_brief_consumed_for"] = entry["refinement_brief_path"]
_save_queue(queue)
_log(f"REFINEMENT-BRIEF {entry['id']} -> {child_id} "
     f"(brief={entry['refinement_brief_path']})")
run_id = child_id
```

**New parser, `_parse_refinement_brief_yaml`:** unlike `_parse_brief_frontmatter`
(which requires a leading `---`-delimited block inside an `.md` file),
this schema is a **plain YAML document** — confirmed against the actual
live file at `briefs/P4_ts_trend_r1_er_gate.yaml` (top-level keys:
`brief_id`, `lineage`, `source`, `status`, `motivating_observation`,
`hypothesis`, `gate_definition`, `inherited_unchanged_from_parent`,
`evaluation` [containing `pass_rule`, `baseline_comparators`,
`metric_basis`], `pre_registration`, `operational_constraints`,
`deferred_fixes_noted_not_actioned_here`). This is, concretely, the
existing manifestation of B1's own stated symptom: this file is the
*current, live* `brief_path` for the `P4_ts_trend` queue entry, and
`_parse_brief_frontmatter` would raise `ValueError` on it today (no
leading `---` block) if that entry's lineage were ever re-driven through
the fresh-launch path — not a hypothetical, a standing landmine in the
current queue file. `_parse_refinement_brief_yaml` loads the file as a
plain `yaml.safe_load`, and validates presence of at minimum `brief_id`,
`lineage`, `hypothesis`, `gate_definition`, `evaluation` (raising a clear
`ValueError` naming the missing key, mirroring
`_parse_brief_frontmatter`'s existing error style) — not full schema
validation, just required-top-level-key presence.

**`_materialize_refinement_run`:**
1. Copy `brief_path`'s raw bytes byte-for-byte into
   `runs/<child_id>/artifacts/user_brief_verbatim.yaml` (custody rule:
   verbatim install, never reconstructed/paraphrased).
2. Compute `sha256` of those bytes; this is the checksum the B1
   acceptance fixture (§8) checks against the source file's own hash.
3. Write `pre_registration.yaml` with: `run_id`, `hypothesis_id` (from
   `brief["brief_id"]`, not a placeholder — closes B6 as a side effect
   for this path specifically, though B6's general fix is separately
   ledgered), `registered_at`, `lineage` (copied verbatim from the
   brief's own `lineage` block: `parent_queue_entry`, `parent_run`,
   `relation`, `parent_verdict`), `gate_definition` (copied verbatim —
   B4 copy-through discipline applied at the one place this kernel
   touches pre-registered text), `pass_rule` (copied verbatim from
   `evaluation.pass_rule` — same discipline; this repo's own
   `evaluation.pass_rule` prose is exactly the underspecified-delegation
   shape B11 flags, but copying it verbatim rather than paraphrasing it
   is still strictly better than today and doesn't require B11's fix to
   be safe), `machine_constraints` (if present, same as today's
   `_materialize_run`), and `user_brief_checksum: sha256:<hex>`.
4. Does **not** decide what `pending_stage` the child starts at beyond
   the existing default (`hypothesis_generation`, set by
   `create_pipeline_state` inside `setup_run`) — see open question in
   §9. I looked for a principled reason to skip stages (the brief reads
   as a fully-specified hypothesis, similar to a
   `hypothesis_generation`-split sibling which *does* skip to
   `innovation_expansion`, `run_phase1_research.py` lines 1828-1832) but
   decided not to invent that here: CLAUDE.md's global workflow rule
   ("Innovation happens before validation") and B1's own acceptance
   criterion don't require a skip, and choosing one unilaterally risks
   silently bypassing a real stage for a brief that *looks* complete but
   wasn't validated by `innovation-expansion`/`quant-validation` against
   this specific gate wording. Left as an explicit open question for the
   operator rather than decided here.

**B2 non-regression (dry-run branching):** extracted a small, shared
classifier so `dry_run_verify()` and `process_once()` don't diverge in
what counts as "the next action" for a given entry:
```python
def _next_action_for_entry(entry: dict) -> str:
    if entry.get("refinement_brief_path") and \
       entry.get("refinement_brief_consumed_for") != entry["refinement_brief_path"]:
        return "refinement_brief"
    if not entry.get("run_ids"):
        return "fresh_launch"
    return "continue"
```
`dry_run_verify()` calls this on its selected entry and, for
`"refinement_brief"`, exercises `_parse_refinement_brief_yaml` +
`_materialize_refinement_run` against a sandboxed `run_dryrun_verify`
directory (same zero-footprint pattern already used for the fresh-launch
branch — `dry_run_verify`, lines 889-947), so a malformed refinement
brief is caught before a real launch. This does **not** achieve B2's full
fix (dry-run parity for the *plain* continuation branch — `"continue"` —
still isn't simulated at all, before or after this change); it only
means B1's *own* new branch doesn't repeat B2's defect on day one. B2
itself stays a separate, later ledger item, now with `_next_action_for_entry`
already available for it to extend.

---

## 8. Fixture plan (design only)

All fixtures run against a sandboxed campaign root, extending the
existing `run_dryrun_verify` precedent (`dry_run_verify()`, lines
889-947: dedicated `run_dryrun_verify` directory under `runs/`, deleted
in a `finally` block, zero real `campaign_state.yaml`/`campaign_queue.yaml`
writes, zero LLM spend via stubbed/synthetic artifacts written directly
rather than invoking agents). For fixtures that need a full *queue* (not
just one run directory), the plan is a temporary copy of
`campaign_queue.yaml`/`campaign_state.yaml` into a pytest `tmp_path`,
with `run_campaign.ROOT`/`QUEUE_PATH`/module globals monkeypatched to
point at the tmp copies for the duration of the test — mirroring how
`tests/test_campaign_config_sync.py` and
`tests/test_daily_bar_engine_support.py` already isolate state (both on
file in this repo; not re-read line-by-line this phase, named from the
directory listing as the existing precedent for this repo's fixture
style).

**A1 fixture** (acceptance: "a refine verdict on fixture run N causes the
NEXT process invocation (fresh process) to launch run N+1, queue entry
still in_progress, child appended to run_ids"):
1. Build a fixture run N with `pending_stage: verdict_interpreter` and a
   stubbed `verdict_interpretation.yaml` (`status: refine`) +
   `proposed_brief.yaml`, under a tmp `runs/`.
2. Invoke `orch.run_loop(N)` directly (not through `process_once`) to
   drive it through `_route_refine` — assert `continuation_child`/
   `continuation_created_by` land in run N's `pipeline_state.yaml`
   *and* run N+1 exists on disk, in one call.
3. **Separately instantiate** `process_once()` (simulating a fresh
   process — no in-memory state carried over, only what's on disk) with
   the queue entry's `run_ids = [N]` and N's `pipeline_state.yaml` as
   just written. Assert: `run_ids` becomes `[N, N+1]`, entry status
   stays `in_progress`, no `DONE` line logged. This is the specific case
   NEXT_SESSION.md's A1 symptom describes and the current dir-diff logic
   fails at zero-warning.

**A3 fixture** (acceptance: "process killed between scaffold and
registration → reconciler flags the orphan on next start"; "a
quarantined_orphan fixture dir is never selected or renumbered over"):
1. Simulate the crash window directly: call `setup_run`/
   `_materialize_run` (or the refine-route equivalent) to create a
   fixture run dir, but *skip* the corresponding queue/`campaign_state`
   registration step (simulating the crash). Call `reconcile_orphans()`
   — assert the new dir appears in its return value and in the
   `RECONCILE` log line.
2. Create a second fixture dir, mark it via the existing
   `quarantined_orphan` convention (status marker / README). Call
   `reconcile_orphans()` — assert it's returned (still reported) but
   does **not** appear in the "unexpected" sub-list, and call
   `_next_new_run_id()`/`_next_run_id()` — assert neither ever returns
   that dir's number (already true today by construction — the fixture
   should demonstrate this rather than newly enforce it) and that
   `_select_entry()` never returns an entry pointing at it as a live
   `run_ids` member.
3. Regression check for §4's correction: a fixture run_id present *only*
   in `trial_sharpes` (not `campaign_state.runs`, not any queue
   `run_ids`) must **not** be flagged by `reconcile_orphans()` — this is
   the `run_041`/`run_042` case, and its absence from the test would
   silently reintroduce the false-positive this design note's own
   arithmetic check caught.

**B1 fixture** (acceptance: "a YAML refinement brief on an in-progress
entry → next invocation scaffolds the child with
user_brief_verbatim.yaml checksum-identical to the source and
pre_registration.yaml populated"):
1. Fixture queue entry: `status: in_progress`, `run_ids: [N]` (N a
   minimal existing fixture run, no `continuation_child` set — the
   non-conflict case). Set `refinement_brief_path` to a fixture copy of
   the real schema shape (minimally, a trimmed version of
   `briefs/P4_ts_trend_r1_er_gate.yaml`'s top-level keys).
2. Run `process_once()`'s new branch. Assert: `run_ids` becomes
   `[N, child_id]`; `runs/<child_id>/artifacts/user_brief_verbatim.yaml`
   exists and its `sha256` equals the source fixture file's own
   `sha256` (computed independently in the test, not by re-reading the
   code's own computed value); `pre_registration.yaml` exists and
   contains `lineage`, `gate_definition`, `pass_rule` (byte-equal to the
   source brief's own values — a one-character-changed corrupted copy
   should fail this assertion, same discipline as B4's own fixture
   plan) and `user_brief_checksum` matching.
3. Idempotency: run `process_once()` a second time with the same
   `refinement_brief_path` unchanged — assert no second child is
   scaffolded (`refinement_brief_consumed_for` guard holds).
4. Conflict case: repeat step 1 but with N's `pipeline_state.yaml`
   *already* carrying a `continuation_child` (simulating internal
   routing having already fired) — assert the new hard-pause fires
   (`refinement_brief_conflicts_with_existing_continuation`) and that
   **neither** child is silently discarded (both directories still
   exist on disk afterward).

---

## 9. Files to be modified (Phase B, not this phase) + open questions

**`workflow/run_phase1_research.py`:**
- `_route_refine` — add `continuation_child`/`continuation_created_by`
  write before `return "completed_refined"`.
- `_route_pivot` — same.
- `_route_escalate` — same, both `instrument` and `timeframe` branches,
  before `return "completed_escalated"`.
- Module docstring note: this modifies `run_phase1_research.py`, which
  `run_campaign.py`'s own top-of-file docstring currently asserts never
  happens ("Nothing in workflow/run_phase1_research.py is modified" —
  `run_campaign.py` lines 13-14). That claim needs updating as part of
  Phase B; flagged here so it isn't missed as a stray inaccurate comment
  afterward (E-series-style doc hygiene, folded into this change rather
  than filed separately since it's a direct consequence of this kernel).

**`workflow/run_campaign.py`:**
- `_LINEAGE_CONTINUATION_STAGES` — add `"completed_refined"`.
- `process_once()` — replace dir-diff-based lineage continuation check
  with the persisted-field read; add the reconciler call; add the
  `refinement_brief_path` branch ahead of the existing fresh-launch
  check.
- New functions: `_referenced_run_ids()`, `reconcile_orphans()`,
  `_is_quarantined_orphan()`, `_parse_refinement_brief_yaml()`,
  `_materialize_refinement_run()`, `_next_action_for_entry()`.
- `dry_run_verify()` — call `_next_action_for_entry()` and branch;
  extend to exercise the refinement-brief path when selected.
- New constant `BASELINE_PATH`.

**`config/campaign_baseline_runs.yaml`** — new file (§6); four entries
need the `NOT YET SPOT-CHECKED` placeholder resolved before being trusted
as grandfathered (`run_045`, `run_046`, `run_049`, `run_052`).

**`RUNBOOK.md`** — section 3's pause table needs a new row for
`refinement_brief_conflicts_with_existing_continuation` (§7); not done
this phase, flagged so Phase B doesn't ship the behavior without the
operator-facing doc catching up in the same change (matches this
session's own E3 doctrine: corrections/new behavior need legible,
co-shipped documentation).

**Open questions for the operator, before/alongside `DESIGN APPROVED K4`:**
1. Should a `refinement_brief_path`-sourced child start at
   `hypothesis_generation` (this design's default, unchanged from today)
   or skip ahead (e.g. to `innovation_expansion` or
   `backtest_specification`), given the brief already carries a fully
   specified hypothesis/gate/pass-rule? Left undecided in §7 — this
   changes pipeline behavior meaningfully and isn't dictated by B1's
   acceptance criterion either way.
2. Confirm the `refinement_brief_conflicts_with_existing_continuation`
   hard-pause (§7) is the wanted behavior for the internal-vs-operator
   collision case, versus some other resolution (e.g. operator brief
   always wins silently, with the internal child auto-renamed
   `_draft_superseded`-style rather than pausing).
3. Whether `config/campaign_baseline_runs.yaml`'s four unresolved
   entries should be investigated now (a small, bounded read-only task)
   before Phase B starts, or deferred to whoever does the Phase-B
   implementation.
4. Whether the temp-then-rename hardening noted in §5/§6 is worth doing
   now (larger, cross-cutting, touches the `setup_run.py` subprocess
   boundary) or left as a future increment given the reconciler already
   makes the residual window safe.

---

## Read-back

File written once; content above is the full note (10 numbered
sections). Read back after write: word/section count confirmed present
(§0 Scope, §1 Ledger items read, §2 Code quotes (a/b/c), §3 artifacts-field
consumers, §4 spot-checked runs + baseline cross-check, §5 A1 design, §6
A3 design, §7 B1 design, §8 Fixture plan, §9 Files-to-modify + open
questions) — 10 sections, matches the step-8 requirement (quotes,
step-3/4 reports, three designs, fixture plan, files-to-be-modified list,
open questions all present as one coherent document).
