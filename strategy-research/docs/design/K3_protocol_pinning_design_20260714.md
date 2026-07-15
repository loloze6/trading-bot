# K3 — Protocol Pinning + Stale-Escalation Hard-Fail (B3 + B10): Design Note

**Phase:** A (design only — no code, no tests, no state written this phase)
**Author:** Implementation agent, this session, 2026-07-14
**Status:** DRAFT — awaiting operator message `DESIGN APPROVED K3` before implementation

---

## 0. Scope and non-goals

In scope: ledger items **B3** (`machine_constraints.protocol_ref` — pin
an EXISTING named protocol file without triggering
`_generate_monthly_windows`) and **B10** (the silent stale-
`campaign_state.last_escalation` fallback, confirmed live for run_057's
own predecessor, must hard-fail instead of silently running the wrong
protocol). Both are one coherent change: B3 gives a brief a way to PIN a
protocol; B10 closes the gap that exists precisely because briefs
currently have no such mechanism and the orchestrator falls back to
stale, campaign-wide state instead.

Not in scope, context only: B4+B7+D3 (copy-through, pre-registration as
required input, operator_directives.yaml), B8 (semantic spec conformance),
C6 (prescreen statistic for latched sparse signals) — none of these
interact with protocol SELECTION, only with what happens after a protocol
is already chosen and executed. K1/K6/A6/C3 (per NEXT_SESSION.md's own
framing) are unrelated re-scoping decisions, untouched here.

No campaign process is running (operator-stated). No code, test, or
config file is touched this phase — every quote below is read-only.

---

## 1. Ledger items read (verbatim, re-confirmed this phase against the
current file, not assumed from memory)

**B3** (`PIPELINE_IMPROVEMENTS_20260712_v4.md` lines 114-127):
> Symptom: `machine_constraints.protocol` triggers
> `_ensure_protocol_from_constraints` → `_generate_monthly_windows`, which
> would have silently REPLACED the pre-registered
> `protocols/ts_trend_daily_v1.json` (15 semi-annual windows) with fresh
> monthly windows... Fix: `machine_constraints.protocol_ref: <path>` —
> pins an existing file, F4d conformance-gate enforces the executed
> protocol matches it, generation path untouched. Acceptance: fixture:
> run with `protocol_ref` executes exactly those windows; a mismatched
> protocol file hard-fails conformance.

**B10** (lines 360-373):
> Symptom: with no run_context.yaml, protocol resolution falls back to
> `campaign_state.last_escalation.protocol_path` — which held
> `escalation_tf_15m.json`, a 15-MINUTE protocol, for this 1d run...
> Code fix: the else-branch must hard-fail (or at minimum
> timeframe-check) instead of silently adopting last_escalation; ties
> into B3 (first-class protocol_ref in machine_constraints). Acceptance:
> fixture: run with mismatched last_escalation and no pin refuses to
> execute rather than running the wrong timeframe.

---

## 2. Code read (quoted, current file, not assumed unchanged from any
earlier session read)

### (a) The stale-fallback branch exists TWICE, verbatim, not once

`workflow/run_phase1_research.py`, `run_tool_worker()`, the
`signal_prescreen` branch (lines 936-949):
```python
run_ctx_path = ARTIFACTS / "run_context.yaml"
run_ctx = (load_yaml(run_ctx_path) or {}) if run_ctx_path.exists() else {}
run_type = run_ctx.get("run_type", "")
if run_type == "replication_diagnostic":
    protocol_path = ROOT / "protocols" / "baseline_v1.json"
elif run_type == "forced_diagnostic":
    proto_name = run_ctx.get("protocol", "baseline_v1.json")
    protocol_path = ROOT / "protocols" / proto_name
else:
    campaign = load_campaign_state()
    last_escalation = campaign.get("last_escalation") or {}
    protocol_path_str = last_escalation.get("protocol_path")
    protocol_path = Path(protocol_path_str) if protocol_path_str else ROOT / "protocols" / "baseline_v1.json"
```
The SAME `protocol_execution` branch (lines 991-1009) — byte-identical
selection logic, only the surrounding print statements differ:
```python
elif stage_name == "protocol_execution":
    ...
    if run_type == "replication_diagnostic":
        print("🔁 replication_diagnostic run — ignoring last_escalation, using baseline_v1.json")
        protocol_path = ROOT / "protocols" / "baseline_v1.json"
    elif run_type == "forced_diagnostic":
        proto_name = run_ctx.get("protocol", "baseline_v1.json")
        protocol_path = ROOT / "protocols" / proto_name
        print(f"🔬 forced_diagnostic run — using protocol: {proto_name}")
    else:
        campaign = load_campaign_state()
        last_escalation = campaign.get("last_escalation") or {}
        protocol_path_str = last_escalation.get("protocol_path")
        protocol_path = Path(protocol_path_str) if protocol_path_str else ROOT / "protocols" / "baseline_v1.json"
```
Any B10 fix that touches only one of these leaves the other live —
`signal_prescreen` runs FIRST in the real pipeline, so a fix applied only
to `protocol_execution` would still let a stale-protocol prescreen
execute (wasting real spend) before ever reaching the second copy.

### (b) The GENERATION path (`machine_constraints.protocol`) B3 must not
touch, and where the new `protocol_ref` key slots in alongside it

`_load_machine_constraints` (lines 1531-1536) reads the WHOLE
`machine_constraints` dict from `pre_registration.yaml` — both today's
`protocol` key and the new `protocol_ref` key would live in this same
dict, as siblings.

`_ensure_protocol_from_constraints` (lines 1564-1611, called from exactly
one site, `run_loop()`'s own top, lines 4030-4034 — confirmed by grep,
not assumed):
```python
def _ensure_protocol_from_constraints(run_dir: Path, run_id: str, constraints: dict) -> Path | None:
    proto_constraint = constraints.get("protocol")
    if not proto_constraint:
        return None
    ...
    windows = _generate_monthly_windows(start, end)
    protocol_obj = {...}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(protocol_obj, f, indent=2)
    ...
    run_ctx = {"run_type": "forced_diagnostic", "protocol": out_path.name}
    save_yaml(run_ctx_path, run_ctx)
    return out_path
```
Call site (`run_loop`, lines 4030-4034):
```python
# F4d: generate the protocol + run_context override from pre_registration.yaml's
# machine_constraints, if present, BEFORE anything else runs. Idempotent.
_machine_constraints = _load_machine_constraints(RUN_DIR)
if _machine_constraints:
    _ensure_protocol_from_constraints(RUN_DIR, run_id, _machine_constraints)
```
This is the ONE place, run once per run at the very top of `run_loop()`,
before the stage loop starts — the natural, and only sensible, place to
ALSO resolve `protocol_ref` (§4). `constraints.get("protocol")` (generate)
and a new `constraints.get("protocol_ref")` (pin) must be mutually
exclusive — nothing today enforces that either way since `protocol_ref`
doesn't exist yet (confirmed: `grep -n protocol_ref` across
`run_phase1_research.py` returns only the ledger's own comment-quotes,
never a real key access).

### (c) The existing conformance gate only checks the GENERATION shape

`_check_prescreen_conformance` (lines 1618-1682), called from exactly one
site, `determine_post_prescreen_route` (line 2963), AFTER a real prescreen
subprocess has already executed:
```python
proto_constraint = constraints.get("protocol")
if proto_constraint:
    expected_symbols = set(proto_constraint.get("symbols", []))
    actual_symbols = set(protocol_obj.get("symbols", []))
    if expected_symbols and expected_symbols != actual_symbols:
        violations.append(...)
    actual_start = min((w["test"]["start"] for w in actual_windows), default=None)
    actual_end = max((w["test"]["end"] for w in actual_windows), default=None)
    ...
```
Two things follow directly from reading this, both load-bearing for §4/§5:
1. This function has NO branch for `protocol_ref` at all today — a
   `protocol_ref`-pinned run's actual executed protocol is currently
   UNCHECKED by this gate (it would silently pass with zero violations,
   regardless of what actually ran).
