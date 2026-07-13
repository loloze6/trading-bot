# K2 — Verdict Machinery (A8 + A9 + B11 + C7, C9 rider): Design Note

**Phase:** A (design only — no code, no tests, no state written this phase)
**Author:** Implementation agent, this session, 2026-07-13
**Status:** DRAFT — awaiting operator message `DESIGN APPROVED K2` before implementation

---

## 0. Scope and non-goals

In scope: ledger items **A8** (verdict/routing vocabulary split), **A9**
(`_route_kill` no longer conflates hypothesis-kill with campaign-space-empty),
**B11** (pre-registered total verdict+routing mapping, operator-side schema),
**C7** (machine-checkable pass-rule evaluator replacing the prose-criteria
parser), and **C9 as a rider** (KB-exhaustion gate on the verdict stage's own
proposal-generating paths). Designed as one coherent change to the
verdict/routing layer, per NEXT_SESSION.md's task-1 sequencing (this is the
"verdict/routing vocabulary split, total pass-rule mapping, machine-evaluated
criteria" cluster).

Context only, read for non-foreclosure, NOT fixed here:
- **C8** (adopted method doctrine: identity-matching on symbol/window/
  entry_time/exit_time + percent-return agreement, never absolute PnL/row
  counts, for cross-run trade comparison) — C7's evaluator does not do
  cross-run trade comparison itself; where it needs to (none of run_057's
  pass-rule criteria do), it must follow C8, not reinvent a PnL-matching
  rule. No conflict found.
- **A2** (distinct terminal strings for refine vs. pivot, plus a
  `route_taken` field) — already partially anticipated by K4's
  `continuation_created_by` field (`_route_refine`/`_route_pivot`/
  `_route_escalate`, `run_phase1_research.py`). A8's `lineage_routing`
  field (§4) is a superset of what A2 asks for at the routing layer;
  A2's own terminal-string rename is left undone and does not conflict
  with anything designed here — `pending_stage` values are untouched.
