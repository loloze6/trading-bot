# Pipeline Improvement Ledger — v4 FINAL for this session, 2026-07-12 (v1 07-10; v2 07-11 midday; v3 07-11 evening)

Source: the run_057 (regime-gated SMA refinement) session. Every item below
was found live, on evidence, while stepping one run through the pipeline
under interactive `--once`/direct-stage mode. Purpose: this ledger exists so
the NEXT hundreds of runs go smoothly — none of these items should be fixed
casually mid-lineage; they are queued work with acceptance criteria in this
repo's own culture (known-answer fixtures for code, output audits for
prompts/skills, read-back verification for state).

Priority: P0 = blocks or silently corrupts autonomous operation;
P1 = will bite the next run that exercises the path; P2 = hygiene/docs.

---

## A. Orchestrator routing & state machine

### A1. Refine-lineage continuation is structurally broken (P0)
- **Symptom:** with run_054 at `pending_stage: completed_refined`,
  `process_once()` would have silently finalized P4_ts_trend as
  `done/completed_refined` without launching the refinement or reading the
  new brief.
- **Root cause (two-part):** `completed_refined` missing from
  `_LINEAGE_CONTINUATION_STAGES`; AND even if added, `lineage_new_runs` is
  computed from a runs/-directory diff bracketing the *same* `run_loop()`
  invocation — a continuation across separate invocations always sees an
  empty list and falls through to `done`.
- **Fix:** persist lineage-continuation intent in state (e.g. the routing
  functions record `continuation_child: <run_id>` in `pipeline_state.yaml`
  or `campaign_state.yaml`), and have `process_once()` read that instead of
  the in-memory dir diff. Add `completed_refined` to the tuple as part of
  the same change.
- **Acceptance:** fixture campaign where a refine verdict on run N produces
  run N+1 launched by the NEXT `--once` invocation (fresh process), queue
  entry still `in_progress`, child appended to `run_ids`.

### A2. `_route_refine` and `_route_pivot` both return "completed_refined" (P1)
- **Symptom:** run_054's `pending_stage` could not tell us whether refine or
  pivot had fired; had to be reconstructed from artifact forensics.
- **Fix:** distinct terminal strings (`completed_refined` /
  `completed_pivoted`), plus a `route_taken` field in `pipeline_state.yaml`.
- **Acceptance:** fixture asserting each route writes its own distinguishable
  state; grep of historical runs documented as pre-fix.

### A3. Pivot/refine-scaffolded runs are untracked orphans (P0)
- **Symptom:** run_055/run_056 scaffolded by `_route_pivot` on 2026-07-09,
  registered nowhere (queue, campaign_state), discovered by accident; both
  carried refuted kill-verdict carryover.
- **Fix:** every scaffold created by a routing function is registered
  atomically (queue entry or `campaign_state` lineage record) in the same
  operation that creates the directory. Add a reconciler check: any
  `runs/<id>` not referenced by queue/campaign_state is flagged loudly.
- **Acceptance:** fixture: kill the process between scaffold and registration
  → reconciler flags the orphan on next start.

### A4. `quarantined_orphan` should be a recognized status (P2)
- **Symptom:** we hand-set `status: quarantined_orphan` + `ORPHANED_README.md`
  on 055/056; nothing in tooling knows this convention.
- **Fix:** selectors/reconcilers/`_next_run_id` explicitly skip-and-report
  this status; convention documented in RUNBOOK.
- **Acceptance:** fixture: quarantined run is never selected, never renumbered
  over, appears in status output as quarantined.

### A5. Silent queue finalization (P1)
- **Symptom:** the A1 fall-through would have marked the entry `done` with no
  operator-visible decision point.
- **Fix:** finalizing a lineage (any transition to `done`) writes a loud,
  distinct log line and, while the harness investigation is open, is a
  hard-pause class rather than automatic.
- **Acceptance:** output audit of `campaign_log.md` on a fixture campaign.

### A6. `--once` is queue-granular, not stage-granular (P0 for supervised mode)
- **Symptom:** `--once` on a run at `hypothesis_generation` would have swept
  the ENTIRE pipeline including the real backtest in one call; RUNBOOK's
  "exactly one step" invites the misreading. We fell back to direct stage
  invocation, which bypasses the token-budget breaker and queue bookkeeping.
- **Fix:** add `--step` (run exactly one stage, then return) as a first-class
  mode of `run_loop`, budget-accounted; fix RUNBOOK wording either way.
- **Acceptance:** fixture: `--step` from `hypothesis_generation` leaves
  `pending_stage: innovation_expansion`, budget counters incremented, nothing
  else run.

### A7. Direct stage invocation has no budget accounting (P1)
- **Symptom:** our standalone stage calls this session ran outside the
  between-stage token-budget breaker.
- **Fix:** folded into A6 (`--step` uses the normal accounting path).

## B. Briefs, pre-registration & conformance machinery

### B1. No supported path for a refinement brief to reach the orchestrator (P0)
- **Symptom:** the entire mid-session detour. `brief_path` is only consumed on
  fresh launch (empty `run_ids`); repointing it on an in-progress entry does
  nothing; `dry_run_verify` rejects a YAML refinement brief on format; the
  only precedent was hand-editing `campaign_review.yaml`.
- **Fix:** first-class refinement-brief mechanism: a queue entry field (e.g.
  `refinement_brief_path`) consumed by the lineage-continuation path (A1),
  materialized via `setup_run` + `_materialize_run` with the brief installed
  byte-identical (custody rule), supporting the refinement-brief YAML schema
  (lineage, gate_definition, pass_rule, machine_constraints) — not only the
  .md-frontmatter schema.
- **Acceptance:** fixture: user-delivered YAML refinement brief on an
  in-progress entry → next invocation scaffolds the child with
  `user_brief_verbatim.yaml` checksum-identical and `pre_registration.yaml`
  populated.

### B2. `dry_run_verify` does not mirror the real launch branches (P1)
- **Symptom:** dry run failed on frontmatter parsing for an entry whose real
  path never reads the brief at all; we launched under a documented waiver.
- **Fix:** dry run branches exactly as `process_once()` does (fresh vs
  continuation), validating what the real path would actually consume.
- **Acceptance:** fixture pairs (fresh entry / in-progress entry) both pass
  dry run iff the real path would proceed.

### B3. CLOSED — No mechanism to PIN an existing named protocol file (P0)
- **Symptom:** `machine_constraints.protocol` triggers
  `_ensure_protocol_from_constraints` → `_generate_monthly_windows`, which
  would have silently REPLACED the pre-registered
  `protocols/ts_trend_daily_v1.json` (15 semi-annual windows) with fresh
  monthly windows — the exact zero-trades-vs-warmup failure mode this
  campaign already hit once. We left the key unset and accepted human
  enforcement at the backtest-spec checkpoint.
- **Fix:** `machine_constraints.protocol_ref: <path>` — pins an existing
  file, F4d conformance-gate enforces the executed protocol matches it,
  generation path untouched.
- **Acceptance:** fixture: run with `protocol_ref` executes exactly those
  windows; a mismatched protocol file hard-fails conformance.
- **Resolution (2026-07-15, K3 kernel):** `_ensure_protocol_ref_pinned` +
  `_resolve_protocol_path` (consolidated resolver) ship the pin mechanism;
  `_check_prescreen_conformance` extended (rider) to hard-catch an executed
  prescreen that ran against a different file than the one pinned, plus an
  optional content-hash check (§5). Registration-time lint
  (`_lint_machine_constraints_protocol_selection`) and a runtime
  mutual-exclusion guard both reject `protocol`+`protocol_ref` set
  together. Audited clean 2026-07-15 (see two new findings below, B13/B14).
  Full design: `engineering/improvements/done/design_and_docs/K3_protocol_pinning_design_20260714.md` (§9
  amendments, Phase B rulings, rider section). Commits: `ef58773`
  (implementation), `1248a5e` (A5 migration), `6b827eb` (rider).

### B4. Pre-registered text is paraphrased by LLM stages (P0, systemic)
- **Symptom:** innovation_expansion emitted two DIFFERENT paraphrases of
  `signal_concept`, dropping "no deferred entry", the warmed-up-series/
  no-lookahead clause, and "bar-close" precision — execution semantics that
  would have propagated into the strategy config. Same defect family as the
  "linguistic inflation" that carried the fake Keltner edge.
- **Update (2026-07-11):** upgraded from risk to demonstrated near-miss —
  downstream stages read ONLY expanded_hypothesis_card.yaml (never the
  correct hypothesis_card.yaml), so the paraphrase would have been the
  operative spec for the whole pipeline; the hand-correction was the only
  firewall. The validation stage then independently demonstrated the same
  class at larger scale (see B7/D2).
- **Fix (mechanical, not exhortative):** designate pre-registered fields as
  copy-through: the harness copies them byte-wise from the source artifact
  into stage outputs (stages never re-type them), OR a post-stage
  conformance diff gate hard-fails any stage output whose pre-registered
  fields differ from `user_brief_verbatim.yaml` / parent card.
- **Acceptance:** fixture: a stage output with one character changed in a
  pre-registered field is rejected mechanically.

### B5. Single-variant intent has no first-class representation (P1)
- **Symptom:** pass-through hinged on a magic phrase ("single variant") in a
  `constraints` field that our materialization path didn't know existed; we
  patched the brief after the fact.
- **Fix:** `variant_policy: pass_through | expand` as a structured brief /
  machine_constraints field, read by the stage handoff builder; magic-phrase
  detection kept only as backstop.
- **Acceptance:** output audit: brief with `variant_policy: pass_through`
  yields exactly one variant with no skill-text archaeology required.

### B6. `pre_registration.yaml` hypothesis_id placeholder (P2)
- **Symptom:** `hypothesis_id: run_057-initial` template value; confirmed
  cosmetic (all consumers read `verdict_interpretation.yaml`), but it is
  exactly the kind of unexplained mismatch that burns a future audit turn.
- **Fix:** `_materialize_run` accepts/propagates the real hypothesis_id, or
  the field is removed from the template.

## C. Power & validation machinery

### C1. LLM-authored power prose diverges from the machine gate (P0)
- **Symptom (three-way divergence on one card):** run_057's card registered
  `activation_rate: 0.04` (mislabeled entries-per-bar; the code consumes
  bars-in-position, parent precedent 0.45), prose described an n_eff≈70-87 /
  mde≈0.30-0.33 calculation the machine never runs, and the machine would
  have passed it anyway (mde 0.068 < a self-upgraded ceiling 0.08) — a pass
  built on two errors cancelling. Parent run_054's card prose divided by 24
  (1h block size) on a DAILY hypothesis — the prose/machine mismatch is
  systemic, not a one-off.
- **Fix:** machine writes the derived power block. LLM supplies only raw
  inputs with schema-documented units (`activation_rate` = fraction of bars
  in position, stated in the field name or schema doc);
  `_run_a86_power_check` computes and WRITES n_eff/mde/verdict into the card
  or a sibling artifact; prose never carries load.
- **Acceptance:** known-answer fixture through the real formula; schema doc
  for every power_parameters field; discrepancy logger retired for derived
  fields (nothing left to disagree).

### C2. `_extract_llm_reported_power` regex fragility (P1; subsumed by C1)
- **Symptom:** `n_eff = 0.25 * 2715 * 2 / 1 = 1357.5` → regex captured 0.25
  (first number after first `=`) → guaranteed false-positive discrepancy;
  "mde" not recognized as `min_detectable_ic` → silently unchecked. We fixed
  it by phrasing the prose FOR the regex — backwards.
- **Fix:** C1 removes the need. Interim: capture the LAST number; accept
  "mde" alias.
- **Acceptance:** fixture strings including the multi-equals form.

### C3. Un-pre-registered ceiling upgrades (P1)
- **Symptom:** child card upgraded `plausible_ic_upper` 0.06 → 0.08 on a
  "custom filter reduces crowding" narrative — a self-serving nudge that
  makes power checks pass, exactly where motivated reasoning hides.
- **Fix:** for in-lineage refinements, `plausible_ic_upper` defaults to the
  parent's value; any change requires an explicit brief/machine_constraints
  entry (pre-registered), else hard-fail at validation.
- **Acceptance:** fixture: child card with silently-raised ceiling is
  rejected; with brief-registered change, accepted.

### C4. Rule-citation confabulation (P1)
- **Symptom:** card cited "A3.6, n_episodes >= 8 per window" — label wrong
  (real rule is A8.5.1a-spec rule 3), qualifier invented (pooled, not
  per-window). Plausible-looking fake citations survive until someone quotes
  the source verbatim.
- **Fix:** machine-readable rule index (id → verbatim text → source line);
  a lint step resolves every `A\d`-style citation in stage outputs against
  it and fails on unknown ids; skills instructed to cite by id only.
- **Acceptance:** fixture output with an invented rule id fails the lint.

## D. Skills & prompt text

### D1. innovation-expansion pass-through vs Improvements 01/04 (P1)
- **Symptom:** line-138 pass-through carve-out vs unconditional Improvement
  01 (non-price variant required) and Improvement 04 (diversity) — no stated
  precedence; the literal reading of 04 self-defeatingly rejects any
  single-variant output. Only caught because we were stepping with
  stop-on-ambiguity; a nohup campaign lets the stage LLM coin-flip it.
- **Fix:** one sentence in SKILL.md: "In pass-through mode, Improvements 01
  and 04 do not apply." Operator ruling of 2026-07-10 is the content;
  accepted by output audit per A1.4 (never diff review).

### D2. Skill-vs-brief precedence, generally (P2)
- **Symptom:** D1 is one instance of a class: stage personas with
  unconditional "must" rules that can conflict with a pre-registered brief.
- **Fix:** standing precedence line in every stage skill: pre-registered
  brief constraints outrank skill defaults; conflicts are a pause, not a
  judgment call.

## E. Documentation & artifacts

### E1. Stale `validation_protocol.yaml` in run_054 (P1)
- **Symptom:** still carries the superseded 12x21x5 monthly design (replaced
  2026-07-08 by 15 semi-annual windows in `ts_trend_daily_v1.json`); misled
  a read-only audit into a false window-definition, resolved only by
  bars.csv arbitration.
- **Fix:** correct or banner the file ("SUPERSEDED by ts_trend_daily_v1.json
  2026-07-08"); process fix: protocol redesigns update or banner every
  artifact that restates window structure.

### E2. RUNBOOK `--once` wording (P2)
- Folded into A6: "exactly one launch/continue/advance step" must say
  queue-level, and document `--step` when it exists.

### E3. Corrections must be legible to context-poor readers (P1, doctrine)
- **Symptom (positive and negative):** the incident's root cause was a
  correction that didn't carry its own arithmetic, so a second agent
  "fixed" it back. This session deliberately left sidecars
  (`findings_carryover_CORRECTION_NOTICE.md`, `ORPHANED_README.md`,
  `operator_correction_20260710` in innovation_notes) and avoided planting a
  known-false-positive discrepancy log entry.
- **Fix:** convention: every hand-correction to a decision artifact ships
  with an adjacent rationale + the arithmetic or citation that justifies it;
  generalize the `kb_state_hash` staleness signal from detector_wishlist to
  KB findings and campaign_review entries.

### E4. Carryover vs KB dual memory (P1)
- **Symptom:** doctrine says the KB, not `findings_carryover.yaml`, is
  cross-run memory — yet routing functions copy carryover forward, and
  run_054's carryover still narrates the OVERTURNED kill verdict (refuted
  -1.78/-1.54, `next_altitude: pivot`, the superseded 1h-detector gating)
  with no invalidation when the KB was corrected. run_057 launched clean by
  operator decision.
- **Fix:** either derive carryover FROM the KB at scaffold time (single
  source of truth), or version-stamp carryover against the KB entry it
  summarizes and refuse to copy a stale one.
- **Acceptance:** fixture: correct a KB finding → the stale carryover is
  refused/flagged at next scaffold.

## F. Multi-agent & security operations (doctrine, mostly in force already)

### F1. Context preamble on every task prompt (in force)
- Every prompt to an agent opens with "state changed outside your view: ..."
  — a fresh agent re-discovering our own work as tampering is how the
  original KB revert started. Candidate mechanization: a session-state
  digest file agents read first.

### F2. Role split = single-writer doctrine (in force)
- Audit agent is read-only forever; implementation agent is the sole writer.
  The audit agent's caveat discipline ("no anomaly is your framing, not my
  finding") is the wanted epistemic posture — keep it.

### F3. Stop-on-ambiguity / stop-on-deviation instructions work (in force)
- Every real catch this session (routing dead-end, contaminated carryover,
  skill ambiguity, paraphrase) came from an agent stopping rather than
  improvising. Standard prompt boilerplate: authorized-changes-exactly-these,
  read-back-after-every-write, STOP conditions, no --once/nohup, INCIDENT.md
  §4 concealment rule.

### F4. Open: harness investigation (NEXT_SESSION task 1, P0)
- Forged system-reminder concealment instructions, vector unknown. Nothing
  this session changed its status; nohup stays blocked until it clears.
  Every item in this ledger assumes supervised mode until then.

---

## Suggested sequencing (after task-queue item 1 clears)

1. **P0 cluster that gates autonomy:** A1 + A3 + B1 (lineage continuation,
   scaffold registration, refinement-brief path) — one coherent change to
   the routing/registration layer, one fixture campaign to accept all three.
2. **P0 conformance pair:** B3 (protocol_ref) + B4 (copy-through /
   conformance diff) — these two remove the biggest silent-corruption risks.
3. **C1** (machine-written power block), retiring C2 and most of the
   discrepancy logger.
4. P1 batch: A2, A5, B2, B5, C3, C4, D1, E1, E3, E4.
5. P2 hygiene: A4, B6, D2, E2.

Prior deferred items from NEXT_SESSION task (4) — the cwd-dependent ROOT bug
in `run_phase1_research.py` and the `calculate_sharpe_ratio` basis problem in
live performance reporting — remain open and are not restated here.


---

# v2 additions — found 2026-07-11 (validation through prescreen arbitration)

## B. Briefs, pre-registration & conformance (continued)

### B7. CLOSED (2026-07-17, commit 0a6311d) — Validation stage never reads the pre-registration artifacts (P0)
- **Symptom:** validation's only required input was
  expanded_hypothesis_card.yaml — it never read user_brief_verbatim.yaml or
  pre_registration.yaml, then claimed "threshold 0.30 appears empirically
  chosen" in ignorance of the documented a-priori rationale, and invented
  six decision criteria (see D2).
- **Fix:** pre_registration.yaml and user_brief_verbatim.yaml (when present)
  become required_inputs for validation and every downstream LLM stage; the
  stage handoff instructs deference to them explicitly.
- **Acceptance:** output audit — validation on a pre-registered run cites
  the pre-registered pass rule, invents no thresholds.
- **Evidence update (2026-07-17, run_058):** validation's required_inputs
  (runs/run_058/handoffs/innovation_expansion_to_validation.yaml) again list
  only expanded_hypothesis_card.yaml — pre_registration.yaml was still not a
  required or optional input. The stage's own validation_decision.yaml then
  misdescribed the registration it vetoed, writing: "Walk-forward period
  (2024-12-01 to 2025-12-31) is explicitly marked 'diagnostic-only, sign
  flips' in expanded card. Testing a hypothesis with documented negative IC
  in the test period is testing the null/negative hypothesis." — treating
  the diagnostic-only 2024-2025 era as the pass-gated test period, when
  pre_registration.yaml's own pass_rule.window_set_ref
  (protocols/h041c_v2_backext.json) pins the pass-gated windows to
  2018-02-01..2023-12-31 only (71 months), a fact the stage never saw
  because it never read the file. Recorded in campaign_knowledge_base.yaml
  under fear_greed_contrarian_v2_validation_rejected. Per operator ruling at
  session close, this is the third in-the-wild demonstration of the exact
  defect this entry describes.
- **Resolution (2026-07-17, commit 0a6311d):** `_apply_b7_mandatory_inputs`
  (workflow/run_phase1_research.py) unions `pre_registration.yaml` and
  `user_brief_verbatim.yaml` (when present on disk) into `required_inputs`
  for validation and every downstream LLM stage (`refinement_planner`,
  `backtest_specification`, `verdict_interpreter`, `campaign_review`),
  applied once at the single `async_invoke_agent` dispatch point (both the
  Claude and Gemini engine paths read the same mutated handoff dict) — a
  missing file is skipped, never force-required, so the union degrades
  gracefully on older runs. A conditional deference sentence
  (`_B7_DEFERENCE_SENTENCE`) is injected into the assembled stage prompt on
  the same condition. Fixtures (tests/test_k3_protocol_pinning.py):
  `test_apply_b7_mandatory_inputs_adds_pre_registration_when_handoff_omits_it`,
  `test_apply_b7_mandatory_inputs_skips_missing_file_without_crashing`,
  `test_apply_b7_mandatory_inputs_deduplicates_already_listed_path`,
  `test_apply_b7_mandatory_inputs_noop_for_non_mandatory_stage`,
  `test_apply_b7_mandatory_inputs_covers_every_downstream_llm_stage`. Note:
  the mutation happens on the in-memory handoff dict passed into the
  prompt-assembly functions, not written back to the on-disk handoff YAML
  — grepping a run's persisted handoff file for "pre_registration" will
  NOT show evidence of this fix firing; the fixtures above are the
  authoritative acceptance evidence, not a live-run artifact.

