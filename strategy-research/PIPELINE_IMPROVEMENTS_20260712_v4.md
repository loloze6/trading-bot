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
  Full design: `docs/design/K3_protocol_pinning_design_20260714.md` (§9
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

### B7. Validation stage never reads the pre-registration artifacts (P0)
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
  defect this entry describes; the fix has still not shipped.

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
  `docs/design/K3_protocol_pinning_design_20260714.md` (§4, §9 A5). Commits:
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

### B15. No first-class path from a fresh hypothesis registration to a schedulable queue entry (P1)
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