2. This gate fires ONLY after `determine_post_prescreen_route` runs —
   i.e., AFTER the real `prescreen_signal.py` subprocess has ALREADY
   executed against whatever protocol got selected (line 2963 is reached
   post-hoc). B10's fix must be earlier and stronger than this: the
   stale-fallback branch itself (§2a) must refuse to select a protocol at
   all when it cannot be trusted, BEFORE any subprocess spends real
   compute against the wrong window set — this gate alone, even extended
   for `protocol_ref`, cannot retroactively un-spend that trial.

### (d) The hard-fail cannot be unconditional — `_route_escalate`'s own
children depend on exactly this fallback

Verified by re-reading `_route_escalate` (already quoted in full in the
K4 design note's §2; re-checked here for THIS specific question): the
`instrument` branch writes a `run_context.yaml` for its child with keys
`escalation_type`, `target_symbol`, `target_timeframe`,
`escalation_reason`, `source_run`, `note` — **no `run_type` key at all**,
let alone `"forced_diagnostic"`. The `timeframe` branch writes **no
run_context.yaml override at all** for its child. In BOTH cases, the
child's `run_ctx.get("run_type", "")` is `""` on its very first stage —
it falls into the exact `else` branch quoted in §2a, and its ONLY source
of truth for which protocol to run against is
`campaign_state.last_escalation.protocol_path`, which `_route_escalate`
itself just set correctly, one call earlier, in the SAME routing
function (`record_escalation(...)`, K4/K2 design notes' own quoted code).

This is directly, currently live: `campaign_state.yaml`'s own
`last_escalation` field, as of this session, is
`{"target": "timeframe", "detail": "15m", "protocol_path": "protocols\\escalation_tf_15m.json"}`
— the record of run_049's own (not-yet-executed) 15m timeframe
escalation from run_047. Every context preamble this whole session has
said "do not trigger anything that consumes it" for exactly this reason:
**it is not purely stale garbage — it is also the one currently-live,
correct pointer for run_049's own still-pending lineage**, should it ever
be resumed. A hard-fail that refuses this fallback unconditionally would
break that legitimate case, not just the stale-reuse bug; the two are
presently indistinguishable from the code's point of view, because
`last_escalation` carries no marker of WHICH run it was written for or
whether that run has already consumed it.

### (e) Interaction check with K4 and K2 (per instruction 6e — "none" only
after checking named call sites)

Checked: `_route_refine`, `_route_pivot`, `_route_escalate` (K4's
`continuation_child`/`continuation_created_by` write sites),
`_dispatch_verdict_route`, `_resolve_verdict_fields`,
`_check_pass_rule_evaluation_conformance` (K2's verdict/routing layer),
and `tools/verdict_criteria_evaluator.py`'s `evaluate_pass_rule_criteria`
(K2's C7 evaluator, which itself reads `pre_registration.yaml`'s
`pass_rule` block and `protocol_result.yaml`'s `protocol_file` field for
its own, SEPARATE, name-level `window_set_ref` check — see K2's design
note §6, operator amendment A3). None of K4's routing functions read or
write `machine_constraints`, `protocol_ref`, or `last_escalation` — they
operate entirely after a run's protocol has already been selected and
executed, at the verdict/lineage-continuation layer. **Result: none**,
with one adjacency worth flagging, not a conflict: K2's C7 evaluator
already has its OWN, independently-designed `window_set_ref` field
inside `pre_registration.yaml`'s `pass_rule` block (compared against
`protocol_result.yaml`'s `protocol_file` — a POST-HOC, name-level
evaluation-time check). B3's new `machine_constraints.protocol_ref` is a
DIFFERENT field, checked at a DIFFERENT time (protocol SELECTION,
before any execution) for a DIFFERENT purpose (which file gets run,
not which file's results get evaluated against a pass rule). The two
should almost certainly be required to name the SAME file when both are
present on the same brief — flagged as an open question in §8 rather
than silently assumed, since nothing today enforces that consistency
and a brief author could otherwise register them independently and
inconsistently.

---

## 3. Design: `machine_constraints.protocol_ref` (B3)

### Schema
```yaml
machine_constraints:
  protocol_ref: protocols/ts_trend_daily_v1.json   # path, relative to ROOT
  protocol_ref_note: >                              # optional, human-readable
    Pre-registered semi-annual window set; do NOT regenerate.
```
Mutually exclusive with `machine_constraints.protocol` (the generation
constraint) — a brief specifying BOTH is a materialization-time lint
error (§3, lint), not a runtime ambiguity to resolve by picking one
silently.

### Resolution (new function, `_ensure_protocol_ref_pinned`, called
alongside `_ensure_protocol_from_constraints` at `run_loop()`'s own top)
```python
def _ensure_protocol_ref_pinned(run_dir: Path, run_id: str, constraints: dict) -> Path | None:
    ref = constraints.get("protocol_ref")
    if not ref:
        return None
    ref_path = ROOT / ref
    run_ctx_path = run_dir / "artifacts" / "run_context.yaml"
    if run_ctx_path.exists():
        existing = load_yaml(run_ctx_path) or {}
        if existing.get("run_type") == "forced_diagnostic" and existing.get("protocol") == str(ref):
            return ref_path  # already pinned this run — idempotent, no re-write
    if not ref_path.exists():
        raise FileNotFoundError(
            f"machine_constraints.protocol_ref={ref!r} does not exist at {ref_path} -- "
            f"a pinned ref must name an EXISTING protocol file (this is the whole point "
            f"of pinning: never silently generate a substitute)."
        )
    # Version-stamp check (see section 4) happens here, not deferred to conformance.
    save_yaml(run_ctx_path, {"run_type": "forced_diagnostic", "protocol": ref, "protocol_ref_pinned": True})
    return ref_path
```
**Guarantee that a resolved ref never triggers `_generate_monthly_windows`:**
by construction — `_ensure_protocol_ref_pinned` never calls
`_generate_monthly_windows` (it only ever reads an existing file's path
and writes a `run_context.yaml` pointer to it); `_ensure_protocol_from_
constraints` (the ONLY caller of `_generate_monthly_windows`) is gated on
`constraints.get("protocol")`, a DIFFERENT key. The mutual-exclusivity
lint (below) is what prevents a brief from ever supplying both keys in a
way that could race or ambiguously combine them; absent that lint, the
call order at `run_loop()`'s top would still never invoke the generator
for a `protocol_ref`-only brief, but a brief with BOTH keys set would
silently run `_ensure_protocol_from_constraints` too (since it does not
know about `protocol_ref` and has no reason to skip itself) — hence the
lint is required, not optional hardening.

**Failure modes:**
- **Missing ref** (`ref_path` does not exist): `FileNotFoundError`,
  raised immediately, at `run_loop()`'s very top — before any stage
  handoff, before any subprocess. This is the loudest, earliest failure
  point available; per this campaign's own doctrine (F5c/F4d precedent),
  an engineering failure must never be swallowed into a silent fallback.
- **Ambiguous ref** (both `protocol` and `protocol_ref` set on the same
  brief): caught at MATERIALIZATION time (lint, run_campaign.py's
  `_materialize_run`/`_materialize_refinement_run`, same site B11's lint
  already runs from — one more lint function alongside
  `_lint_pass_rule_total_mapping`, not a new mechanism), never at
  runtime. A brief that fails this lint never reaches
  `runs/<id>/artifacts/pre_registration.yaml` at all.
- **Stale ref** (`ref_path` exists but its CONTENT was modified after
  registration without renaming — e.g., windows redefined in place):
  NOT caught by this design — this is exactly the content-hash-pinning
  gap K2's own A3 amendment explicitly deferred to K3 (this kernel).
  Addressed in §4 below (version-stamping), not left as a second silent
  gap under a different name.

### Materialization-time lint (extends `_lint_pass_rule_total_mapping`'s
own call site, does not duplicate its mechanism)
New checks, in a sibling function `_lint_machine_constraints_protocol_
selection(machine_constraints: dict) -> list`:
1. `protocol` and `protocol_ref` both present → violation, naming both
   values (same "never dispatch on one field while ignoring an
   incoherent other" discipline K2's pair-validation rider established).
2. `protocol_ref` present but not a string, or empty → violation.
3. (Best-effort, matches B3's own adjacency flag in §2e): if the SAME
   `pre_registration.yaml` also carries a structured `pass_rule.
   window_set_ref` (K2/C7 schema), the two must name the same file —
   WARNING (not a hard reject; see §8's open question on whether this
   should be a lint-time hard reject instead).

### Read-back behavior
Same discipline as every other shared-state write this campaign now
uses (K4's `save_yaml`/`_save_queue` atomicity, K2's lint call sites):
`_ensure_protocol_ref_pinned`'s `run_context.yaml` write goes through the
existing `save_yaml` (already atomic, temp-file-then-`os.replace`, per
K4's rider — no new atomicity work needed here, it's inherited for free).

---

## 4. Design: B10 — hard-fail the stale-`last_escalation` fallback,
without breaking its one legitimate consumer

### The core design decision, stated explicitly (this is the crux of
this whole kernel, not a side detail)

A bare, unconditional hard-fail on the `else` branch (§2a) breaks
`_route_escalate`'s own children (§2d) — a REAL, currently-pending case
(run_049), not a hypothetical. The fix therefore has TWO parts, not one:

**Part 1 — `campaign_state.last_escalation` gains a claim/consumption
marker**, mirroring the KB's own `reactivation_consumed_by` pattern
(already-shipped precedent, `_write_kb_findings_entry`'s F09 hook):
```yaml
last_escalation:
  target: timeframe
  detail: 15m
  protocol_path: protocols/escalation_tf_15m.json
  claimed_by_run: run_049          # NEW -- set by _route_escalate itself,
                                    # at the SAME call that sets last_escalation
  claimed_at: '2026-07-06'         # NEW
```
`_route_escalate`'s own `record_escalation(...)` call (both instrument
and timeframe branches) is the natural, single write site — it already
knows `next_run_id`/`next_inst`/`next_tf` at that exact point (quoted in
K4's design note §2, re-verified this phase at the same line numbers).
This is an ADDITIVE field; nothing reads `last_escalation` today in a way
that would break from two new keys appearing alongside the existing
three.

**Part 2 — the `else` branch (§2a, both call sites) becomes:**
```python
else:
    campaign = load_campaign_state()
    last_escalation = campaign.get("last_escalation") or {}
    claimed_by = last_escalation.get("claimed_by_run")
    protocol_path_str = last_escalation.get("protocol_path")
    if protocol_path_str and claimed_by == run_id:
        # This run IS the escalation's own designated next run -- the
        # fallback is correct FOR THIS ONE RUN, not stale reuse. Still
        # printed loudly (never silent) and still exactly one hop --
        # claimed_by is not transitively inherited by any further
        # lineage continuation from this run.
        protocol_path = Path(protocol_path_str)
        print(f"⚠️  [B10] Using campaign_state.last_escalation.protocol_path "
              f"({protocol_path_str}) -- this run ({run_id}) is its claimed "
              f"consumer. Fragile: prefer machine_constraints.protocol_ref "
              f"on this run's own pre_registration.yaml instead.")
    else:
        raise RuntimeError(
            f"[B10] No run_context.yaml override and no machine_constraints."
            f"protocol_ref for {run_id}, and campaign_state.last_escalation "
            f"(protocol_path={protocol_path_str!r}) is either empty or "
            f"claimed by a different run ({claimed_by!r}) -- refusing to "
            f"silently run against stale, unrelated campaign-wide state. "
            f"Pin this run's protocol explicitly via machine_constraints."
            f"protocol_ref in pre_registration.yaml."
        )
```
This is deliberately a `RuntimeError`, not a `human_pause` route return —
consistent with how `_ensure_protocol_ref_pinned`'s own missing-ref case
is designed (§3): this fires inside `run_tool_worker`, a `run_loop()`-
internal helper, at the point BEFORE any subprocess spends real compute;
`run_loop()`'s own outer `try/except` (already existing, quoted in K4's
design note §2f-equivalent reading) already converts any such exception
into `status: "failed"` + `last_error` — the SAME mechanism every other
engineering-failure class in this file already uses. No new pause-
classification code is needed in `run_campaign.py`'s
`_classify_human_pause` for the RuntimeError path itself, only for the
RUNBOOK documentation of what a human sees (below).

**Detection condition, stated precisely:** fires when (a) no
`run_context.yaml` exists or it lacks `run_type` in
`{"replication_diagnostic", "forced_diagnostic"}`, AND (b) this run's
`pre_registration.yaml` (if any) has no `machine_constraints.protocol_ref`,
AND (c) `campaign_state.last_escalation.claimed_by_run` is either absent
or names a DIFFERENT run than the current one.

**RUNBOOK §3 mapping:** this needs a NEW row (not implemented this
phase — design only), reason string e.g.
`stale_escalation_protocol_unclaimed`, distinct from K2's
`pass_rule_evaluation_disagreement`/`kb_reactivation_violation` rows
(different subsystem, different failure class). `status: "failed"` +
`last_error` is where a human currently learns of ANY `RuntimeError` in
this file (existing mechanism, per `run_loop`'s own except-block) —
`_classify_human_pause`/`_hard_pause_reason` in `run_campaign.py` would
need a new branch recognizing this specific `last_error` shape (or,
more robustly, `_ensure_protocol_ref_pinned`/the hard-fail branch could
set a dedicated flag via `update_state(..., flags={"stale_escalation_
unclaimed": True})` BEFORE raising, so the classifier has a clean,
non-string-matched signal to key on — flagged as the recommended
approach in §8's open questions, not decided unilaterally here since it
touches `run_campaign.py`'s classifier, arguably B10's own scope but
adjacent enough to confirm with the operator first).

---

## 5. Design: version-stamping pinned protocols (first-class, launch-
blocking concern per the operator's own framing — not an appendix)

### What is stamped, where, when

Every protocol JSON file under `protocols/` gains two new top-level
fields, written once at AUTHORING time (by whoever creates the file —
human or a future tooling helper, NOT retroactively rewritten for
existing files by this kernel):
```json
{
  "symbols": [...], "timeframe": "1d", "windows": [...],
  "protocol_version": "2026-07-08",
  "protocol_content_hash": "sha256:<hex of the canonical JSON body minus these two fields>"
}
```
`protocol_content_hash` is computed over the file's own content MINUS
the two new stamp fields themselves (to avoid a circular hash-of-a-hash
problem) — canonicalized by sorting keys and using a fixed separator,
matching this repo's own existing convention for reproducible hashing
(K4's `hashlib.sha256` usage on raw brief bytes is BYTE-level, appropriate
there since that's a verbatim-install guarantee; here we need a
STRUCTURAL hash tolerant of key reordering from hand-edits, so
`json.dumps(obj, sort_keys=True)` before hashing, not raw bytes).

### Where it is verified

`_ensure_protocol_ref_pinned` (§3) is extended: after confirming
`ref_path.exists()`, if `pre_registration.yaml`'s `machine_constraints`
ALSO carries a `protocol_ref_content_hash` (a NEW, optional pre-
registered field — the brief author's own copy of what they expect,
pinned at REGISTRATION time, before this run ever executes), compute the
actual file's hash the same way and compare:
```python
expected_hash = constraints.get("protocol_ref_content_hash")
if expected_hash:
    actual_hash = _compute_protocol_content_hash(ref_path)
    if actual_hash != expected_hash:
        raise RuntimeError(
            f"[B3] machine_constraints.protocol_ref={ref!r}'s content hash "
            f"{actual_hash!r} != pre-registered {expected_hash!r} -- the "
            f"pinned file's CONTENT changed since this brief was registered "
            f"(e.g. windows silently redefined in place). Refusing to "
            f"execute against a file that no longer matches what was "
            f"pre-registered."
        )
```
`protocol_ref_content_hash` is OPTIONAL on the brief (absence means "name
only, no content guarantee" — the exact, explicitly-scoped limitation K2's
A3 amendment already named as future K3 work) — this makes it
first-class, not silently required, so existing/simpler briefs (like a
theoretical future `protocol_ref`-only brief with no hash) still work,
just without the stronger guarantee.

### How a registration brief references it

`pre_registration.yaml`'s `machine_constraints` block:
```yaml
machine_constraints:
  protocol_ref: protocols/ts_trend_daily_v2.json
  protocol_ref_content_hash: "sha256:<hex>"   # optional; omit for name-only pinning
```
A NEW small tool function (not designed in full here — flagged as an
open question in §8: should this ship as part of K3's own implementation,
or as a separate small utility script under `tools/`?) would compute and
print a candidate hash for a human authoring a brief to paste in — e.g.
`python tools/stamp_protocol.py protocols/ts_trend_daily_v2.json`, writing
the `protocol_version`/`protocol_content_hash` fields into the file
itself AND printing the hash for copy-paste into the brief's
`machine_constraints.protocol_ref_content_hash`. This is the
launch-blocking piece for "the next registration workload" the operator
named — without it, an operator authoring a new pinned brief has no
tool-assisted way to get the hash right, only manual `sha256sum` +
canonicalization by hand, which is exactly the kind of manual step this
campaign's own doctrine (E3, "corrections must be legible to
context-poor readers") argues against leaving unautomated.

---

## 6. Fixture / test plan

Reuses the established K4/K2 fixture pattern throughout: sandboxed
`tmp_path` root, the NOW-COMMITTED `tests/conftest.py` autouse guard
(confirmed present and functional this phase — 257 tests green on the
committed tree, per this session's own verification) providing sandbox-
by-default coverage for every `rpr.ROOT`/`camp.ROOT`-relative path this
kernel's own code touches, with `campaign_root`-style fixtures (or the
autouse guard alone, where a full campaign context isn't needed) for
anything requiring more specific setup.

### MANDATORY subsection — the two documented guard gaps, checked
individually against K3's own fixture surface (per SESSION_LOG's
residual-risk subsection; this is exactly the subject-matter class —
protocol file writes — that caused the stray-write incident)

1. **`setup_run.py`'s subprocess-spawn path.** K3's own production code
   (`_ensure_protocol_ref_pinned`, the hard-fail branch, the content-hash
   check) never scaffolds a new run and never calls `setup_run`/
   `_scaffold_next_run`/`subprocess.run` — it operates entirely on the
   CURRENT run's own `pre_registration.yaml`/`run_context.yaml` and on
   files under `protocols/`. **Checked, not applicable**: no K3 fixture
   needs to exercise the subprocess-spawn path at all, so this gap
   cannot be triggered by anything this kernel's own tests do. The ONE
   place K3's fixtures DO need care is the pre-existing
   `subprocess.run([...prescreen_signal.py/run_protocol.py...])` calls
   inside `run_tool_worker` itself (§2a) — a fixture testing "the hard-
   fail fires BEFORE any subprocess spend" must assert this by NEVER
   reaching that line (i.e., assert the exception/RuntimeError is
   raised, and separately assert — via a monkeypatched `subprocess.run`
   that fails the test if called — that it was never invoked), not by
   letting a real subprocess attempt run and hoping it fails for an
   unrelated reason.
2. **`_load_token_budget()`'s source-relative config read.** K3's
   subject matter (protocol paths, `machine_constraints`, `last_
   escalation`) has zero interaction with token-budget accounting.
   **Checked, not applicable**: no K3 fixture calls `_load_token_budget`
   or anything that transitively does (`run_tool_worker`, `_ensure_
   protocol_ref_pinned`, and the new lint function do not touch the
   token-budget code path at all — confirmed by reading `run_loop`'s own
   circuit-breaker block, which is a SEPARATE, later section of the same
   while-loop, never called from the top-of-`run_loop` protocol-
   resolution code this kernel touches).

### Known-answer fixtures
- **B3 pin-executes-exactly-those-windows**: fixture `pre_registration.
  yaml` with `protocol_ref` pointing at a small, fixture-authored
  protocol JSON (2-3 windows, distinct from `baseline_v1.json`'s shape so
  a test can tell them apart); call `_ensure_protocol_ref_pinned`
  directly; assert the returned path IS the fixture file (never a
  generated one) and that no `_generated.json` file appears anywhere
  under the sandboxed `protocols/`.
- **B3 mismatched-hash hard-fails**: same fixture, but
  `protocol_ref_content_hash` set to a deliberately wrong value; assert
  `RuntimeError` naming both hashes.
- **B10 negative-proof — the literal acceptance criterion**: "a run with
  mismatched last_escalation and no pin refuses to execute rather than
  running the wrong timeframe." Fixture: `campaign_state.yaml` with
  `last_escalation.protocol_path` pointing at a 15m-shaped fixture
  protocol, `claimed_by_run` either absent or naming a DIFFERENT run_id
  than the one under test, no `run_context.yaml`, no `protocol_ref` on
  the run's own `pre_registration.yaml`. Call the (refactored, shared —
  see §8) protocol-resolution helper directly; assert `RuntimeError`, and
  separately assert (per the mandatory subsection above) that
  `subprocess.run` was never called.
- **B10 legitimate-claim fixture (the run_049 shape, the reason a bare
  hard-fail is wrong)**: same setup, but `claimed_by_run` names THIS
  run's own id. Assert the fallback succeeds (returns the claimed
  protocol path), a loud warning is printed/logged, and — critically —
  that a SECOND, different run_id querying the SAME `last_escalation`
  (unclaimed by it) still hard-fails. This is the fixture that actually
  distinguishes this design from a naive "just hard-fail always" reading
  of the ledger text.
- **Duplication-closed fixture**: assert BOTH `run_tool_worker` branches
  (`signal_prescreen` and `protocol_execution`) route through the SAME
  underlying resolution call (proposed refactor, §8) rather than two
  independently-maintained copies — regression-proofs §2a's own finding.

### Survey of existing tests this change could disturb
Checked (not assumed) against every test file that imports
`run_phase1_research`: `test_daily_bar_engine_support.py` (touches
`_run_a86_power_check`/timeframe dispatch, not protocol selection — no
overlap), `test_prereg_conformance_gate.py` (DOES touch
`_ensure_protocol_from_constraints`/`_generate_monthly_windows`/
`_check_prescreen_conformance` directly — this is the ONE file requiring
a close read before implementation, since B3/B10's new lint and the
extended conformance check sit right next to what it already exercises;
its own existing fixtures use `constraints.get("protocol")` — the
generation key — exclusively, never `protocol_ref`, so they should be
unaffected by an ADDITIVE new key, but this must be VERIFIED by running
that file specifically before/after, not assumed from reading alone).
No other test file references `last_escalation`, `_ensure_protocol_from_
constraints`, or `run_tool_worker` by name (grepped, not assumed).

---

## 7. Non-goals, open questions, deviations from the ledger's framing

**Non-goals this phase:** no code, no `tools/stamp_protocol.py`, no
RUNBOOK row, no `_classify_human_pause` branch — all deferred to Phase B
pending `DESIGN APPROVED K3`.

**Deviations from the ledger's literal framing (flagged, not silent):**
1. B10's own text says "the else-branch must hard-fail (**or at minimum
   timeframe-check**)" — offering a weaker, timeframe-only check as an
   acceptable minimum. This design does NOT adopt the weaker option: a
   timeframe-check alone would not have caught a wrong-SYMBOL or wrong-
   WINDOW-RANGE stale escalation, only the specific wrong-timeframe shape
   run_049's stale value happens to be. The claim/consumption-marker
   design (§4) is a strictly stronger fix that also happens to close the
   timeframe case, chosen because the weaker option was explicitly
   optional in the ledger's own wording, not because the stronger option
   was mandated.