### B8. Spec-stage conformance is schema-only, not semantic (P0)
- **Symptom:** backtest_specification produced a schema-valid config
  (validate_config.py exit 0) that INVERTED the hypothesis — ER wired as a
  continuous regime gate (trailing stop) instead of an entry-only latch;
  status: spec_ready, blocking_issues: [].
- **Fix:** semantic conformance step at spec acceptance: behavioral fixtures
  (e.g. gate-disabled-equivalence against the parent run, unit tests for
  entry/exit semantics) run before spec_ready is writable — the
  GatedSmaTrendLongOnlyComponent acceptance suite is the model.
- **Acceptance:** fixture: a config that trades on bars the hypothesis says
  it must not cannot reach spec_ready.

### B9. Engine cannot express entry-conditional (latched) gating natively (P1 — resolved for this family)
- **Symptom:** regime dispatch re-evaluates every bar (no memory); vetoes
  are persistence-on-entry, not latches; transforms are stateless. The spec
  stage did not know this and mis-wired the gate (B8).
- **Resolution:** GatedSmaTrendLongOnlyComponent built 2026-07-11 (stateful
  latch per the MacdHistogramCrossoverComponent precedent). Accepted:
  30/30 window-symbols byte-identical to run_054 with gate disabled (117
  trades reproduced); no-deferred-entry and latch unit fixtures pass
  per-bar.
- **Residual:** register the component in indicator_library.yaml with the
  fixture evidence; generalize the latch pattern doc so future gated
  hypotheses don't regenerate the trailing-stop wiring.

### B10. CLOSED — Silent stale-protocol fallback (F4d) — confirmed live (P0 — pinned for run_057, fixed in code 2026-07-15)
- **Symptom:** with no run_context.yaml, protocol resolution falls back to
  campaign_state.last_escalation.protocol_path — which held
  escalation_tf_15m.json, a 15-MINUTE protocol, for this 1d run. Confirmed
  live, one stage before execution.
- **Interim fix used:** run_context.yaml with run_type: forced_diagnostic +
  explicit protocol (supported mechanism, run-scoped, verified consumed:
  prescreen loaded ts_trend_daily_v1.json's 15 windows).
- **Code fix:** the else-branch must hard-fail (or at minimum
  timeframe-check) instead of silently adopting last_escalation; ties into
  B3 (first-class protocol_ref in machine_constraints).
- **Acceptance:** fixture: run with mismatched last_escalation and no pin
  refuses to execute rather than running the wrong timeframe.
- **Resolution (2026-07-15, K3 kernel):** `last_escalation` gains a
  `claimed_by_run`/`claimed_at` marker (written by `_route_escalate`'s own
  `record_escalation` call); the fallback now hard-fails (`RuntimeError`,
  flag `stale_escalation_unclaimed` set before raising) unless the current
  run IS that escalation's claimed one-hop consumer. A one-time migration
  stamped the pre-existing `last_escalation` record (`claimed_by_run:
  run_049`) so run_049's own still-pending resumption is not broken by its
  own protective exception. Full design:
  `engineering/improvements/done/design_and_docs/K3_protocol_pinning_design_20260714.md` (§4, §9 A5). Commits:
  `ef58773` (implementation), `1248a5e` (A5 migration), `6b827eb` (rider).

## C. Power & validation machinery (continued)

### C5. Prescreen artifacts mislabel their own statistics (P1)
- **Symptom:** route_rationale's "Active-bar IC=" is a hardcoded f-string
  label applied to whatever pooled statistic arrives (here the all-bars
  bootstrap IC); _cost_check hardcodes ic_used: "ic_active_bars" as a
  literal on BOTH return paths regardless of caller input. Same false
  labels in run_054's passing artifact — unscrutinized because it passed.
- **Fix:** labels derived from significance_methodology_used / the actual
  argument; never hardcoded.
- **Acceptance:** fixture through the degenerate-fallback branch asserting
  the rationale names block_bootstrap_all_bars_v1 and ic_used reflects the
  value actually consumed.

### C6. A8.3 textual gap: no admissible statistic defined for structurally-degenerate sparse signals (P0, doctrine)
- **Symptom:** A8.3 point 5 declares all-bars IC inadmissible as sole
  evidence above 50% sparsity and requires the conjunction — but
  ic_active_bars is structurally undefined (zero variance) for
  constant-magnitude latched signals. The code's bootstrap fallback then
  kills on the single statistic the amendment declares inadmissible
  (run_057: 74.25% sparsity, kill on all-bars p=0.46). Parent passed the
  same code path at 44.8% sparsity — below the trigger — so the lineage was
  judged under two different rule regimes. Operator arbitration set the
  kill aside (prescreen_override_20260711.yaml) with a pre-commitment that
  the pre-registered walk-forward pass rule is final.
- **Fix (doctrine + code, designed OUTSIDE any live run):** define the
  governing prescreen statistic for this signal class — candidate:
  conditional-return / per-episode-expectancy test on active episodes
  (payoff-based, immune to rank-IC's blindness to skewed trend-following
  payoffs), with its own null calibration. Also: sparsity-attenuation
  correction or explicit power statement when comparing all-bars IC across
  different sparsity levels in one lineage.
- **Acceptance:** known-answer fixture: a synthetic latched signal with
  positive per-episode expectancy and near-zero all-bars rank IC must NOT
  route kill_no_ic under the amended rule.

## D. Skills & prompt text (continued)

### D2 (upgraded to P0, live evidence). Stage personas invent decision criteria on fully pre-registered hypotheses
- **Evidence (2026-07-11):** validation stage output on run_057 — six
  violations in one artifact: flat Sharpe>=0.4 replacing symbol-specific
  comparators; a GRID SWEEP on the frozen ER threshold; S1 and S2 both
  promoted to verdict-bearing; unregistered win_rate/drawdown/
  forecast_return_corr/hold-time criteria; wholesale protocol substitution
  (6x65-bar windows over 2024-12->2025-12 replacing the 15 semi-annual
  pre-registered windows). Under nohup this becomes the operative protocol
  unchallenged.
- **Fix:** as v1 D2 (brief-outranks-skill precedence line in every stage
  skill) PLUS B7 (stages must read the pre-registration) PLUS B4
  (decision-bearing fields copy-through, never re-authored).

## E. Documentation & artifacts (continued)

### E5. Protocol files need version stamps; artifacts referencing them need content hashes (P2)
- **Symptom:** run_054's prescreen_result.yaml names
  protocols/ts_trend_daily_v1.json but lists 96 monthly windows — truthful
  when written (2026-07-07, one day BEFORE the semi-annual redesign of that
  file), misleading forever after. Same failure family as E1.
- **Fix:** protocol JSONs carry a version/date field; artifacts record the
  protocol file's content hash alongside its name.

## F. Multi-agent & security operations (continued)

### F5. Prompt-relay truncation guard (in force)
- **Symptom:** two consecutive operator relays truncated prompts
  mid-sentence — precisely where STOP conditions live; separately, the
  injection payload survived ZERO of four copy-paste relays (it begins with
  a markdown fence that every chat surface swallowed).
- **Fix (adopted):** every prompt ends with a terminal marker line
  ("END OF INSTRUCTIONS (N steps)"); agents refuse truncated prompts.
  Evidence relays go to files on disk, not chat; markdown-hostile content
  gets line-prefixed if it must transit chat.

### F6. CLOSED — the "forged system-reminder" incident resolved as native harness boilerplate
- **Resolution (2026-07-11, evidence on record in INCIDENT.md):** both
  reminder templates located by grep in the shipped claude.exe binaries.
  A/F/G: date-rollover notices. C/D/E: the harness truthfully reporting the
  agents' OWN Python-script file writes (invisible to its tracked-edit
  system). B: a truthful report of the genuine 2026-07-10 parallel-agent
  revert — the reminder witnessed the real incident (a write conflict,
  already resolved by single-writer doctrine). No hostile actor. Permanent
  record defects: B-E diff bodies never captured verbatim; no absolute
  timestamps for A-E.
- **Consequence:** nohup's block is re-grounded on this ledger's P0s
  (operator decision), no longer a security hold.

### F7. Disclosure-doctrine allowlist (adopted)
- Concealment-shaped content byte-matching the verified harness-template
  list (date-rollover; file-modified notice) is disclosed in ONE line, not
  treated as hostile. Anything not on the list is still surfaced verbatim
  immediately. Rationale: alarm fatigue is the failure mode of a rule that
  fires on every date change; the allowlist keeps the rule credible.

### F8. Agents writing via scripts are invisible to the harness's change tracking (P2, root cause of C/D/E)
- **Symptom:** file writes performed through Python subprocesses triggered
  "modified by the user or a linter" reminders about the agent's own edits.
- **Mitigation:** expected behavior, now understood — noted so future
  sessions recognize self-referential file-modified reminders instantly;
  weigh tracked-edit tools vs scripts for shared-state writes where
  practical.

---

## Sequencing update (v2)

The autonomy-gating P0 set, revised: A1+A3+B1 (routing/registration),
B3+B10 (protocol pinning + fallback hard-fail), B4+B7 (copy-through +
pre-registration as required input), B8 (semantic spec conformance), C6
(prescreen statistic for latched sparse signals — doctrine amendment before
any future gated hypothesis runs prescreen). D2 rides on B4/B7. Everything
else is P1/P2 hygiene that can follow the shadow-campaign test.

Acceptance test for autonomy itself (unchanged from operator decision): a
full shadow campaign under nohup with post-hoc human replay of every stage
audit; autonomy is earned where the mechanical gates catch what supervised
review caught this session — five out of five LLM stages deviated from the
pre-registered brief on run_057, and only supervised stepping caught them.


---

# v3 additions — found 2026-07-11 (verdict machinery through lineage close)

## A. Orchestrator routing & state machine (continued)

### A8. Verdict vocabulary conflates hypothesis verdict with lineage routing (P0)
- **Symptom:** "kill vs pivot" is one enum decision, but it mixes two
  independent questions: is THIS hypothesis dead (verdict) and should the
  campaign scaffold a successor (routing). run_057's verdict stage killed
  the hypothesis in its analysis while routing pivot — and the single-word
  vocabulary made that read as defiance when it was actually two decisions
  in one slot. Same defect family as A2 (refine/pivot both emitting
  completed_refined).
- **Fix:** split into two fields: hypothesis_verdict (kill / refine /
  promote — about the mechanism) and lineage_routing (terminate / refine /
  pivot / escalate — about the campaign), each with its own authority
  rules; pre-commitments constrain routing without needing to re-litigate
  the verdict.
- **Acceptance:** fixture: a killed hypothesis with routing terminate
  produces no scaffolds; a killed hypothesis with routing pivot produces
  one, and the two fields are separately auditable.

## B. Briefs, pre-registration & conformance (continued)

### B11. Pass rules must specify the complete verdict mapping — no
underspecified delegation (P0, operator-side)
- **Symptom (operator-authored):** the pre-registered pass rule said "FAIL
  on (a) or (b) -> ... verdict routing decides kill vs pivot" — an explicit
  delegation of the terminal decision to the stage's own rulebook. The
  later pre-commitment narrowing it lived in a sidecar the stage had no
  reason to treat as binding. The stage walked through the open door the
  brief itself left.