- **D3** (`operator_directives.yaml` first-class channel) — run_057's own
  incident (the pre-commitment sidecar with no precedence channel) is the
  direct motivating case for **both** D3 and B11. B11 (§6) closes the
  specific sub-case D3 names ("B11's total-mapping rule removes the
  largest class of delegations that make directives necessary at all") but
  does not build the general `operator_directives.yaml` artifact D3 asks
  for. Hook left explicit in §6.

No campaign process is running (operator-stated; queue is all-terminal,
consistent with the K4 rider's own observation that the real dry run hit
`AssertionError`/then the informative log line on an empty queue).
`campaign_state.last_escalation.protocol_path` remains stale
(`escalation_tf_15m.json`) — nothing designed here reads or writes
`last_escalation`; §2's reading of `protocol_execution`'s protocol-selection
`else` branch (which DOES consume it) is READ-ONLY for this note, never
exercised.

---

## 1. Ledger items read (context, current text confirmed unchanged)

A8, A9, B11, C7, C9, C8 (doctrine), A2, D3 — re-read fresh this phase
against `PIPELINE_IMPROVEMENTS_20260712_v4.md` (not solely relied on from
the earlier orientation read) to guard against drift; content confirmed
byte-identical to what was summarized in this session's first turn. Not
re-quoted in full here (already on file in that document); load-bearing
phrases are quoted inline in §4-§7 where they drive a specific design
choice.

---

## 2. Code quotes (step 2)

### (a) `verdict_interpreter` stage block (`run_loop`, `run_phase1_research.py`)

```python
# lines 3641-3667 (current, K4-unmodified — K4 touched routing functions, not this block)
if current_stage == "verdict_interpreter":
    _vi_path = RUN_DIR / "artifacts" / "verdict_interpretation.yaml"
    if _vi_path.exists():
        try:
            import yaml as _yaml_check
            _yaml_check.safe_load(_vi_path.read_text(encoding="utf-8"))
            _skip_agent = True
            print(f"⏭️  verdict_interpretation.yaml already valid — skipping LLM re-run.")
        except Exception:
            pass  # invalid YAML — re-run the agent
    ...
```
Confirms `verdict_interpretation.yaml` is LLM-authored (written by the
`verdict-interpreter` skill's agent invocation), not code-generated — the
skip-agent short-circuit only fires when the file already parses, it never
constructs the content itself. This is why run_057's `verdict_interpretation.yaml`
carries hand-correction fields (`operator_correction_20260711`) rather than
a code-level fix: there is no code path that writes this file's decision
fields; a human edited the LLM's own output in place.

### (b) `determine_post_verdict_route()` — the single-enum dispatch A8 splits

```python
# lines 3290-3379
def determine_post_verdict_route(path: Path, run_id: str):
    interp = load_yaml(path / "artifacts" / "verdict_interpretation.yaml")
    status = (interp.get("status") or interp.get("protocol_verdict") or "").strip().lower()
    campaign = load_campaign_state()
    ...
    status = _apply_circuit_breaker(status, interp, campaign)
    ...
    if status == "promote":
        ...
        return "holdout_evaluation"
    if status == "kill":
        return _route_kill(path, run_id, interp, campaign)
    ...
    if status == "refine":
        return _route_refine(path, run_id, interp, campaign)
    if status == "pivot":
        return _route_pivot(path, run_id, interp, campaign)
    if status == "escalate":
        return _route_escalate(path, run_id, interp, campaign)
    raise ValueError(f"Unknown verdict status: '{status}'")
```
One field (`status`, aliased `protocol_verdict`) drives BOTH "is the
hypothesis dead" (kill vs. not) and "what does the campaign do next"
(refine/pivot/escalate/promote) — the exact conflation A8 names. run_057's
own incident (§3) is the live instance: the LLM stage computed `status:
pivot` (a routing decision — "go try something else") while its OWN prose
(`primary_failure_mode`, `root_cause`) already concluded the mechanism was
dead — two different, uncombinable judgments forced into one slot.

### (c) `_route_kill` — the campaign-wide write A9 splits out

```python
# lines 2064-2083
def _route_kill(path: Path, run_id: str, interp: dict, campaign: dict) -> str:
    print("\n🛑 KILL: space exhausted or question answered negatively.")
    decision = {
        "campaign_id": campaign.get("campaign_id", "default"),
        "terminal_run": run_id,
        "decision": "kill",
        ...
    }
    save_yaml(ROOT / "campaign_decision.yaml", decision)
    print(f"  → Campaign decision written to campaign_decision.yaml")
    state = load_campaign_state()
    state["status"] = "space_empty"
    _save_campaign_state(state)
    return "completed_rejected"
```
Confirms A9's symptom exactly: the ONLY route that terminates a lineage
ALSO unconditionally writes a campaign-wide `campaign_decision.yaml` and
sets `campaign_state.status = "space_empty"` — the whole campaign, not
just this hypothesis. `_route_kill`'s own print statement ("space exhausted
**or** question answered negatively") already names the conflation in its
own log line. There is no code path that kills one hypothesis without
also declaring the campaign's search space empty.

### (d) `_route_refine`/`_route_pivot` as modified by K4 (2026-07-13)

Already carry the K4 kernel's `continuation_child`/`continuation_created_by`
write (`docs/design/K4_routing_registration_design_20260712.md` §5, verified
present at `run_phase1_research.py` lines 1981/2004/2060/2081 by grep this
session). A8's `lineage_routing` field (§4) is additive to this — the write
site (end of each routing function, before its terminal-string return) is
the SAME site A8's new field is recorded at; no conflict, no rework of K4's
mechanism needed. `_route_kill`'s split (§4) needs an equivalent write of
`continuation_child: null` / `continuation_created_by: "_route_kill"` for
symmetry with K4's reconciler expectations — flagged in §4.

### (e) The `protocol_execution` verdict machinery C7 replaces

`workflow/run_phase1_research.py`, the subprocess wrapper (lines 991-1029):
```python
cmd = [str(TBOT_PYTHON), str(ROOT / "tools" / "run_protocol.py"),
       str(config_path), str(protocol_path),
       "--validation-protocol", str(validation_path), "--out-dir", str(RUN_DIR)]
result = subprocess.run(cmd, capture_output=True, text=True)
...
summary_path = RUN_DIR / "protocol_summary.json"
with open(summary_path, encoding="utf-8") as f:
    summary = json.load(f)
save_yaml(ARTIFACTS / "protocol_result.yaml", summary)
```
`protocol_result.yaml` **is** `protocol_summary.json`, copied verbatim.
Two independently-computed verdicts live inside it (both present in
run_057's own artifact, §3):
1. **Top-level `verdict`/`verdict_reason`** (`tools/run_protocol.py` lines
   1094-1159) — generic, hardcoded thresholds from the protocol file's own
   `promotion` block (`median_sharpe_gt: 0, max_abs_drawdown_pct_lt: 30,
   min_trade_count_gte: 20, kill_median_sharpe_lt: -1` — the SAME generic
   defaults `_ensure_protocol_from_constraints` falls back to, lines
   1567-1570 — never hypothesis-specific).
2. **`hypothesis_verdict`** (`evaluate_against_decision_rules()`,
   `tools/run_protocol.py` lines 656-817) — parses `validation_protocol.yaml`'s
   PROSE `decision_rules`/`required_evidence` via keyword matching.

The keyword matcher C7 names:
```python
# lines 450-470
_KEYWORD_TO_FIELD = [
    (['mr frequency', 'mr freq', 'regime frequency', ...], 'regime_frequency'),
    (['win rate', 'win_rate', 'hit rate'],                  'median_win_rate'),
    (['sharpe'],                                             'median_sharpe'),
    (['drawdown'],                                           'max_abs_drawdown_pct'),
    (['trade count', 'trade_count', 'trades'],              'min_trade_count'),
    (['walk-forward pooled ic', 'walk forward pooled ic'],  'median_forecast_return_corr'),
]
...
def _evaluate_criterion(text: str, extended: dict, is_reject: bool) -> dict:
    if _is_untested(text):
        return {'criterion': text, 'result': 'UNTESTED', 'reason': 'not available in current metrics pipeline'}
    field = _resolve_field(text)
    if field is None:
        return {'criterion': text, 'result': 'UNTESTED', 'reason': 'no matching metric keyword'}
    ...
```
This is a **prose interpreter**, structurally unable to consume the
pre-registered pass rule (which is itself prose, in `pre_registration.yaml`,
not the free-text `validation_protocol.yaml` this parser actually reads —
two DIFFERENT documents, neither of them machine-structured).

### (f) `skills/verdict-interpreter/SKILL.md` — verdict vocabulary and Rule 6

```
- status                    # YOUR decision: promote | refine | pivot | escalate | kill
```
(lines 34-35, "Output requirements") — confirms the single-enum vocabulary
A8 splits, verbatim from the skill's own spec.

Rule 6 (lines 303-333), the rule run_057 actually fired:
```
RULE 6 — No diagnostic signal (all metrics null):
  IF median_forecast_return_corr is null AND median_gross_pnl is null:
    ...
    CASE B — Regime starvation (all symbols have min_trade_count = 0):
      ...Correct action: INCREMENTAL threshold relaxation only...
```
D3's phrase "faithfully applied Rule 6 CASE B" refers to this exact text —
the skill's own rulebook, applied correctly, pointed toward "refine via
threshold relaxation," while the pre-registered brief explicitly forbade
threshold adjustment (`user_brief_verbatim.yaml`'s pass rule, §3: "no
threshold adjustment permitted within this brief") and the pre-commitment
sidecar said the verdict must be final-kill. Confirms D3's root-cause
framing precisely: the stage followed its own instructions correctly and
still produced the wrong answer, because nothing told it the sidecar
outranked the rulebook.

---

## 3. run_057 known-answer artifacts

### Pre-registered pass rule, verbatim (`pre_registration.yaml`, also
duplicated in `user_brief_verbatim.yaml`'s `evaluation.pass_rule`):

> "PASS (-> refine/promote routing per verdict-interpreter) iff: (a) gated
> bar-level median Sharpe >= 0.5791 (BTCUSDT) AND >= 0.0318 (ETHUSDT),
> computed over the same 15-window sets; and (b) per-episode expectancy of
> taken entries > 0 (sign plus expectancy +/- SE; no t-stat bar,
> pre-registered as such because the gated subset has strictly fewer
> trades); and (c) A3.4 sparse rule: any window whose gated episode count
> falls below the trade floor contributes null Sharpe, and expectancy +/-
> SE is primary for the aggregate judgment. FAIL on (a) or (b) -> the gate
> did not rescue the edge; verdict routing decides kill vs pivot; no
> threshold adjustment permitted within this brief."

This is B11's own textbook case of an underspecified delegation ("verdict
routing decides kill vs pivot") — the exact defect B11 exists to close.
The separate, later pre-commitment (`prescreen_override_20260711.yaml`,
its final line): *"The pre-registered pass rule in pre_registration.yaml
is the sole and final verdict authority for this run. If walk-forward
fails it, the verdict is kill; no further arbitration or gate relief will
be sought for this lineage."* — narrows FAIL-(a)/(b) to kill/terminate,
but as a SIDECAR the stage had no schema reason to treat as binding (D3).

### `protocol_result.yaml` — both verdicts, and why BTCUSDT's median is null

Per-symbol summary (machine-computed, `tools/run_protocol.py` lines
1094-1116, already correctly implementing the A3.4 null-for-sparse
convention at the PER-WINDOW level — `core.sharpe` is `null` for every
window below the trade floor, not zero):
```yaml
per_symbol_summary:
  BTCUSDT: {median_sharpe: null, max_abs_drawdown_pct: 20.909, min_trade_count: 0, zero_trade_slot_pct: 33.33}
  ETHUSDT: {median_sharpe: -0.686, max_abs_drawdown_pct: 36.874, min_trade_count: 0, zero_trade_slot_pct: 20.0}
verdict: refine
verdict_reason: 'BTCUSDT: median_sharpe=null (all windows sparse), min_trades=0<20;
  ETHUSDT: median_sharpe=-0.686<=0, max_dd=36.9%>=30, min_trades=0<20'
hypothesis_verdict:
  verdict: refine
  criteria_results:
  - criterion: '...FAIL on (a) or (b)...'
    field: median_sharpe
    required: 0.5791
    result: FAIL
    per_symbol:
    - {symbol: BTCUSDT, result: UNTESTED, reason: median_sharpe not computed}
    - {symbol: ETHUSDT, actual: -0.686, required: '>= 0.5791', result: FAIL}
  - {criterion: 'Standing campaign gates...', result: UNTESTED, reason: no matching metric keyword}
  - criterion: 'Per-window trade count >= 3...'
    field: min_trade_count
    result: FAIL
  - {criterion: 'S1...and S2...are reported-only secondaries...', result: UNTESTED, reason: no matching metric keyword}
  verdict_reason: 2 of 2 evaluable criteria FAIL; 2 UNTESTED
  diagnostics:
    per_trade_expectancy_bps: {mean: 433.7313, se: 441.388, t_stat: 0.9827, n: 42}
```
Verified directly against the raw per-window `results` list in the same
file: **every one of BTCUSDT's 15 windows has `core.sharpe: null`**
(0-4 trades each, all below the trade floor) — `median_sharpe=null` is not
a computation gap, it is `statistics.median([])` over an empty non-null
set, which is the CORRECT behavior of the existing per-window code given
zero non-sparse BTCUSDT windows. The defect is entirely downstream of that
correct computation: nothing converts "the aggregate is null because every
window was sparse" into "this fails a `>= 0.5791` floor" — a null value
can never satisfy a `>=` threshold, but the current code path leaves it as
`UNTESTED`/absent from the FAIL/PASS tally instead of resolving it to FAIL
against the pre-registered floor. This is the single, precise mechanism
C7's evaluator must fix (§6) — not "compute a missing statistic" (already
computed, correctly, per-window) but "apply the pre-registered comparator
to a value the pass rule itself anticipates can be null" (clause (c) says
exactly this: sparse windows "contribute null Sharpe").

Criterion (b) (`per-episode expectancy > 0`, sign-only per the
pre-registered wording): `per_trade_expectancy_bps.mean = 433.7313 > 0` →
**PASS** — confirmed by both the machine's own `trade_diagnostics_summary`
and `verdict_interpretation.yaml`'s (hand-corrected) `criteria_summary`.

### The machine verdict C7's evaluator must produce

Applying the pre-registered pass rule exactly as quoted, against
`protocol_result.yaml`'s own already-computed `per_symbol_summary` (no
recomputation from bars.csv/trades.json needed — see §6):
- **Criterion (a): FAIL.** BTCUSDT `median_sharpe = null` cannot satisfy
  `>= 0.5791` (null-per-A3.4 resolves to FAIL against any `>=` floor, per
  clause (c)); ETHUSDT `-0.686` fails `>= 0.0318` outright.
- **Criterion (b): PASS.** `433.7313 > 0`.
- **Per the pass rule's own text: "FAIL on (a) or (b) -> ... kill vs
  pivot."** Under B11's total-mapping fix (§5), this brief's FAIL-(a)
  branch must have carried an explicit `{hypothesis_verdict: kill,
  lineage_routing: terminate}` pair (matching the later pre-commitment) —
  had it, C7's evaluator would output exactly that, machine-authored, no
  hand-correction needed. This is the concrete "known-answer" the §8
  fixture checks: **FAIL-(a), verdict kill, medians computed (not
  UNTESTED)** — matching `verdict_interpretation.yaml`'s CURRENT,
  hand-corrected `protocol_verdict: kill` / `status: kill`, but produced
  by code from `protocol_result.yaml` + `pre_registration.yaml` alone, not
  by an operator editing the LLM's file after the fact.

### `user_brief_verbatim.yaml`

Confirmed identical in content to `pre_registration.yaml`'s pass rule
(both quote the same text) plus the full hypothesis/gate_definition/
evaluation/pre_registration/operational_constraints sections already
described in the K4 design note's B1 section (§7 there) — not re-quoted
again here; no new information for K2 beyond confirming the pass rule
text is consistent across both artifacts (as it must be under B4's
copy-through doctrine, already in force).

---

## 4. Design: A8 + A9 — verdict/routing split

### Schema (new fields on `verdict_interpretation.yaml`)

Replace the single `status`/`protocol_verdict` enum's DECISION authority
(the field itself stays, see backward-compat below) with two new
required fields:
```yaml
hypothesis_verdict: kill | refine | promote      # about the MECHANISM
lineage_routing: terminate | refine | pivot | escalate   # about the CAMPAIGN
```
**Authority rules** (mirrors the acceptance criterion's own framing):
- `hypothesis_verdict: kill` + `lineage_routing: terminate` → the lineage
  ends, NO scaffold, `_route_kill`'s per-hypothesis half only (§ below) —
  this hypothesis is dead AND the campaign does not continue this thread.
- `hypothesis_verdict: kill` + `lineage_routing: pivot` → run_057's ACTUAL
  situation: the mechanism is dead, but the campaign scaffolds a
  structurally different successor (same as today's "pivot" meaning) — one
  scaffold, via `_route_pivot`, unchanged from K4's mechanics.
- `hypothesis_verdict: kill` + `lineage_routing: escalate` → mechanism
  dead, campaign escalates search space (instrument/timeframe) — via
  `_route_escalate`, unchanged mechanics.
- `hypothesis_verdict: refine` + `lineage_routing: refine` → today's
  ordinary refine (parameter-level iteration) — via `_route_refine`.
- `hypothesis_verdict: promote` + `lineage_routing` is **not evaluated**
  (promote always proceeds to `holdout_evaluation`, per existing code
  line 3331-3306 — no routing question to ask).
- **Invalid pairs** (e.g. `hypothesis_verdict: refine` + `lineage_routing:
  terminate` — refining but ending the lineage is incoherent) are a
  `ValueError` at the SAME place `determine_post_verdict_route` already
  raises one for an unknown status (line 3379) — fail loudly, never
  silently pick one field over the other.

Pre-commitments (B11, §5) constrain `lineage_routing` directly (e.g. "FAIL
on (a) -> kill/terminate") WITHOUT needing to re-litigate
`hypothesis_verdict` — this is what "pre-commitments constrain routing
without needing to re-litigate the verdict" (A8's own fix text) means
concretely: a pre-registered brief can pin `lineage_routing` for a given
outcome while leaving `hypothesis_verdict` to the stage's own diagnostic
judgment (kill vs. refine), or pin both, per B11's schema.

### `_route_kill` split (A9)

`_route_kill` today does two unrelated things in one call: write
`campaign_decision.yaml` + set `campaign_state.status = "space_empty"`
(campaign-scope), and return `"completed_rejected"` (hypothesis-scope,
lineage-terminal). Split:
```python
def _route_kill(path, run_id, interp, campaign) -> str:
    """Per-hypothesis termination ONLY. No campaign-wide write."""
    print("\n🛑 KILL: hypothesis dead (mechanism falsified/no edge).")
    diag = _extract_diagnostics(path)
    update_campaign_state_after_run(run_id, "hypothesis", "", 
                                     interp.get("hypothesis_family", ""), "kill", diag)
    # K4 symmetry: record the (null) continuation explicitly, same site A1 uses.
    update_state(path=path, continuation_child=None, continuation_created_by="_route_kill")
    return "completed_rejected"
```
`campaign_decision.yaml`/`space_empty` move to **campaign-review scope**:
a NEW, explicit route (`_route_campaign_space_empty` or equivalent),
invoked only from `determine_post_campaign_review_route()` when
`campaign_review`'s own recommendation is `terminate_campaign` (a new,
explicit `campaign_review` recommendation value — not inferred from any
single hypothesis's kill). This mirrors exactly how `_route_escalate`'s
own instrument/timeframe exhaustion already calls `_mark_campaign_status
("space_empty")` (lines 2003, 2040) when the search space is GENUINELY
exhausted at the campaign-review/escalate layer — A9's fix makes
`_route_kill` stop doing that same thing prematurely, one layer too early,
for a single hypothesis. `_route_escalate`'s own two `_mark_campaign_status
("space_empty")` calls (instrument/timeframe exhaustion) are already
campaign-scope-correct and are NOT touched by this design — they already
live at the right layer, `_route_kill`'s did not.

### Backward-compatibility — every consumer of the old field (enumerated from code)

Six real call sites read `interp.get("status")` /
`interp.get("protocol_verdict")` today (grepped, not assumed):
1. `determine_post_verdict_route()` (`run_phase1_research.py` line 3290) —
   the primary router. **Migration:** reads `hypothesis_verdict`/
   `lineage_routing` directly once both are present; if EITHER is absent
   (an old-schema artifact, or a not-yet-migrated skill output), falls
   back to deriving both from the legacy `status` field via a fixed
   mapping table (`kill`→`{kill,terminate}` unless a pivot/escalate
   sidecar exists — ambiguous historical cases are NOT auto-resolved,
   they raise the SAME "unknown verdict" error class, now naming which
   field is missing).
2. `determine_post_campaign_review_route()`'s `continue`-branch duplicate
   dispatch (line ~3447-3458) — same migration, same fallback (this is
   flagged as its OWN, pre-existing duplication defect: two independent
   copies of the same status→route dispatch logic; A8's change is a
   natural point to factor this into one shared function, `_dispatch_
   verdict_route(status_fields, path, run_id, interp, campaign)`, called
   from both sites — a simplification opportunity, not required by any
   ledger item, flagged as an open question in §9 rather than assumed).
3. `_auto_generate_findings_carryover()` (line 2807) — branches
   `what_not_to_try` text by status. **Migration:** switches on
   `lineage_routing` (its branches are about what the NEXT run should
   avoid — a routing question, not a mechanism question) with the same
   legacy fallback.
4. `_verify_verdict_outputs()` (line ~2881) — validates the right
   deliverable exists for the verdict (`proposed_brief.yaml` for
   refine/pivot, `research_decision.yaml` for kill/promote,
   `escalation_request.yaml` for escalate). **Migration:** the file
   requirement is actually a `lineage_routing` question (which artifact
   the CAMPAIGN needs next), not a `hypothesis_verdict` one — switches to
   `lineage_routing`.
5. `run_campaign.py::_extract_run_numbers()` — `d.get("status") or
   d.get("protocol_verdict")` for a **log line only**
   (`verdict_status=...`). **Migration:** prefers
   `hypothesis_verdict`/`lineage_routing` if present (logs both,
   e.g. `verdict=kill/routing=pivot`), falls back to the legacy field for
   old runs' artifacts — read-only, no behavior depends on it, safest
   possible migration.
6. `skills/verdict-interpreter/SKILL.md`'s own "Output requirements"
   section (line 34-35) — the skill's OWN documentation of the schema it
   must emit. **Migration:** rewritten to require `hypothesis_verdict` +
   `lineage_routing` instead of `status`; `status` is KEPT as a
   derived/legacy-mirror field (`status = lineage_routing` when they
   coincide in meaning, e.g. `refine`/`pivot`/`escalate`; `status = kill`
   when `hypothesis_verdict == kill` regardless of routing) so that
   consumer #5 (log-only) and any external/historical tooling reading old
   runs never breaks, and a human skimming `verdict_interpretation.yaml`
   still sees a familiar single-word summary alongside the two
   authoritative fields.

No consumer is left silently reading a field that no longer carries
authority — every switch to the new fields is explicit, and every fallback
path is the OLD behavior exactly (never a new inference), so a
not-yet-migrated artifact (any run before this change) continues to route
exactly as it does today.

---

## 5. Design: B11 — total verdict+routing mapping

### Schema (new block in `pre_registration.yaml`, alongside the existing
`machine_constraints`/`gate_definition` — additive, nothing existing
renamed)

```yaml
pass_rule:
  statement: >
    <the human-readable pass rule text, exactly as pre-registered today —
    UNCHANGED, still the authoritative prose for human readers>
  outcomes:                    # TOTAL mapping — every branch named in
                                # `statement` must have an entry here
    - branch: PASS
      hypothesis_verdict: promote
      lineage_routing: null    # promote never asks a routing question (§4)
    - branch: FAIL-a
      hypothesis_verdict: kill
      lineage_routing: terminate
    - branch: FAIL-b
      hypothesis_verdict: kill
      lineage_routing: terminate
    - branch: sparse_inconclusive     # A3.4's own named case
      hypothesis_verdict: refine
      lineage_routing: refine
      discretion: stage         # OPT-IN escape hatch, see below
```
`discretion: stage` is the ONLY way a branch may omit a concrete
`hypothesis_verdict`/`lineage_routing` pair — it must be an EXPLICIT,
named opt-in (not the absence of a pair, which is what today's "verdict
routing decides kill vs pivot" free-text amounts to). When present, the
stage retains today's freedom for that branch ONLY, and must still choose
from the vocabulary A8 defines (no free-text escape). Every branch in
`pass_rule.statement`'s own prose (identified by materialization-time
parsing, see lint below) that has NO corresponding `outcomes` entry, and
no `discretion: stage` on the entry it WOULD need, is a rejected brief.

**Mid-run pre-commitments** (run_057's actual failure mode: the sidecar
`prescreen_override_20260711.yaml` narrowed an already-`discretion: stage`
branch AFTER the brief was frozen): must be written INTO this SAME
`outcomes` block (amending the specific branch's entry, replacing
`discretion: stage` with a concrete pair), with an audit trail field:
```yaml
    - branch: FAIL-a
      hypothesis_verdict: kill
      lineage_routing: terminate
      amended_at: '2026-07-11'
      amended_by: operator_precommitment
      amendment_reason: >
        A8.3 sparse-signal conjunction rule made the prescreen kill route
        inadmissible as sole evidence; walk-forward's own criterion (a) is
        final per this amendment. See prescreen_override_20260711.yaml.
```
never into a separate sidecar file the stage has no schema reason to read.
This is the direct fix for D3's root-cause chain (§0): once amendments
live IN the pass-rule artifact the stage already reads as a required
input (ties to B7, already-ledgered, not this kernel's own item but the
same input-plumbing K2 depends on), there is no sidecar left to miss.

### Materialization-time lint

New validation function, `_lint_pass_rule_total_mapping(pre_registration:
dict) -> list[str]` (empty = conforms), called at the SAME point
`_materialize_run`/`_materialize_refinement_run` (`run_campaign.py`,
K4) currently write `pre_registration.yaml` — a non-conforming brief
never reaches `runs/<id>/artifacts/pre_registration.yaml` at all; the
launch (or refinement-brief materialization) fails loudly with the
specific missing branch named, mirroring `_parse_brief_frontmatter`'s
existing required-field `ValueError` style. Checks:
1. Every `branch` named in `pass_rule.outcomes` has both
   `hypothesis_verdict` (one of `kill|refine|promote`) and
   `lineage_routing` (one of `terminate|refine|pivot|escalate|null`) OR
   an explicit `discretion: stage`.
2. `hypothesis_verdict: promote` branches have `lineage_routing: null`
   (promote never routes — §4) — a non-null routing on a promote branch
   is a lint error (contradicts A8's authority rule), not silently
   accepted.
3. (Best-effort, not required to block) a light textual cross-check that
   `pass_rule.statement`'s own prose actually enumerates the SAME branch
   labels used in `outcomes` (catches a brief where the human wrote "FAIL
   on (a) or (c)" in prose but only registered outcomes for "FAIL-a" and
   "FAIL-b") — reported as a WARNING in the materialization log, not a
   hard reject, since prose branch-labeling is inherently fuzzier than the
   structured `outcomes` list itself.

An operator can author a conformant brief from this note alone: write
`pass_rule.statement` as today, enumerate every branch the statement's own
prose distinguishes under `outcomes`, give each a concrete
`hypothesis_verdict`/`lineage_routing` pair (or `discretion: stage`
explicitly), and the lint either accepts it or names the exact missing
branch.

---

## 6. Design: C7 — machine-checkable criteria evaluator

### Schema (structured criteria in `pre_registration.yaml`, alongside
B11's `outcomes` block — same document, criteria feed the branch
selection)

```yaml
pass_rule:
  criteria:
    - id: a
      metric: median_sharpe            # field name in per_symbol_summary
      metric_basis: bar_level           # per C8/metric-basis doctrine — never fragment-level
      comparator: ">="
      per_symbol_threshold:
        BTCUSDT: 0.5791
        ETHUSDT: 0.0318
      null_handling: fails_threshold    # A3.4: a null/undefined aggregate
                                        # NEVER satisfies a ">=" floor — see
                                        # run_057's own BTCUSDT case, section 3
      window_set_ref: protocols/ts_trend_daily_v1.json   # ties to B3 (protocol
                                        # pinning, already-ledgered, not this
                                        # kernel's item) — evaluator refuses to
                                        # run against a mismatched protocol_file
    - id: b
      metric: per_trade_expectancy_bps
      metric_basis: episode_level       # per_trade_expectancy_bps is already
                                         # episode-level by construction (A3.4)
      comparator: ">"
      threshold: 0
      statistic: mean                   # sign-only per this brief's own
                                         # pre-registered wording — no t-stat
                                         # bar; a DIFFERENT brief could instead
                                         # require e.g. "t_stat >= 2" here
    - id: c
      metric: sparse_window_handling
      rule: null_contributes_to_aggregate   # documents (c)'s own text machine-
                                             # readably; not independently
                                             # evaluated (it's the null_handling
                                             # policy criterion (a) already uses)
```

### Evaluator (new function, `evaluate_pass_rule_criteria(protocol_result:
dict, pre_registration: dict) -> dict`, location: a NEW module,
`tools/verdict_criteria_evaluator.py`, imported by
`run_phase1_research.py`'s protocol_execution stage handler — NOT inside
`tools/run_protocol.py`, to keep the pre-registered-criteria evaluator
independent of the generic-threshold/prose-criteria machinery it replaces
rather than layering on top of it)

Reads:
- `protocol_result.yaml`'s `per_symbol_summary` (already-computed
  `median_sharpe`/`max_abs_drawdown_pct`/`min_trade_count` per symbol —
  REUSED, not recomputed; run_057's own case (§3) confirms these values
  are already correctly computed at the per-window level) and
  `trade_diagnostics_summary.per_trade_expectancy_bps` (already-computed
  episode-level mean/se/t_stat/n).
- `pre_registration.yaml`'s new `pass_rule.criteria` list (§ above).

For each criterion:
1. Look up the named `metric` in `protocol_result`'s appropriate block
   (`per_symbol_summary[symbol][metric]` for per-symbol criteria,
   `trade_diagnostics_summary[metric][statistic]` for pooled ones).
2. If the value is `None`/absent and `null_handling: fails_threshold` —
   resolve to **FAIL**, machine-authored, with a reason string naming
   WHY (`"BTCUSDT median_sharpe is null (all N windows below the A3.4
   trade floor) — a null aggregate cannot satisfy >= 0.5791, resolved as
   FAIL per the pre-registered null_handling policy"`) — this is the
   exact fix for run_057's own gap (§3): no more `UNTESTED`, a REAL,
   reasoned FAIL.
3. If the value is `None`/absent and no `null_handling` is specified —
   `SPEC_ERROR` (mirrors `tools/run_protocol.py`'s own existing
   `SPEC_ERROR` category for an impossible-to-evaluate criterion, lines
   632-636) — a brief that doesn't pre-register what a null means for its
   own criterion is a brief the lint (§5) should have caught missing a
   `null_handling` field; this is the runtime backstop.
4. Otherwise apply `comparator`/`threshold` (or `per_symbol_threshold`)
   directly — no keyword matching, no prose parsing, no unit-ambiguity
   guessing (the exact three failure classes C7's replaced parser had:
   `_is_untested`'s hardcoded keyword list, `_resolve_field`'s "no
   matching metric keyword," and the documented raw-vs-percent ambiguity
   in `_evaluate_criterion`'s own comment, lines 471-480).

Output — a NEW, machine-authored artifact,
`runs/<id>/artifacts/pass_rule_evaluation.yaml`:
```yaml
criteria_results:
  - id: a
    result: FAIL
    per_symbol:
      BTCUSDT: {value: null, threshold: 0.5791, result: FAIL, reason: "null aggregate (A3.4, all windows sparse) cannot satisfy >= threshold"}
      ETHUSDT: {value: -0.686, threshold: 0.0318, result: FAIL}
  - id: b
    result: PASS
    value: 433.7313
    threshold: 0
statement_branch_matched: FAIL-a          # which B11 outcomes branch this
                                           # resolves to (first FAIL branch
                                           # in criteria id-order — a FAIL on
                                           # criterion 'a' IS branch 'FAIL-a')
hypothesis_verdict: kill                  # copied from B11's outcomes[FAIL-a]
lineage_routing: terminate                # copied from B11's outcomes[FAIL-a]
evaluated_at: '2026-07-13T...'
evaluator_version: 1
```
This artifact is what the `verdict-interpreter` LLM stage receives as a
**required input** (new handoff field, mirroring B7's own "pre_registration.yaml
as required_inputs" fix — already ledgered, this kernel just adds ANOTHER
required input alongside it) — **the machine writes the verdict, the LLM
stage reads it**, exactly inverting today's flow (LLM computes `status`
prose-first, code never checks it against anything binding). The skill's
own job shifts from "decide kill/refine/pivot" to "explain WHY, cite
`pass_rule_evaluation.yaml`'s verdict, and supply the qualitative fields
(`root_cause`, `config_to_failure_map`, `trade_attribution`) that no
formula can produce" — `hypothesis_verdict`/`lineage_routing` in
`verdict_interpretation.yaml` become COPY-THROUGH fields from
`pass_rule_evaluation.yaml` (B4 copy-through discipline, already-ledgered,
directly reused here), not independently re-decided prose. A stage output
that disagrees with `pass_rule_evaluation.yaml`'s verdict is a
`human_pause` (mirrors B8's semantic-conformance-gate precedent), never a
silent overwrite either direction.

**Prose criteria banned from the decision path:** `validation_protocol.yaml`
and its `evaluate_against_decision_rules()` keyword-matched path are NOT
called by `determine_post_verdict_route`'s decision-making anymore —
`protocol_execution`'s subprocess call to `tools/run_protocol.py` still
runs (it computes the underlying per-window/per-symbol statistics
`pass_rule_evaluation.yaml` consumes), but `--validation-protocol`'s
OWN verdict fields (`hypothesis_verdict`/top-level `verdict` inside
`protocol_result.yaml`) become informational-only, explicitly labeled as
such, never read by the routing layer. `validation_protocol.yaml` itself
is not deleted (still useful as descriptive context for a human/the
skill's own prose), but its criteria are no longer decision-bearing —
exactly C7's own fix text ("prose criteria banned from the decision
path").

---

## 7. Design: C9 rider — KB exhaustion gate on the verdict stage's own
proposal paths

### A verified, code-level root cause the ledger text doesn't name

Cross-referenced `_check_kb_reactivation_conformance()` (the existing
campaign-review-side gate, `run_phase1_research.py` lines 1658-1710)
against `campaign_knowledge_base.yaml`'s actual findings schema. The
function reads `f.get("hypothesis_id")` (**singular**) at line 1693. The
KB's `findings:` list is NOT schema-uniform: **9 of 15 findings** use a
singular `hypothesis_id` field, but **5 — including all three Keltner
findings C9's own symptom names** (`keltner_mean_reversion_no_edge`,
`keltner_breakout_inverted`, `keltner_scoremode_no_edge`) plus the two RSI
findings — use a **plural `hypothesis_ids` list** instead (verified by
direct parse: `grep`-and-`yaml.safe_load` count, not assumed). One finding
has neither field. Concretely: `f.get("hypothesis_id")` returns `None` for
every Keltner finding, so the `if not hyp_id: continue` guard (line 1694)
skips these findings ENTIRELY, regardless of what text
`next_research_question` contains. **Even where the existing gate DOES
run today (campaign-review's own reframe path), it structurally cannot
catch a re-proposal of the exact family this ledger item's own symptom
names**, independent of the "wrong stage" gap C9 already documents. This
is not a contradiction of the ledger (the documented symptom — "the check
doesn't exist at verdict_interpreter's pivot path" — is still accurate and
sufficient on its own to explain the incident) but a DEEPER, previously
undiagnosed reason a naive "just call the existing function from the
verdict stage too" fix would still fail on exactly this historical case.
Any C9 implementation MUST fix this schema handling, or it ships not
actually closing the gap it claims to.

### Where the "proposal" actually lives, per route (verified from code)

- **`_route_refine`**: reads `proposed_brief.yaml` (LLM-authored,
  `path/artifacts/proposed_brief.yaml`) and copies it into the child's
  `research_brief.yaml` via `setup_next_run`. This IS the literal
  "before writing proposed_brief.yaml" moment the ledger names — the gate
  belongs immediately before `setup_next_run(path, next_id)` is called
  (`run_phase1_research.py`, inside `_route_refine`).
- **`_route_pivot`**: verified it does **NOT** read or write
  `proposed_brief.yaml` at all (its own inline comment, line ~1967 area:
  "Scaffold directory only — no proposed_brief to copy. The next run's
  brief is produced by hypothesis_generation using findings_carryover.yaml
  as input"). The ledger's "before writing proposed_brief.yaml" framing
  does not literally apply to this route — there is no file to gate at
  this point in the CODE. The forward-looking content that could name a
  forbidden family at pivot time is `verdict_interpretation.yaml`'s own
  prose (`primary_failure_mode`, `config_to_failure_map`, `root_cause`,
  `hypothesis_family`) and/or `findings_carryover.yaml`'s
  `what_not_to_try`/notes fields (both already written by the time
  `_route_pivot` runs). **Design choice, stated explicitly rather than
  silently assumed:** the gate for the pivot route checks THIS text
  (the same fields `_check_kb_reactivation_conformance`-style text
  matching already scans elsewhere) immediately before
  `_route_pivot` scaffolds the next run — the earliest point any
  forward-looking family name is actually available in this route's own
  code path, even though it is not literally "before writing
  proposed_brief.yaml." A forbidden mention here is necessarily a
  HUMAN's/LLM's own suggestion of where to go next, not yet a formal
  hypothesis card (that's `hypothesis_generation`'s job, a later, already
  separately-gated stage) — catching it here is strictly earlier and
  cheaper than waiting for that stage to formalize it into a wasted
  scaffold.
- **`_route_escalate`**: does not propose a hypothesis family at all
  (instrument/timeframe escalation, same methodology carried forward
  verbatim) — no gate needed, confirmed by reading both branches
  (§2 of the K4 design note already quoted this code in full).

### Fix (generalizing and repairing `_check_kb_reactivation_conformance`)

1. **Schema fix (prerequisite, not optional):**
   `_check_kb_reactivation_conformance` (and any new caller) reads
   `f.get("hypothesis_ids") or ([f["hypothesis_id"]] if f.get("hypothesis_id")
   else [])` — normalizing BOTH schema shapes to a list before the
   `hyp_id.lower() not in text` check, iterating every id in that list.
   This is a correctness fix to EXISTING, shipped code (the campaign-review
   gate), not new code — flagged as an in-scope bug fix bundled with C9
   since C9's own acceptance criterion is meaningless without it (a pivot
   test against `keltner_mean_reversion_no_edge` would still silently pass
   the gate otherwise, per the verified defect above).
2. **New call site 1 — refine:** inside `_route_refine`, before
   `setup_next_run(path, next_id)`: parse `proposed_brief.yaml`'s own
   `research_goal`/`existing_context`/`constraints`-equivalent prose
   fields (same extraction shape `_check_kb_reactivation_conformance`
   already uses) and run the (now schema-fixed) exhaustion check against
   `campaign_knowledge_base.yaml`. A forbidden-family match →
   `update_state(path=path, status="paused_for_human",
   flags={"kb_reactivation_violation": True}, kb_reactivation_violations=[...])`
   and return `"human_pause"` — **before** `setup_next_run` runs, so no
   child is scaffolded (same "check before scaffold" ordering K4's own
   B1 conflict-check rider already established as this repo's pattern).
3. **New call site 2 — pivot:** inside `_route_pivot`, before its
   `_scaffold_next_run`/subprocess call: run the same check against the
   concatenated text of `verdict_interpretation.yaml`'s
   `primary_failure_mode`/`config_to_failure_map`/`root_cause.
   supporting_evidence` and `findings_carryover.yaml`'s `what_not_to_try`/
   `notes`. Same pause treatment, same "before scaffold" ordering.
4. **Shared helper:** both call sites use ONE function,
   `_check_kb_exhaustion_before_proposal(text: str, kb: dict) -> list`,
   a thin wrapper around the schema-fixed
   `_check_kb_reactivation_conformance`'s own matching logic (refactored
   to accept raw text directly rather than requiring a
   `next_research_question`-shaped dict, since refine/pivot's inputs
   aren't shaped like campaign_review's `next_research_question`) — one
   matching implementation, three call sites total counting the existing
   campaign-review one, not three divergent copies.

---

## 8. Fixture plan (design only)

All fixtures follow the K4 pattern exactly: sandboxed `tmp_path` root,
`monkeypatch` of `ROOT`/`CAMPAIGN_STATE_PATH`/`QUEUE_PATH` module globals,
subprocess/`setup_run` stubbing per K4's own established precedent
(`tests/test_k4_routing_registration.py`'s `campaign_root` fixture and its
`_fake_setup_run`/`_fake_subprocess_run` helpers are directly reusable,
not reinvented). Zero real-state writes, zero LLM spend (every fixture
constructs `verdict_interpretation.yaml`/`protocol_result.yaml`/
`pre_registration.yaml` directly as test data, never invokes an agent).

**C7 known-answer fixture** (acceptance: run_057's own artifacts re-judged
by the structured evaluator must yield FAIL-(a)/kill with medians
computed, not UNTESTED):
1. Copy run_057's REAL `protocol_result.yaml` and `pre_registration.yaml`
   (read-only source files, copied into the tmp fixture root — never
   mutated in place) into a fixture run directory; extend
   `pre_registration.yaml`'s copy with the new `pass_rule.criteria`/
   `pass_rule.outcomes` blocks (§5/§6 schemas) encoding EXACTLY the
   pre-registered rule already quoted in §3 (criterion a:
   `median_sharpe >= {0.5791, 0.0318}` per-symbol, `null_handling:
   fails_threshold`; criterion b: `per_trade_expectancy_bps.mean > 0`;
   outcomes FAIL-a → `{kill, terminate}`).
2. Call `evaluate_pass_rule_criteria(protocol_result, pre_registration)`
   directly.
3. Assert: `criteria_results[a].result == "FAIL"`,
   `criteria_results[a].per_symbol.BTCUSDT.value is None` (computed and
   PRESENT, not absent/UNTESTED — the field exists with a null value and
   an explicit reason, distinguishable from "never evaluated"),
   `criteria_results[a].per_symbol.ETHUSDT.value == -0.686`,
   `criteria_results[b].result == "PASS"`,
   `statement_branch_matched == "FAIL-a"`, `hypothesis_verdict == "kill"`,
   `lineage_routing == "terminate"`.

**A9 fixture** (acceptance: a kill verdict on one queue entry leaves
`campaign_state.status` untouched and other entries schedulable):
1. Two fixture queue entries, both `ready`/`in_progress`-eligible.
2. Drive the first through the split `_route_kill` (§4) directly (same
   direct-function-call pattern K4's own A1 fixture uses for
   `_route_refine`/`_route_pivot`/`_route_escalate`).
3. Assert: `campaign_state.yaml`'s `status` field is absent or unchanged
   from its pre-call value (never set to `"space_empty"`); no
   `campaign_decision.yaml` written anywhere under the fixture root; the
   SECOND queue entry is still returned by `_select_entry()` as
   schedulable.

**B11 lint fixture** (acceptance: rejects a pass rule with an unmapped
FAIL branch, accepts a total mapping):
1. Fixture `pre_registration.yaml` with `pass_rule.outcomes` covering
   PASS and FAIL-a only, prose statement naming FAIL-a AND FAIL-b — call
   `_lint_pass_rule_total_mapping(...)`, assert a non-empty violation list
   naming `FAIL-b` specifically.
2. Same fixture with FAIL-b added (concrete pair or explicit
   `discretion: stage`) — assert empty violation list.
3. Regression: a `promote` branch carrying a non-null `lineage_routing` —
   assert it's flagged (authority-rule violation, §4/§5).

**A8 fixture** (acceptance: a killed hypothesis with routing terminate
produces no scaffolds; killed + pivot produces one, and the two fields are
separately auditable):
1. Fixture `verdict_interpretation.yaml` #1: `hypothesis_verdict: kill`,
   `lineage_routing: terminate`. Drive through
   `determine_post_verdict_route`'s new dispatch (§4). Assert: return
   value is `"completed_rejected"`, NO new `runs/<id>` directory created,
   `campaign_state.status` untouched (shares the A9 fixture's own
   assertion helper).
2. Fixture #2: `hypothesis_verdict: kill`, `lineage_routing: pivot` (the
   run_057 shape). Assert: exactly one new scaffolded run directory
   exists (via `_route_pivot`), AND both `hypothesis_verdict` and
   `lineage_routing` are independently readable/assertable from the
   PARENT run's own `verdict_interpretation.yaml` afterward (never
   overwritten into a single collapsed field) — this is the "separately
   auditable" half of the acceptance criterion.

**C9 fixture** (acceptance: a pivot route against a KB-exhausted family
refuses to emit the proposal and pauses):
1. Fixture `campaign_knowledge_base.yaml` with a plural-`hypothesis_ids`
   finding (`keltner_mean_reversion_no_edge`-shaped, to specifically
   regression-test the schema fix in §7 — a fixture using ONLY a
   singular-schema finding would not catch a regression of the real bug
   found this phase).
2. Fixture `verdict_interpretation.yaml`/`findings_carryover.yaml` whose
   prose names `keltner_mean_reversion` (one of that finding's
   `hypothesis_ids` entries, not its `id`) as the pivot direction.
3. Call the new pivot-route gate (§7 point 3) directly. Assert: returns/
   pauses via `human_pause` with `kb_reactivation_violation: True` flagged
   (same flag name the existing campaign-review gate already uses — one
   vocabulary, two call sites), NO scaffold created, and — separately — a
   fixture using the SAME finding's `id` string instead of an entry from
   its `hypothesis_ids` list does NOT falsely match (proves the fix
   matches on the list's actual members, not a looser substring
   coincidence).

---

## 9. Files to be modified (implementation phase, not this phase) + open questions

**`workflow/run_phase1_research.py`:**
- `verdict_interpretation.yaml` schema additions consumed:
  `hypothesis_verdict`/`lineage_routing` (§4).
- `determine_post_verdict_route()` — new-field dispatch + legacy fallback
  (§4); `_route_kill` split (§4); `_route_refine`/`_route_pivot` gain the
  C9 gate calls (§7) before their respective scaffold calls;
  `_check_kb_reactivation_conformance` gets the `hypothesis_ids`/
  `hypothesis_id` schema fix (§7) and a text-accepting wrapper,
  `_check_kb_exhaustion_before_proposal`.
- `_auto_generate_findings_carryover()`, `_verify_verdict_outputs()` —
  switch to `lineage_routing` (§4).
- New: `_lint_pass_rule_total_mapping()` (§5) — called from
  `run_campaign.py`'s materialization functions (below), defined here
  since it validates a `pre_registration.yaml`-shaped dict independent of
  queue mechanics.
- protocol_execution stage handler — calls the new evaluator (below)
  after `run_protocol.py`'s subprocess returns, writes
  `pass_rule_evaluation.yaml`.

**New module, `tools/verdict_criteria_evaluator.py`:**
- `evaluate_pass_rule_criteria()` (§6).

**`workflow/run_campaign.py`:**
- `_materialize_run()`/`_materialize_refinement_run()` (K4) call
  `_lint_pass_rule_total_mapping()` on any `pre_registration.yaml` they
  write; a violation refuses materialization (mirrors K4's own
  refinement-brief required-key `ValueError` style).

**`skills/verdict-interpreter/SKILL.md`:**
- Output requirements: `status` → `hypothesis_verdict` + `lineage_routing`
  (`status` retained as a derived mirror, §4); the stage's OWN job
  description updated to reflect that `pass_rule_evaluation.yaml` (a
  REQUIRED input, new) carries the verdict — the skill explains/qualifies
  it, does not decide it independently; a stage output disagreeing with
  `pass_rule_evaluation.yaml` is a `human_pause`, documented explicitly.
- Rule 6 CASE B and the other five diagnostic rules are UNCHANGED — they
  still drive `root_cause`/`altitude_justification` qualitative content;
  only the PASS/FAIL/routing decision itself moves to the machine.

**`templates/research_brief.yaml`** (or wherever the brief template
lives) and **`briefs/*.yaml`** authoring guidance: the B11
`pass_rule.outcomes`/C7 `pass_rule.criteria` schemas need to be
documented somewhere an operator authoring a NEW brief will find them —
flagged as a doc-hygiene follow-up, not blocking.

**Open questions for the operator:**
1. §4's `_dispatch_verdict_route()` factoring (removing the duplicate
   status→route dispatch between `determine_post_verdict_route` and
   `determine_post_campaign_review_route`'s continue-branch) — worth
   doing now as part of this same change, or deferred? It touches code
   this kernel already has open, but isn't required by any single ledger
   item.
2. §6 places the new evaluator in a NEW module
   (`tools/verdict_criteria_evaluator.py`) rather than extending
   `tools/run_protocol.py` in place — confirm this separation is wanted
   (rationale: keeps the pre-registered-criteria evaluator's lifecycle
   independent of the generic/prose machinery it's replacing, and avoids
   growing `run_protocol.py`'s already-large `evaluate_against_
   decision_rules` further) versus the alternative of retiring
   `evaluate_against_decision_rules` entirely and inlining its
   replacement in the same file.
3. §5's `pass_rule.outcomes` schema nests under the EXISTING
   `pre_registration.yaml` top-level `pass_rule` scalar-string field
   (today: a single prose string) — this design turns that field from a
   string into a dict with `statement`/`outcomes`/`criteria` children.
   Every existing run's `pre_registration.yaml` (a plain string today,
   confirmed by run_057's own artifact, §3) is a legacy shape under this
   change. Confirm this is acceptable (old runs are read-only historical
   artifacts, never re-materialized) rather than requiring a
   string-or-dict polymorphic reader.
4. §7's fix to `_check_kb_reactivation_conformance` (the
   `hypothesis_ids`/`hypothesis_id` schema normalization) is a real bug
   fix to EXISTING, already-shipped campaign-review-gate code, bundled
   into this kernel because C9's own acceptance criterion depends on it.
   Confirm bundling it here (rather than filing it as an independent,
   smaller fix landing first) is the wanted sequencing.

---

## Read-back

File written once; content above is the full note (10 numbered sections:
§0 Scope, §1 Ledger items read, §2 Code quotes (a-f), §3 run_057
known-answer artifacts, §4 A8+A9 design, §5 B11 design, §6 C7 design, §7
C9 rider design, §8 Fixture plan, §9 Files-to-modify + open questions) —
matches the step-9 requirement (sections mirroring steps 2-8, plus
files-to-be-modified and open questions, as one coherent document).

---

## Phase B rulings + deviations (2026-07-13)

Body above is unchanged from Phase A approval. This section records the
operator's Phase B rulings/amendments and every point where implementation
deviated from the approved design, per the Phase B prompt's step 1
instruction ("never silently improved").

### Operator rulings applied

- **R1**: `_dispatch_verdict_route()` implemented as the single shared
  dispatcher, called from both `determine_post_verdict_route` and
  `determine_post_campaign_review_route`'s continue-branch. Consolidating
  the two surfaced a REAL pre-existing behavioral divergence, not just a
  textual duplication — see deviation 2 below.
- **R2**: `tools/verdict_criteria_evaluator.py` created as a new,
  independent module (not folded into `tools/run_protocol.py`).
- **R3**: `evaluate_pass_rule_criteria()` returns `{"result":
  "legacy_not_evaluable", "reason": ...}` for a string-shaped, absent, or
  otherwise non-conformant `pass_rule` — verified never to raise (fixtures
  `test_r3_*`, 3/3 passing).
- **R4**: the `hypothesis_id`/`hypothesis_ids` schema fix inside
  `_check_kb_reactivation_conformance` (`workflow/run_phase1_research.py`)
  is bundled into this kernel as instructed. **Flagged explicitly per R4:
  this is a bug fix to EXISTING, already-shipped campaign-review-gate
  code** (the A5.4/F09 gate predates K2 entirely) — not new K2 behavior.
  Without it, C9's own acceptance criterion (a pivot against a
  KB-exhausted Keltner-family finding pauses) would silently fail, since
  every Keltner finding uses the plural schema.

  **Parked data-hygiene item (not fixed, filed per R4):** direct parse of
  `campaign_knowledge_base.yaml`'s 15 `findings` entries shows a genuinely
  inconsistent schema: **9 use singular `hypothesis_id`**
  (`funding_rate_mean_reversion_inconclusive`,
  `funding_rate_mean_reversion_run047_invalidated`,
  `fear_greed_contrarian_inconclusive`, `volume_impulse_continuation_blocked`,
  `ema_spread_trend_continuation_v1_auto`,
  `funding_rate_continuous_mean_reversion_auto`,
  `funding_rate_continuous_mean_reversion_expanded_auto`,
  `macd_trend_continuation_extended_2018_2025_auto`,
  `p4_sma_trend_longonly_daily_auto`), **5 use plural `hypothesis_ids`**
  (`keltner_mean_reversion_no_edge`, `keltner_breakout_inverted`,
  `keltner_scoremode_no_edge`, `rsi_mean_reversion_no_edge`,
  `rsi_momentum_trending_cost_drag`), and **1 has neither field**
  (`er_detector_unusable_btc_eth_1h`). The code fix (§7, normalizing both
  shapes to a list before matching) makes this robust going forward, but
  the KB FILE itself is not normalized to one schema — a future session
  should either standardize every finding on `hypothesis_ids` (list, even
  for single-hypothesis findings) or document why the split is
  intentional. Not blocking; filed here so it isn't rediscovered from
  scratch.

### Operator amendments applied

- **A1**: `pass_rule_evaluation.yaml` now always includes
  `branches_failed` (every failing branch, id-order-independent) alongside
  `statement_branch_matched` (the id-order-selected one) — verified by
  `test_c7_run_057_known_answer_fail_a_kill_terminate`. The lint
  (`_lint_pass_rule_total_mapping`) emits a WARNING (never a rejection)
  when multiple registered FAIL branches carry differing verdict pairs —
  `test_b11_lint_warns_on_differing_fail_pairs` — and
  `evaluate_pass_rule_criteria()` emits the SAME warning at evaluation
  time (in the result dict's own `warning` field) as a second, independent
  check against the run's actual criteria outcomes, not just the
  registered outcomes shape.
- **A2**: RUNBOOK.md section 3 updated. **Deviation, stated explicitly**:
  implemented as ONE expanded row for `kb_reactivation_violation`
  (covering both trigger sites — the pre-existing campaign-review gate
  AND the new C9 verdict-stage gate — with the same reason string) plus
  ONE genuinely new row for `pass_rule_evaluation_disagreement`, rather
  than two textually-separate rows for the KB-exhaustion case. Both
  trigger sites set the IDENTICAL flag name
  (`kb_reactivation_violation`) and produce the identical reason string
  via identical detection code (`_hard_pause_reason`/
  `_classify_human_pause` in `run_campaign.py` cannot and does not
  distinguish them) — a second row keyed on the same Reason-column value
  would read as a duplicate table entry, not a second distinguishable
  pause. The expanded row's content explicitly documents both triggers
  and both resolution paths instead.
- **A3**: `evaluate_pass_rule_criteria()`'s `window_set_ref` check compares
  file basenames only (`ref_name`/`actual_name` in the code, with an
  inline comment naming this limitation at the check site — see §6/code).
  **Limitation restated here per A3**: a brief registering
  `window_set_ref: protocols/foo.json` passes this check as long as
  `protocol_result.yaml`'s own recorded `protocol_file` has the same
  basename — even if `protocols/foo.json`'s CONTENT (its actual window
  list) was silently redefined after registration without renaming the
  file. Content-hash pinning (verifying the actual bytes/hash match what
  was pre-registered, not just the name) is explicitly K3/B3+B10 scope,
  not implemented in this kernel.

### Deviations from the approved design (with reasons)

1. **A9's campaign-scope termination reuses an EXISTING recommendation
   value instead of inventing a new one.** The Phase A design proposed a
   new campaign_review recommendation, `"terminate_campaign"`. On
   implementation, `determine_post_campaign_review_route` was found to
   ALREADY have a `rec == "terminate"` branch (pre-K2, pre-existing) that
   already called the old, unsplit `_route_kill` — i.e., the
   campaign-scope-explicit termination path A9 wants isolated already
   existed under a different, already-shipped name. Rather than adding a
   redundant second enum value, `rec == "terminate"` now calls the new
   `_route_campaign_terminate` (the split-out campaign-wide half)
   instead of the now-per-hypothesis-only `_route_kill`. No new
   recommendation vocabulary was needed. See the inline code comment at
   `determine_post_campaign_review_route`'s `rec == "terminate"` branch.
2. **R1's consolidation surfaced a real, pre-existing behavioral
   divergence between the two dispatch copies, not just textual
   duplication.** `determine_post_campaign_review_route`'s continue-branch
   handled `status == "promote"` as a bare `return "completed_promoted"`,
   skipping `_write_promotion_audit` and the `holdout_evaluation` gate
   entirely — unlike `determine_post_verdict_route`'s own promote handling
   (writes `promotion_audit.yaml`, routes to `holdout_evaluation`). Nothing
   in the codebase documents this as an intentional difference, and this
   campaign's own standing doctrine treats the single-use holdout gate as
   mandatory for every promote. R1 explicitly rejects "two divergent
   copies"; unifying onto `_dispatch_verdict_route` necessarily picks ONE
   behavior, and the complete one (promotion_audit + holdout_evaluation)
   is the only one consistent with standing doctrine. Flagged inline in
   code (the continue-branch's own comment) and here — this closes what
   was, in effect, a live holdout-bypass bug for any hypothesis promoted
   via campaign_review's continue path.
3. **`_dispatch_verdict_route` does not independently validate every
   `hypothesis_verdict`/`lineage_routing` PAIR for semantic coherence**
   (the design note's §4 text mentions an incoherent pair, e.g.
   refine+terminate, should raise `ValueError`). The implementation
   dispatches purely on `lineage_routing`'s value (with
   `hypothesis_verdict` distinguishing only the terminal promote case),
   which correctly routes every REAL combination this kernel produces
   (kill+terminate, kill+pivot, kill+escalate, refine+refine,
   refine+pivot, refine+escalate) but does not reject a theoretically
   incoherent pair an artifact could carry. None of the required fixtures
   exercise this case. Flagged as a scope-limited simplification, not a
   silent gap.
4. **C9's gate calls `_check_kb_reactivation_conformance` directly at both
   new call sites, rather than adding the separate
   `_check_kb_exhaustion_before_proposal` wrapper the design note's §7
   named.** `proposed_brief.yaml` (refine) is already a
   research_brief.yaml-shaped document with compatible field names, so it
   is passed to the existing function directly; the pivot route assembles
   its available prose into a `{"research_goal": <text>}` dict, matching
   the existing function's own expected shape. Same net effect, one fewer
   indirection layer, no duplicated matching logic either way.
5. **The evaluator does not mechanize a `sparse_inconclusive`-style
   auto-triggered branch.** The design note's §5/§6 schema examples showed
   a `sparse_inconclusive` branch with `discretion: stage` as an
   illustration, but never specified what MECHANICAL condition (as
   opposed to an ordinary criterion FAIL) should select it. The
   implemented evaluator only resolves the `PASS` branch (all criteria
   PASS) or the first-id-order `FAIL-<id>` branch — a brief wanting
   sparse-inconclusive-style behavior registers it as an ordinary
   criterion with its own FAIL branch (with `discretion: stage` if the
   verdict should be left to the LLM stage for that specific branch), not
   via an unspecified auto-detection rule.
6. **A new function not explicitly speced in Phase A,
   `_check_pass_rule_evaluation_conformance()`, was written this phase**
   to actually implement the "stage output disagrees with
   pass_rule_evaluation.yaml is a human_pause" behavior §6/§9's
   SKILL.md-update plan described in prose but did not reduce to a
   concrete comparison function. It compares `verdict_interpretation.yaml`'s
   resolved `hypothesis_verdict`/`lineage_routing` against
   `pass_rule_evaluation.yaml`'s own values whenever the latter carries a
   BINDING verdict (`result` `PASS`/`FAIL`, no `discretion: stage`),
   pausing (flag `pass_rule_evaluation_disagreement`) on any mismatch.
   Wired into both `determine_post_verdict_route` and
   `determine_post_campaign_review_route`'s continue-branch (R1
   consistency — one check, not a divergent second copy).
7. **Noted, not a functional deviation**: run_057's own REAL
   `pre_registration.yaml` nests its (legacy, string-shaped) `pass_rule`
   under `machine_constraints.pass_rule`, while K4's already-shipped
   `_materialize_refinement_run` places a NEW brief's `pass_rule` at the
   pre_registration.yaml TOP level. This kernel's lint/evaluator both read
   top-level `pre_registration.get("pass_rule")`, consistent with K4's
   already-established convention, not run_057's older ad-hoc nesting.
   Every legacy artifact (including run_057's) is unaffected either way —
   `evaluate_pass_rule_criteria()` sees no top-level `pass_rule` key on
   such a file and correctly returns `legacy_not_evaluable`.

### Test results

243 passed (224 pre-existing + 19 new in
`tests/test_k2_verdict_machinery.py`), 0 failed, 0 regressions
(`tests/test_k4_routing_registration.py`'s own 14 re-verified passing
unchanged). Full verbatim output is in this session's final report to the
operator, not duplicated here.

---

## K2 rider (2026-07-13): pair validation + holdout-path guard test

Operator arbitration on K2 Phase B: accepted overall, with **deviation 3
rejected in part** (pair coherence must be enforced, not left as a
documented gap) and **deviation 2 requiring a guard test** (a regression
fixture proving the holdout-bypass fix stays closed, not just a one-time
fix). Both addressed as a small rider, scoped to exactly two changes.

**Change 1 — pair validation (closes deviation 3).** Implemented in
`_dispatch_verdict_route()` (chosen over `_resolve_verdict_fields()`
because dispatch is where BOTH resolved fields are already in hand and is
the single funnel every caller goes through — `_resolve_verdict_fields`
by contrast is called separately at two sites and would need the same
check duplicated, working against R1's whole point). Validates
`(hypothesis_verdict, lineage_routing)` against the design's own §4
authority table before any routing happens:
```
valid_pairs = {
    ("kill", "terminate"), ("kill", "pivot"), ("kill", "escalate"),
    ("refine", "refine"), ("promote", None),
}
```
Anything else raises `ValueError` naming BOTH field values verbatim, never
dispatching on `lineage_routing` alone while silently ignoring an
incoherent `hypothesis_verdict` (or vice versa). Legacy single-field
fallback is unaffected: `_resolve_verdict_fields`'s pure-legacy path (no
artifact-declared `hypothesis_verdict`) always lands on one of these five
pairs by construction (the `_LEGACY_STATUS_TO_VERDICT_ROUTING` table only
ever produces these five), so no old-schema run is affected. The two real
ways an invalid pair could previously reach dispatch — a new-schema
artifact declaring an incoherent pair itself, or the circuit-breaker-fired
branch mixing an artifact-declared `hypothesis_verdict` with a
legacy-mapped `lineage_routing` (e.g. `hv="refine"` surviving while the
breaker forces `lr="pivot"`) — are both now caught.

Note one narrowing versus the Phase A design's own prose: §4's authority
list, read literally, never actually named `refine+pivot`/`refine+escalate`
as valid either (only `refine+refine` appears for `hypothesis_verdict:
refine`) — the Phase B implementation had been permissive of them by
omission (dispatching purely on `lineage_routing`). This rider closes that
gap exactly as the operator's instruction specifies: those two combinations
now raise, matching the design's authority table as written, not a broader
reading of it.

**Change 2 — holdout-path guard test (regression for deviation 2, no code
change).** `test_holdout_path_guard_campaign_review_continue_promote_
reaches_holdout_gate` drives `determine_post_campaign_review_route`'s
`rec == "continue"` (no `next_research_question`) branch with a fixture
`hypothesis_verdict: promote` and asserts the RETURNED stage is
`"holdout_evaluation"` (never the old `"completed_promoted"` bypass) AND
that `promotion_audit.yaml` was actually written to disk — checking the
scheduled stage and the side-effecting artifact, not merely the absence of
an exception, per the instruction's own emphasis.

**Fixtures added (13 new, all in `tests/test_k2_verdict_machinery.py`):**
one naming-both-values rejection test, a parametrized sweep of six other
incoherent pairs (`promote+pivot`, `refine+pivot`, `refine+escalate`,
`promote+refine`, `kill+None`, `bogus+refine`), five accept-tests (one per
valid pair, each driving the real sub-route to confirm the validation
gate doesn't block legitimate dispatch), and the one holdout-path guard
test above.

**Deviations:** none. Two test-authoring mistakes were caught and fixed
before this report (not shipped, not deviations from the design): an
early draft of the parametrized-rejection sweep incorrectly included
`kill+escalate` — one of the five VALID pairs — in the "must reject" list;
and the `promote+null` accept-test initially omitted the
`verdict_interpretation.yaml` fixture file `_write_promotion_audit` reads,
surfacing as a `FileNotFoundError` rather than a real code defect. Both
were test bugs, caught by the very first local run, and corrected before
reporting.

**Test results:** 256 passed (243 pre-existing + 13 new), 0 failed, 0
regressions.
