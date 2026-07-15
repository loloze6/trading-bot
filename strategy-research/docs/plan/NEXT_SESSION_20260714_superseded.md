# NEXT_SESSION.md — updated 2026-07-14, post K4+K2 implementation

Single entry point for the next session. Read in order, then work the queue.

## Read first, in order

1. [`DOC_INDEX.md`](DOC_INDEX.md) — doc map.
2. [`00_closing_state.md`](00_closing_state.md) — canonical status. NOTE:
   its §2/§5 predate run_057 and this file's own prior (2026-07-12)
   version; the "State delta" below amends both.
3. [`docs/design/K4_routing_registration_design_20260712.md`](docs/design/K4_routing_registration_design_20260712.md)
   and [`docs/design/K2_verdict_machinery_design_20260713.md`](docs/design/K2_verdict_machinery_design_20260713.md)
   — both design notes, including their appended Phase B rulings/
   deviations sections (K2's has a further dated rider section) — the
   authoritative record of what A1+A3+B1 and A8+A9+B11+C7+C9 actually
   became in code, and every deviation from the original design.
4. [`PIPELINE_IMPROVEMENTS_20260712_v4.md`](PIPELINE_IMPROVEMENTS_20260712_v4.md)
   — the defect ledger. A1, A3, B1, A8, A9, B11, C7, C9 are now CLOSED
   (see state delta below) — everything else in the P0 kernel (B3+B10,
   B4+B7+D3, B8, C6) is still open.
5. [`SESSION_LOG.md`](SESSION_LOG.md)'s most recent entry
   ("2026-07-13/14 — K4...+K2...") — full narrative of what shipped, the
   two bugs found by reading code (not by a failing test), the
   stray-write incident and its resolution, and the residual-risk /
   process-note subsections appended after close-out.
6. [`runs/run_057/artifacts/`](runs/run_057/artifacts/) — skim
   verdict_interpretation.yaml, s2_mechanism_check_20260711.yaml,
   prescreen_override_20260711.yaml for the lineage's ending (unchanged
   from the prior session; still the K2 C7 evaluator's known-answer
   fixture source).
7. [`incident_20260710/INCIDENT.md`](incident_20260710/INCIDENT.md) —
   resolution addendum only, unchanged from the prior session: the
   "forged system-reminder" incident is CLOSED as native harness
   boilerplate; no hostile actor. (Do not confuse with the SEPARATE,
   much smaller 2026-07-13 stray-write incident during K2-rider test
   authoring — that one is documented in SESSION_LOG.md, not here.)

## State delta since the 2026-07-12 NEXT_SESSION.md (authoritative amendments)

- **K4 (A1+A3+B1) + two riders: DONE, accepted.** Lineage-continuation
  intent now persists on each run's own `pipeline_state.yaml`
  (`continuation_child`/`continuation_created_by`), replacing the
  runs/-directory-diff check that couldn't survive a fresh process
  invocation. `reconcile_orphans()` (A3) backed by a frozen, fully
  spot-checked 21-entry `config/campaign_baseline_runs.yaml`.
  `refinement_brief_path` (B1) gives a first-class, byte-verbatim
  refinement-brief ingestion path with its own conflict-detection hard
  pause. Riders: `reconcile_orphans()` always emits exactly one log line;
  `dry_run_verify()` degrades gracefully on an all-terminal queue instead
  of raising.