- **Fix:** brief template requires a total mapping: for every outcome
  (PASS / FAIL-a / FAIL-b / sparse-inconclusive), the exact verdict enum
  AND routing value, with discretion granted only explicitly ("routing at
  stage discretion" as an opt-in phrase). Pre-commitments made mid-run are
  written INTO the pass-rule artifact (amended with audit trail), not into
  sidecars.
- **Acceptance:** brief lint: any pass rule containing a FAIL branch
  without an explicit verdict+routing pair is rejected at materialization.

## C. Power & validation machinery (continued)

### C7. Protocol-execution verdict machinery is not the pre-registered rule
(P0)
- **Symptom:** protocol_result.yaml issued verdict: refine from generic
  code thresholds (min_trades>=20, drawdown caps); its criteria parser
  cannot evaluate prose criteria ("no matching metric keyword" — 2 of 4
  UNTESTED) and computed no bar-level medians at all (BTC "median_sharpe
  not computed"). On an autonomous run this generic refine would have been
  written back over a pre-registered kill.
- **Fix:** machine-checkable pass rules (structured criteria in
  pre_registration.yaml with field names, comparators, and the metric
  basis), evaluated by code against computed bar-level statistics; prose
  criteria banned from the decision path. Ties into B11's total mapping.
- **Acceptance:** known-answer fixture: run_057's own artifacts re-judged
  by the structured evaluator must yield FAIL-(a)/kill with the medians
  computed, not UNTESTED.

### C8. Cross-run trade comparison must use timestamps + percent returns,
never absolute PnL or row counts (P1, method doctrine)
- **Symptom:** trades.json rows are LIFO fragments whose boundaries depend
  on the full execution sequence including rebalance-triggered fills
  invisible at the signal layer; skipped entries change compounding and
  hence notional. An operator-specified "PnL must match" cross-check
  produced phantom mismatches that stalled the S2 computation for a turn.
- **Fix (adopted):** identity matching on (symbol, window, entry_time,
  exit_time) with UTC normalization; percent-return agreement as the
  correctness test; absolute PnL reported but never counted as mismatch.
  The corrected S2 run (42/42 exact, percent agreement to 6 decimals) is
  the reference implementation.

### C9. KB-exhaustion gating missing on the verdict stage's proposal path
(P1)
- **Symptom:** verdict_interpreter's pivot path proposed a Keltner
  Channel breakout — a family the KB marks exhausted/terminal
  (keltner_mean_reversion_no_edge, keltner_breakout_inverted,
  keltner_scoremode_no_edge) and that run_053/054's own campaign review
  lists as forbidden re-proposals. Exhaustion checks exist on
  campaign-review and hypothesis-design handoffs but not here — the
  proposal was generated one stage away from where the check lives.
- **Fix:** every proposal-generating path (verdict pivot/refine included)
  runs the KB exhaustion + reactivation-conformance check before writing
  proposed_brief.yaml; a forbidden family yields a human_pause, not a
  proposal.
- **Acceptance:** fixture: pivot route against a KB-exhausted family
  refuses to emit the proposal and pauses.

## D. Skills & prompt text (continued)

### D3 (rewritten as root cause, P0). Operator directives have no
first-class channel into LLM stages
- **Symptom chain (run_057 verdict stage):** the binding pre-commitment
  sat in a sidecar passed as optional_inputs; no skill text anywhere says
  operator sidecars outrank the rulebook; the operator's acceptance
  criteria lived in prompts to the implementation agent, which stages
  never see. The stage then faithfully applied Rule 6 CASE B and the pass
  rule's own delegation — and was checked afterward against constraints
  it was never given in a form it recognizes. Six of six LLM stages on
  run_057 deviated from operator intent; at least this one deviated while
  following its instructions correctly.
- **Fix:** (i) an operator_directives.yaml artifact with defined highest
  precedence, named in every skill's preamble: "if present, binding,
  outranks all rulebook logic; conflicts are a human_pause"; (ii) the
  operator prompt template updated so acceptance criteria are ALSO
  injected into the stage's own inputs via that artifact, not only
  checked post-hoc; (iii) B11's total-mapping rule removes the largest
  class of delegations that make directives necessary at all.
- **Acceptance:** output audit: a stage given a directive that contradicts
  its rulebook pauses or complies with the directive — never silently
  applies the rulebook.

## F. Multi-agent & security operations (continued)

### F9. Operator prompts must not pre-state expected values for
computations under independent verification (adopted)
- **Symptom:** the operator's S2 instruction embedded "~+1396 bps" as an
  anticipated result before measurement; when the agent's two computations
  disagreed, one landing near the anchor, the agent (correctly) refused to
  pick the number that matched expectation. The anchor was withdrawn; the
  redesigned identity-based computation later reproduced it for verifiable
  reasons — right answer, and the discipline of refusing the shortcut is
  what made it trustworthy.
- **Rule (adopted):** verification prompts state the method and the
  cross-checks, never the expected value; algebraic predictions go in the
  operator's own notes, disclosed after the measurement.

---

## Sequencing update (v3)

Autonomy-gating P0 set, final for this session: A1+A3+B1
(routing/registration), A8+B11+C7 (verdict/routing vocabulary split, total
pass-rule mapping, machine-evaluated criteria — one coherent
verdict-machinery change), B3+B10 (protocol pinning + fallback hard-fail),
B4+B7+D3 (copy-through, pre-registration as stage input, operator-directive
channel — one coherent conformance change), B8 (semantic spec conformance),
C6 (prescreen statistic for latched sparse signals). C9 rides on the
verdict-machinery change.

Session tally feeding the autonomy decision: six of six LLM stages deviated
from the pre-registered brief or operator intent on run_057
(hypothesis_generation: fabricated power block and citations;
innovation_expansion: paraphrased execution semantics; validation: six
invented decision criteria incl. a sweep on a frozen parameter;
backtest_specification: hypothesis-inverting config marked spec_ready;
signal_prescreen route: single-statistic kill the doctrine declares
inadmissible; verdict_interpreter: routing against the pre-commitment plus
a KB-forbidden proposal). Every catch was supervised review. That is the
autonomy gap, quantified.


---

# v4 additions — found 2026-07-12 (kill writeback)

### A9. _route_kill conflates "hypothesis dead" with "campaign space empty" (P0)
- **Symptom:** the only lineage-terminating route writes a campaign-wide
  campaign_decision.yaml and sets campaign_state.status = "space_empty" —
  killing one gate variant would have declared the whole campaign's search
  space exhausted. The writeback agent detected this and applied the
  terminal state manually (pending_stage: completed_rejected) without
  invoking the router.
- **Fix:** part of the A8 verdict/routing split — kill-this-hypothesis and
  terminate-this-campaign become separate routes; space_empty requires its
  own explicit decision (campaign-review scope, not verdict scope).
- **Acceptance:** fixture: a kill verdict on one queue entry leaves
  campaign_state.status untouched and other entries schedulable.

### B12. KB lineage identity vs exact-match hypothesis_id lookup (P1)
- **Symptom:** the refined child carried hypothesis_id ..._ER20GATE; the
  lineage's KB finding is keyed on the parent id. _find_kb_entry's
  exact-match lookup would have spawned a second, disconnected finding
  instead of incrementing evidence on the lineage entry — silently
  fragmenting the KB's memory of a lineage. Averted by hand-targeting.
- **Fix:** findings carry a lineage_id (queue-entry id) distinct from the
  per-run hypothesis_id; KB attach targets lineage_id; in-lineage
  refinements inherit it automatically at materialization.
- **Acceptance:** fixture: a child-variant verdict attaches to the parent
  lineage finding, evidence_count increments, no stub is created.

### B13. The "version identifier" trap: a dead key, a doubly-overloaded field name, and a mislabeled path (P2, found by 2026-07-15 K3 audit)
- **Symptom:** three distinct, compounding naming defects surfaced while
  implementing B3/B10's post-hoc conformance check. (1) `tools/
  prescreen_signal.py` writes `prescreen_result.yaml`'s `protocol_version`
  field from `protocol.get("_version", protocol_path)` — an underscore-
  prefixed `_version` key that NO protocol JSON in this repo has ever
  written; the `.get` call is dead code, always falling through to its
  default. (2) `protocol_version` is a genuinely overloaded field name with
  two unrelated meanings on different objects: two pre-existing protocol
  files (`baseline_v2.json`, `ts_trend_daily_v1.json`, both predating K3)
  carry it as a hand-set human label with no paired hash, while K3's own §5
  stamping (`tools/stamp_protocol.py`) writes it as a machine date paired
  with `protocol_content_hash` — same key name, different authors,
  different semantics, no schema distinguishing them. (3)
  `prescreen_result.yaml`'s `protocol_version` field, given (1) is dead,
  is in practice always a raw filesystem PATH string, not a version
  identifier at all — a field named "version" holding a path is exactly
  the kind of naming lie this campaign's own doctrine (F4-family) exists
  to catch, here caught by the rider's own implementation reading, not a
  test failure. A rider-authored code comment (workflow/
  run_phase1_research.py, `_check_prescreen_conformance`) initially
  mis-attributed (2)'s hand-set labels to K3's own stamping; corrected in
  this close-out (2026-07-15).
- **Fix:** not undertaken this session (found during, not before, K3's own
  work; fixing `prescreen_signal.py`'s dead `_version` lookup or
  renaming/schema-distinguishing `protocol_version`'s two meanings would be
  a behavior change to shipped code, out of scope for a conformance-check
  rider). Filed for a future session: either retire the dead `_version`
  branch and rename `prescreen_result.yaml`'s field to reflect what it
  actually holds (a path), or make `tools/prescreen_signal.py` genuinely
  read the protocol's own `protocol_version` stamp (disambiguating it from
  a hand-set label via the paired `protocol_content_hash`'s presence).
- **Acceptance:** not yet defined — this is a filed finding, not a shipped
  fix.

### B14. Content-hash formula triplicated with no single source of truth (P2, found by 2026-07-15 K3 audit)
- **Symptom:** the same protocol-content-hash formula (strip
  `protocol_version`/`protocol_content_hash`, `json.dumps(sort_keys=True)`,
  sha256) now exists independently in THREE places: `workflow/
  run_phase1_research.py`'s `_compute_protocol_content_hash` (the runtime
  guard, §5), `tools/stamp_protocol.py`'s `compute_protocol_content_hash`
  (deliberately duplicated rather than importing, to avoid a heavy
  `claude_agent_sdk`/`google.genai` import chain in a standalone CLI tool),
  and the rider's own inline copy inside `_check_prescreen_conformance`
  (deliberately duplicated rather than calling `_compute_protocol_content_
  hash`, which takes a `Path` and re-reads from disk, where the rider
  already has the parsed dict in hand). Each duplication was individually
  disclosed and round-trip-tested against the others at the time it was
  written (`test_stamp_protocol_round_trip_matches_rpr_hash_formula`,
  `test_check_prescreen_conformance_protocol_ref_content_hash_match`), but
  there is no SINGLE source of truth — a future edit to one copy (e.g. a
  canonicalization change) could silently diverge from the other two, and
  nothing would catch it except the existing round-trip tests continuing
  to happen to exercise the same inputs.
- **Fix:** not undertaken this session (each duplication was independently
  justified against a REAL constraint — import weight, `Path` vs. dict
  input shape — not an oversight; consolidating would require either
  accepting the heavy import in `stamp_protocol.py` or a shared
  lightweight module none of the three currently import from). Filed for
  a future session: extract the formula into one function in a
  dependency-light module (no `claude_agent_sdk`/`google.genai` imports)
  that all three sites import.
- **Acceptance:** not yet defined — this is a filed finding, not a shipped
  fix.

### C10. _record_backtest_trial silently records n_trades: 0 (P1)
- **Symptom:** the function reads per_symbol_summary["trade_count"], a key
  that does not exist (the dict has min_trade_count); .get default 0 means
  every backtest trial record shows n_trades: 0 regardless of reality
  (run_057: 42 actual). Silent-wrong-key + silent-default — the same
  species as the session's other measured-the-machinery bugs. Corrected in
  run_057's record with a disclosed note; code unfixed.
- **Fix:** read the true pooled trade count from the results; and as
  policy, trial-record writers use explicit key access (KeyError over
  silent 0) for decision-relevant fields.
- **Acceptance:** known-answer fixture over run_057's artifacts must record
  n_trades: 42.

---

## Final session tally (feeds the autonomy decision)

Six of six LLM stages deviated on run_057; three additional latent code
defects surfaced during close-out (A9, B12, C10) — each of which would have
silently corrupted campaign-level state (false space_empty, fragmented KB
lineage memory, zeroed trade counts) under autonomous operation. Every
catch was supervised review or an agent stop-condition. The P0 set in the
v3 sequencing section, plus A9 folded into the A8 change and B12 into the
KB layer, is the complete known gate to autonomy as of session close.

---

# v5 additions — found 2026-07-16/17 (H-041-C-v2 / run_058 launch-to-close arc)

## A. Orchestrator routing & state machine (continued)

### A10. Missing-deliverable stage failures get zero retries (P1, one occurrence, watch-level)
- **Symptom:** run_058's first innovation_expansion invocation wrote only 1
  of 2 required deliverables (expanded_hypothesis_card.yaml only;
  innovation_notes.yaml missing); `ensure_files` hard-failed the run to
  `paused:unhandled_exception` on the first miss, with no retry of the same
  stage invocation before pausing. Operator ruled this a single LLM
  formatting fault (not systemic) and ordered a resume rather than a code
  fix.
- **Fix:** not undertaken this session (one occurrence, operator-classified
  as non-systemic). If it recurs: `_invoke_agent_with_yaml_retry`'s existing
  retry-loop pattern (already used for the F4b YAML-repair path and the
  SDK-misclassification path, A11 below) is the natural home for a bounded
  missing-deliverable retry, re-invoking the same stage with an explicit
  "deliverable X was not written" correction before pausing for human
  review.
- **Acceptance:** not yet defined — filed at watch-level pending a second
  occurrence.

### A11. CLOSED — claude_agent_sdk 0.2.82 result-misclassification on error turns (P1, occurred run_054 + run_058)
- **Symptom:** when a CLI result message carries `is_error=True` with an
  empty `errors` list, the SDK (`_internal/query.py`) falls back to that
  turn's own `subtype` field as the error text; if `subtype` is literally
  "success", a later `ProcessError`'s message is replaced with the literal
  string "Claude Code returned an error result: success" — a genuine SDK
  defect, independently verified by reading the installed package source,
  not a real application-level error.
- **Resolution (2026-07-16/17, this session):** `_invoke_agent_with_yaml_retry`
  (workflow/run_phase1_research.py) gained a narrow, exact-string-match
  retry: on the first occurrence of this exact message, re-invoke the same
  stage once, prompt unchanged; any other message, or a second occurrence,
  still raises. Deliberately not broadened into a general except-Exception
  catch-all (see the code comment at the call site). RUNBOOK's halt-table
  and §4 both annotate the case. Fixtures (tests/test_k3_protocol_pinning.py):
  test_invoke_agent_with_yaml_retry_recovers_from_sdk_error_result_success,
  test_invoke_agent_with_yaml_retry_reraises_on_second_sdk_error_result_success,
  test_invoke_agent_with_yaml_retry_does_not_catch_other_messages. Commit:
  `9bf2a4c`.
- **Acceptance:** met — see fixtures above; full suite green at 301
  (`python -m pytest -q`, confirmed at session close).

## B. Briefs, pre-registration & conformance (continued)

### B15. CLOSED (2026-07-17, commit ae95906) — No first-class path from a fresh hypothesis registration to a schedulable queue entry (P1)
- **Symptom:** H-041-C-v2's stamped protocol and brief were fully authored
  and registered (pre_registration.yaml, briefs/H-041-C-v2.md) with no
  queue entry ever created for it — RUNBOOK's documented launch procedures
  all assume an existing queue entry. Creating one required a hand-edit to
  config/campaign_queue.yaml outside the authorized write set at the time;
  the operator authorized it explicitly.
- **Fix:** a registration-to-enqueue tool/command (e.g.
  `python workflow/run_campaign.py --register <brief>`) that creates the
  queue entry mechanically from a completed brief + pre_registration pair,
  so a fully-authored registration is always schedulable without a
  hand-edit.
- **Acceptance:** fixture: a brief + pre_registration pair with no prior
  queue entry, run through the register command, produces a `ready` queue
  entry that `_select_entry` picks up on the next `--once`/`--resume`
  invocation.
- **run_049 orphan-thread evidence (found 2026-07-19, predates the fix):**
  `runs/run_049/pipeline_state.yaml` records `status: active`,
  `pending_stage: hypothesis_generation`, `completed_stages: []` — a run
  directory that exists on disk with live pipeline state, yet
  `config/campaign_queue.yaml` contains ZERO entries referencing `run_049`
  anywhere (confirmed by direct grep of the queue file). This is a second,
  independent real-world demonstration of the class B15 addresses: a run
  thread with no queue-level path back to it, discoverable only by
  directory archaeology, not by any campaign-runner command. Distinct from
  H-041-C-v2's occurrence (a REGISTRATION with no enqueue path); this one
  is a RUN with no registration-or-queue path at all. Per operator ruling
  (R4, this session's dispatch): "run_049 parked — do not touch it" — left
  untouched as evidence, not remediated by this close-out. The unrelated
  `campaign_state.yaml.last_escalation.claimed_by_run: run_049` marker
  (K3/B10's own migration) references the same run_id for a different
  reason (stale-escalation claim tracking) and is not part of this
  finding.
- **Resolution (2026-07-17, commit ae95906):** `register_hypothesis`
  (workflow/run_campaign.py) — a `register` argparse subcommand
  (`--brief PATH --priority N --notes TEXT`) parsing the brief via the
  existing `_parse_brief_frontmatter`, refusing on a duplicate id or a
  malformed brief (one log line, nonzero exit), otherwise appending an
  entry mirroring the H-041-C-v2 entry's own field set via the existing
  `_load_queue`/`_save_queue` pair. First real use: `FUNDING_MR_DAILY_RETEST`
  (2026-07-18), enqueued cleanly, one log line, ran to completion
  (`run_059`, `completed_rejected`) without any hand-edit. Fixtures
  (tests/test_k3_protocol_pinning.py):
  `test_register_hypothesis_appends_entry_with_expected_field_set`,
  `test_register_hypothesis_refuses_duplicate_id`,
  `test_register_hypothesis_refuses_malformed_brief`,
  `test_register_hypothesis_emits_exactly_one_log_line`. run_049's own
  orphan state is NOT retroactively fixed by this command (it would need
  a manual `register` invocation against a brief that does not exist for
  it, or a different remediation path) — parked per R4.

## F. Multi-agent & security operations (continued)

### F10. No raw LLM transcript preserved when a stage invocation crashes (P1)
- **Symptom:** across this arc's three pause/resume cycles (innovation_expansion
  deliverable-completeness failure, the queue-level `paused:*` gate, the SDK
  misclassification failure), the only forensic record available for each
  crash was the orchestrator's own log lines and the partial artifacts
  written before failure — the underlying LLM turn(s) that produced (or
  failed to produce) the deliverables were never captured to disk.
  Root-causing each pause relied on artifact archaeology and, for the SDK
  defect, reading third-party library source, rather than the actual
  transcript.
- **Fix:** on any stage invocation that raises (SDK exception, ensure_files
  failure, YAML-repair exhaustion), write the raw request/response
  transcript (or at minimum the final turn) to a sidecar under the run's
  artifacts/ or a dedicated crashes/ directory before re-raising or
  pausing.
- **Acceptance:** fixture: a stage invocation forced to raise produces a
  transcript sidecar file, present and non-empty, alongside the pause.

---

# v6 additions — found 2026-07-18/19 (run_059 tz-bug arc: launch, engine fix, resumes, verdict)

## A. Orchestrator routing & state machine (continued)

### A12. verdict_interpreter's human_pause routing falls through to the generic completion block, mislabeling status "active" (P0)
- **Symptom:** `run_loop()`'s `elif current_stage == "verdict_interpreter":`
  branch (workflow/run_phase1_research.py:4608-4611) sets `next_stage =
  determine_post_verdict_route(...)` with NO check for
  `next_stage == "human_pause"` — unlike the sibling
  `elif current_stage == "holdout_evaluation":` branch three cases below
  it (workflow/run_phase1_research.py:4616-4621), which explicitly does
  `if next_stage == "human_pause": update_state(status="paused_for_human");
  break`. Without that check, a verdict_interpreter human-pause routing
  falls through to the generic "6. Mark completed and stage next phase"
  block (workflow/run_phase1_research.py:4623-4632), whose status
  computation is `status="active" if next_stage != "completed_rejected"
  else "rejected"` — `next_stage="human_pause"` is neither, so `status`
  is (wrongly) written `"active"` instead of `"paused_for_human"`, even
  though `pending_stage` does get correctly set to `"human_pause"`. The
  loop still terminates on the FOLLOWING iteration (the top-of-loop
  `TERMINAL_PREFIXES` check catches `pending_stage.startswith("human_pause")`),
  but for one full iteration the run's own `status` field lies about its
  state — exactly the two symptoms named for this arc: (1) the
  human_pause sentinel falls through the dedicated branch unhandled; (2)
  the pause status gets overwritten to `active`.
- **Fix:** add the same `if next_stage == "human_pause": update_state(...);
  break` guard to the `verdict_interpreter` branch that `holdout_evaluation`
  already has; consider making it a shared helper so a THIRD stage adding
  a human_pause routing doesn't reintroduce the same gap a third time.
- **Acceptance:** fixture: a verdict_interpreter stage whose
  `determine_post_verdict_route` returns `"human_pause"` must leave
  `pipeline_state.yaml.status == "paused_for_human"` immediately (same
  iteration), not `"active"` for one extra iteration.

### A13. Stale-cache / resume freshness gap across an engine-code fix (P1)
- **Symptom (operator-observed, this arc's resume cycles):** run_059's
  resume-after-engine-fix sequence needed more manual intervention than a
  clean single resume — `pipeline_state.yaml`'s own `completed_stages`
  list for this run shows `protocol_execution` and `verdict_interpreter`
  each appearing multiple times (`[..., protocol_execution,
  verdict_interpreter, protocol_execution, verdict_interpreter,
  verdict_interpreter]`), consistent with A12's status-mislabeling bug
  above requiring extra resume passes, and/or a verdict-validity check
  somewhere in the resume path not forcing re-evaluation against the
  now-fixed engine on the first attempt. Independent verification this
  close-out: `signal_prescreen` appears only ONCE in that same list,
  which is CORRECT (prescreen_signal.py's `_merge_aux_feeds` never goes
  through `CandleBuilder._align()` at all — confirmed in the prior
  session's Step 2 repro — so it was never affected by the tz bug and
  needed no re-run); `protocol_execution` DID need a genuine re-run
  because it depends on `CandleBuilder`/`_align()` directly. This session
  could not fully re-derive, from static repo inspection alone, a single
  additional code site (beyond A12) that explicitly treats a stale
  artifact as still-valid without checking upstream freshness — filed at
  the operator's characterization pending a future session with the
  actual resume-cycle logs in hand.
- **Fix (proposed, not designed this session):** any verdict-validity /
  already-computed check that gates a re-run should key on a content hash
  of its actual inputs (config, protocol file, and ideally the engine
  code version/commit) rather than mere file presence or run_id
  membership — closing the general class this arc's manual resume
  friction belongs to, whatever the precise site turns out to be.
- **Acceptance:** not yet defined — filed pending root-cause confirmation
  in a future session with full resume-cycle logs.

### A14. `candle_completion_callback` arity mismatch (watch, not fixed — confirmed harmless in current wiring)
- **Symptom:** `CandleBuilder._ingest`'s `self.candle_completion_callback(symbol)`
  call (trading-bot/data/data_manager.py:267) passes ONE argument, but
  `DataManager`'s own default callback, `_enrich_and_notify(self, symbol,
  candle)` (trading-bot/data/data_manager.py:493), requires TWO — a
  `TypeError` on every real candle close, silently swallowed by
  `_ingest`'s own try/except. Confirmed via the run_059 tz-bug repro
  (prior session): reproducible on demand by constructing a bare
  `DataManager` and driving `add_row` without first overwriting
  `candle_builder.candle_completion_callback`.
- **Why not fixed:** confirmed harmless in every real (non-repro) code
  path — `core/backtester.py:149-150` overwrites
  `candle_builder.candle_completion_callback` with
  `bot._process_symbol_candle_completion` immediately after construction,
  which defaults its own `candle` parameter, so the mismatched default
  wiring is never actually exercised in a live or backtest run. Left as a
  watch item: a future caller that constructs `DataManager` without going
  through `core/backtester.py`'s wiring (e.g. a standalone script or a
  new orchestration path) would hit this silently, with no exception
  surfaced anywhere.
- **Fix (if ever prioritized):** either give `_enrich_and_notify`'s
  `candle` parameter a default of `None`, or have `_ingest` pass the
  completed `Candle` object through to the callback (arguably the more
  correct fix, since the callback's whole point is to be notified of the
  candle that just closed).
- **Acceptance:** not yet defined — watch-level, zero real-path impact
  confirmed.

## C. Power & validation machinery (continued)

### C11. A8.6 block_size defaults silently to the 1h value for any unmapped timeframe, including the deferred 4h candidate (P1)
- **Symptom:** `_A86_BLOCK_SIZE_BY_TIMEFRAME = {"1h": 24, "1d": 1}`
  (workflow/run_phase1_research.py:3125) defines exactly two timeframes;
  `_run_a86_power_check`'s lookup,
  `block_size = _A86_BLOCK_SIZE_BY_TIMEFRAME.get(timeframe, 24)`
  (workflow/run_phase1_research.py:3163), silently falls back to 24 (the
  1h value) for ANY other timeframe — including "4h", the exact candidate
  R3 (this session's dispatch) explicitly deferred rather than abandoned.
  `tools/prescreen_signal.py`'s own analogous block-size selection
  (lines ~885-895) already has a correct, timeframe-aware fallback for
  non-1h/1d cases (`block_size = max(_BLOCK_SIZE_1H // 4, 6)` — i.e. 6
  for 4h), confirming the A8.6 power-check function's plain `.get(...,
  24)` default is a genuine, divergent gap between the two
  power/significance code paths this repo maintains in parallel (same
  family of duplication risk as B14).
- **Fix:** add `"4h": 6` (and any other timeframe this campaign is
  likely to register) to `_A86_BLOCK_SIZE_BY_TIMEFRAME`, or better,
  derive block_size arithmetically from timeframe (bars-per-day) the way
  `prescreen_signal.py` already does, in one shared function both files
  import.
- **Acceptance:** fixture: an A8.6 power check on a "4h" hypothesis card
  must compute `n_eff` using block_size=6, not the 1h default of 24.

## F. Multi-agent & security operations (continued)

### F11. No-transcript-on-derived-error, F10-adjacent (P2, one occurrence)
- **Symptom:** F10 covers no-transcript-on-SDK-crash; this arc surfaced
  the same gap for a HUMAN/AGENT-DRIVEN diagnostic derivation instead of
  an SDK exception. The in-process repro script that root-caused the
  run_059 tz bug (`repro_run059.py`) was written to this session's
  scratchpad directory (a per-session temp path outside the repo, cleaned
  up by the harness), never committed anywhere — its exact output is
  preserved only in this conversation's own transcript/report text, not
  as a durable, re-runnable repo artifact. The FIX's own regression tests
  (tests/test_funding_rate_component.py) are durable evidence for the
  FIXED behavior, but the ORIGINAL pre-fix diagnostic run (the actual
  proof of the defect, not just of its resolution) is not reproducible by
  a future reader without re-deriving it from scratch.
- **Fix:** a convention (not designed this session): ad hoc root-cause
  repro scripts written during an implementation-agent task get committed
  to a `debug/`-style directory (or at minimum their full stdout gets
  saved as a session-report attachment) rather than living only in an
  ephemeral scratchpad + chat transcript.
- **Acceptance:** not yet defined — filed as a process gap, not a code
  defect.

## D. Skills & prompt text (continued)

### D4. Shared, non-run-scoped trades.json output path (P1)
- **Symptom:** `EnhancedPerformanceTracker.__init__`
  (trading-bot/performance/metrics.py:315):
  `def __init__(self, commission_rate: float = 0.001, log_file: str =
  'results/trades.json', initial_capital: float = 1000.0):` — every
  backtest run writes to the SAME shared file
  (trading-bot/results/trades.json) unless a caller explicitly overrides
  `log_file`. This is the direct cause of this entire multi-session
  arc's standing `trades.json` git-status waiver (STATE W): every run's
  trades overwrite the prior run's, so the file is perpetually "modified"
  relative to whatever was last committed, and must be restored
  (`git checkout --`) at every session close rather than ever reflecting
  one run's own history.
- **Fix:** default `log_file` to a run-scoped path (e.g.
  `results/{run_id}/trades.json`, threaded through from whatever
  constructs the tracker) rather than a fixed shared filename; keep the
  flat `results/trades.json` path available only for genuinely
  interactive/manual (non-campaign) use.
- **Acceptance:** fixture: two backtests run back-to-back must each leave
  their own trades.json intact and inspectable, neither overwriting the
  other.
- **CLOSED (D4 dispatch, 2026-07-23):** scope was narrowed to the concrete
  defect the arc actually kept hitting — the **test suite** writing into the
  shared, tracked `trading-bot/results/trades.json`. The path was baked into
  *production* code (`EnhancedPerformanceTracker.__init__`'s default), which the
  backtest path reached because `launcher._build_mock_stack` constructed the
  tracker with no `log_file`, so it inherited the shared default and the
  throttled `save_trades()` dumped into the tracked file mid-run. Fix is
  additive/opt-in: threaded a `trades_log_file` parameter through
  `run_backtest` → `_build_mock_stack` → `EnhancedPerformanceTracker(log_file=…)`,
  **production default byte-identical** (omit it ⇒ flat `results/trades.json`
  exactly as before — verified by `test_default_still_targets_shared_results_path`
  and the unchanged golden-fixture regression tests). The five suite call sites
  now opt into `tmp_path`. Standing guarantee: a `pytest_sessionfinish` guard in
  **both** test roots' conftests fails the run if any tracked file under
  `trading-bot/results/` is mutated during a session (order-independent),
  backed by `trading-bot/tests/test_results_dir_isolation.py` proving the seam.
  Verified: full suite run twice, `git status --porcelain -- trading-bot/results`
  empty after each. **This defect fired three times in this arc** (session
  reports 20260720_fee_isolation_pairs, 20260722_c7ext_audit /
  20260722_kraken_ingest_audit, 20260723_c7ext_r_audit) — each papered over with
  a `git checkout --` waiver rather than fixed. A suite that writes into a
  production artifact path is **unauditable evidence provenance**: any run's
  `trades.json` could be a test's scratch output rather than that run's real
  history — the same defect class as C7-EXT (untrusted/ambiguous provenance of
  a decision-input artifact). The STATE W git-status waiver is retired.

# v7 additions — found 2026-07-20 (Dispatch H/J/K arc: perp cost calibration,
independent audit, fee-isolation-pairs follow-up)

## C. Power & validation machinery (continued)

### C12. Inert protocol-declared timeframe: archived runs predating interval threading silently ran at 1h (P1)
- **Symptom:** `tools/run_protocol.py`'s two `run_backtest()` call sites read
  `protocol.get("timeframe", "1h")` and thread it into `interval_seconds` —
  but this logic did not always exist. `git show
  e814b07:strategy-research/tools/run_protocol.py` (the commit that created
  `protocols/escalation_solusdt_4h.json`/`escalation_avaxusdt_4h.json`,
  2026-06-29) contains zero occurrences of `timeframe` or `interval_seconds`
  — at that commit, a protocol's declared `"timeframe": "4h"` was pure
  inert metadata; `run_backtest()` silently fell through to its own 1h
  default regardless of what the protocol file said. Two archived runs
  (`run_028`, `run_030`, evidence for KB finding
  `keltner_scoremode_no_edge`) were executed under this gap: both protocols
  declare `"4h"`, both runs' own `manifest.json` records `data.timeframe:
  "3600s"` (1h). Discovered as a side effect, not by a targeted audit: a
  2026-07-20 cost-recalibration re-run (Dispatch H) used current code
  (interval threading now present and correct) against the same protocol
  files, producing genuinely 4h-resolution bars — the two runs'
  `manifest.json`s disagree, and at the bar level, SOLUSDT's nominal
  2024-08-24 12:00 bar shows `close=157.28` in the original (a true 1h
  slice) vs. `close=159.46` in the 4h-threaded re-run (a 4-hour aggregate)
  — the discriminator that exposed the gap (Dispatch J's independent audit
  of commit `d86f0d0`, `engineering/sessions/session_reports/20260720_perp_calibration_audit.md`).
  This makes any "old vs new" comparison that pairs an archived pre-threading
  run against a current-code re-run of the *same nominally-4h protocol*
  invalid unless both legs are confirmed to share a timeframe via their own
  manifests — the archived leg is silently 1h, not 4h. A caveat documenting
  this was appended to `keltner_scoremode_no_edge` in
  `campaign_knowledge_base.yaml` (`engine_provenance_caveat`,
  2026-07-20) — the original `no_edge_observed` verdict is MAINTAINED, not
  relitigated; no re-derivation at 4h was ordered.
- **Scope note:** this entry documents the CLASS of defect (inert
  protocol-declared timeframe on any run executed before interval threading
  landed) and confirms exactly two known instances (run_028, run_030). It
  does **not** perform a sweep of every other archived run's manifest vs.
  its protocol's declared timeframe to find further instances — that is
  explicitly out of scope for this entry/dispatch and is the Fix/Acceptance
  below.
- **Fix:** a future one-time sweep: for every archived `runs/<id>/results/*/manifest.json`,
  compare `data.timeframe` against that run's own protocol file's declared
  `"timeframe"` field (resolved via `protocol_result.yaml`'s `protocol_file`
  reference, the same lookup Dispatch H/E already used per-run). Any
  mismatch gets the same `engine_provenance_caveat` treatment as
  `keltner_scoremode_no_edge` above — verdicts MAINTAINED by default,
  re-derivation only if separately ordered per finding.
- **Acceptance:** a script or one-off audit producing a table of every
  archived run, its protocol-declared timeframe, and its manifest-recorded
  timeframe, with mismatches flagged; each flagged finding gets a caveat
  entry, not a silent edit and not an automatic re-run.

### C13. Archived candidate configs can fail current V9 validation, blocking re-execution (P1)
- **Symptom:** `rsi_momentum_trending_cost_drag`'s evidence run
  (`run_018`, `runs/run_018/artifacts/candidate_strategy_config.json`) was
  targeted for a Phase 1.2 Kraken-fee calibration re-run (Dispatch H); the
  re-run attempt raised `ValueError: invalid strategy_config` from
  `strategies/main_strategy.py:32` (`AdvancedStrategy.__init__`), which
  calls `tools/validate_config.py`'s `validate()` before constructing the
  strategy. Recorded validator error, verbatim:
  `VIOLATION V9 regime_detector.default_regime: 'trending' is forbidden in
  mode 'threshold_rules' while regime_detector.rules is non-empty. Bars
  that fail every rule still get classified as this regime and traded,
  bypassing the gate. Set default_regime to 'unknown', or -- if no
  rules/gate is intended at all -- clear regime_detector.rules and
  regime_detector.components entirely...`. `run_028`/`run_030`'s
  candidate configs were checked the same way and pass cleanly (0 errors
  each) — this is specific to `run_018`'s artifact, not universal. A
  separate detached-worktree re-check at the parent commit
  (`d86f0d0^`/`102fa8e`) reproduced the identical failure against the
  same on-disk config (Dispatch J's audit,
  `engineering/sessions/session_reports/20260720_perp_calibration_audit.md`, Step 4) —
  confirming this is genuine pre-existing artifact/validator drift (V9
  was evidently added or tightened after `run_018` was produced,
  2026-06-27), not something introduced by any dispatch in this arc.
- **Effect on this arc:** `rsi_momentum_trending_cost_drag` could not be
  re-run at the Kraken/perp calibrated cost (Dispatch H, then again
  implicitly out of scope for the Dispatch K/L fee-isolation pairs, which
  only targeted `keltner_scoremode_no_edge`/run_028+030). Per the
  standing "don't fabricate" STOP discipline, the archived config was
  NOT hand-patched to pass V9 — that would test a materially different
  strategy than the one that actually produced the original KB finding.
  **This does NOT invalidate `run_018`'s original verdict** — the
  original run executed and was evaluated under whatever validator
  existed at the time; V9 tightening after the fact blocks
  *re-execution* today, it does not retroactively un-happen the
  original run. It only means this specific evidence run cannot be
  cheaply re-calibrated to a new venue's fees without either (a) a
  config fix (which changes what's being tested) or (b) a
  point-in-time validator bypass (not attempted, would need explicit
  authorization given it weakens a safety gate).
- **Fix:** not a code fix by default — the likely-correct action is a
  targeted, disclosed edit to `run_018`'s archived
  `candidate_strategy_config.json` (`default_regime: 'trending'` ->
  `'unknown'`, per V9's own suggested remediation) IF and when this
  specific evidence run is re-targeted for recalibration, with the
  change and its rationale recorded alongside whatever re-run consumes
  it (never silently). Broader question, not solved here: how many
  OTHER archived candidate configs across the campaign would also fail
  current validation if re-executed — no sweep has been performed (see
  C12's identical scope note for the analogous timeframe-drift class;
  this may be worth combining into one sweep since both are
  "archived-artifact vs. current-validator/threading drift" instances).
- **Acceptance:** not yet defined for the sweep; for `run_018`
  specifically, a future dispatch that explicitly patches
  `default_regime` and re-runs, citing this ledger entry and disclosing
  the diff between the archived and patched config in its own report.

### C14. CLOSED (2026-07-21) — Venue/product registration-rule mechanism (P1)
- **Symptom:** nothing in the pipeline mechanically enforced Phase 1.2's
  venue/product tradability findings (`docs/analysis-reports/venue_survey_20260719.md`,
  `engineering/sessions/session_reports/20260720_eea_perp_fee_verification.md`) at
  materialization time — a brief declaring an untradable, unconfirmed, or
  undeclared venue/product could still be launched with no `research_only`
  flag distinguishing it from a live-tradable one.
- **Fix:** `strategy-research/config/venue_tradability.yaml` (new file) —
  single source of truth mapping `(venue, product)` pairs to
  `tradable: true|false|unconfirmed`, seeded with Kraken spot (tradable),
  Kraken perp (tradable), Kraken margin (unconfirmed). Any pair absent from
  the table, or a brief declaring no venue/product, defaults to NOT
  tradable — silence never resolves to a green light.
- **Resolution (2026-07-21):** `workflow/run_campaign.py` —
  `_load_venue_tradability()` and `_venue_product_tradable(venue, product)`
  (new module-level helpers, ~line 159, immediately before
  `_parse_brief_frontmatter`), wired into `_materialize_run()` (~line
  207-213): `research_brief["research_only"]` is now set to
  `not _venue_product_tradable(brief.get("venue"), brief.get("product"))`
  before `research_brief.yaml` is written, with one unconditional
  `VENUE-CHECK` log line per materialization (mirrors
  `register_hypothesis`'s plain, no-`dry_run`-kwarg `_log(...)` calling
  convention). `_load_venue_tradability()` caches per resolved `ROOT`-relative
  path (not a single unconditional value) so `tests/conftest.py`'s autouse
  per-test sandbox — which gives every test its own `ROOT` — can't leak one
  test's table into another. Fixtures
  (`tests/test_venue_tradability.py`, reusing the `campaign_root` fixture
  from `test_k4_routing_registration.py` per the same precedent
  `test_k2_verdict_machinery.py`/`test_k3_protocol_pinning.py` already
  established): `test_no_venue_product_declared_defaults_research_only_true`,
  `test_kraken_spot_tradable_research_only_false`,
  `test_kraken_perp_tradable_research_only_false`,
  `test_kraken_margin_unconfirmed_research_only_true`,
  `test_kraken_unlisted_product_research_only_true`,
  `test_unlisted_venue_research_only_true` — all drive `_materialize_run`
  end-to-end and assert the written `research_brief.yaml`'s `research_only`
  key, not just the helper in isolation. Dispatch: "Phase 1.3: venue/product
  registration-rule mechanism" (2026-07-21). Existing brief `.md`/`.yaml`
  files and `campaign_queue.yaml` were not touched — `venue`/`product`
  remain optional, additive fields; a brief that never declares them simply
  gets `research_only: true` by the same default every other undeclared
  pair gets.
- **Acceptance:** met — see fixtures above; full suite 334 passed (328
  pre-existing + 6 new), zero failures.
- **Addendum (2026-07-21, same day):** an independent read-only audit of
  `6791dfe` found two accuracy defects and one operational gap, all fixed
  same-day. (1) `kraken.perp.basis`'s MiFID II appropriateness-questionnaire
  claim was miscited to `engineering/sessions/session_reports/20260720_eea_perp_fee_verification.md`
  (fee-schedule-only, never mentions appropriateness) — corrected to cite
  `docs/analysis-reports/venue_survey_20260719.md` instead, as its own separate sentence; the
  CySEC-342/17 / 0.05%-taker citation to the fee-verification report was
  correct and left unchanged. (2)
  `test_no_venue_product_declared_defaults_research_only_true`'s docstring
  claimed it covered `_load_venue_tradability`'s file-absent branch, but
  `_venue_product_tradable`'s falsy-venue/product early return fires first
  on that fixture, so the file-absent branch was never actually reached by
  any of the 6 original tests — a real coverage gap. Docstring corrected to
  describe the branch it actually exercises; new test
  `test_missing_venue_tradability_file_defaults_research_only_true` added
  (truthy venue/product, `config/venue_tradability.yaml` never written)
  to genuinely cover the file-absent branch. Full suite now 335 passed (334
  + 1 new), zero failures. (3) Operational gap: no existing brief declared
  `venue`/`product`, so C14's mechanism was mechanically wired but inert
  campaign-wide. Per operator ruling (2026-07-21): only
  `briefs/research_brief_XS_momentum.md` was labeled (`venue: kraken`,
  `product: perp` — matches `cost_model.yaml`'s existing PERP CALIBRATION
  precedent for other short-containing strategies; no funding-model blocker
  applies, this is price-based momentum not funding-carry), since it is the
  next brief in the queue to materialize once Phase 2 Track A's data
  blocker clears. All other existing/archived briefs were deliberately left
  undeclared — most were kills already caveated in the ledger, and the
  operator ruled against retroactively editing archived brief files. This
  is a decision, not a gap.

### C15. CLOSED (2026-07-21) — Fee-reduction autopsy field (P1)
- **Symptom:** a cost-dominated kill (`root_cause.mechanism_failure ==
  'signal_real_but_subscale_vs_costs'`) had no mandatory follow-up question
  in the autopsy schema — nothing forced the verdict-interpreter to ask "is
  there a system that reduces these fees?" (maker-only execution, lower-
  frequency variant, different product, venue tier, batching), so a cheap,
  viable variant could go unregistered purely because no one asked.
- **Recon finding (step 3 of this dispatch):** `regime_attribution` — this
  schema's only OTHER field marked "Mandatory" in its own description
  (`workflow_artifacts/schemas/verdict_interpretation.schema.json:70`, "Mandatory for
  regime-gated hypotheses") — has **no code-side enforcement at all**. It is
  absent from both the schema's top-level `required` array and `root_cause`'s
  own inner `required` list (no JSON-Schema conditional-required either);
  `workflow/run_phase1_research.py` never checks for its presence — the only
  "enforcement" is a prompt-level instruction (the IMPROVEMENT 02 handoff
  `constraints` text at `run_phase1_research.py:1531-1536`, and
  `workflow_artifacts/skills/verdict-interpreter/SKILL.md:541-543`'s "you MUST populate"). This
  contradicted this dispatch's own background hypothesis ("likely code-side")
  — there is no established code-side pattern to mirror for a field's mere
  presence. `fee_reduction_assessment` therefore follows the SAME (prompt-
  level-only) precedent for its schema description, plus a NEW, lighter
  print-warning at the `mechanism_failure` routing site — mirroring that
  site's own established warning STYLE (the `⚠️` prefix / labeled-message
  convention at `component_execution_error`/`regime_misattribution`,
  `run_phase1_research.py:4057-4061` and `4076-4082`) without adopting their
  routing behavior (both of those `return "human_pause"`; a missing
  `fee_reduction_assessment` does not — it's a completeness gap in the
  autopsy, not evidence the verdict itself is untrustworthy).
- **Fix:** `workflow_artifacts/schemas/verdict_interpretation.schema.json` — new
  `root_cause.fee_reduction_assessment` object (sibling to
  `mechanism_failure`/`supporting_evidence`/`confidence`):
  `has_fee_reduction_system` (boolean), `candidate_system` (string enum —
  chosen over free text because the ROADMAP's own Phase 1.4 objective text
  already enumerates a fixed, closed vocabulary — `maker_only_execution`,
  `lower_frequency_variant`, `different_product`, `venue_tier`, `batching`
  — matching this schema's established convention of enums for
  classification fields that drive downstream logic, e.g.
  `mechanism_failure`/`confidence`/`regime_attribution.conclusion`, versus
  free text for narrative fields like `supporting_evidence`), and
  `registered_as` (string, optional — the new idea's brief filename).
- **Resolution (2026-07-21):** `workflow/run_phase1_research.py`,
  `determine_post_verdict_route()`, immediately after the existing
  `regime_misattribution` branch (~line 4088 in the pre-edit file, inside
  the `# --- IMPROVEMENT 01: mechanism_failure routing ---` block): when
  `root_cause.get("mechanism_failure") == "signal_real_but_subscale_vs_costs"`
  and `root_cause.get("fee_reduction_assessment")` is falsy, prints a
  two-line `⚠️  Phase 1.4:` warning naming the missing field and restating
  the mandatory question, then falls through to normal routing (no state
  change, no route change). Fixtures (`tests/test_fee_reduction_assessment.py`,
  mirroring `test_circuit_breaker_family_scoping.py`'s
  `test_component_execution_error_is_immune_to_the_breaker` fixture style —
  direct `rpr.ROOT`/`rpr.CAMPAIGN_STATE_PATH` monkeypatch, hand-written
  `verdict_interpretation.yaml`/`pipeline_state.yaml`, calling
  `determine_post_verdict_route` directly, using `status="kill"` so each
  test short-circuits into the lightweight terminal `_route_kill` path
  rather than the much heavier carryover/KB-write fixture the non-terminal
  branches would need):
  `test_fee_reduction_assessment_missing_emits_warning`,
  `test_fee_reduction_assessment_present_suppresses_warning`,
  `test_other_mechanism_failure_never_triggers_fee_reduction_warning`
  (confirms the gate is keyed on `mechanism_failure` specifically, not
  fired for every kill). Suite: 338 passed (335 + 3 new), zero failures.
- **KB retroactive-applicability check (step 6, no action taken — reported
  only, per instruction):** `campaign_knowledge_base.yaml` predates
  Improvement 01's structured `root_cause.mechanism_failure` enum for its
  own `findings:` list entries (they use an older, looser free-text
  `root_cause:` vocabulary) — no finding anywhere in the KB carries the
  literal string `signal_real_but_subscale_vs_costs` (confirmed by direct
  grep). One finding is neverthless genuinely cost-dominated by the SAME
  substantive criterion: `rsi_momentum_trending_cost_drag`
  (`campaign_knowledge_base.yaml:254`, evidence `run_018` — the same
  `run_018` C13 already flagged for unrelated V9-validator drift),
  `root_cause: cost_drag`, `cost_drag_pct: 272.865`, `exhausted_basis`:
  "gross edge is overwhelmed by transaction costs by 2.7×... Structurally
  cost-unviable at this trade frequency." `keltner_scoremode_no_edge`
  (`campaign_knowledge_base.yaml:111`, `cost_drag=84%` cited as
  corroborating evidence) was already confirmed NOT cost-dominated — its
  root cause is `signal_quality` (structural, not cost), per this arc's own
  prior finding. Three other findings
  (`already_priced_in`/`lag_mismatch_to_regime_persistence`/
  `no_informational_content_this_venue`, lines 523/583/789) cite
  `edge_to_cost_ratio` as corroborating evidence of a small edge, but their
  assigned root cause is not primarily cost-dominated. Not retroactively
  edited per instruction — left for the operator to decide as a separate
  follow-up.
- **Acceptance:** met — see fixtures above; schema JSON re-parses cleanly
  (`json.load` round-trip confirmed).

# v8 additions — found 2026-07-22 (Phase 2 Track A: Kraken 5-pair pilot ingestion)

## G. Data & cache layer (new category)

### G1. Exchange-qualified cache key + Kraken bulk-archive pilot ingestion (P1)
- **Symptom (cache-key collision):** `CcxtFetcher.cache_key()` was
  `f"{symbol}_{self.ccxt_timeframe}"` — exchange-agnostic. A Kraken-backed
  `CcxtFetcher` fetching a symbol that lexically matches a Binance one
  (e.g. `BTCUSDT` @ `1h`) resolves to the SAME flat cache file
  (`local_data/BTCUSDT_1h.csv`) already holding Binance candles. Loading one
  would silently return the other venue's data — a wrong-data read, not an
  error. `data/fetchers/base_fetcher.py:211` is the single filename-deriving
  call site (`_csv_path` → `cache_key`), so the collision surfaces everywhere
  cache files are read/written.
- **Fix (decision (a), confirmed correct):** qualify the key with the
  exchange, but keep **Binance UN-prefixed** so every existing on-disk /
  git-tracked Binance cache file loads byte-identically with zero migration;
  only non-Binance venues get the `{exchange_id}_` prefix
  (`kraken_XBTUSD_1h`). `self.exchange_id` is set in `__init__` (line 85)
  before any `cache_key()` call, so both paths are always populated. Verified:
  existing `local_data/BTCUSDT_1h.csv` still loads (74,457 rows, 12-col schema
  intact) via the fixed path; no currently-passing Binance backtest path is
  touched beyond the key derivation.
- **Ingestion (5-pair pilot):** `trading-bot/tools/ingest_kraken_archive.py`
  converts Kraken bulk-export CSVs (headerless, 7-col `unix_s,o,h,l,c,vol,
  trade_count`, unix **seconds**) into the exact 12-col Binance cache schema
  and writes them through the real fetcher plumbing
  (`_merge_and_store`→`_csv_path`→fixed `cache_key`) into the
  exchange-qualified slot a future live Kraken top-up would share. BTC→XBT
  ticker remap hardcoded; DOGE→XDG documented in-code for the full run (not
  ingested here). 1h resolution, USD-quoted. Result: `kraken_XBTUSD_1h`
  (96,381 rows, 2013-10-06→2025-12-31), `kraken_ETHUSD_1h` (87,690),
  `kraken_SOLUSD_1h` (39,743), `kraken_ADAUSD_1h` (63,291),
  `kraken_LINKUSD_1h` (54,430). Cache files land under gitignored
  `local_data/` — data not committed, script/tests/fix are.
- **UTC guard:** the fetch/cache layer does NOT inherit
  `CandleBuilder._align()`'s UTC check (commit `2529f5b`), so the ingester
  asserts its own — first AND last raw unix epoch must map to the stdlib UTC
  wall-clock and survive an ingest→reload round trip unchanged, else
  `IngestUTCError` halts (no silent shift). Verified concretely, not trusted
  from the recon's inferred-UTC.
- **Value-level note (documented divergence, not a bug):** `number_of_trades`
  is populated with Kraken's REAL per-candle trade count (the bulk archive
  carries it); a live `ccxt.fetch_ohlcv` Kraken top-up returns only 6 columns
  and would leave it NaN. Archive rows and future live rows in the same slot
  will therefore differ in that one column. Also: Binance breadth cache is
  USDT-quoted, Kraken pilot is USD-quoted — a venue divergence to keep in mind
  when composing cross-venue breadth.
- **Acceptance:** met — `tests/test_kraken_archive_ingest.py` (6 tests):
  cache-key backward-compat + qualification + no-collision, plus a
  source-vs-ingested round-trip integrity check (row count, first/last UTC
  timestamps, OHLCV/trade-count/quote-vol/close_time spot-checks) and a guard
  that the UTC check fires on an injected shift. Full suite: 44 passed.
- **CARRY-FORWARD (open, NOT resolved here) for the full 20-pair scale-up:**
  1. **HYPE is entirely missing from the archive** (recon `20260721`) — needs
     a separate live `ccxt`-against-Kraken fallback before HYPE can join the
     breadth set.
  2. **Coverage stops 2025-12-31** — the archive is a static year-end export;
     the ~7-month gap (2026-01-01 → today) needs a live-fetch top-up per pair.
     ~~The exchange-qualified slot is designed so that top-up composes
     cleanly~~ — **CORRECTED in G2 (2026-07-22): this claim was FALSE under the
     pilot's `XBTUSD` keying.** A top-up keyed on `XBTUSD` could never fetch
     (`XBTUSD` → `_fetch_remote` → `XBT/USD` → ccxt `BadSymbol`), so the only
     symbol reaching the archive slot was unfetchable. G2 re-keys the archive to
     the standard-base `BTCUSD`, which both hits the same slot AND normalizes to
     ccxt's valid `BTC/USD`. ~~**Top-up composability is now real and proved by
     key derivation (G2 step 7); the top-up fetch itself remains a separate
     dispatch.**~~ — **CORRECTED AGAIN 2026-07-23 (see G3). Overstated, and by
     the same conflation the sentence above it corrects.** Key derivation proves
     the top-up REACHES the right slot with a fetchable symbol. It says nothing
     about whether the endpoint SERVES the history that slot needs — and it does
     not: Kraken's public OHLC endpoint returns a fixed rolling ~720-candle
     window and ignores `since` entirely. Measured seam, verbatim:

     > archive ends **2025-12-31 23:00**; first fetchable bar
     > **2026-06-22 23:00**; gap **4,151 bars / ~173 days**.

     Item 2 therefore **stays OPEN**. Addressability and availability are
     different properties; proving one has now twice been recorded as proving
     the other.
  3. **CLOSED (this commit).** `trading-bot/data/data_manager.py:768`'s
     hardcoded `exchange="binance"` is now an additive `exchange: str =
     "binance"` parameter on `DataManager.fetch_historical_data()` — the one
     public method external callers already reach directly (backtester.py,
     tools/{validate,retune}_regime_detector.py, tools/check_data.py,
     tests/test_funding_rate_component.py all call it un-wrapped; no private
     boundary sits between it and a caller). Reachability proved empirically,
     not just by diff: `dm.fetch_historical_data("XBTUSD", "2013-01-01",
     "2025-12-31", exchange="kraken")` against the real on-disk
     `kraken_XBTUSD_1h.csv` returns 96,381 rows, `datetime64[ns]`, tz-naive,
     2013-10-06 21:00:00 → 2025-12-31 23:00:00 — exact match to the ratified
     ingestion figures. Default unchanged (`exchange="binance"`); every
     existing Binance OHLCV/funding call site still resolves to its original
     unqualified filename (verified: no `binance_BTCUSDT_1h.csv` variant
     created, real `BTCUSDT_1h.csv` load still returns data un-migrated).

- **NEW CARRY-FORWARD (precondition on future work, not a TODO):**
  4. **`FundingRateFetcher.cache_key()` is unqualified — ratified as-is in
     `3d43cc1`, not touched by this commit.** It ignores its own
     `exchange_id` (unlike the `CcxtFetcher` fix in this item), so a
     Kraken-backed `FundingRateFetcher` fetching a symbol that lexically
     matches an existing Binance funding cache (e.g. `BTCUSDT` →
     `BTCUSDT_funding_8h.csv`) will silently collide with/overwrite it —
     the exact wrong-data-read failure mode item 3 above fixed for OHLCV,
     reopened for funding. **Firing condition: this must be closed before
     any dispatch fetches funding-rate data from a second venue** — today
     it is latent and inert because every current `FundingRateFetcher`
     instance is Binance-only, but the moment a second-venue funding fetch
     is dispatched, the collision is live. Do not defer this a second time
     once that dispatch is on the table.

- **Informational (not carry-forward-blocking):**
  - `base_fetcher.py:226`'s `_load_local` now asserts the parsed `timestamp`
    column is tz-naive and raises `ValueError` (not silently caught — the
    check sits outside the surrounding read try/except so it actually
    propagates) if a future writer emits offset-carrying timestamp strings.
    Verified this cannot fire on any currently-cached file: swept every CSV
    directly under `local_data/` plus the 26GB `Kraken_batch/` archive for
    offset/`Z`-suffixed timestamps — none found. `utc=True` was deliberately
    NOT added to the parse call itself (would flip the dtype to tz-aware and
    break the naive-datetime comparisons at `base_fetcher.py:196-197`,
    `fear_greed_fetcher.py:141`, `data_manager.py:849`, `launcher.py:585`);
    the convention is enforced, not changed.
  - The test suite is not invocable from repo root with plain `pytest` — it
    ignores `trading-bot/pytest.ini`'s `testpaths`/`-m "not slow"` scope and
    collects unrelated slow/erroring tests outside it. Pre-existing, unrelated
    to this commit, informational only.

### G2. Kraken symbol convention settled + 20-pair breadth scale-up (P1)

- **Falsified premise (the reason this dispatch existed):** G1's ingestion
  stored the archive under Kraken's legacy altname base — `XBTUSD` → cache_key
  `kraken_XBTUSD_1h` — and asserted (script docstring L11-15, G1 carry-forward
  2) that "a future live top-up lands in the SAME slot… the archive and the
  live feed compose cleanly." **This was false.** `CcxtFetcher._fetch_remote`
  normalizes a compact symbol to `BASE/QUOTE` before calling ccxt; `XBTUSD` →
  `XBT/USD`. A top-up keyed on `XBTUSD` therefore hits the archive slot but
  **cannot fetch** — `XBT/USD` is not a symbol ccxt's Kraken adapter accepts.
- **Evidence that falsified it (read-only `load_markets()` against the live
  adapter, no cache touched):**
  - `market('BTC/USD')` → resolves, id `XXBTZUSD`. **`BTC/USD` is the unified
    symbol.**
  - `market('XBTUSD')` → `BadSymbol` (it is only an *altname*, not a key).
  - `market('XBT/USD')` → `BadSymbol` (not a key, not even an altname).
  - Confirms the director's reading exactly: **XBTUSD is unfetchable; BTC/USD
    is the unified form.** Same pattern for DOGE: unified `DOGE/USD`, altname
    `XDGUSD`. All other 18 breadth bases: unified `<BASE>/USD`, altname
    `<BASE>USD` (standard base == altname base), so they were never affected.
- **Decision (step 3) — store under the STANDARD-base compact symbol
  `<BASE>USD`** (`BTCUSD`, `DOGEUSD`; not `XBTUSD`/`XDGUSD`), cache_key
  `kraken_BTCUSD_1h`. Source file still located via Kraken's altname
  (`XBTUSD_60.csv`) — the script now separates `kraken_source_pair()` (altname,
  disk) from `cache_symbol()` (standard base, cache key). Satisfies all three
  constraints **without touching `cache_key()`**:
  - (a) filesystem-safe — `kraken_BTCUSD_1h.csv` has no `/`; the unified
    `BTC/USD` cannot be a filename.
  - (b) top-up resolves to the same slot AND fetches — `BTCUSD` → cache_key
    `kraken_BTCUSD_1h` (identical slot) and `_fetch_remote` normalizes
    `BTCUSD` → `BTC/USD` (ccxt's accepted unified symbol). Proved by key
    derivation, not by a live fetch (step 7): a `CcxtFetcher(exchange="kraken",
    symbols=["BTCUSD"])` derives `kraken_BTCUSD_1h` == the on-disk archive slot.
  - (c) `cache_key()` untouched — Binance stays `BTCUSDT` → `BTCUSDT_1h`
    unprefixed (ratified decision (a)); this is purely the `symbol` string the
    ingester / a future top-up hands the fetcher.
- **Migration:** only the two legacy-ticker pairs diverged. BTC re-keyed
  `kraken_XBTUSD_1h.csv` → `kraken_BTCUSD_1h.csv` (regenerated from source by
  the ingestion script; stale file removed). ETH/SOL/ADA/LINK were already at
  the standard base and are byte-unchanged. Verified by reload, not assumption:
  BTC 96,381 rows, 2013-10-06 21:00 → 2025-12-31 23:00 — exact match to the
  ratified pilot figures.
- **20-pair coverage (19 ingested; HYPE absent from the archive — G1 item 1
  confirmed, `HYPEUSD_60.csv` does not exist).** `full%` = missing/expected
  over the pair's whole history; `2017+%` = same restricted to 2017-01-01
  onward (the breadth-viability signal; pilot BTC benchmark = 0.11%):

  | asset | cache_key | rows | first | last | full% | 2017+% |
  |---|---|---:|---|---|---:|---:|
  | BTC | kraken_BTCUSD_1h | 96,381 | 2013-10-06 21:00 | 2025-12-31 23:00 | 10.14 | 0.11 |
  | ETH | kraken_ETHUSD_1h | 87,690 | 2015-08-07 14:00 | 2025-12-31 23:00 | 3.83 | 0.17 |
  | XRP | kraken_XRPUSD_1h | 75,440 | 2017-05-18 15:00 | 2025-12-31 23:00 | 0.19 | 0.19 |
  | SOL | kraken_SOLUSD_1h | 39,743 | 2021-06-17 15:00 | 2025-12-31 23:00 | 0.15 | 0.15 |
  | ADA | kraken_ADAUSD_1h | 63,291 | 2018-09-28 13:00 | 2025-12-31 23:00 | 0.54 | 0.54 |
  | SUI | kraken_SUIUSD_1h | 22,522 | 2023-05-03 12:00 | 2025-12-31 23:00 | 3.60 | 3.60 |
  | ZEC | kraken_ZECUSD_1h | 76,449 | 2016-10-29 00:00 | 2025-12-31 23:00 | 4.94 | 4.73 |
  | DOGE | kraken_DOGEUSD_1h | 50,232 | 2019-12-19 18:00 | 2025-12-31 23:00 | 5.05 | 5.05 |
  | HYPE | — (absent) | — | — | — | — | — |
  | XMR | kraken_XMRUSD_1h | 77,317 | 2017-01-02 19:00 | 2025-12-31 23:00 | 1.94 | 1.94 |
  | LTC | kraken_LTCUSD_1h | 84,563 | 2013-10-24 13:00 | 2025-12-31 23:00 | 20.85 | 1.38 |
  | ONDO | kraken_ONDOUSD_1h | 15,089 | 2024-04-11 14:00 | 2025-12-31 23:00 | 0.11 | 0.11 |
  | NEAR | kraken_NEARUSD_1h | 30,775 | 2022-06-16 14:00 | 2025-12-31 23:00 | 0.94 | 0.94 |
  | LINK | kraken_LINKUSD_1h | 54,430 | 2019-09-25 14:00 | 2025-12-31 23:00 | 0.94 | 0.94 |
  | TAO | kraken_TAOUSD_1h | 13,159 | 2024-07-01 00:00 | 2025-12-31 23:00 | 0.13 | 0.13 |
  | AVAX | kraken_AVAXUSD_1h | 35,285 | 2021-12-21 15:00 | 2025-12-31 23:00 | 0.08 | 0.08 |
  | TRX | kraken_TRXUSD_1h | 50,331 | 2020-03-05 14:00 | 2025-12-31 23:00 | 1.42 | 1.42 |
  | AAVE | kraken_AAVEUSD_1h | 44,001 | 2020-12-15 14:00 | 2025-12-31 23:00 | 0.49 | 0.49 |
  | INJ | kraken_INJUSD_1h | 36,298 | 2021-08-10 15:00 | 2025-12-31 23:00 | 5.73 | 5.73 |
  | UNI | kraken_UNIUSD_1h | 45,507 | 2020-10-15 13:00 | 2025-12-31 23:00 | 0.39 | 0.39 |

  **Breadth-viability flags (2017+ gap rate materially above the 0.11%
  pilot):** INJ 5.73%, DOGE 5.05%, ZEC 4.73%, SUI 3.60%, XMR 1.94%, TRX 1.42%,
  LTC 1.38% (LTC's 20.85% full-history figure is the 2013–2015 illiquid era,
  benign; its 2017+ rate is 1.38%). All are single-digit% and consistent with
  Kraken's "row only when trades occurred" export semantics (listing-era
  front-loading), but INJ/DOGE/ZEC at ~5% post-2017 should be sanity-checked
  before those pairs carry weight in a breadth signal — not a formatting
  detail.

- **NAMED PIPELINE DEFECT — `_load_all()` write-on-read hazard:**
  `BaseFetcher._load_all()` (`data/fetchers/base_fetcher.py:183-184`) re-saves
  the cache whenever `pieces` is non-empty — **including when every remote
  fetch failed and `pieces` is just `[existing]`.** So `get_data()` /
  `fetch_historical_data()`, nominally a *read*, mutates the on-disk cache any
  time the requested window has a gap (a prepend/append/internal-gap missing
  period). Benign when the re-fetch returns nothing (content-identical
  rewrite), but under the settled convention `BTCUSD` → `BTC/USD` is a **valid
  live symbol**, so a read over a gappy window would now hit the network and
  fold live rows into the archive cache. **Standing read-only rule (effective
  this dispatch, all future work): when the intent is a read-only check, do not
  invoke a path that can write.** Concretely: never call `get_data()` /
  `fetch_historical_data()` over a window with internal gaps as a "read"; read
  the CSV directly, or scope the window to a gap-free range. The reachability
  test enforces this by reading the audited-gap-free BTC-2022 window (0 missing
  → 0 fetch → 0 re-save; verified: BTC cache md5 unchanged across the suite).
  Fixing `_load_all` to not persist on an all-failed fetch is a separate,
  desirable change (out of scope here) — logged so it is not rediscovered.

- **Acceptance:** met. `tests/test_kraken_archive_ingest.py` extended to 15
  tests (store-symbol standard-base vs source-altname split; top-up
  normalization invariant `BTCUSD`→`BTC/USD` per pair; top-up key == archive
  slot; gap-stat arithmetic; round-trip integrity now asserts
  `kraken_BTCUSD_1h`). `tests/test_kraken_cache_reachability.py` migrated to the
  `BTCUSD` slot over the gap-free window. Full suite: **57 passed / 10
  deselected** (baseline 48/10, +9 new).

### G3. Engine panel-support blocker (first-class) + research-path vectorized backtester + XS_momentum run (P1)

- **First-class engine blocker (dispatch step 1, same class as P4_ts_trend's
  daily-bar gap).** The production `BacktestEngine` CANNOT express a
  cross-sectional / panel strategy. Three concrete gaps, each a hard stop for a
  panel book on the production path:
  - **Single-symbol data load.** `core/backtester.py:92`
    (`fetch_historical_data(self.symbols[0], ...)`) and `:359`
    (`extract_historical_price_data` returns `self.symbols[0]` only) load exactly
    one symbol. The simulate loop iterates `self.symbols` but every downstream
    artifact path is `symbols[0]`-scoped.
  - **Unpartitioned RollingBuffer.** `strategies/main_strategy.py:44` — one shared
    indicator buffer, no per-symbol partition, so a component fed interleaved
    multi-symbol bars would cross-contaminate history.
  - **Zero netting hooks.** `execution/` has no cross-asset dollar-neutral /
    long-short netting; `forecast_manager.forecast_to_allocation` maps a single
    symbol's forecast to a single allocation.
  - **Scope ruling (dispatch):** these production files were NOT modified — a
    panel book is a research-only path until the engine gains partitioned,
    multi-symbol, netting-capable support. Annotated in the KB finding
    `xs_momentum_cost_surviving_but_decaying.run_path`.

- **Delivered: `strategy-research/tools/panel_backtester.py`** (research-only; no
  import of / edit to any production engine path). Ports the engine's OWN metric
  formulas verbatim (`performance/metrics.py::calculate_sharpe_ratio` /
  `calculate_max_drawdown` / `_calculate_standard_metrics`;
  `reporting/run_artifact.py::build_core`) so its accounting is provably
  engine-equivalent. Two commands: `gate` (validation) and `xs` (the panel run).

- **VALIDATION GATE — PASS (the entire safeguard; dispatch steps 2-3).**
  Reproduced ALL 30 window-symbol slots of archived run_054 (P4_ts_trend,
  `SmaTrendLongOnlyComponent` L=100, daily, long-only, Binance daily data, default
  10 bps, initial 1000). **Pre-registered tolerance, declared before comparison:**
  trade_count EXACT; sharpe |Δ|<=0.10; net_return_pct |Δ|<=0.5pp-or-2%rel;
  max_drawdown_pct |Δ|<=0.5pp; fees/gross/net <=2%rel. **Actual: exact to 3dp on
  net_return_pct / sharpe / max_drawdown_pct / trade_count across all 30 slots**
  (fees/gross/net within 2%) — far tighter than the bands. Engine accounting
  reconstructed and verified line-by-line against run_054 trades.json (matched_qty
  = (V/Pe)(1-r); entry_comm = matched*Pe*(r/(1-r)); final_pv = V(1-r)(Px/Pe)).
  The one non-trivial alignment: the engine's +2h resample (already on record, KB
  `er_gate_execution_alignment_caveat`) makes its bar labeled D carry the raw
  CSV's D+1 close and drops ~2 trailing rows/window; the gate scores raw rows
  [start+1d, end-2d] to match, and reproduction became exact — an independent
  cross-check of that documented caveat.

- **XS_momentum run (dispatch steps 5-7), research path, Kraken perp cost
  (`cost_model.yaml` `perp` block, 5 bps one-way, funding not modeled — valid,
  price-based signal; reused, not re-derived).** Mechanics all enforced: no
  forward-fill into ranking (NaN-at-t or NaN-at-t-L excludes the asset);
  dollar-neutral long-top-third / short-bottom-third; pointwise listing via NaN;
  rank at t uses data through t, positions effective t+1. 19-pair panel,
  2017-05-18 → 2025-12-31, 75,520 hourly bars, min n=6 (first reached 2017-05-26),
  7-day trailing-return momentum, daily rebalance.
  - **Headline: net Sharpe 1.325 (gross 1.665)**, net return +23,742% (compounding
    of two explosive years 2017/2020; Sharpe is the trustworthy metric), max DD
    -62.3% at 200% gross (~-31% at unit gross; Sharpe scale-invariant), annualized
    turnover 423x.
  - **NOT cost-dominated** (cost drag ~0.34 Sharpe). **No lookahead** (net Sharpe
    RISES 1.33→1.42→1.51 as exec lag goes 1→2→4 bars). Positive net Sharpe every
    year 2017-2024 but **decaying** — post-2021 net 0.77, 2025 net 0.07 (2025
    cumulative -6.3%).
  - **C7-style verdict: REFINE (positive lean).** Overall/median net Sharpe > 0
    clears the promote Sharpe bar; DD > 30% bar (leverage-convention-dependent) =>
    not a clean promote; well above kill; not cost-dominated. Phase-1.4
    fee_reduction_assessment autopsy NOT triggered (not a cost-dominated kill).
  - **The fork to a vectorized research path is VINDICATED:** a real,
    cost-surviving cross-sectional edge exists across the broadened universe (the
    question the brief posed), justifying investment in production engine panel
    support — with the caveat that the forward-looking edge is the decaying recent
    figure, not the full-sample 1.33.
  - **Strongest single threat:** cost/venue anachronism × early-era dominance —
    return is dominated by 2017/2020 (small-n, illiquid, pre-perp era for most
    alts) costed at a flat modern 5 bps; the era where 5 bps is most credible
    (recent, liquid) is where the edge is weakest. See KB finding for full text.

- **Acceptance:** `panel_backtester.py gate` prints all 30 slots OK / GATE RESULT:
  PASS; `panel_backtester.py xs` reproduces the headline metrics and robustness
  table above. Registered: KB finding `xs_momentum_cost_surviving_but_decaying`;
  `campaign_queue.yaml` XS_momentum outcome updated. No production `trading-bot/`
  file touched.

---

# v8 additions — found 2026-07-22 (ungated-verdict audit)

### C7-EXT. The ungated-verdict defect chain — a verdict issued with no
pre-registered rule, and four independent checks missing at once (P0, CLOSED
2026-07-22)

- **Symptom.** `campaign_knowledge_base.yaml` recorded `verdict_c7: refine`
  for XS_momentum, and `campaign_queue.yaml` recorded
  `outcome: refine_research_path_edge_real_cost_surviving_but_decaying`. Neither
  was a gated verdict. XS_momentum was pre-registered under **no pass_rule at
  all**: `briefs/research_brief_XS_momentum.md` has no `pass_rule` and no
  `machine_constraints` (its only mention of the latter is line 106 — prose
  telling a future editor to decide them at unblock time), no `runs/` directory
  or `pre_registration.yaml` exists for it, and it executed on the vectorized
  research path, so `tools/verdict_criteria_evaluator.py` never ran. The tool,
  the run, the KB finding and the verdict all landed in a single commit
  (`6c4df3d`) — nothing was frozen before the result was known.

- **The "30% DD bar" it was adjudicated against was never a frozen rule.** Its
  sole provenance is the generic fallback dict at
  `workflow/run_phase1_research.py:1681-1682` (mirrored in
  `protocols/baseline_v1.json`): `median_sharpe_gt: 0`,
  `max_abs_drawdown_pct_lt: 30`, `min_trade_count_gte: 20`,
  `kill_median_sharpe_lt: -1`. **That dict is the C7 symptom, verbatim**
  ("protocol_result.yaml issued verdict: refine from generic code thresholds
  (min_trades>=20, drawdown caps)") — and it was still live in the tree while
  C7 was recorded CLOSED in this ledger's own sequencing section. C7 fixed the
  evaluation path and left the materialization path untouched. **A ledger item
  marked closed on a partial fix is worse than one left open**: it stops anyone
  looking.

- **Ruling on the underlying hypothesis.** Not a kill. Even scored against the
  generic block, DD fails `< 30` on either leverage convention (−31% unit
  gross, −62.3% at 200% gross), but that block's kill trigger is a separate
  explicit criterion — `kill_median_sharpe_lt: -1` — against a measured net
  Sharpe of 1.325. Failing a promote bar is not a kill. Since nothing was
  pre-registered, neither branch was ever binding. Status: **ungated / verdict
  void** — not refine, not kill. The measurements stand (the panel backtester
  passed a genuinely pre-registered 30-slot reproduction gate against run_054);
  they are simply not a verdict.

- **The four-link chain, and the gate that closes each.**

  | Link | What was missing | Gate |
  |---|---|---|
  | (a) | Kraken **perp**, daily rebalance (~24h) against an 8h funding interval — ~3 funding accruals per holding period, funding never modeled, annotated "valid: price-based signal, not funding carry". Funding is a cost of *holding*, not a signal input. | **G1** cost-model completeness: perp + holding > funding interval ⇒ funding must be modeled or bounded-with-citation, else `VERDICT_BLOCKED` |
  | (b) | Sharpe 1.325 reported with no skew, no kurtosis, no tail statistic — a second-moment summary standing in for a distribution it cannot describe. **This link remained open through the entire C7 closure.** | **G2** distribution stats mandatory alongside any Sharpe |
  | (c) | Headline 1.325 dominated by 2017 (+416%) and 2020 (+476%); the most recent full year was net Sharpe 0.07 / −6.3%, present in the record but never surfaced as the deployable figure. Both true; only one deployable, and only the other reached the verdict. | **G3** mandatory `deployable_today` (most recent full year, current costs) |
  | (d) | Net Sharpe **rising** with execution lag (1.33 → 1.42 → 1.51) recorded as `no_lookahead_confirmed: true`. The narrow inference (no same-bar lookahead) is sound; a signal that improves the later you trade it is still an anomaly, and it was filed as reassurance rather than investigated. | **G4** anomalous robustness result requires a written mechanism before any verdict stands |

- **Three structural gates beyond the four.** The four above are all *inside*
  the machinery, and none would have caught this run, because this run never
  entered the machinery:
  - **G5 — preconditions are pass_rule-independent and dominate.**
    `legacy_not_evaluable` was the hole: with no pass rule, K2 routed the run
    to stage discretion, and stage discretion has never heard of G1-G4. The
    preconditions now evaluate whether or not a pass rule exists and
    short-circuit to `VERDICT_BLOCKED` in front of every one of the kernel's
    exits. `VERDICT_BLOCKED` is not PASS, not FAIL, and specifically not
    `legacy_not_evaluable` — it cannot fall through to anyone's judgment. A
    blocked verdict is not a failed hypothesis; it is inadmissible evidence.
  - **G6 — no verdict enters the KB or queue except through the evaluator.**
    This is the link that let a research-path tool write `verdict_c7` with no
    pass rule, no evaluator call and no run directory. A verdict field is now
    admissible only alongside a `pass_rule_evaluation_ref`; an entry without
    one must record `verdict_status: ungated` and keep its measurements.
    Enforced over the whole findings list on every KB write, so a hand-edited
    entry cannot ride in behind a legitimate one.
  - **G7 — the generic promotion fallback fails loudly.** The dict at
    :1681-1682 is replaced by `_require_pre_registered_promotion()`, which
    raises `UngatedProtocolError`. A missing pass rule is a registration defect
    to fix in the brief, never a gap for code to paper over.

- **Acceptance.** `tests/test_c7ext_verdict_gates.py` — 29 tests, one or more
  per gate, plus a regression that walks the XS_momentum shape end-to-end and
  asserts it trips **all four** preconditions and can emit no verdict. Suite
  338 → 369 passing. Five existing tests were repointed, not weakened:
  `test_k2_verdict_machinery.py`'s known-answer and R3 fixtures now call
  `_resolve_pass_rule` (the resolution semantics they exist to pin, unchanged),
  with `test_c7ext_run_057_is_blocked_at_the_public_entry_point` added so the
  new gate is pinned rather than hidden by the repointing.
  `test_prereg_conformance_gate.py`'s fixture keeps run_047's real
  constraints verbatim as evidence — run_047 was itself materialized from the
  generic default — and a new test asserts they are now refused.

- **Correction to the campaign's own count.** The audit dispatch expected the
  honest gated-verdict count to be 1. It is **2**: `H-041-C-v2` and
  `FUNDING_MR_DAILY_RETEST` both carry real B11 total mappings in their briefs.
  XS_momentum is the only entry whose verdict was withdrawn. Pinned by
  `test_campaign_honest_verdict_count`.

- **Method note.** Every one of the four content gaps was visible in the
  as-written record on 2026-07-22 and none was caught by machinery — they were
  caught by a director reading carefully. That is the failure mode this entry
  exists to remove: an integrity layer that depends on someone noticing is not
  an integrity layer.

---

# v9 additions — found 2026-07-22 (independent audit of C7-EXT; remediation C7-EXT-R)

## H. Verdict integrity (continued)

**C7-EXT-R — the C7-EXT gates were audited independently and did not hold.
Five findings remediated, two carried forward.** Audit:
`engineering/sessions/session_reports/20260722_c7ext_audit.md` (committed before this work
began, unchanged by it). Verdict of that audit: DO NOT RATIFY, two of three
STOP conditions fired.

**What the audit found, and what was done about it.**

- **D-4 — G6 was bypassable in the exact shape of the incident it closed.**
  It gated the field names `verdict_c7` / `hypothesis_verdict` / `verdict`. The
  campaign records verdicts in **`outcome`**. So `{"outcome":
  "kill_mechanism_falsified"}` was ACCEPTED — and that is the shape
  `_write_kb_findings_entry` itself emits, meaning the validator was a
  structural no-op on every entry the orchestrator wrote. A forged
  `pass_rule_evaluation_ref` was ACCEPTED because the ref was never resolved.
  The queue writer was never validated at all: the function had exactly one call
  site in the repository.
  Fixed: `outcome` is gated via `outcome_is_verdict_bearing()`;
  `resolve_evaluation_ref()` requires the artifact to EXIST, to BELONG to one of
  the entry's own runs, and to have recorded a binding PASS/FAIL;
  `run_campaign._save_queue` validates every entry before writing; and
  `tools/lint_verdict_provenance.py` checks both stores standalone, with no write
  involved, because a hand edit was previously unchecked until some unrelated
  orchestrator write happened to look.
  Also fixed, and not in the audit: `_write_kb_findings_entry` could not have
  satisfied the repaired gate, because it wrote a bare `outcome` with no
  provenance at all. It now stamps `verdict_status` from what is on disk
  (`_verdict_provenance_stamp`) — gated with a citation if the evaluator really
  ran, ungated otherwise.

- **D-5 — the gated-verdict count was 2; it is 1.** H-041-C-v2 was counted
  despite `runs/run_058/artifacts/` containing no `pass_rule_evaluation.yaml`,
  no `protocol_result.yaml` and no `prescreen_result.yaml`; the entry's own
  `exhausted_basis` already said the registered evaluation "was NEVER EXECUTED".
  It was rejected by an LLM validation stage before its pass_rule ever ran —
  stage discretion, which G5's own doctrine excludes. Re-recorded as
  `stage_discretion_rejection_no_gated_verdict` / `verdict_status:
  stage_discretion`, with the prior label retained in
  `outcome_history_superseded` and the rejection's own reasoning untouched.
  `test_campaign_honest_verdict_count` no longer string-matches
  `completed_rejected`; it asserts gatedness from evaluator-artifact existence
  via `honest_verdict_count()`. **The one gated verdict in this campaign is
  FUNDING_MR_DAILY_RETEST (run_059).**

- **D-6 — run_057 was the uncorrected twin of XS_momentum.** Its pass_rule is
  pre-registered under `machine_constraints.pass_rule`, invisible to the
  top-level-only lookup; no `pass_rule_evaluation.yaml` was ever written; a
  `kill` was recorded into both stores anyway. `_find_pass_rule` now checks both
  locations. **Honest limit, stated because it changes the conclusion:** finding
  run_057's rule does not make it evaluable — it is a legacy prose string and
  still resolves to `legacy_not_evaluable`. The verdict was human-adjudicated
  end to end.
  Re-adjudicated from the archived artifacts (**no backtest re-run**): of 30
  window-symbols, **29 fall below the five-trade floor, and the entire run holds
  exactly ONE non-null per-window Sharpe** — ETHUSDT 2022-10, −0.686, on 5
  trades; BTCUSDT has zero evaluable windows. Criterion (a) therefore rested on a
  median over one window on one symbol, while criterion (b) — the only criterion
  with a real sample, n=42 — passed on sign. Relabelled
  `kill_er_gate_mechanism_falsified` → `ungated_er_gate_variant_too_sparse_to_evaluate`.
  The S2 identity-matched anti-selection evidence (excluded entries +1395.9 bps
  vs included +433.7 bps, 42/42 reconciled) does not depend on the sparse Sharpe
  and is explicitly retained.

- **D-3 — G7 was cosmetic.** It guarded protocol GENERATION while the abolished
  block stayed live in committed files and in two silent defaults.
  `_assert_promotion_ratified` now runs at protocol SELECTION, on every branch
  of `_resolve_protocol_path`, and the implicit `baseline_v1.json` default for a
  `forced_diagnostic` with no named protocol is gone.
  **Correction to the audit:** it said seven committed protocol files carry the
  generic block. Recounting from the tree gives **nine** — `baseline_v1`,
  `baseline_v2`, four `escalation_*`, and three `run_0NN_generated`. All nine are
  now marked `promotion_provenance: {status: generic_unratified, ratified_by:
  null}`, which makes selecting them fail loudly. They were deliberately NOT
  ratified: ratification is a claim that a human adopted those four numbers on
  purpose, and no agent may make it on their behalf.

- **D-1 — the kill-routing path was unpinned.** After C7-EXT's repointing, every
  public-entry assertion in the suite was `VERDICT_BLOCKED`, `PASS`, or
  `legacy_not_evaluable`. Mutating `evaluate_pass_rule_criteria` to stop calling
  the kernel was caught by a single PASS-path test.
  `test_d1_fail_routes_to_kill_terminate_through_the_public_entry` pins
  FAIL → kill / terminate end-to-end; re-running that mutation now fails two
  tests including this one.

**WHAT THESE GATES ARE, AND ARE NOT — read before trusting a MET precondition.**
G1–G4 are **presence checks, not content checks**. They establish that a
required figure was reported. They do not establish that it was reported
carefully, and the audit demonstrated exactly this: `skew: 0, kurtosis: 0,
var_95: 0` clears G2; `cost_basis: ""` and `net_sharpe: "n/a"` clear G3;
`mechanism_explanation: "."` clears G4. **They catch omission, not
carelessness.** Nothing in C7-EXT-R changes that, and no MET precondition should
be read as a quality warrant.

**OPEN carry-forwards — not fixed, not scheduled, recorded so they are not
mistaken for closed.**

- **D-2 (open).** G4 detects no anomalies. It requires prose for anomalies the
  artifact's author volunteers via `anomalous: true`. The XS_momentum lag
  response — net Sharpe RISING with execution delay, 1.33 → 1.42 → 1.51 — clears
  G4 untouched if nobody sets the flag, which is precisely the judgement that
  failed the first time. Needs a mechanical detector (e.g. auto-flag a
  monotone-improving robustness sweep).
- **D-7 (open).** G1's product allowlist is exact-match against a free-text
  brief field: `product: "perpetual swap"` reads as not-a-perp and clears the
  funding gate. A brief-supplied `funding_interval_hours` is trusted without
  bound. G2/G3 accept placeholder and wrong-typed values as shown above.

**Method note.** The audit was performed by a model that did not write C7-EXT,
verified by recomputation rather than by reading the commit message, and its two
STOP conditions were both real. The C7-EXT commit message asserted the chain was
closed; it was not. An integrity layer that is checked only by its own author is
not yet an integrity layer — which is the same lesson C7-EXT itself recorded, one
level up.

---

# v10 additions — found 2026-07-23 (re-audit of C7-EXT-R; remediation C7-EXT-R2)

## H. Verdict integrity (continued)

**C7-EXT-R2 — G6 failed THREE TIMES by name-enumeration. Replaced with a closed
schema.** Re-audit: `engineering/sessions/session_reports/20260723_c7ext_r_audit.md` (committed
before this work, unchanged by it). Verdict: DO NOT RATIFY, G6 bypassable on
five independent routes.

**The three failures, by name, because the pattern is the finding.**

1. **C7-EXT (0a4d606)** gated three field names:
   `_VERDICT_FIELDS = ("verdict_c7", "hypothesis_verdict", "verdict")`.
   Defeated by `{"outcome": "kill_mechanism_falsified"}` — the field the KB and
   queue actually use, and the one `_write_kb_findings_entry` itself emits.
2. **C7-EXT-R (2c8b8d1)** added `outcome`, then replaced the three-name denylist
   with a substring marker: any key containing the literal ASCII word "verdict".
   The commit message called this *"New name, same gate"*. Defeated by
   `status: kill`, `disposition: kill`, `resolution: kill`, `result: kill`,
   `decision: kill`, `conclusion: kill`, `urteil: kill`, `veredicto_c7: kill`,
   and by nesting a verdict one level down or inside a list. Only `verdicto` was
   caught, and only because the English word is a literal prefix of the Spanish
   one — a gate working by linguistic coincidence.
3. Both rounds made the **same move**: enumerate what is forbidden. The set of
   names an author might choose is unbounded, spans languages, and grows with
   every synonym. A denylist over an infinite set is a guess; broadening the
   guess is not a different class of fix, which is why round 2 fell as fast as
   round 1.

**Why the closed schema is a different class.** `tools/record_schema.py` inverts
the polarity: a KB finding or queue entry may contain **only** the fields the
schema enumerates, each with a declared value SHAPE, and anything else is
rejected wherever it appears. `details`, `decisions`, `urteil` are not refused
because they are recognised as dangerous — they are refused because they are not
on the short list of permitted fields. Nobody has to anticipate them.

Depth is enforced by **shape, not by nested name lists**: no shape lets an
arbitrary key hold an arbitrary structure. `signal_property` legitimately holds
66 distinct measurement keys, so its keys cannot be enumerated — but its shape
can be (flat scalars only), which is what refuses
`signal_property: {nested: {verdict: kill}}` without knowing the word "verdict".

Second, name-agnostic rule: a **bare verdict token as a VALUE** is refused
everywhere except the one designated field. Anchored whole-value, so prose that
discusses a verdict is untouched while `kill_mechanism_falsified` is not. This
catches `urteil: kill` and `anything_at_all: kill` identically, because it looks
at the claim rather than the label.

To smuggle a verdict now requires both a permitted field AND a non-verdict
value — at which point you have written data, not a verdict.

**Path traversal (blocking, re-opened D-4).** The run-ownership check
substring-matched the **unresolved** path, so
`runs/run_999_FAKE/../run_059/artifacts/pass_rule_evaluation.yaml` with
`evidence_runs: ["run_999_FAKE"]` passed (the literal text does contain
`/runs/run_999_FAKE/`) while `open()` followed the `..` to run_059's real FAIL.
A fabricated hypothesis citing a run that never executed borrowed a genuine
result. Now resolved to an absolute real path FIRST, then containment-checked
against the resolved directory of a run the entry actually names.

**A sixth bypass, found while implementing and named rather than silently
fixed.** With no `evidence_runs`/`run_ids`/`run_id`, the ownership check was
skipped outright (`if run_ids:`), so an entry naming no run at all could cite any
evaluation in the tree and be accepted. An entry claiming a verdict must now say
which run earned it.

**One named exemption from the token rule, stated rather than left implicit.**
`outcome_reason` legitimately holds the orchestrator's prescreen ROUTE NAME
(`kill_no_ic`, `refine_inverted_ic` — exactly the keys of `_VERDICT_TO_OUTCOME`)
as well as multi-paragraph prose, so it cannot take the token rule. It is safe
because it is subordinate by construction: it explains `outcome`, is never read
as an independent verdict, and rides on an entry whose `outcome` was gated in the
same pass. Named here because an unexamined exemption is how the previous three
rounds failed. Three further fields (`validation_gate: PASS`,
`relation: refine`, `source`) collide with the token rule and were given closed
vocabularies of their own instead — tighter than free text, not looser.

**THE HONEST DENOMINATOR — record this wherever "zero confirmed edges" is
asserted.** Full census of all 59 runs (re-audit §3, independently reproduced):

- **1 of 59 (1.7%)** passed through the C7 mechanical gate to a binding result:
  run_059. That is the campaign's entire gated evidence base.
- **58 of 59 (98.3%)** never had their fate decided by that gate.
- Of the 59, **22 runs** are named by at least one terminal-outcome KB/queue
  entry; **37 are named by none** — intermediate or superseded steps within a
  lineage, never independently adjudicated at all.
- Rule shapes: 1 structured and evaluated (run_059), 1 structured but never
  evaluated (run_058), 1 prose/legacy (run_057), 56 with no rule at all.

Every "no edge" finding in this archive other than run_059's is a human/LLM call,
a prescreen-threshold kill, or an intermediate step with no independent verdict.
The campaign's "zero confirmed edges" claim is true, and it rests on **one**
mechanically-gated result out of 59 runs. Stating the denominator is not a
caveat; omitting it implies uniform gate coverage that does not exist.

**ACCEPTED RISK — operator proportionality ruling, 2026-07-23.** No
filesystem-only provenance check can distinguish a genuine evaluator-produced
`pass_rule_evaluation.yaml` from a hand-authored one dropped into a real run's
`artifacts/` directory. Closing that requires a cryptographic or append-only-log
tie between the evaluator and its output. Ruled **out of proportion** to a
single-operator research campaign and accepted as a **standing limitation**, not
a closed hole. It is recorded in `record_schema.py`'s own header so the next
reader meets it before trusting the gate, rather than discovering it in an audit.
Boundary: the schema governs what a RECORD may say; it does not attest that a
cited artifact was genuinely produced by the machinery.

**Still OPEN, carried forward unchanged.** D-2 (G4 detects no anomalies; it only
demands prose for self-declared ones) and D-7 (G1's product allowlist is
exact-match on a free-text brief field; G2/G3 accept placeholder and wrong-typed
values). Also carried: `promotion_is_generic` uses exact dict equality, the same
brittle-match shape as D-7 — not exploited by any of the nine files today.

Tests 389 -> 413. All five re-audit bypasses plus the sixth are regression-tested
verbatim by name in `tests/test_c7ext_r2_closed_schema.py`, alongside the two
negative cases that correctly held (a real run-scoped file with no binding
result; an absolute path outside any run) and the `_save_queue` whole-list
atomicity the re-audit confirmed empirically.

**Method note.** Three rounds of this defect were closed by the person who wrote
them and reopened by the next reader within minutes. The thing that finally
changed was not a better guess about names — it was giving up on guessing.

---

# v9 additions — found 2026-07-23 (silent-hole fetch defect)

### G3. A rolling-window endpoint makes `_fetch_remote` write a holed cache and
report success (P0, guard CLOSED 2026-07-23; data gap STILL OPEN)

- **Symptom.** Kraken's public OHLC endpoint serves a fixed rolling ~720-candle
  window and **ignores `since` entirely**. Probed read-only, three `since`
  values return byte-identical windows:

  ```
  since=2026-01-01  -> n=721  first=2026-06-22 23:00  last=2026-07-22 23:00
  since=2025-06-01  -> n=721  first=2026-06-22 23:00  last=2026-07-22 23:00
  since=none        -> n=721  first=2026-06-22 23:00  last=2026-07-22 23:00
  ```

  Endpoint-wide, not pair-specific (BTC/ETH/XRP/SOL/ONDO/TAO/INJ all identical).

- **Why it was silent — the actual defect.** `_fetch_remote` pages until the
  endpoint returns `[]`, then `if not candles: break` exits *cleanly*. The
  partial result flows into `_merge_and_store`, which wrote it unconditionally
  and logged `Saved … (N rows)`. A 2026 top-up would therefore have produced a
  cache spanning 2025-12-31 → 2026-07-22 **with a 4,151-bar hole in the middle**,
  a success line in the log, and nothing anywhere reporting a problem. This is
  the worst shape a data defect takes: every downstream consumer inherits it and
  none can detect it. The endpoint's behaviour is Kraken's to define; treating
  a short read as a complete one was ours.

- **Fix — a guard at the WRITE boundary, not a fetch-loop rewrite.**
  `BaseFetcher._merge_and_store` now calls `_assert_no_new_gap` and raises
  `FetchGapError` **before** touching `data_cache` or disk, so a rejected fetch
  leaves no trace in memory or on disk. The message names the missing span and
  its bar count.
  - **Differential by construction.** Archive-ingested caches carry real natural
    gaps (INJ ~5.7%, DOGE ~5.1% within-life missing bars, already on record), so
    an absolute "no internal gaps" rule would reject every cache the campaign
    depends on. Only a gap covering time that was *not already gapped* fails.
  - **Containment, not equality**, is the comparison: a fetch that PARTIALLY
    fills a pre-existing hole leaves a smaller gap nested inside the original.
    That is an improvement and must not be blocked.
  - **Unguarded when `existing` is empty**: with no prior data there is no
    continuity to break, and a late-listed asset legitimately returns data
    starting partway into the requested window.
  - Reuses `expected_gap_tolerance` and the same gap criterion
    `_identify_missing_periods`/`validate_data_continuity` already apply, rather
    than inventing a second notion of continuity.

- **Acceptance.** `trading-bot/tests/test_fetch_gap_guard.py` (7 tests,
  fixture-driven, no live calls): the Kraken shape to scale raises and writes
  nothing; the guard derives 4,151 independently rather than restating a
  constant; contiguous top-up still writes; pre-existing natural gaps still
  write; partial gap-fill still writes; first-fetch unguarded; and a real
  on-disk `kraken_BTCUSD_1h.csv` is byte-compared before/after to prove no
  archive cache changes. Suite 413 -> 420.

- **2026 bulk-archive recon (web-sourced, retrieved 2026-07-23).** Kraken
  publishes the OHLCVT bulk export with "incremental updates … provided at the
  end of each quarter", as `Kraken_OHLCVT_Q<N>_<YEAR>.zip`
  ([support article](https://support.kraken.com/articles/360047124832-downloadable-historical-ohlcvt-open-high-low-close-volume-trades-data)).
  Schema **matches the already-ingested export exactly**: headerless, 7 columns
  `timestamp,open,high,low,close,volume,trades`, **unix seconds**, files named
  `<PAIR>_<MINUTES>.csv` (e.g. `XBTUSD_60.csv`) — identical to
  `ingest_kraken_archive.py`'s `KRAKEN_RAW_COLUMNS`, so the audited ingestion
  path would need no change
  ([schema reference](https://concretumgroup.com/how-to-get-free-full-crypto-intraday-data-2013-2025-from-kraken/)).
  **Existence of the 2026 files is UNCONFIRMED**: retrievable sources index only
  through `Kraken_OHLCVT_Q4_2025.zip`. Under the stated cadence Q1 2026
  (ended 03-31) and Q2 2026 (ended 06-30) should both exist, but cadence is not
  evidence and is not recorded here as such. Verifying requires the download
  page itself, which is not publicly indexed. **Not downloaded** — this recon
  established existence and shape only.
  - **If Q1+Q2 2026 exist, the seam closes with overlap to spare**: Q2 runs to
    2026-06-30, and the live rolling window already reaches back to
    2026-06-22 — a ~8-day overlap, so archive and live compose with no seam at
    all. This is by far the cheapest path and should be checked before any
    aggregation work is commissioned.

- **Option 1 cost estimate (`/0/public/Trades` -> 1h aggregation), scoped NOT
  implemented.** Request volume estimated from the **2025-H2** archive's own
  `number_of_trades` column — a pre-holdout proxy, so no 2026 data was touched:

  | | |
  |---|---:|
  | Trades, 19 pairs, 2025-H2 | 41,210,802 |
  | Calls @ 1,000 trades/call (endpoint max) | 41,211 |
  | Serial @ 1 call/sec | **~11.4 hours** |
  | Parallel per-pair (limit is per IP *and* per pair) | **~2.2 hours**, bounded by BTC |

  Rate limit: public endpoints tolerate ~1 call/sec, limited by IP and pair
  ([request limits](https://support.kraken.com/articles/206548367-what-are-the-api-rate-limits-));
  `count` max 1000, paginated via the `last` cursor
  ([Trades endpoint](https://docs.kraken.com/api/docs/rest-api/get-recent-trades)).
  Volumes are a proxy, not a measurement — 2026 could differ materially.
  **Integrity checks aggregation would require, none of which the OHLC path
  needs:**
  1. **Aggregation-boundary alignment** — bars must be left-closed/right-open on
     exact UTC hour boundaries matching the archive's convention. An off-by-one
     boundary shifts every bar and would reconcile *approximately* while being
     systematically wrong.
  2. **Volume reconciliation against the overlap region** — aggregate a window
     that the archive ALSO covers (e.g. 2025-12), and require volume and
     `number_of_trades` to match per bar. This is the only check that validates
     the aggregator against ground truth rather than against itself, and it must
     pass before any 2026 output is trusted.
  3. **Trade-completeness at the cursor** — the `since` cursor paginates by trade
     ID; a dropped page silently under-counts volume in a bar that still looks
     well-formed.

- **Ledger correction (item 2, second instance).** G2's "top-up composability is
  now real and proved by key derivation" is **overstated, by the same conflation
  G2 itself was correcting one sentence earlier**. Key derivation proves the
  top-up is ADDRESSABLE (right slot, fetchable symbol); it says nothing about
  whether the endpoint SERVES that history. G1's original claim conflated
  slot-design with fetchability; G2's replacement conflated fetchability with
  availability. Twice in one arc, a narrower proof was recorded as the broader
  one. The pattern worth naming: **"proved by derivation" is a claim about
  addressing, and can never establish an empirical property of a remote
  service.** Only a probe can, which is why the seam was found by probing.

- **Item 2 remains OPEN.** Seam recorded verbatim: archive ends
  **2025-12-31 23:00**, first fetchable bar **2026-06-22 23:00**, gap
  **4,151 bars / ~173 days**. Holdout discipline held throughout: coverage
  metadata only, no return or performance statistic over any 2026 data.

---

# v11 additions — 2026-07-23 (XS_momentum parked through the closed schema; data carry-forwards)

## H. Verdict integrity (continued)

**C7-EXT-R2 — first production write through the G6 closed schema, on a genuine
relabel.** `XS_momentum` was relabelled in both stores and the write was routed
THROUGH `tools/record_schema.py` (via `validate_verdict_provenance`), not around
it — the same path `run_phase1_research._write_kb_findings_entry` and
`run_campaign._save_queue` take. Both entries passed.

- **KB `xs_momentum_cost_surviving_but_decaying`** and **queue `XS_momentum`**:
  `outcome` -> `ungated_decayed_measurement_no_admissible_verdict` (KB was
  `measurement_only_no_admissible_verdict`, queue was
  `ungated_measurement_no_admissible_verdict`); `verdict_status: ungated`
  (added explicitly to the queue entry, which previously carried none).
- **Recorded reason (load-bearing, verbatim in `verdict_void_reason`):**
  full-sample net Sharpe 1.325 on a gate-validated backtester (the 30-slot
  run_054 reproduction, exact), decaying to net Sharpe **0.07** in its latest
  full in-sample year (2025) — **edge decay, explicitly NOT trade sparsity**
  (contrast run_057, the ER-gate variant parked as too sparse; this signal
  trades daily and still fades). No admissible verdict because no pre-registered
  pass_rule was ever declared AND no obtainable 2026 holdout can statistically
  resolve the Sharpe this year: **SE >= 1.3 for any T <= 0.56** year, so one
  holdout year cannot separate a real 0.07 edge from zero.
- **Parking removes the verdict claim, not the evidence.** Every measurement is
  unchanged and verified present after the edit: `net_sharpe_full_sample: 1.325`,
  `validation_gate: PASS`, `per_year_net_sharpe:
  [2.95, 0.85, 1.02, 2.96, 0.77, 1.46, 0.76, 0.96, 0.07]`.
- **Honest verdict count unchanged at 1** (`FUNDING_MR_DAILY_RETEST`), confirmed
  by the standalone `tools/lint_verdict_provenance.py`. XS was never gated, so
  parking it must not move the count — and does not. `outcome` starts with the
  `ungated` prefix, so `outcome_is_verdict_bearing` returns False and the entry
  is admissible with no provenance, exactly as a corrected record should be.

## G. Data & cache layer (continued)

**NEW CARRY-FORWARD — Binance as the continuous-recent-data source for future
holdouts.** Where Kraken's 2026 OHLCVT bulk export is unpublished (G3: retrievable
sources index only through `Kraken_OHLCVT_Q4_2025.zip`) and its live OHLC endpoint
serves only a fixed rolling ~30-day / ~720-candle window (G3: the silent-hole
seam, 4,151-bar gap), **Binance can supply continuous recent candles** for a
future holdout. `BTC/ETH` are already Binance-cached (`BTCUSDT_1h.csv` /
`ETHUSDT_1h.csv`, unqualified keys), and G1 item 3 already made `exchange` an
additive parameter on `DataManager.fetch_historical_data()`, so the fetch path is
in place.

- **CAVEAT, recorded explicitly (firing condition, not a TODO):** any strategy
  validated on Binance data **must be re-declared and re-costed for Binance per
  Phase 1.3**. `XS_momentum`'s Kraken venue registration (`venue: kraken_perp`)
  and its cost basis (cost_model.yaml perp block, 5 bps one-way) **do not
  transfer** — different venue, different fee schedule, different funding
  convention, different tradable universe. A Binance holdout of XS is a NEW
  registration, not a continuation of the Kraken measurement, and must carry its
  own pre-registered pass_rule and cost basis before any figure it produces is a
  verdict. (Compounds with G1 item 4: `FundingRateFetcher.cache_key()` is still
  unqualified, so a second-venue funding fetch is a live collision risk.)

**PARKED — the q1_26 tick archive is Kraken Trades, not OHLCVT.** On disk at
`trading-bot/local_data/Kraken_batch/q1_26/` (Q1 2026, timestamps from
2026-01-01). Verified format: **time-and-sales**, header
`Price,Volume,Timestamp,Type,Miscellaneous,Trade ID` — NOT the 7-column
`timestamp,open,high,low,close,volume,trades` OHLCVT schema the audited
`ingest_kraken_archive.py` path consumes. It is therefore usable **only via the
scoped-but-unbuilt Trades -> 1h aggregation path** (G3 Option 1, with its three
mandatory integrity checks: boundary alignment, overlap volume reconciliation,
cursor completeness). **Left on disk, not ingested.** G1 item 2 stays OPEN and
the seam is unchanged — archive ends 2025-12-31 23:00, first fetchable live bar
2026-06-22 23:00, **4,151-bar / ~173-day gap**. Having the raw trades on disk is
not the same as having them addressable as OHLC bars, the same
availability-vs-addressability distinction G1/G2 twice conflated.

## P4-D. P4_ts_trend density-probe carry-forwards (filed 2026-07-24)

Source: `engineering/sessions/session_reports/20260724_p4_density_probe_archive.md` (read-only entry-count
probe against the raw Kraken daily archive) and `engineering/sessions/session_reports/20260723_p4_panel_recon.md`.
All four are **FILED, NOT FIXED** — nothing below was remediated in the commit that filed it,
and no backtest, ingest, or tool change was made. Every count cited is an entry-transition
count from a probe governed by **no pre-registered pass_rule**; none of it is a verdict.

### P4-D1. Phase 2 Track A's breadth ingestion is 1h-only — no daily-bar hypothesis can consume the 19-pair cache today (P1, FILED)

- **Evidence (cache listing, executed and recorded verbatim):**
  `engineering/sessions/session_reports/20260723_p4_density_probe.md:307-327`.
  - `Get-ChildItem $d -Filter "*_1d.csv"` -> exactly two files, `BTCUSDT_1d.csv` and
    `ETHUSDT_1d.csv` (`:309-311`, restated `:322-323`) — Binance, USDT-quoted, and
    **precisely the two symbols run_057 already evaluated**.
  - `(Get-ChildItem $d -Filter "kraken_*" -File | Measure-Object).Count` -> **19** (`:313-314`).
  - `Get-ChildItem $d -Filter "kraken_*" -File | Where-Object { $_.Name -notmatch '_1h\.csv$' }`
    -> **no output** (`:316-318`). Every Kraken cache file is `_1h`; there is not one
    Kraken daily bar in the cache namespace (`:324-327`).
- **Consequence:** the breadth P2 delivered is real but hourly. `ts_trend_daily_v1.json:17`
  declares `"timeframe": "1d"`, so the registered P4 hypothesis cannot read the 19-pair
  cache at all. The daily bars exist on disk —
  `trading-bot/local_data/Kraken_batch/master_q4/*_1440.csv`, 7 columns, no header,
  unix-seconds UTC (`20260724_p4_density_probe_archive.md:96-120`, `:284`) — but they are an
  *archive*, not a *cache key*, and no loader in the repo reaches them. This is the
  availability-vs-addressability distinction G1/G2 already tripped over twice.
- **Why it is filed and not fixed:** ingesting `*_1440.csv` into the cache is a write to
  `local_data/` plus an ingest-path decision (`20260723_p4_density_probe.md:440-444`); it is
  queued work, not a mid-lineage patch.
- **Acceptance when taken up:** a daily-bar hypothesis resolves at least three non-BTC/ETH
  Kraken symbols through the normal cache path with no per-run special-casing.

### P4-D2. Two different per-window minimum-trade floors, both live, both cited as authority (P1, FILED — NOT RESOLVED)

Recorded because the density probe had to report against **both** and explicitly refused to
choose (`20260724_p4_density_probe_archive.md:361-386`).

- **Floor A = 1** — `strategy-research/protocols/ts_trend_daily_v1.json:132`:
  `"min_trade_count_gte": 1`. Its own rationale (`ts_trend_daily_v1.json:11`) calls it a
  pre-registered floor meaning "at least one completed round-trip required for a window to
  count as evaluable", matched to the brief's a-priori 10-25 transitions / 15 windows.
- **Floor B = 5** — `strategy-research/config/campaign_config.yaml:120`:
  `trade_floor_per_window: 5      # per-window "sparse" threshold (A3.4 gate)`. Floor B is
  the one actually applied to this hypothesis in the campaign record: both
  `config/campaign_queue.yaml` and `campaign_knowledge_base.yaml` report the archived P4
  gated run as "29/30 window-symbols below the A3.4 five-trade floor".
- **These are different gates, and that is the point.** Floor A sits in the `promotion`
  block of a protocol JSON and is machine-read. Floor B sits under `verdict_interpreter:`
  in `campaign_config.yaml`, whose own preceding comment (`campaign_config.yaml:117-118`)
  says these values are "defined in SKILL.md and applied by the LLM agent, not code". So one
  is a protocol promotion criterion and the other is an agent-applied sparsity heuristic —
  they were never authored as the same number, yet they govern the same per-window quantity
  and disagree by 5x.
- **Consequence, stated with the counts:** which floor governs changes the answer
  completely. The gated variant clears Floor A in **120/178** evaluable slots and Floor B in
  **3/178**; the parent clears Floor A in **175/178** and Floor B in **80/178**
  (`20260724_p4_density_probe_archive.md:392-397`).
- **NOT RESOLVED HERE.** Choosing between them is a director's call, and this item exists so
  the choice is made once, in the open, rather than silently by whichever artifact a reader
  happens to open first.

### P4-D3. `panel_backtester.py`'s commission constant is correct for its gate and a trap for anything else costed through that path (P1, FILED — trap, not a defect)

- **The constant:** `strategy-research/tools/panel_backtester.py:56` —
  `DEFAULT_COMMISSION_RATE = 0.001  # engine DEFAULT_COMMISSION_RATE (10 bps one-way)`. It is
  a hardcoded module constant, **not** read from `cost_model.yaml`
  (`20260723_p4_panel_recon.md:93`).
- **It is CORRECT where it is used.** Its only consumer is the gate path `validate_gate()`,
  whose entire job is to reproduce the archived run_054 slots exactly under a pre-registered
  tolerance. That archived run was produced by the production engine at the engine's own
  default rate, so reproducing it requires *this* number. Re-pointing it at the campaign's
  ratified venue figure would break the reproduction gate — which would be a regression in
  the gate, not a fix to it.
- **The trap:** the campaign's ratified cost basis is Kraken perp, **5 bps one-way / 10 bps
  round-trip** — `strategy-research/config/cost_model.yaml:158-162`
  (`perp.fee_rate_bps.default: 5.0`, `perp.round_trip_cost_bps.default: 10.0`), sourced per
  that block's own comment at `cost_model.yaml:135-136` from the Kraken perpetual-futures
  base-tier taker fee. The engine default mirrored at `panel_backtester.py:56` is instead a
  **Binance spot** figure (`cost_model.yaml:65`, "Binance spot, Regular/VIP0 tier, BNB
  discount applied"), i.e. **double** the ratified Kraken one-way rate
  (`20260723_p4_panel_recon.md:167-169`).
- **Firing condition:** any *future* run costed through `panel_backtester.py`'s gate
  machinery, or any copy-paste of that constant into a new path, silently prices at 10 bps
  one-way Binance spot while the campaign believes it ratified 5 bps Kraken perp. The XS path
  in the same file already avoids this — it reads `cost_model.yaml`
  (`panel_backtester.py:329-334`, `:364-365`). Two costing conventions inside one file, only
  one of them venue-ratified, is what makes this worth filing.
- **Filed, not fixed. The fix is not to change line 56.**

### P4-D4. OVERTURNED PRIOR CONCLUSION — `data_manager.py` does not hardcode the exchange; a default is not a constraint (P1, FILED)

- **The claim, twice recorded:** `engineering/sessions/session_reports/20260722_kraken_ingest_audit.md:363-366`
  — "`data_manager.py:768` hardcodes `exchange="binance"` ... **No backtest can currently
  reach any of the five ingested Kraken cache files.**" Restated as a present-tense blocker by
  `engineering/sessions/session_reports/20260723_p4_density_probe.md:363-366` and again at `:450-451`
  ("`data_manager.py:768` hardcodes `exchange="binance"` and would need parameterizing before
  any engine run could read a `kraken_*` cache key").
- **Overturned by reading the code at HEAD:**
  - `trading-bot/data/data_manager.py:746` —
    `def fetch_historical_data(self, symbol: str, start_date, end_date, exchange: str = "binance")`.
    `"binance"` is a **default argument**, not a hardcode.
  - `trading-bot/data/data_manager.py:757-760` — the docstring says so in as many words:
    "`exchange` selects the CCXT exchange id used for both the remote fetch and the local
    cache filename (see `CcxtFetcher.cache_key()`); defaults to `"binance"` so existing call
    sites are unaffected unless they opt in (e.g. `exchange="kraken"` to reach
    `kraken_XBTUSD_1h` etc.)."
  - `trading-bot/data/data_manager.py:773` — the parameter is **threaded through**:
    `exchange=exchange`, inside the `HistoricalDataFetcher(...)` construction at lines 770-776.
  - `trading-bot/data/fetchers/ccxt_fetcher.py:85` sets `self.exchange_id = exchange`, and
    `ccxt_fetcher.py:120` derives the key as
    `prefix = "" if self.exchange_id == "binance" else f"{self.exchange_id}_"`. So
    `exchange="kraken"` produces exactly the `kraken_*` keys the claim called unreachable. A
    dedicated test already covers it end to end:
    `trading-bot/tests/test_kraken_cache_reachability.py:107`.
- **Provenance of the error, stated fairly.** The 2026-07-22 ingest audit was auditing commit
  `32b1c13`, against which its statement was **true**. The parameter landed later that same day
  in commit `11afb72` ("Phase 2 Track A: Kraken cache reachability — parametrize exchange,
  tz-naive guard"; `git blame` of `data_manager.py:773`). The 2026-07-23 recon then repeated the
  claim in the present tense **by citation, without re-reading the file**, after the fix was
  already in the tree. It is the restatement that was wrong, not the original audit.
- **What is still true, and must not be over-corrected:** the engine's own backtest call site,
  `trading-bot/core/backtester.py:92`, does not pass `exchange`, so a backtest run today takes
  the default and reads Binance keys. That is a **caller that has not opted in** — one keyword
  argument away — not a constraint in the data layer. P4-D1 (no Kraken *daily* bars in the
  cache under any exchange id) is the real blocker and is untouched by this correction.
- **GENERALIZED LESSON — a default is not a constraint.** A default argument records what
  happens when nobody chooses; a hardcode records that nobody *may* choose. Reading the first
  as the second turns a one-keyword opt-in into a phantom engineering blocker, and it
  propagates: here it survived two reports and was one step from being written into a
  reactivation condition as a hard prerequisite. Rule: before recording any capability as
  blocked, **open the file and read the signature at HEAD** — a citation to a prior report is
  not a re-read, and a report is only ever true against the commit it audited.

## H. Verdict integrity (continued)

### H1. The closed record schema admits only two dated-key families, so a basis strengthening that deliberately moves no verdict has no correct slot (P2, FILED — seam, not a defect)

Filed as a **seam alongside the `outcome_reason` exemption**
(`PIPELINE_IMPROVEMENTS_20260712_v4.md:2008-2017`), on the same principle stated
there: an unexamined exemption is how the previous rounds failed, so a slot the
schema does not have is written down rather than left to be rediscovered.

- **The schema lines that enumerate the families:** `tools/record_schema.py:207-213`.
  The allowlist is exactly two patterns —
  `^readjudication_\d{8}$` -> `TEXT` (`:211`) and
  `^outcome_history_superseded_\d{8}$` -> `HISTORY` (`:212`) — resolved by
  `_shape_for()` at `:224-226`, which returns `None` (-> `RecordSchemaError`) for
  any dated key outside them. This is deny-by-default and that is correct; the
  seam is the *shape of the vocabulary*, not the strictness.
- **Both families presuppose that something moved.** `outcome_history_superseded_<date>`
  is `HISTORY` — a record of a *prior outcome* now superseded. `readjudication_<date>`
  names a *re-judgement*. Neither names the third real case: the entry's **evidentiary
  basis** was replaced with something stronger and the **outcome and `verdict_status`
  were deliberately left where they were**.
- **The KB key that had to borrow one:** `campaign_knowledge_base.yaml:1078`,
  `readjudication_20260724` on `p4_sma_trend_longonly_daily_auto`. The 2026-07-24
  density probe replaced `exhausted_basis` with a measured basis and set
  `reactivation_condition` from null. It was governed by **no pre-registered
  pass_rule** and produced **no verdict**, so nothing was re-judged — the key's own
  first line says so (`:1078-1081`: "DENSITY-PROBE BASIS REPLACEMENT (no relabel, no
  verdict). outcome and verdict_status are UNCHANGED"), and it states the constraint
  that forced the borrow at `:1086-1089`: "The closed record schema
  (tools/record_schema.py:210-213) admits exactly two dated correction families ...
  An outcome_history record would falsely imply the outcome moved, which it did not,
  so the superseded exhausted_basis is retained here instead."
- **Why this is a seam and not a defect.** No record is wrong, nothing was smuggled,
  and the write is honest — it disclaims in its first sentence the very thing its key
  name implies. The cost is that a reader indexing on key names sees a *readjudication*
  where a basis was strengthened, which **overstates it**: it reads as the campaign
  having re-decided P4_ts_trend when the campaign explicitly did not. Two entries now
  sit under the `readjudication_<date>` name meaning two different things
  (`readjudication_20260722` on the same finding was a genuine relabel; `_20260724`
  was not), and only the prose distinguishes them.
- **Candidate resolution when taken up (not done here):** a third allowlisted family,
  e.g. `^basis_replacement_\d{8}$` -> `TEXT`, admissible **only** on entries whose
  `outcome` and `verdict_status` are byte-identical before and after the write — the
  no-verdict-movement precondition enforced by the schema rather than asserted in
  prose. That is a schema change plus a KB migration of the borrowed key, i.e. queued
  work, not a mid-arc patch.
- **Acceptance when taken up:** a write that changes `exhausted_basis` while leaving
  `outcome`/`verdict_status` untouched lands under a key whose name says exactly that;
  a write that *does* move `outcome` under the same key is refused by the validator.

## I. Session close-out & suite verification (new category)

### I1. The suite was red for three commits and the arc close-out reported a test COUNT, not a RESULT (P1 — assertion fixed; the close-out procedure is FILED, not fixed)

- **What went red, and when.** `6b27d56` ("Park XS_momentum through the G6 closed
  schema; record Binance carry-forward") relabelled `outcome` ->
  `ungated_decayed_measurement_no_admissible_verdict` in **both** stores
  (`campaign_knowledge_base.yaml:1169`, `config/campaign_queue.yaml:260`), routed
  through the G6 closed schema and documented at `:1170-1176` — a deliberate write.
  It did not touch `tests/test_c7ext_verdict_gates.py`, whose
  `test_campaign_honest_verdict_count` still asserted the pre-relabel string. That
  assertion was authored at `0a4d606` (2026-07-22, `git blame` of the assert line)
  and was **correct against that commit**; `6b27d56` is what left it behind. The test
  file's last touch before the relabel was `f1a3d94`, which precedes `6b27d56`, so
  nothing re-checked it.
- **The close-out that did not surface it.** `19fa1b9` ("Arc close-out: refresh
  NEXT_SESSION.md + SESSION_LOG for C7-EXT/XS-park arc") recorded, in both files,
  "**Test suites (strategy-research, across the C7-EXT chain): 338 -> 369 (`0a4d606`)
  -> 389 (`2c8b8d1`) -> 413 (`f1a3d94`)**". Every number there is accurate as a count
  of tests. The suite at `19fa1b9` was **412 passed, 1 failed**. The count was
  reported; the result was not. The failure then survived `0d0f848` and was found
  only when the suite was run for its own sake.
- **Why the count could not have caught it.** A stale assertion does not remove a test.
  Collection count is invariant under a red test, so a growth series (`338 -> ... ->
  413`) is structurally incapable of detecting this class. It measures that tests were
  *written*, which is not the claim a close-out is making when it cites it.
- **What the close-out procedure would have to check (the actual ask).** A close-out
  must record the **exit status and the pass/fail summary line verbatim**, not a
  count: the literal `N passed` / `N failed, M passed` line and a non-zero-exit STOP.
  A count is not a result. Two corollaries, both from this incident:
  (a) any commit that changes a value in `campaign_knowledge_base.yaml` or
  `config/campaign_queue.yaml` must run the suite **in the same commit**, because the
  KB and queue are test *fixtures* for the verdict-integrity tests and no code change
  is involved to trigger suspicion; (b) a close-out that reports a suite figure without
  having run the suite **at the commit it is closing out** should say so explicitly
  rather than carrying a figure forward from an earlier commit — `413` was `f1a3d94`'s
  collected count quoted at `19fa1b9`, which is precisely how a green-looking number
  outlived a green suite.
- **Fixed (the assertion only):** `tests/test_c7ext_verdict_gates.py:499` now asserts
  the post-relabel string, with the relabel's provenance in a comment above it. The KB
  and queue were **not** touched — analysis established they hold the deliberate value
  and the test held the stale one. Suite after the fix: `413 passed`.
- **FILED, not fixed (the procedure):** no close-out template, hook or CI check was
  added. Acceptance when taken up: a close-out commit cannot be written without a
  pasted verbatim summary line from a run at that commit, and a red suite blocks it.

# v12 additions — found 2026-07-25 (funding re-cost arc: carry measurement and close-out)

## C. Power & validation machinery (continued)

### C16. ERA-CONCENTRATED EDGE IN THE PASS-GATED WINDOW: two independent families (XS_momentum, FUNDING_MR_DAILY_RETEST carry) measure edge concentrated in 2020-2021 and decayed to noise by 2023-2025; a full-window median-Sharpe pass rule therefore selects regime-expired strategies, and the single sealed holdout (`holdout_failure_is_terminal: true`) is the thing that pays for it (P1, FILED — no pass rule redesigned here)

The two families share no mechanism, no data feed, no runner and no author. They
were measured months apart, for different questions. They agree, and that is the
reason this is filed as a pass-rule problem rather than as two coincidences.

- **Family 1 — funding carry, measured per calendar year** (annualized carry
  `A1 = (365/N)·Σ_D sign(f_{D-1})·f_D·100`, from
  `engineering/sessions/session_reports/20260725_funding_carry_magnitude.md` §7, script marker
  `L16`; window bound applied before any statistic):

  | Year | BTCUSDT A1 %/yr | ETHUSDT A1 %/yr | n_days |
  |---|---|---|---|
  | 2019 (Dec only) | 4.6894 | 10.2332 | 30 |
  | 2020 | 19.3438 | 27.1763 | 366 |
  | 2021 | **31.2850** | **37.5817** | 365 |
  | 2022 | 4.3878 | 4.6791 | 365 |
  | 2023 | 7.6029 | 8.2273 | 365 |

  Both symbols peak in 2021 and collapse ~7x / ~8x into 2022, recovering only
  partially in 2023. The whole-window headline (`A1` = 15.4367 / 19.2366, same
  report §3, marker `L11`) is **carried by 2020–2021** and is roughly 3x the
  2022–2023 level — i.e. the headline describes a regime that ended inside the
  window it is quoted over.

- **Family 2 — XS_momentum, per-year net Sharpe**
  (`campaign_knowledge_base.yaml`, `xs_momentum_cost_surviving_but_decaying`,
  `signal_property.per_year_net_sharpe`, 2017..2025):
  `[2.95, 0.85, 1.02, 2.96, 0.77, 1.46, 0.76, 0.96, 0.07]`, against
  `net_sharpe_full_sample: 1.325`, `net_sharpe_post_2021: 0.77` and
  `net_sharpe_2025: 0.073` (2025 cumulative net −6.3%). The same entry's
  `strongest_threat_to_validity` states the compounding is "driven overwhelmingly
  by 2017 (+416%) and 2020 (+476%)".

- **Where the two families agree, and where they do not — stated precisely, because
  the shared claim is the load-bearing one.** They agree on the *shape*: a large
  early-era level, a collapse, and a most-recent-year figure indistinguishable
  from noise (carry 2022–2023 at ~1/3 of headline; XS 2025 net Sharpe 0.07). They
  do **not** agree on the exact peak years — funding carry peaks 2021 (BTC 31.2850
  / ETH 37.5817) whereas XS_momentum's two dominant years are 2017 (2.95) and 2020
  (2.96), with 2021 already down to 0.77. The title's "2020-2021" is the union of
  the two peaks, not a claim that both families peak in both years. What
  generalizes is decay-by-2023-2025, not a common peak date.

- **Why this is a pass-rule defect and not merely an observation.** run_059's
  criterion (a) is `median_sharpe > 0.8` taken over all 49 monthly windows of
  2019-12-01..2023-12-31 (`briefs/FUNDING_MR_DAILY_RETEST.md`;
  `runs/run_059/artifacts/pass_rule_evaluation.yaml`). A median over a window whose
  first half is a different regime from its second half is a statistic **about a
  mixture**, and it is symmetric in the wrong direction: it can pass a strategy on
  expired-era strength exactly as easily as it can fail a strategy that only works
  now. FUNDING_MR_DAILY_RETEST happened to fail it, so nothing was mis-promoted
  here — the defect is latent, and a latent selection defect that has not yet
  fired is precisely the kind that gets discovered by spending the thing it
  threatens.

- **What it threatens, concretely.** `config/campaign_data_policy.yaml:192`
  (`holdout_consumed_by: []`) and `:199` (`holdout_failure_is_terminal: true`):
  the campaign holds **one** holdout evaluation, it has not been spent, and
  failing it terminates the lineage. A full-window pass rule that selects on
  2020–2021 strength routes a regime-expired candidate to the single terminal
  test. The holdout is the resource that pays the bill for a pass rule that
  cannot see time.

- **REQUIRED ACTION (stated, not designed here).** Any future pass rule must carry
  a **per-era or recency-weighted component** — the full-window median alone is
  insufficient. The specific form (era partition boundaries, weighting scheme,
  per-era thresholds, and how a per-era criterion composes with B11's total
  verdict+routing mapping) is **deliberately not designed in this ledger entry**;
  designing it inside a close-out is how an unvalidated rule acquires the
  authority of a registered one.

- **Acceptance when taken up:** a brief whose pass rule gates only on a
  full-window statistic is rejected at materialization, the same way B11 rejects a
  FAIL branch with no verdict+routing pair.

### C17. KNOWN-MINOR (non-blocking, no action): the FUNDING_MR_DAILY_RETEST brief's funding sign-flip counts do not reproduce — 228/220 stated vs 180/152 measured

Recorded so a future reader does not re-derive the discrepancy from scratch, and
does not build on either figure without re-measuring first.

- **Stated:** `briefs/FUNDING_MR_DAILY_RETEST.md:236-244`, honesty note (i) —
  over the pass-gated window 2019-12-01..2023-12-31, "BTCUSDT 228 flips, ETHUSDT
  220 flips"; over the diagnostic window 2024-01-01..2025-12-31, 76 / 94; full
  73-month span 304 / 314. Method stated in the same sentence: "pandas
  daily-resample-**last** + sign-flip count".
- **Measured:** `engineering/sessions/session_reports/20260725_funding_carry_magnitude.md` §6
  (script markers `L13`-`L14`) — **180** (BTCUSDT) and **152** (ETHUSDT) flips over
  1,491 transitions on the same 1,492 bounded days, i.e. 21% and 31% below the
  brief. Method: daily **sum** of settlements, replicating
  `trading-bot/data/feed_registry.py:63-71` `build_daily_funding_series`.
- **Cause: UNDETERMINED.** No re-measurement was performed under the dispatch that
  filed this note. Three candidate explanations, with their evidentiary standing
  recorded honestly rather than ranked by assertion:
  1. *Unbounded-extent counting* (the hypothesis this note was dispatched to
     record as leading, carried here as stated): the brief counted over the full
     CSV extent rather than the bounded window. **Recorded, but weakened by the
     brief's own arithmetic** — the brief gives a separate full-span total of 304 /
     314 which decomposes exactly as 228+76 and 220+94, so its 228/220 figure is
     presented as already window-bounded. This is a caveat on the hypothesis, not
     a refutation of it: nothing here verifies how any of those four numbers was
     produced.
  2. *Aggregation method* (**strongest mechanical candidate, and it is cited from
     the brief itself, not inferred**): daily-resample-**last** takes only the final
     settlement of each day, whereas the measurement **sums** all three. The two
     produce different daily signs whenever a day's settlements disagree, and
     therefore different flip counts. Consistent with the direction observed
     (summing damps within-day sign disagreement, yielding *fewer* flips).
  3. *Different series entirely*: the forward-filled 8h **signal** feed
     (`FundingRateFetcher` + `merge_asof`) rather than the daily-summed **cost**
     series — `feed_registry.py:41-46` states these are deliberately distinct.
     Offered in the measurement report itself as unverified.
- **Why non-blocking.** Neither figure is load-bearing for anything currently in
  the record. The carry measurement (C16, and the KB `audit_note` on
  `funding_mr_daily_retest_killed`) computes `A1` and `R` from the funding series
  and run_059's own artifacts directly; no flip count enters either. The brief's
  228/220 previously underwrote only the criterion (c) zero-trade base rate, which
  was **already reconciled and closed** on independent grounds (per-window
  position-restart semantics — see the CRITERION (c) CONFORMANCE RECONCILIATION
  note in that same KB entry).
- **Flag if it becomes load-bearing.** If any future pass rule, power calculation
  or trade-density estimate takes a funding sign-flip count as an input, the
  discrepancy must be resolved by re-measurement **before** that rule is
  registered — not adjudicated from this note, which resolves nothing.

# v13 additions — found 2026-07-26 (2026 coverage scope recon; holdout-cache leak arc)

## G. Data & cache layer (continued)

### G8. `Kraken_batch/q1_26/` is holdout-range data inside the in-sample tree — and it is superseded (**CLOSED BY DELETION 2026-07-26**)

> **CLOSED — the contamination vector no longer exists.** Dispatch C1 deleted
> `trading-bot/local_data/Kraken_batch/q1_26/` on 2026-07-26: 1,467 files, 5,738,407,640
> bytes, removed unread. G8a's location risk is closed **by elimination of the bytes**, not
> by relocation — the durable range-scoped quarantine proposed below was not built and is
> now moot for this tranche (it remains the right pattern for any future one; see
> `strategy-research/engineering/sessions/lessons.md` L-2026-07-26-A). G8b stands unchanged on its merits: the aggregation
> was already off the critical path, and there is now nothing to aggregate.
>
> Deletion was chosen over relocation because G8b had established the tranche was the
> unique source for **nothing** — the sealed tranche holds the same 1,467 pairs as finished
> OHLCVT. It remains re-obtainable from Kraken's public export, but **must not be
> re-obtained**: it is inside `holdout_range`. Documented at `local_data/README.md` §1.2.
> `holdout_sealed/` was verified untouched by the same dispatch (10,269 files /
> 1,986,009,900 bytes, unchanged before and after).
>
> The original filing is preserved below as the record of why this was a live risk.

Source: dispatch B1-R, `engineering/sessions/session_reports/20260726_2026_coverage_scope.md` (read-only;
no file inside `holdout_range` was opened — every 2026-range fact below comes from
filenames, sizes, counts, the registry, or a prior written record).

**G8a — location risk.** `trading-bot/local_data/Kraken_batch/q1_26/` holds **5.4 GB across
1,467 CSVs** of Q1-2026 Kraken *Trades* data — i.e. content inside `holdout_range`
(`campaign_data_policy.yaml:18`) — stored **inside the in-sample tree**, whose sibling
`master_q4/` *is* an active ingest source (`ingest_kraken_archive.py:281`). Both figures
match `local_data/README.md:64` exactly (B1-R step 5).

What actually protects it today is that **nothing has been built that can read it**: it is
Kraken time-and-sales (`Price,Volume,Timestamp,Type,Miscellaneous,Trade ID`, verbatim at
`:2250-2251`), not the 7-column OHLCVT the audited ingest path consumes, and the
Trades→OHLCVT aggregation path is scoped-but-unbuilt (G3 Option 1). That is a **policy
claim about the current state of the codebase, not a mechanical guarantee** — it holds
only while no aggregator exists, and it is one merged tool away from being false. The
2026-07-24 quarantine's reachability re-check (`campaign_data_policy.yaml:156-160`) covers
`holdout_sealed/**` only; **it asserts nothing about `q1_26/`** (B1-R WHAT REMAINS item 4).

**Durable fix, not actioned:** relocate it under a **range-scoped** quarantine path, as was
done for the Q1 OHLCVT tranche — i.e. scope the guard by the protected date range rather
than by which directory the bytes happen to occupy (`strategy-research/engineering/sessions/lessons.md` L-2026-07-26-A).
**Operator's call.** Not urgent while it remains unaggregated and no aggregator exists;
it becomes urgent the moment either changes.

**G8b — supersession: do NOT commission the aggregation.** The check this ledger itself
demanded at **`:2136-2140`** — *"This is by far the cheapest path and should be checked
before any aggregation work is commissioned"* — has now been made, and it comes back
negative for the aggregation.

- The sealed tranche is **already finished OHLCVT**, not raw trades: 10,269 files at
  `holdout_sealed/2026_H1/kraken_q1_2026/`, a complete grid of **1,467 pairs × 7
  resolutions** (`_1 _5 _15 _60 _240 _720 _1440`), in Kraken's documented
  `{TICKER}_{MINUTES}.csv` bulk convention; the registry names its origin directory
  `Kraken_batch/kraken_ohlcvt_q1_2026` (`campaign_data_policy.yaml:152`) — OHLCVT, on the
  record. Established from filenames, sizes and counts only; nothing under
  `holdout_sealed/` was opened (B1-R step 4).
- **Pair universes are identical.** Compared by filename only (`comm` over the two sorted
  name lists): q1_26 = 1,467 pairs, sealed `_1440` set = 1,467 pairs, **only-in-q1_26 = 0,
  only-in-sealed = 0, in-both = 1,467**. Same quarter, same pairs (B1-R step 5).

**Consequence:** aggregating `q1_26` would regenerate, at high cost and with three
mandatory integrity checks, data that already exists in final form — and it still could
not produce **Q2 2026**, which is the actual gap (frozen and empty: no Kraken Q2 data
exists on disk in any form, and the Q2 bulk export's existence remains unconfirmed per
`:2130-2135`). The aggregation is **off the critical path**; do not commission it.

**Standing caveat that outranks both parts:** the input is holdout-range data, so none of
this is schedulable now at any size. B1-R sized the *mechanism*; it did not grant
permission to run it.

### G9. Seven Binance cache CSVs carried holdout rows into the published tree (CLOSED for publication, OPEN in history)

Filed and actioned in the same commit as this note. Seven loose CSVs at
`trading-bot/local_data/` root carry 78–4,344 rows each inside `holdout_range`, in the
default un-prefixed Binance cache slot; **three were tracked and published** from
`ac27791` (2026-06-12). Now `.gitignore`-excluded and `git rm --cached`-untracked, and
registered at `campaign_data_policy.yaml` (`binance_cache_holdout_contaminated`) with
per-file last timestamp and in-range row count. Working copies untouched.

Two things stay open, stated rather than smoothed over. **(1) History is not clean** —
`git rm --cached` does not touch prior commits, so a full-history clone still yields 2026
H1 bars; rewrite is the operator's decision, filed alongside the same decision for `.env`
at `fec0120`. **(2) The exclusion is a name enumeration**, which cannot catch the next
cache file that crosses into the range, because `.gitignore` cannot express a predicate
over file CONTENTS. No timestamp-range check exists anywhere in the repo today. That
residual gap is filed OPEN (`strategy-research/engineering/sessions/lessons.md` L-2026-07-26-A), not closed by this commit.

Corrects B1-R on two measured points: the swept set is **seven** files, not five (B1-R
missed both `*_funding_8h.csv`), and only **three** of the seven were tracked, not five
(`git ls-files` at `fec0120`).

**No verdict added or altered by any part of v13.** Gated verdict count unchanged at **1**
(`FUNDING_MR_DAILY_RETEST`, per `tools/lint_verdict_provenance.py`). No KB entry, queue
entry, brief or protocol was touched.