2. B3's own acceptance criterion says "a mismatched protocol file
   hard-fails conformance" (implying the EXISTING post-hoc conformance
   gate, `_check_prescreen_conformance`, is where this belongs). This
   design instead hard-fails at PROTOCOL SELECTION time
   (`_ensure_protocol_ref_pinned`, before any subprocess runs), same
   reasoning as §2c point 2 — catching it post-hoc would still let a real
   prescreen subprocess execute against the wrong file first. The
   post-hoc conformance gate is ALSO extended (not designed in full
   detail above — flagged here) to check `protocol_ref` for defense in
   depth (a second, independent check on the ACTUALLY-recorded
   `prescreen_result.yaml`'s own `protocol_version`, catching any path
   that somehow bypassed the selection-time check), but is not the
   PRIMARY enforcement point the ledger's wording suggests.

**Open questions for the operator:**
1. Should the K2/C7 `pass_rule.window_set_ref` and this kernel's
   `machine_constraints.protocol_ref` be REQUIRED to name the same file
   when both are present (hard lint reject), or is the WARNING this
   design proposes (§3) sufficient? They serve different purposes
   (selection vs. evaluation) but a brief author registering them
   inconsistently seems like a real, catchable authoring error.
2. Where should the "loudly detectable, non-string-matched" signal for
   `run_campaign.py`'s pause classifier live — a new `flags` key set by
   `_ensure_protocol_ref_pinned`/the hard-fail branch before raising
   (recommended, §4), or should `run_campaign.py`'s own classifier parse
   the `RuntimeError`'s `last_error` string? The former is more robust
   (matches this campaign's own existing flag-based classification
   pattern) but touches `run_campaign.py` as part of what could be
   framed as a purely `run_phase1_research.py`-side kernel — confirm
   scope before Phase B.