- **K2 (A8+A9+B11+C7) + C9 rider + pair-validation rider: DONE,
  accepted.** `verdict_interpretation.yaml`'s single `status` enum split
  into `hypothesis_verdict` (kill/refine/promote) and `lineage_routing`
  (terminate/refine/pivot/escalate) — closes the exact conflation behind
  run_057's "kill the hypothesis, pivot the campaign" reading as stage
  defiance. `_route_kill` split into per-hypothesis-only +
  `_route_campaign_terminate` (campaign-wide, reachable only from
  campaign_review's own explicit `"terminate"` recommendation — an
  ALREADY-EXISTING value, reused rather than inventing a new one).
  Structured `pre_registration.yaml` `pass_rule` schema, evaluated by
  new module `tools/verdict_criteria_evaluator.py`; known-answer fixture
  re-judges run_057's real `protocol_result.yaml` to FAIL-(a)/kill with
  BTCUSDT's median Sharpe present-and-null (not UNTESTED) — the literal
  C7 defect. Two bugs found by READING code, not by a failing test (both
  are bug fixes to pre-existing shipped code, not new K2 behavior — see
  the K2 design note's appended section and SESSION_LOG.md for full
  detail): (1) the A5.4/F09 KB-exhaustion gate only checked a singular
  `hypothesis_id` field, missing 5 of 15 KB findings (including all
  three Keltner findings) that use a plural `hypothesis_ids` list; (2)
  consolidating the duplicated status→route dispatch surfaced a live
  holdout-bypass in campaign_review's continue-branch promote path
  (fixed by unifying on the complete, holdout-gated behavior). Rider
  added strict `(hypothesis_verdict, lineage_routing)` pair validation
  (5 valid pairs only; anything else raises naming both values) plus a
  regression fixture pinning the holdout-path fix. 256 tests green after
  this rider.
