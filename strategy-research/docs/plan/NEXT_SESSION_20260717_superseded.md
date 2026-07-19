# NEXT_SESSION.md — updated 2026-07-17, post run_058 close-out (H-041 family closed)

Single entry point for the next session. Read in order, then work the queue.

## Read first, in order

1. [`DOC_INDEX.md`](DOC_INDEX.md) — doc map.
2. [`campaign_knowledge_base.yaml`](campaign_knowledge_base.yaml) —
   `fear_greed_contrarian_v2_validation_rejected` (H-041-C-v2, newest
   finding) and `fear_greed_contrarian_inconclusive` (H-041-C, its parent)
   — the F&G / H-041 family is now fully closed; read the newer entry's
   `exhausted_basis` in full, including its FACTUAL CORRECTION paragraph,
   before citing `runs/run_058/artifacts/validation_decision.yaml`
   anywhere.
3. [`PIPELINE_IMPROVEMENTS_20260712_v4.md`](PIPELINE_IMPROVEMENTS_20260712_v4.md)
   — the defect ledger. This session's v5 additions: **B7** evidence
   addendum (third in-the-wild demonstration — validation still does not
   read pre_registration.yaml, still misdescribes registrations it vetoes);
   **A10** (missing-deliverable stage failures get zero retries — watch-level,
   one occurrence); **A11 CLOSED** (SDK 0.2.82 result-misclassification —
   retry rider shipped, commit `9bf2a4c`); **B15** (no first-class
   registration→enqueue path — hand-edit was required for H-041-C-v2);
   **F10** (no raw LLM transcript preserved on stage crash).
4. [`SESSION_LOG.md`](SESSION_LOG.md)'s most recent entry — full narrative
   of the H-041-C-v2 registration through run_058's launch-to-close arc:
   the five walls hit (brief format, pass_rule copy-through, missing
   deliverable, queue-level resume, SDK misclassification) and each
   one's shipped cure, ending in the terminal validation rejection and
   this session's closure ruling.
5. [`RUNBOOK.md`](RUNBOOK.md) §3 (halt-table, now annotated with the SDK
   misclassification case) and §4 (resume-after-pause, now carrying the
   queue-level `paused:*` gate callout and the audit-log-overwrite
   limitation) before touching any paused run.

## State delta since the 2026-07-15 NEXT_SESSION.md (authoritative amendments)

- **K3 (B3+B10, protocol pinning): CLOSED.** Unchanged from the prior
  delta — carried forward as fact, not re-litigated this session.
- **B4: partially shipped.** The pass_rule copy-through rider landed
  (`_materialize_run`'s fresh_launch path now extracts
  `evaluation.pass_rule` into `pre_registration["pass_rule"]`, mirroring
  `_materialize_refinement_run`) — commit `63a6af9`. The rest of B4
  (mechanical copy-through/conformance-diff gate for ALL pre-registered
  fields across ALL stages) remains open.
- **H-041-C-v2 / run_058 arc: ENDED, completed_rejected.** The pipeline
  reached a terminal state at the `validation_gate` stage itself
  (`runs/run_058/artifacts/validation_decision.yaml`, status: reject) —
  it never reached `backtest_specification`, `signal_prescreen`,
  `protocol_execution`, or `verdict_interpreter`; no
  prescreen_result.yaml / protocol_result.yaml /
  pass_rule_evaluation.yaml / verdict_interpretation.yaml exist for this
  run.