3. Should `tools/stamp_protocol.py` (§5, the hash-computation helper) be
   part of THIS kernel's Phase B deliverable, or a separate, smaller
   follow-on task? It's the literal launch-blocking piece for the next
   registration workload per the operator's own framing, but it's also
   a standalone utility with no dependency on the hard-fail/pinning
   logic itself.
4. Proposed refactor (mentioned in §6's duplication-closed fixture, not
   fully designed above): factor `run_tool_worker`'s two identical
   protocol-selection blocks (§2a) into ONE shared function (e.g.
   `_resolve_protocol_path(run_dir, run_id) -> Path`), called from both
   branches. This is not strictly required to fix B10 (the fix could be
   pasted into both branches identically, matching the existing
   duplication style), but leaving it duplicated means any FUTURE change
   to this logic requires remembering to update it twice — the same
   class of risk R1 (K2's dispatch consolidation) closed a live bug
   under. Recommended for Phase B; confirm before implementation since
   it's a larger diff than the minimal fix.

---

## 8. Files to be modified (Phase B, not this phase)

**`workflow/run_phase1_research.py`:**
- `_route_escalate` — both branches gain `claimed_by_run`/`claimed_at` on
  `last_escalation` (via `record_escalation`, extended signature).
- New: `_ensure_protocol_ref_pinned`, `_compute_protocol_content_hash`,
  `_lint_machine_constraints_protocol_selection`.
- `run_tool_worker`'s two protocol-selection branches — hard-fail per §4
  (and, if the §7 open-question-4 refactor is approved, consolidated into
  one shared resolver).
- `_check_prescreen_conformance` — extended for `protocol_ref` (defense
  in depth, §7 deviation 2).
- `run_loop()`'s top — calls `_ensure_protocol_ref_pinned` alongside the
  existing `_ensure_protocol_from_constraints` call.

**`workflow/run_campaign.py`:**
- `_materialize_run`/`_materialize_refinement_run` — call the new lint
  function alongside the existing B11 lint call.
- (Pending §7 open question 2) possibly `_classify_human_pause`/
  `_hard_pause_reason` — a new flag-keyed branch.

**New tool** (pending §7 open question 3): `tools/stamp_protocol.py`.

**`RUNBOOK.md`:** one new pause-table row (pending naming/placement
decision, §4).

**`tests/`:** new fixture file, `tests/test_k3_protocol_pinning.py`
(naming mirrors `test_k4_...`/`test_k2_...` precedent), covering §6 in
full.

---

## Read-back

File written once; content above is the full note (9 numbered sections:
§0 Scope, §1 Ledger items read, §2 Code read (a-e), §3 B3 design, §4 B10
design, §5 version-stamping design, §6 Fixture/test plan (with the
mandatory guard-gap subsection), §7 Non-goals/open questions/deviations,
§8 Files to be modified) — matches step 6's requirement (a-f content
areas, each present: a→§3, b→§4, c→§5, d→§6, e→§2e, f→§7).

