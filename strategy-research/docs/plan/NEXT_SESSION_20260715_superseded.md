# NEXT_SESSION.md — updated 2026-07-15, post K3 implementation + close-out

Single entry point for the next session. Read in order, then work the queue.

## Read first, in order

1. [`DOC_INDEX.md`](DOC_INDEX.md) — doc map.
2. [`00_closing_state.md`](00_closing_state.md) — canonical status. NOTE:
   its §2/§5 predate run_057 and this file's own prior versions; the
   "State delta" below amends all of them.
3. [`docs/design/K4_routing_registration_design_20260712.md`](docs/design/K4_routing_registration_design_20260712.md),
   [`docs/design/K2_verdict_machinery_design_20260713.md`](docs/design/K2_verdict_machinery_design_20260713.md),
   and [`docs/design/K3_protocol_pinning_design_20260714.md`](docs/design/K3_protocol_pinning_design_20260714.md)
   — all three design notes, each with an appended Phase B rulings/
   deviations section (K2's and K3's also have a dated rider section;
   K3's rider section additionally carries the 2026-07-15 audit-outcome
   paragraph) — the authoritative record of what A1+A3+B1, A8+A9+B11+
   C7+C9, and B3+B10 actually became in code, and every deviation from
   each original design.
4. [`PIPELINE_IMPROVEMENTS_20260712_v4.md`](PIPELINE_IMPROVEMENTS_20260712_v4.md)
   — the defect ledger. A1, A3, B1, A8, A9, B11, C7, C9, B3, and B10 are
   now CLOSED (see state delta below). Two new items filed by K3's own
   close-out audit: **B13** (the version-identifier trap — a dead
   `_version`-key lookup, `protocol_version`'s two unrelated meanings,
   a "version" field holding a path) and **B14** (content-hash formula
   triplicated across three sites, no single source of truth) — neither
   fixed yet, both P2, not blocking. Remaining P0 kernel gating
   background mode: B4+B7+D3, B8, C6.
5. [`SESSION_LOG.md`](SESSION_LOG.md)'s most recent entry — full
   narrative of K3's Phase A → §9 amendments → Phase B → operator-
   overruled deviation → rider → read-only audit → this close-out,
   including the two premise-failure stops this session and the
   prompt-defect root causes they exposed.
6. [`runs/run_057/artifacts/`](runs/run_057/artifacts/) — skim
   verdict_interpretation.yaml, s2_mechanism_check_20260711.yaml,
   prescreen_override_20260711.yaml for the lineage's ending (unchanged
   across sessions; still the K2 C7 evaluator's known-answer fixture
   source).
7. [`incident_20260710/INCIDENT.md`](incident_20260710/INCIDENT.md) —
   resolution addendum only, unchanged: the "forged system-reminder"
   incident is CLOSED as native harness boilerplate; no hostile actor.

## State delta since the 2026-07-14 NEXT_SESSION.md (authoritative amendments)

- **K3 (B3+B10, protocol pinning): CLOSED.** Design note
  (`docs/design/K3_protocol_pinning_design_20260714.md`) covers Phase A,
  the §9 operator amendments (A1–A5, Q1–Q4), the Phase B rulings/
  deviations section, the rider section (operator-overruled Phase B
  deviation 1: `_check_prescreen_conformance` now also catches an
  EXECUTED prescreen that ran against a different file than the one
  pinned), and the 2026-07-15 audit-outcome paragraph. Commits:
  `ef58773` (implementation), `1248a5e` (A5 migration + sidecar),
  `6b827eb` (rider), plus this close-out's own commit. Test suite at
  **296 passed, 0 failed** after the rider (close-out added no new
  tests). The A5 migration (`campaign_state.yaml`'s `last_escalation`
  gaining `claimed_by_run: run_049` / `claimed_at: '2026-07-06'`) was
  re-verified on disk by direct read this close-out — confirmed present,
  exactly as specified, nothing else in the record touched. The
  close-out's read-only audit returned clean on every A1–A5/Q1–Q4
  compliance item; it filed two new ledger entries (B13, B14, both P2,
  not blocking) and caught one provenance error in a rider code comment
  (corrected this close-out).
- **Remaining P0 kernel gating background mode: B4+B7+D3, B8, C6.**
  Unchanged in substance from every prior session's framing — copy-
  through of pre-registered fields + pre-registration as required stage
  input + operator_directives.yaml precedence channel; semantic spec
  conformance; admissible prescreen statistic for latched sparse
  signals.