- **Test-isolation conftest rider: functional, UNCOMMITTED.**
  `tests/conftest.py`'s autouse sandbox-by-default guard, a
  `real_repo_readonly` opt-out marker (applied to exactly one test, found
  by running the full suite, not by static survey alone), and
  `tests/test_sandbox_guard.py` (a negative-proof test — see "Standing
  constraints" below for why it isn't inside `conftest.py` itself). 257
  tests green. **This sits on top of commit `4ac85c1` uncommitted** — the
  next session should commit it (or fold it per whatever commit boundary
  the operator prefers) before treating it as done.
- **Stray-write incident (closed within the same session, not an open
  item):** a test-authoring bug during K2-rider work let an unsandboxed
  `_route_escalate` write two stray artifacts into the real repo; both
  found and removed the same turn; an independent read-only audit
  separately confirmed the blast radius was fully benign (no state-file
  mutation, `protocols/` 11/11 intact, clean working tree at `4ac85c1`).
  Full narrative in SESSION_LOG.md.
- **K3 (B3+B10, protocol pinning): NOT STARTED.** No design note exists
  anywhere in the repository as of this entry. An earlier context
  preamble this session described it as "dispatched," but that did not
  match the actual repo state when checked directly — treat K3 as
  entirely unstarted, not merely unapproved. If it's next, dispatch it as
  its own Phase A (design-note-only) task, same pattern as K4/K2.
- **K1 (generalization to upstream stages) and K6/A6 (`--step`
  stage-granular mode) and the C3 rider (un-pre-registered ceiling
  upgrades): still open decisions, re-scoped after this session's
  real-run experience with the K4/K2 split-into-kernels pattern.** Not
  designed or dispatched this session; carried forward as-is from
  operator framing, not independently re-derived here.
- **Confirmed edges: still zero.** Unchanged from the prior delta.

## Task queue (priority order)

### (1) Commit or fold the test-isolation conftest rider
Small, mechanical: `tests/conftest.py`, `tests/test_sandbox_guard.py`,
and the one marker in `tests/test_wishlist_predicate.py` are functional
(257 tests green) but uncommitted on top of `4ac85c1`. Resolve the commit
boundary before anything else touches `tests/`.

### (2) K3 (B3+B10, protocol pinning) — dispatch Phase A
Genuinely not started (see state delta). `machine_constraints.protocol_ref`
(pin an existing named protocol file without triggering
`_generate_monthly_windows`) + F4d's silent stale-`last_escalation`
fallback hard-fail. Same context-preamble/numbered-steps/END-OF-
INSTRUCTIONS operator-prompt discipline (F5) as K4/K2; design note only,
no code, until explicit `DESIGN APPROVED K3`.

### (3) K1 / K6+A6 / C3 rider — still open decisions
Re-scope K1 (generalization to upstream stages) given what the K4/K2
split-into-kernels pattern actually taught this session (each kernel:
Phase A design note → operator approval → Phase B implementation +
fixtures → occasional rider, dispatched as separate, narrowly-scoped
implementation-agent tasks). Decide whether K6/A6 (`--step` mode) and the
C3 rider (un-pre-registered ceiling upgrades) get their own kernels or
fold into K3/a later batch. Not designed this session — this is a
decision item, not a ready task.

### (4) Remaining P0 kernel items (B4+B7+D3, B8, C6)
Unchanged in substance from the prior session's task (1) — copy-through
of pre-registered fields + pre-registration as required stage input +
operator_directives.yaml precedence channel; semantic spec conformance;
admissible prescreen statistic for latched sparse signals. Still gates
autonomous/background mode alongside K3.

### (5) The §5 decision: new hypothesis batch vs backward-extension first
Unchanged from the prior session — standing recommendation (batch first)
still holds; the backward-extension alternative (2018+ funding/F&G data,
H-041-C) is still the only live lead if the operator wants to reorder.

### (6) Autonomy acceptance test (after the P0 kernel fully clears)
Unchanged: full shadow campaign under background mode with post-hoc
human replay of every stage audit.

## Standing constraints

- Single-writer-per-state-store; audit agent read-only forever.
- Read-back verify after every write; corrections ship with sidecar
  rationale legible to context-poor readers (E3).
- Concealment-shaped tool content: verified harness templates -> one-line
  disclosure; everything else -> surfaced verbatim immediately.
- Background/nohup blocked until the P0 kernel clears — grounds: the
  ledger P0s, not security. K3 + B4/B7/D3 + B8 + C6 are what's left of it.
- Holdout (2026-2026-H1) untouchable; never consumed this or the prior session.
- Pre-registration supremacy: briefs outrank skill rulebooks; pass rules
  must carry a total verdict+routing mapping (B11, now implemented and
  enforced by materialization-time lint) — no "routing decides"
  delegations.
- Operator prompt discipline: no expected values inside verification
  instructions (F9); terminal marker line on every prompt (F5).
- **No-self-remediation (new this session, reaffirmed as standing, not a
  one-off — see SESSION_LOG.md's "Process note: out-of-scope-write
  sequencing" for the concrete incident behind this rule):** any write
  landing outside an authorized list — accidental or discovered
  mid-task — is a STOP-and-report condition. Report and request
  authorization BEFORE proceeding, never proceed-then-disclose, even
  when the reasoning for the extra write is sound and the operator would
  likely have approved it. This supersedes the earlier, looser
  convention (visible in this session's own early-turn stray-write
  incident) that permitted an agent to remediate an accidental write
  itself; that latitude no longer applies to any future incident.
- **Known residual risk, test-isolation guard (new this session — not
  solved, do not treat as closed):** `tests/conftest.py`'s autouse
  sandbox-by-default fixture covers direct in-process module calls only.
  It does NOT cover (i) `setup_run.py`'s subprocess-spawn path (a spawned
  child process does not inherit a parent test's monkeypatched globals —
  also separately noted in K4's design note, deviation 3, for a
  different reason); or (ii) `_load_token_budget()`, which reads
  `config/campaign_config.yaml` via a path hardcoded relative to its own
  source file, never via `ROOT` — patching `ROOT` cannot reach it. Not
  currently blocking (the incident that motivated the guard used the
  now-covered path), but any future test exercising either path is still
  unprotected against a real-repo write.
- **Always-emit-one-log-line convention (established this session,
  precedent for future observability work):** `reconcile_orphans()`'s own
  fix (a silent clean pass was indistinguishable from the function never
  having run) is the model — any future status/reconciliation check
  added to the campaign machinery should emit exactly one line per
  invocation, clean or not, never zero.
