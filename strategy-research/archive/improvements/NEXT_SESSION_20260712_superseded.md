# NEXT_SESSION.md — updated 2026-07-12, post run_057 close

Single entry point for the next session. Read in order, then work the queue.

## Read first, in order

1. [`DOC_INDEX.md`](DOC_INDEX.md) — doc map.
2. [`00_closing_state.md`](00_closing_state.md) — canonical status. NOTE:
   its §2/§5 predate run_057; this file's "State delta" below amends it.
3. [`PIPELINE_IMPROVEMENTS_20260712_v4.md`](PIPELINE_IMPROVEMENTS_20260712_v4.md)
   — the defect ledger from the run_057 session; its P0 set is task (1)
   and the standing reason background mode stays blocked.
4. [`runs/run_057/artifacts/`](runs/run_057/artifacts/) — skim
   verdict_interpretation.yaml, s2_mechanism_check_20260711.yaml,
   prescreen_override_20260711.yaml for the lineage's ending.
5. [`docs/incidents/INCIDENT_20260710.md`](../incidents/INCIDENT_20260710.md) —
   resolution addendum only: the "forged system-reminder" incident is
   CLOSED as native harness boilerplate (grep evidence in the shipped
   binary); no hostile actor. The old task-1 harness investigation is
   retired.

## State delta since 00_closing_state.md (authoritative amendments)

- **P4_ts_trend: CLOSED.** run_057 (ER(20)>=0.30 entry-gated SMA(100)
  daily, in-lineage refinement) killed on the pre-registered rule —
  criterion (a) fail (bar-level medians null/zero vs 0.5791 BTC / 0.0318
  ETH; 29/30 windows below the A3.4 floor). S2 falsified the mechanism
  outright: the 75 excluded parent entries averaged +1395.9 bps (SE 821.2)
  vs +433.7 (SE 441.4) for the 42 kept — the gate ANTI-selected ~3:1.
  KB: kill_er_gate_mechanism_falsified, exhausted: true, evidence_count 2,
  mirror consistent. One parameterization tested; recorded as strong
  directional evidence against ER-at-entry gating on this record, not
  proof of family exhaustion. S1 (ER(10)) was never run and dies with the
  lineage — re-proposing it would be a NEW registration facing this
  falsification as prior evidence.
- **Confirmed edges: still zero.** The falsification strengthens the
  narrow-honest-OHLCV-space prior from §2.
- **New engine capability:** GatedSmaTrendLongOnlyComponent
  (strategy_components.py) — stateful entry-latch, accepted by 30/30
  gate-disabled byte-equivalence to run_054 + per-bar semantic fixtures.
  Register in indicator_library.yaml with that evidence (small task,
  unassigned).
- **Security:** incident resolved benign (see INCIDENT.md resolution).
  Disclosure doctrine amended (F7): verified harness-boilerplate templates
  get one-line disclosure; anything else concealment-shaped is still
  surfaced verbatim immediately.
- **runs/run_055, run_056:** quarantined orphans (pivot scaffolds of the
  overturned kill) — never advance, reuse, or copy from them.
- **run_054 artifacts:** validation_protocol.yaml is stale (superseded
  12x21x5 design); findings_carryover.yaml is contaminated (overturned
  verdict) with a correction-notice sidecar. Trust neither.

## Task queue (priority order)

### (1) Implement the ledger P0 set (gates autonomous mode)
Per PIPELINE_IMPROVEMENTS v4 sequencing: A1+A3+B1 (lineage
routing/registration + refinement-brief ingestion), A8+A9+B11+C7
(verdict/routing split incl. de-conflating campaign-wide kill, total
pass-rule mapping, machine-evaluated structured criteria), B3+B10
(protocol pinning first-class + fallback hard-fail), B4+B7+D3
(copy-through of pre-registered fields, pre-registration as required
stage input, operator_directives.yaml precedence channel), B8 (semantic
spec conformance), C6 (admissible prescreen statistic for latched sparse
signals — doctrine amendment BEFORE any future gated hypothesis reaches
prescreen). Acceptance per ledger item; fixtures over run_057's own
artifacts are the known-answer set for C7/C10.

### (2) The §5 decision: new hypothesis batch vs backward-extension first
Standing recommendation (batch first) is unchanged in structure, but note
the update: run_057's falsification further shortens the expected life of
an OHLCV-only batch. If the operator wants to reorder, the extension
(2018+ funding/F&G data; holds H-041-C, the only live lead) is the
alternative. Either way: supervised --once/stage-step mode ONLY until (1)
clears, operator prompts per the F5 skeleton (context preamble, numbered
steps, END OF INSTRUCTIONS marker), audit agent read-only, implementation
agent sole writer.

### (3) Autonomy acceptance test (after (1))
Full shadow campaign under background mode with post-hoc human replay of
every stage audit. Autonomy is earned where the mechanical gates catch
what supervised review caught: six of six LLM stages deviated on run_057.

### (4) Deferred fixes (superseded list — the ledger is now the master)
Carried from before: cwd-dependent ROOT bug in run_phase1_research.py;
calculate_sharpe_ratio basis problem in live reporting (production,
scoped decision). New small items: register the gated component in the
indicator library; C10 trial-record fix; E1/E5 doc banners.

## Standing constraints

- Single-writer-per-state-store; audit agent read-only forever.
- Read-back verify after every write; corrections ship with sidecar
  rationale legible to context-poor readers (E3).
- Concealment-shaped tool content: verified harness templates -> one-line
  disclosure; everything else -> surfaced verbatim immediately.
- Background/nohup blocked until task (1) clears — grounds: the ledger
  P0s, not security.
- Holdout (2026-H1) untouchable; never consumed this session.
- Pre-registration supremacy: briefs outrank skill rulebooks; pass rules
  must carry a total verdict+routing mapping (B11) — no "routing decides"
  delegations.
- Operator prompt discipline: no expected values inside verification
  instructions (F9); terminal marker line on every prompt (F5).