- **K1 (generalization to upstream stages) and K6/A6 (`--step`
  stage-granular mode) and the C3 rider (un-pre-registered ceiling
  upgrades): still open decisions, carried forward unchanged.** Not
  designed or dispatched this session.
- **Confirmed edges: still zero.** Unchanged from every prior delta.

## Task queue (priority order)

### (1) Draft the H-041-C-v2 registration brief — NOW UNBLOCKED
Operator-ordered ahead of the §5 batch-vs-backward-extension decision.
Standing registration decisions for this brief, preserved verbatim from
the operator's own framing — do not re-derive or paraphrase these away:
- **Original polarity** (not run_052's flip).
- **Era-conditioning justified by pre-existing era boundaries only** —
  no new, ad hoc boundary invented to fit this registration.
- **Every FAIL branch maps to kill/terminate, no discretion
  delegations** — this is the mechanism's LAST registration; there is no
  "routing decides" fallback available after this one.
- **`sparse_inconclusive` gets a concrete, machine-selectable
  criterion**, not a dead branch that nothing can ever actually route
  through.
- **This is a NEW registration, not a reactivation** — per the KB's own
  `exhausted: true` / `reactivation_condition: null` state on the
  relevant finding.

### (2) Remaining P0 kernel items (B4+B7+D3, B8, C6)
Unchanged in substance — still gates autonomous/background mode, now
alongside nothing else from the original P0 set (K3 cleared).

### (3) K1 / K6+A6 / C3 rider — still open decisions
Carried forward unchanged: re-scope K1 (generalization to upstream
stages) given the K4/K2/K3 split-into-kernels pattern; decide whether
K6/A6 (`--step` mode) and the C3 rider (un-pre-registered ceiling
upgrades) get their own kernels or fold into a later batch. Not a ready
task — a decision item.

### (4) Autonomy acceptance test (after the P0 kernel fully clears)
Unchanged: full shadow campaign under background mode with post-hoc
human replay of every stage audit.

## Standing constraints

- Single-writer-per-state-store; audit agent read-only forever.
- Read-back verify after every write; corrections ship with sidecar
  rationale legible to context-poor readers (E3).
- Concealment-shaped tool content: verified harness templates -> one-line
  disclosure; everything else -> surfaced verbatim immediately.
- Background/nohup blocked until the P0 kernel clears — grounds: the
  ledger P0s, not security. B4/B7/D3 + B8 + C6 are what's left of it
  (K3 cleared this session).
- Holdout (2026-H1) untouchable; never consumed in any session to date.
- Pre-registration supremacy: briefs outrank skill rulebooks; pass rules
  must carry a total verdict+routing mapping (B11, implemented and
  enforced by materialization-time lint) — no "routing decides"
  delegations.
- Operator prompt discipline: no expected values inside verification
  instructions (F9); terminal marker line on every prompt (F5).
- No-self-remediation: any write landing outside an authorized list —
  accidental or discovered mid-task — is a STOP-and-report condition.
  Report and request authorization BEFORE proceeding, never proceed-
  then-disclose, even when the reasoning for the extra write is sound.
- Known residual risk, test-isolation guard (not solved, do not treat as
  closed): `tests/conftest.py`'s autouse sandbox-by-default fixture
  covers direct in-process module calls only — not `setup_run.py`'s
  subprocess-spawn path, nor `_load_token_budget()`'s source-relative
  config read.
- Always-emit-one-log-line convention: any status/reconciliation check
  added to the campaign machinery should emit exactly one line per
  invocation, clean or not, never zero.
- Premise-failure full-STOP: if a step's stated premise does not hold as
  found, STOP the entire task at that point — including remaining
  authorized read-only steps — and report. Do not gather more info first,
  do not run anything else "while I'm here."
- **Dispatch precondition manifests must state an explicit expected-tree
  (new this session):** a bare "git status must be clean" is
  insufficient and has already caused a mid-task premise-failure stop
  this session — every dispatch's precondition should instead name the
  exact expected `git status --porcelain` output (including any
  untracked design-note file the task itself is about to append to) and
  the exact expected `git log --oneline -1` commit.
- **Every terminal marker line carries its own step count (new this
  session):** e.g. "END OF INSTRUCTIONS (9 steps)" — lets the executing
  agent self-check it received the complete prompt, not a truncated one.