- **The H-041 Fear & Greed contrarian family is CLOSED per the KB**, on
  the totality of evidence (the registration's own honesty clause + the
  KB's prior per-era IC sign-flip evidence + the validation rejection) —
  NOT on the registered mechanical pass_rule, which was never executed.
  A factual correction is recorded permanently on the KB finding
  (`fear_greed_contrarian_v2_validation_rejected`): the rejection
  rationale treated the 2024-2025 walk-forward era as "the test period";
  the pinned protocol's actual pass-gated windows were 2018-02 through
  2023-12-31 only, with 2024-2025 registered as diagnostic-only and
  explicitly excluded from gating. Any future reader citing
  validation_decision.yaml directly must weigh it with that error known.
- **SDK result-misclassification retry rider + RUNBOOK §4 cures:
  shipped**, commit `9bf2a4c`. Queue-level `paused:*`-gate documentation
  cure (RUNBOOK §4) also shipped this arc, commit `d26a437`.
- **Test suite: 301 passed, 0 failed** (`python -m pytest -q`, confirmed
  at this session's close).
- **58 runs on disk, all referenced/grandfathered, 0 unexpected orphans**
  (per the campaign runner's own reconcile check, most recently run
  2026-07-17).
- **Confirmed edges: still zero.** Unchanged from every prior delta.

## OPERATOR CHARTER (verbatim, binding)

The prime directive is a **PROFITABLE STRATEGY, not process.** The
operator has flagged over-focus on details and circling as the
campaign's main risk. Rules in force:

- Every manual review must retire itself into a mechanical gate — a new
  data type must **NEVER** trigger a full human review again once
  handled once.
- **Fix-with-the-workaround** — operational knowledge is documented in
  the same dispatch that pays for it, not deferred.
- **No new process work** unless it is on the background-mode critical
  path or demanded by a concrete intervention.
- **KPI, tracked from now on:** honest verdicts per week, and cost per
  verdict.

## Task queue (priority order)

### (1) GENERATOR SESSION — batch of live hypotheses
Fragment-pattern and trade-diagnostics ideation. The operator's stated
ambitions — regime-aware exit diagnostics → more reactive top-detection
features, ML-scored indicators, timeframe exploration — flow through the
existing registration machinery, which is now cheap per hypothesis
(pre_registration.yaml + brief authoring is a well-worn path after
H-041-C-v2).

### (2) First real-world exercise of prescreen → protocol → C7 evaluation on a LIVE batch hypothesis
These paths have still never run end-to-end on a live (non-diagnostic,
non-retrospective-arbitration) hypothesis. run_058 terminated at
validation_gate before reaching any of them.

### (3) Prune the remaining P0 (B4-rest+D3, B8, C6) by the intervention-cost test
**B7 is the lead candidate** — thrice-evidenced now (run_057 original,
one intervening occurrence, run_058 this arc), the only P0 item with
three independent in-the-wild demonstrations of the same defect.

### (4) Autonomy acceptance test once the pruned kernel clears
Unchanged in substance: full shadow campaign under background mode with
post-hoc human replay of every stage audit.

## Standing constraints

Carried forward from every prior session, plus this session's additions
(marked new below):

- Single-writer-per-state-store; audit agent read-only forever.
- Read-back verify after every write; corrections ship with sidecar
  rationale legible to context-poor readers (E3).
- Concealment-shaped tool content: verified harness templates -> one-line
  disclosure; everything else -> surfaced verbatim immediately.
- Background/nohup blocked until the P0 kernel clears — grounds: the
  ledger P0s, not security.
- Holdout (2026-H1 / `era_2026_holdout`) untouchable; never consumed in
  any session to date.
- Pre-registration supremacy: briefs outrank skill rulebooks; pass rules
  must carry a total verdict+routing mapping (B11) — no "routing
  decides" delegations.
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
- Dispatch precondition manifests must state an explicit expected-tree:
  a bare "git status must be clean" is insufficient — every dispatch's
  precondition should instead name the exact expected
  `git status --porcelain` output and the exact expected
  `git log --oneline -1` commit.
- Every terminal marker line carries its own step count: e.g. "END OF
  INSTRUCTIONS (9 steps)" — lets the executing agent self-check it
  received the complete prompt, not a truncated one.
- **Fix-with-the-workaround (new this session, elevated to charter
  status):** a documented procedure gap that costs the campaign time
  twice ships its documentation cure in the SAME commit as the
  workaround/rider that pays for it — never deferred to a later
  session.
- **Format precedents are chosen by consumption path (new this
  session):** e.g. briefs are authored as `.md` frontmatter, not `.yaml`,
  because `_parse_brief_frontmatter` is what actually consumes them —
  check what reads a file before choosing the format to author it in.
- **Per-value provenance citations in registration dispatches (new this
  session):** any numeric threshold, row count, or window boundary
  handed to an implementation agent for a registration must cite the
  file/command that produced it — the manifest row-count contradiction
  this arc only resolved cleanly because file forensics were run before
  the write, not after.
- **Every numeric measurement cites its command (new this session):**
  e.g. "301 passed (`python -m pytest -q`)" — not a bare number.
- **Write-capable agents never delegate (new this session, reaffirmed):**
  no sub-agent dispatch from within an implementation-agent task.
- **Any `.py`-touching commit runs the full suite (new this session,
  reaffirmed):** no partial/targeted test runs substituted for the full
  suite before a commit that touches orchestrator or workflow code.