---

## §9. Operator rulings and amendments (Phase A close-out, 2026-07-14)

`DESIGN APPROVED K3` is withheld pending Phase B's compliance with the
five amendments and four open-question rulings below. §0–§8's own text is
UNCHANGED — every contradiction between that text and this section is
resolved IN FAVOR OF THIS SECTION; §9 governs.

### Amendments (binding on Phase B)

**A1 — §3's `run_context.yaml` write is inconsistent with §2a's own
consumer; fix the path doubling.**

Verified by re-reading both sides together, not disputed: §3's proposed
write is
```python
save_yaml(run_ctx_path, {"run_type": "forced_diagnostic", "protocol": ref, "protocol_ref_pinned": True})
```
where `ref = constraints.get("protocol_ref")`, and §3's own schema
example gives `ref` as the ROOT-relative value
`"protocols/ts_trend_daily_v1.json"` (§3, Schema). But §2a's own quoted
`forced_diagnostic` consumer (unchanged, pre-existing code) is:
```python
elif run_type == "forced_diagnostic":
    proto_name = run_ctx.get("protocol", "baseline_v1.json")
    protocol_path = ROOT / "protocols" / proto_name
```
Feeding this consumer `run_ctx["protocol"] = "protocols/ts_trend_daily_v1.json"`
produces `ROOT / "protocols" / "protocols/ts_trend_daily_v1.json"` — a
doubled `protocols/protocols/` path that does not exist. §3 as drafted
is broken the first time it is actually exercised end-to-end (which is
exactly what A2's mandatory fixture, below, would have caught before
this was ever offered for approval).

**Phase B must:**
1. Write the BARE FILENAME (not the ROOT-relative `protocol_ref` value)
   into whatever key the consolidated resolver's `forced_diagnostic`-
   family branch consumes — i.e. `Path(ref).name`, not `ref` itself, so
   the existing `ROOT / "protocols" / proto_name` construction keeps
   working unmodified.
2. Lint `protocol_ref` to require it resolve FLAT under `protocols/` —
   i.e. `Path(ref).parent` must be exactly `protocols` (or, expressed
   the other way, `ref` must equal `"protocols/" + Path(ref).name` with
   no further subdirectory nesting). A `protocol_ref` naming a file
   outside `protocols/`, or nested under a subdirectory of it, is a lint
   rejection at materialization time, not a silently-accepted value that
   then fails at selection time the way this exact bug would have.
3. Fix the idempotency comparison in the resolver (§3's own
   `existing.get("protocol") == str(ref)` line) to compare against the
   SAME bare-filename form now being written, not the full `ref` value —
   as drafted this comparison would never match even after fix 1 is
   applied, defeating the idempotency check silently (it would regenerate
   the `run_context.yaml` write every single `run_loop()` entry into this
   run, not just once).

**A2 — a direct-call fixture alone is insufficient; Phase B requires a
mandatory end-to-end known-answer fixture.**

§6's "Known-answer fixtures" subsection, as drafted, tests
`_ensure_protocol_ref_pinned` by calling it directly and inspecting its
return value — this would NOT have caught A1's bug, because the bug is
in what gets WRITTEN to `run_context.yaml` and how the SEPARATE,
downstream `forced_diagnostic` consumer branch reads it back on a LATER
`run_loop()` re-entry, not in `_ensure_protocol_ref_pinned`'s own
immediate return value (which correctly returns `ref_path` — a real
existing file — regardless of what it wrote into `run_context.yaml`).
The direct-call fixture is necessary (it still proves the FIRST-call
resolution and the missing-ref failure mode) but not sufficient.

**Phase B must add**, alongside the existing direct-call fixture: pin a
protocol via `_ensure_protocol_ref_pinned` on a fixture run, THEN
separately invoke `run_tool_worker`'s (or the consolidated resolver's,
per Q4) selection path for that SAME run with `subprocess.run`
monkeypatched to CAPTURE its invocation (the command list actually
passed) rather than either executing it for real or merely asserting it
was never called — assert the captured command's protocol-path argument
resolves to EXACTLY the pinned file, not a doubled or otherwise
malformed path. This is the fixture shape that would have caught A1
before this note was offered for approval, and its absence in the
original draft is noted as a real gap in this design note's own §6, not
merely a style preference.

**A3 — pinned runs must not silently reuse `run_type: "forced_diagnostic"`.**

§3 as drafted writes `"run_type": "forced_diagnostic"` for a
`protocol_ref`-pinned run — indistinguishable, at the `run_context.yaml`
level, from a `protocol`-GENERATED run (`_ensure_protocol_from_
constraints`'s own, pre-existing write, same key, same value). This
collapses exactly the distinction B3 exists to draw (pin vs. generate)
back into one shared marker, and means any FUTURE code reading
`run_type == "forced_diagnostic"` to mean "this run's protocol was
machine-generated from `machine_constraints.protocol`" would be silently
wrong for a pinned run, and vice versa.

**Phase B must:** have the consolidated resolver (§Q4) branch on the
`protocol_ref_pinned` flag §3 already proposes writing (or, if cleaner
in implementation, a new dedicated `run_type` value, e.g.
`"protocol_ref_pinned"`, in place of reusing `"forced_diagnostic"` at
all) — the two pinning/generation cases must be mechanically
distinguishable from `run_context.yaml`'s own content, not merely by
which `machine_constraints` key happened to produce them.

**Phase B must additionally survey every consumer of `run_type`
repo-wide** (not just the two `run_tool_worker` branches already quoted
in §2a) and **record the survey's own results in the Phase B rulings
section** of this note — every `run_ctx.get("run_type", ...)` /
`run_type ==` site found, whether each one needs to recognize the new
value/flag, and which (if any) can safely ignore it. This survey is Phase
B work; it is not performed in this §9 (Phase A remains design-only, per
the standing authorized-write-set discipline for this task).

**A4 — a runtime mutual-exclusion guard at `run_loop()`'s own top,
independent of the materialization lint.**

§3's mutual-exclusion check is currently ONLY a materialization-time lint
(`run_campaign.py`'s `_materialize_run`/`_materialize_refinement_run`
call sites) — this protects any run launched THROUGH `run_campaign.py`'s
own queue machinery, but does not protect a `pre_registration.yaml`
authored or edited by hand and fed to `run_phase1_research.py` directly
(a single-run launch that never passes through materialization at all —
this campaign's own RUNBOOK documents `--once`/direct-stage invocation as
a real, used operational mode, and K4's own design note independently
established that direct single-run launches bypass queue-level
mechanisms).

**Phase B must add**, at `run_loop()`'s own top (the same site
`_ensure_protocol_from_constraints`/`_ensure_protocol_ref_pinned` are
both already called from, §2b/§3), a second, RUNTIME check: if
`constraints` carries both `protocol` and `protocol_ref`, raise
immediately — independent of, and in addition to, the materialization
lint. This is defense in depth for exactly the class of gap A1 and A3
are also about: a single-site fix is not sufficient when there are
multiple entry paths into the same logic.

**A5 — Phase B includes a one-time, operator-authorized migration
stamping the EXISTING `campaign_state.last_escalation` record.**

§4's own protected-consumer design (the `claimed_by_run` marker) is
necessary for run_049's OWN still-pending lineage to keep working once
B10's hard-fail ships — but as of this design note, `campaign_state.
yaml`'s real, current `last_escalation` record
(`{"target": "timeframe", "detail": "15m", "protocol_path":
"protocols\\escalation_tf_15m.json"}`, verified by direct read this
phase) carries NO `claimed_by_run` field at all, because that field does
not exist yet — it is Phase B's own addition. **Without a one-time
migration writing `claimed_by_run: run_049` onto this EXISTING record
before or alongside Phase B's code shipping, run_049's own resumption
would hard-fail under §4's own design the very next time it's attempted**
— the exact protected case §4 exists to preserve would be broken by
§4's own hard-fail on day one, for want of the one historical record the
new field was never retroactively applied to.

**Phase B must ship**, as part of the same change: a one-time,
operator-authorized migration writing `claimed_by_run: run_049` (and a
`claimed_at` date) onto the CURRENT `last_escalation` record in
`campaign_state.yaml`, with a sidecar rationale per E3 (this campaign's
own standing doctrine: corrections must ship with rationale legible to a
context-poor reader). **Note on `claimed_at`'s own sourcing, checked this
phase, not assumed:** `campaign_state.yaml`'s single, whole-file
`updated_at` field (currently `2026-07-12T16:13:05Z`) does NOT reliably
date `last_escalation` specifically — that field has been overwritten by
many unrelated writes since the escalation was actually recorded, and
`campaign_log.md` has no entry for run_049/the escalation event at all
(grepped this phase — none found; the log's own curated format post-dates
this event). The migration's `claimed_at` should instead be sourced from
`00_closing_state.md` §8's own dating of the P1b closure
(2026-07-06, the session in which run_047→run_049's timeframe escalation
was recorded) — Phase B's sidecar rationale should cite this explicitly
rather than inventing a date or misreading the file-level `updated_at`
as if it were field-specific.

### Open-question rulings

**Q1 (§7, open question 1) — RULED: hard lint reject.** A brief
registering `machine_constraints.protocol_ref` and K2/C7's
`pass_rule.window_set_ref` naming DIFFERENT files is a materialization-
time lint REJECTION, not the WARNING §3 originally proposed. Phase B's
lint function (`_lint_machine_constraints_protocol_selection` or its
final name) must raise/reject, naming both values, exactly as this
kernel's own mutual-exclusion check (A4) and K2's B11 lint already do for
their respective incoherent-pair classes.

**Q2 (§7, open question 2) — RULED: flag-based signal;
`run_campaign.py` classifier branch is IN SCOPE for K3.** The hard-fail
branch (§4) sets a dedicated `flags` key (e.g.
`stale_escalation_unclaimed: True`) via `update_state(...)` before
raising, matching this campaign's own existing flag-based pause-
classification pattern (`no_signal_artifact_flagged`,
`kb_reactivation_violation`, `pass_rule_evaluation_disagreement`, etc.).
`run_campaign.py`'s `_classify_human_pause`/`_hard_pause_reason` gains a
new branch recognizing this flag. This touches `run_campaign.py`, not
only `run_phase1_research.py` — confirmed, not a scope violation, per
this ruling; Phase B's authorized-write set must include
`workflow/run_campaign.py` accordingly, and RUNBOOK.md's new pause-table
row (§4, already flagged as needed) names this exact flag.

**Q3 (§7, open question 3) — RULED: `tools/stamp_protocol.py` ships in
K3 Phase B, with its own fixture.** Not deferred to a separate follow-on
task. §8's files-to-modify list already named it as a "new tool"; this
ruling removes the conditionality — it is REQUIRED Phase B scope, and its
own test coverage (computing a stable, canonical hash for a fixture
protocol JSON, round-tripping through `_compute_protocol_content_hash`'s
comparison logic in §5) is part of §6's fixture plan, not optional
polish.

**Q4 (§7, open question 4) — RULED: the `_resolve_protocol_path`
consolidation is APPROVED and now REQUIRED, not optional.** A1 and A3
above are each described as "single-site fixes" only in the sense that,
absent consolidation, each would need to be applied to BOTH of §2a's
duplicated branches independently (and correctly, and identically) —
this ruling removes that risk at the source. Phase B must implement ONE
shared resolver function, called from both the `signal_prescreen` and
`protocol_execution` `run_tool_worker` branches, covering: `replication_
diagnostic`, `protocol`-generated `forced_diagnostic`, `protocol_ref`-
pinned (its own distinguishable branch per A3), and the claim-checked
`last_escalation` fallback (§4) — one function, one set of branches, no
duplicated copy-paste logic anywhere in this call path once Phase B
ships.

---

## Phase B rulings and deviations (2026-07-15)

Body above (§0–§9) is unchanged from Phase A approval. This section
records the run_type consumer survey §9/A3 required, every point where
implementation deviated from the approved design, and a per-amendment
compliance map (implementing code site + the fixture that proves it),
per the same "never silently improved" discipline K4/K2 established.

### A3 run_type consumer survey (required by §9, performed in Phase B)

Every `run_ctx.get("run_type", ...)` / `run_type ==` site in the repo,
found by grep, not assumed:

- `workflow/run_phase1_research.py`, `signal_prescreen` branch (formerly
  lines 936-949, now replaced by a single `_resolve_protocol_path(RUN_DIR,
  run_id)` call) — recognizes the new `protocol_ref_pinned` value (now
  consolidated, per Q4).
- `workflow/run_phase1_research.py`, `protocol_execution` branch (formerly
  lines 991-1025, same replacement) — same, now consolidated.
- `workflow/run_phase1_research.py`, `_ensure_protocol_from_constraints`'s
  own write (`run_ctx = {"run_type": "forced_diagnostic", ...}`) —
  **left UNCHANGED**, exactly as A3 required: stays `"forced_diagnostic"`,
  the generation-path-only marker, never touched.
- `tests/test_prereg_conformance_gate.py` (`assert run_ctx["run_type"] ==
  "forced_diagnostic"`) — **left UNCHANGED, still green**: 9/9 passing in
  isolation after Phase B shipped (verified this phase, see Step 6 below).
- `workflow/run_campaign.py` — grepped, no `run_type` usage anywhere.
  Clean, no change needed.
- `tools/*.py` — grepped, no `run_type` usage anywhere. Clean.
- `skills/backtest-engineering/SKILL.md` — reads `run_type` only to check
  the literal value `"replication_diagnostic"` for an unrelated
  "Replication guard" rule. A different value; safely ignores the new one.
- All other grep hits (`SESSION_LOG.md`, `config/campaign_baseline_runs.yaml`,
  `PIPELINE_IMPROVEMENTS_20260712_v4.md`, briefs, `00_closing_state.md`,
  this design note itself) are prose/doc mentions only, not code consumers.

**Conclusion, confirming A3's own text:** using a NEW, dedicated
`run_type` value (`"protocol_ref_pinned"`, chosen over reusing
`"forced_diagnostic"` plus a bare flag) required zero changes to the
existing generation-path write site or its existing test — only the two
(now-consolidated-into-one) `run_tool_worker` branches needed a new
branch recognizing it.

### Per-amendment compliance map

| # | Requirement | Implementing code | Proving fixture |
|---|---|---|---|
| A1.1 | Write bare filename, not full ref | `_ensure_protocol_ref_pinned` (`run_phase1_research.py`): `bare_name = Path(ref).name` | `test_ensure_protocol_ref_pinned_pins_existing_protocol`, `test_resolve_protocol_path_pinned_run_no_path_doubling` |
| A1.2 | Lint: `protocol_ref` must resolve flat under `protocols/` | `_lint_machine_constraints_protocol_selection` | `test_lint_rejects_nested_protocol_ref_path`, `test_lint_rejects_protocol_ref_outside_protocols_dir` |
| A1.3 | Idempotency compares bare-filename form | `_ensure_protocol_ref_pinned`'s `existing.get("protocol") == bare_name` | `test_ensure_protocol_ref_pinned_idempotent_short_circuits_on_bare_filename_match` (deletes the file between calls — would raise `FileNotFoundError` on a regression) |
| A2 | Mandatory end-to-end fixture, `subprocess.run` CAPTURED not just asserted-uncalled | `run_tool_worker`'s `signal_prescreen` branch, now calling `_resolve_protocol_path` | `test_run_tool_worker_signal_prescreen_uses_pinned_protocol_exactly` |
| A3 | New dedicated `run_type` value, not reused `forced_diagnostic` | `_ensure_protocol_ref_pinned` writes `"run_type": "protocol_ref_pinned"`; `_resolve_protocol_path` branches on it | `test_ensure_protocol_ref_pinned_pins_existing_protocol`, `test_resolve_protocol_path_pinned_run_malformed_missing_protocol_key_raises`; survey above |
| A4 | Runtime mutual-exclusion guard at `run_loop()`'s own top, independent of the lint | Inline guard, `run_loop()`, immediately after `_load_machine_constraints` | `test_run_loop_top_hard_fails_on_both_protocol_keys_before_anything_else` |
| A5 | One-time migration, `campaign_state.yaml`'s existing `last_escalation` gains `claimed_by_run: run_049` | Step 9 of the Phase B task (not yet applied at the time this section is written — applied AFTER commit 1 is verified, per the task's own sequencing) | N/A — one-time state write, not a fixture; see commit 2 |
| Q1 | `window_set_ref`/`protocol_ref` mismatch is a HARD REJECT | `_lint_machine_constraints_protocol_selection` | `test_lint_q1_hard_rejects_window_set_ref_mismatch`, `test_lint_accepts_matching_window_set_ref` |
| Q2 | Flag-based classifier signal; `run_campaign.py` in scope | `_resolve_protocol_path` sets `flags={"stale_escalation_unclaimed": True}` before raising; `run_campaign.py`'s `_hard_pause_reason` gains a branch checking it | `test_resolve_protocol_path_stale_escalation_unclaimed_hard_fails`, `test_hard_pause_reason_classifies_stale_escalation_unclaimed_flag`, `test_hard_pause_reason_generic_unhandled_exception_without_flag` |
| Q3 | `tools/stamp_protocol.py` ships this phase, with its own fixture | New file, `compute_protocol_content_hash`/`stamp`/CLI `main` | `test_stamp_protocol_round_trip_matches_rpr_hash_formula`, `test_stamp_protocol_hash_stable_across_key_reordering` |
| Q4 | One consolidated resolver, both branches | `_resolve_protocol_path`, called from both `run_tool_worker` branches | `test_both_run_tool_worker_branches_call_the_shared_resolver` (spies on the resolver, asserts exactly 2 calls, one per branch, with the correct `(run_dir, run_id)` args) |

Additional coverage beyond the table: the B10 hard-fail's core behavior
(claim-checked fallback, one-hop, never transitively inherited) —
`test_resolve_protocol_path_claimed_run_uses_fallback_legitimately`,
`test_resolve_protocol_path_second_different_run_still_fails`,
`test_resolve_protocol_path_no_last_escalation_at_all_hard_fails`; the
negative-proof that the hard-fail fires BEFORE any subprocess spend —
`test_run_tool_worker_signal_prescreen_hard_fail_never_invokes_subprocess`;
`_route_escalate`'s own `claimed_by_run` write (§4 Part 1) —
`test_route_escalate_instrument_writes_claimed_by_run`; §5's content-hash
guard — `test_ensure_protocol_ref_pinned_content_hash_mismatch_raises`,
`test_ensure_protocol_ref_pinned_content_hash_match_passes`.

### Deviations from §0–§9 (flagged, not silent)

1. **`_check_prescreen_conformance` was NOT extended for `protocol_ref`
   defense-in-depth**, despite §8 listing it as a file to modify. §8's own
   text frames this as "defense in depth" for a case (a `protocol_ref`-
   pinned run's actual executed protocol conflicting with what was
   pre-registered) that A4's runtime guard and Q1's materialization lint
   already close structurally — by the time a pinned run reaches
   `_check_prescreen_conformance` (post-hoc, after a real subprocess ran),
   the incoherent-constraints case A4/Q1 exist to prevent can no longer
   have occurred. Per this campaign's "prefer minimal code changes"
   standing constraint, this extension is deferred rather than added as
   speculative extra coverage for an already-closed gap. Not required by
   any §9 amendment or open-question ruling. Flagged here for the record,
   not silently dropped.
2. **The comment block at `_ensure_protocol_from_constraints`'s own
   `run_ctx` write (explaining why `run_type` must be `"forced_diagnostic"`)
   was left as-is**, not rewritten for clarity as §2/survey text
   speculated it might be. Re-read this phase: the comment's own claim
   (run_type controls which branch of the old duplicated logic fires) is
   still accurate post-consolidation — `_resolve_protocol_path` branches on
   the exact same `run_type` values, just in one function instead of two.
   No correction was needed, so none was made.
3. **A3's "or, if cleaner in implementation" branch was taken explicitly**:
   Phase B implements a genuinely NEW `run_type` value
   (`"protocol_ref_pinned"`), not `"forced_diagnostic"` plus the
   `protocol_ref_pinned: True` flag alone doing the distinguishing work.
   Both flag and dedicated value are written to `run_context.yaml` (the
   flag as an additional, redundant-but-harmless marker); the resolver
   branches on `run_type`, not the flag, for the actual dispatch decision.
4. **`record_escalation()`'s signature gained two new optional keyword
   parameters** (`claimed_by_run`, `claimed_at`-derivation), not named
   explicitly in §4's own code sketch (which showed the desired YAML
   shape but not the exact function-signature mechanics). Backward
   compatible: every OTHER existing caller of `record_escalation` (none
   found outside `_route_escalate`'s own two branches, grepped this
   phase) is unaffected, since both new parameters default to producing
   no `claimed_by_run`/`claimed_at` keys when omitted.

### Step 6 results (verbatim)

- Baseline (Step 1, before any Phase B edit): **257 passed, 0 failed, 3
  warnings, 76.23s**.
- `tests/test_k3_protocol_pinning.py` in isolation: **34 passed** (first
  run, no fixture iteration needed).
- Full suite after Phase B: **291 passed, 0 failed, 3 warnings, 62.99s**
  (257 + 34 = 291 — exact accounting, no other test file changed).
- `tests/test_prereg_conformance_gate.py` in isolation (the file A3
  required stay green and unmodified): **9 passed**, file byte-identical
  to before this kernel (not edited).

---

## K3 rider (2026-07-15): protocol_ref post-hoc conformance extension
(operator ruling on Phase B deviation 1)

**Operator ruling, verbatim reasoning:** deviation 1 (declining to extend
`_check_prescreen_conformance` for `protocol_ref` defense-in-depth) was
REJECTED. A4 (the runtime mutual-exclusion guard) and Q1 (the
materialization-time `window_set_ref` lint) are both REGISTRATION-time
checks — they can only ever catch an incoherent brief BEFORE a run
starts. Neither catches an EXECUTED prescreen that silently ran against
a DIFFERENT protocol file than the one pinned (e.g. a stale
`run_context.yaml` override left over from a prior stage attempt, or a
hand-edited `pre_registration.yaml` whose `protocol_ref` changed after
`signal_prescreen` had already run once against the old value). The
ledger's own B3 text assigns exactly this executed-vs-registered
conformance role to `_check_prescreen_conformance` (the F4d gate this
kernel's §2c already read and quoted). The transitive path through Q1's
lint into the C7 evaluator (`tools/verdict_criteria_evaluator.py`'s own
`window_set_ref` check) covers only `protocol_execution` (the full
backtest stage), and only when the brief's `pass_rule.window_set_ref` is
present — it never runs for `signal_prescreen`, and never fires at all
for a brief with no structured `pass_rule`. This rider closes that gap.

### What was read before implementing (not assumed)

`_check_prescreen_conformance(prescreen_result, constraints,
protocol_obj)`'s existing call site (`determine_post_prescreen_route`,
`workflow/run_phase1_research.py`) already resolves the run's ACTUAL
executed protocol file and passes its full parsed content in as
`protocol_obj` — the exact input this rider needed, no call-site change
required (the authorized write set correctly scoped this to
`_check_prescreen_conformance` only).

The "executed protocol identity" question required reading, not
assuming: `tools/prescreen_signal.py` writes `prescreen_result.yaml`'s
`protocol_version` field as `protocol.get("_version", protocol_path)` —
i.e. it looks for a literal `_version` key (underscore-prefixed) on the
protocol JSON, falling back to the raw CLI `protocol_path` argument
string if absent. Checked every file under `protocols/` this phase: NONE
carries a literal `_version` key — two (`baseline_v2.json`,
`ts_trend_daily_v1.json`) carry `protocol_version` instead (a DIFFERENT,
non-underscored key — this kernel's OWN §5 stamp field), which
`prescreen_signal.py`'s `.get("_version", ...)` call does not match. So
in every real case today, `prescreen_result.yaml`'s `protocol_version`
field is, in practice, always the raw CLI path argument (absolute or
ROOT-relative, exactly as `run_tool_worker` constructed it) — never a
semantic version string. This is why the new check compares BARE
FILENAMES (`Path(...).name`), not full paths or version strings: the
executed identity's path form (constructed from `ROOT / "protocols" /
proto_name` inside `run_tool_worker`) and the pinned `protocol_ref`'s
path form (a ROOT-relative string as written in `pre_registration.yaml`)
are constructed differently and would never compare equal as full
strings even when they name the same file — matching A1's own
bare-filename convention.

### Implementation

`_check_prescreen_conformance` gains one new, independent branch (after
the existing generation-shape checks, gated on `constraints.get(
"protocol_ref")`, mutually exclusive with the `protocol` branch by
construction since A4/Q1 already forbid both being set):

1. **Name-level check (always runs when `protocol_ref` is set):**
   `Path(prescreen_result.get("protocol_version")).name` compared against
   `Path(protocol_ref).name`. Mismatch → violation naming both, same
   string-interpolation style as the existing generation-shape
   violations above it.
2. **Content-hash check (only when the brief also pinned
   `protocol_ref_content_hash`, per §5):** recomputes the hash of the
   ALREADY-LOADED `protocol_obj` (the executed file's real parsed
   content, passed in by the existing call site) using the same
   pop-stamp-fields-then-`json.dumps(sort_keys=True)`-then-sha256 formula
   as `_compute_protocol_content_hash`/`tools/stamp_protocol.py`.
   **Deliberately duplicated, not imported**: this function's authorized
   write set for this rider is `_check_prescreen_conformance` only, and
   `_compute_protocol_content_hash` takes a `Path` (re-reads from disk)
   where this call site already has the parsed dict in hand — matching
   the same "small formula duplicated across 3 sites now
   (`run_phase1_research.py`'s own content-hash guard,
   `tools/stamp_protocol.py`, and this check), never diverging" pattern
   already established and disclosed in Phase B's own rulings section.

### Fixtures (§6 pattern: known-answer both directions, plus the hash path)

- `test_check_prescreen_conformance_protocol_ref_mismatch_names_both` —
  pinned `protocols/pinned_expected.json`, executed
  `.../actually_used.json` → exactly one violation naming both bare
  filenames.
- `test_check_prescreen_conformance_protocol_ref_match_no_violation` —
  same bare filename, different full path (proving the BARE-filename
  comparison, not full-path equality) → zero violations.
- `test_check_prescreen_conformance_protocol_ref_content_hash_mismatch` —
  wrong hash → violation naming "content hash".
- `test_check_prescreen_conformance_protocol_ref_content_hash_match` —
  hash computed via `tools/stamp_protocol.compute_protocol_content_hash`
  on the same object → zero violations (proves the two hash formulas —
  this rider's inline copy and `stamp_protocol.py`'s — agree).
- `test_check_prescreen_conformance_no_protocol_ref_skips_new_branch` —
  no `protocol_ref` on the brief → new branch never fires, pre-existing
  behavior (generation-shape checks only) unaffected.

### Deviations

None. The rider ships exactly the two checks the operator's ruling
specified (name-level always, hash-level only when pinned), touches only
`_check_prescreen_conformance`, and required no call-site change because
the existing call site already supplied every input needed.

### Test counts (verbatim)

- `tests/test_k3_protocol_pinning.py` in isolation: **39 passed** (34 from
  Phase B + 5 new).
- Full suite: **296 passed, 0 failed, 3 warnings, 61.89s** (291 + 5 = 296,
  exact accounting, no other test file changed).
