---
name: campaign-review
description: Reviews the full research campaign history and decides whether to continue
the current search direction, reframe the research question, or declare the campaign
complete. Runs at campaign decision points, not every iteration.
---

# Campaign Review

## Mission
Step back from per-run verdict decisions and assess the campaign as a whole.
Prevent category-level circling by detecting when multiple hypothesis families
have failed for the same root cause, indicating the research question itself
needs refinement.

## Required inputs
- `campaign_state.yaml`   (full history: all runs, families tried, diagnostics log)
- `research_brief.yaml`   (the original research question from the first run)

## Required outputs
- `campaign_review.yaml`

## Output requirements
`campaign_review.yaml` must include:
- campaign_id
- runs_reviewed: count of runs reviewed
- pattern_detected: one of:
    same_root_cause_different_families | search_space_narrowing | no_pattern | converging
- pattern_evidence: list of diagnostic values across runs that support the pattern
- recommendation: one of:
    continue | reframe | escalate_instrument | escalate_component | terminate
- recommendation_rationale: one paragraph citing specific diagnostic values
- next_research_question: ONLY populate this field when recommendation=reframe.
  Leave it ABSENT (do not write the key at all) when recommendation=continue.
  When present: a revised research_brief.yaml content that incorporates what was
  learned — different from a single-run proposed_brief in that it may change the
  fundamental question, not just the signal or parameter.
- budget_assessment: runs_used / campaign_budget, and whether to prioritize speed or
  thoroughness for remaining runs

## Required prerequisite reading
Read workflow_artifacts/skills/quant-fundamentals/SKILL.md before assessing diagnostic trends across runs.
If a pattern's stated mechanism conflicts with an identity in quant-fundamentals,
quant-fundamentals is authoritative — note the conflict in your output rather than
silently following the pattern definition as originally written.

## Pattern definitions

same_root_cause_different_families:
  Two or more DIFFERENT hypothesis families (e.g. rsi_mean_reversion AND keltner_breakout)
  both failed with the SAME primary root cause (e.g. both had cost_drag > 80%).
  This indicates a STRUCTURAL issue: the sizing model, not the signal, is the problem.
  Recommendation: reframe toward solving the structural issue rather than trying more
  signal families. E.g. "how do we find a signal that naturally generates fewer,
  larger trades?" rather than "which signal works best?"

search_space_narrowing:
  Each successive pivot has moved in a consistent direction (e.g. always toward trending,
  always toward higher-ER regimes) and diagnostics are improving monotonically (corr
  moving positive, cost_drag falling).
  Recommendation: continue — the search is converging on something real.

converging:
  One or more runs show positive forecast_return_corr AND cost_drag < 80% AND gross_pnl > 0.
  The loop is close to a promotable result.
  Recommendation: continue with current direction, possibly tighten the hypothesis to
  reduce variance.

no_pattern:
  Runs show no consistent direction in diagnostics; failures have different root causes.
  Recommendation: escalate_instrument or escalate_component to try a genuinely different
  search space.

## Wishlist-gated recommendations (`detector_wishlist.yaml` / `feed_wishlist.yaml`)

Both wishlists exist precisely because their contents are NOT yet actionable — each
entry there was deliberately deferred behind an explicit trigger condition (e.g.
`detector_wishlist.yaml`'s `trigger_condition`: build the first candidate only when
(1) a confirmed ungated edge exists AND (2) Improvement 03 diagnostics show
regime-dependent performance). Recommending a run that consumes a wishlist candidate
BEFORE its trigger has fired quietly deletes the gate — it turns a deferred idea back
into a live run queue item without the condition that justified deferring it ever
having been satisfied.

**Before citing a `detector_wishlist.yaml` or `feed_wishlist.yaml` entry in
`recommendation_rationale` or `next_research_question`:**
1. Read that wishlist file's `trigger_condition` (or per-entry trigger) field directly
   — do not infer it from memory or from this skill's summary above.
2. **Check freshness before trusting `trigger_condition.status`** (2026-07-10,
   added after an incident where a hand-authored `status: triggered` sat
   unverified in the file with no evaluator run behind it): `status`,
   `last_evaluated_at`, `last_evaluated_against`, and `kb_state_hash` are
   written ONLY by `workflow/run_campaign.py::evaluate_and_persist_wishlist_predicate()`
   — never hand-edited, never inferred. Recompute `sha256(campaign_knowledge_base.yaml's
   current bytes)` and compare it to the entry's `kb_state_hash`. If they don't
   match (or `kb_state_hash` is absent), the persisted `status` is STALE —
   do not treat it as fired or not-fired; re-run
   `evaluate_and_persist_wishlist_predicate(family_name)` first (or, if you
   cannot execute code from this stage, flag the staleness explicitly in
   `recommendation_rationale` and treat the trigger as unresolved, not as
   whatever the stale field says).
3. Check whether the trigger has actually fired, citing the specific campaign_state.yaml
   or campaign_knowledge_base.yaml evidence that would need to exist for it to have
   fired (e.g. a KB finding with `outcome` other than `no_edge_observed`/`inconclusive`/
   `invalidated_artifact`, showing genuine ungated edge).
4. If the trigger has NOT fired: do not set `recommendation: reframe` (or any
   recommendation) that converts the wishlist entry into a run. Instead, record it as
   **wishlist support** — a note that this campaign's evidence continues to support
   deferring to that wishlist entry, without recommending it be run now. `recommendation`
   in this case should be `continue` (or another value independently justified by the
   diagnostics), never a reframe whose `next_research_question` targets the untriggered
   wishlist family.
5. If the trigger HAS fired: cite the exact evidence (finding id, outcome, KB values)
   that satisfies it, in `recommendation_rationale`, before recommending the run.

This applies even when the same wishlist family has already been suggested in a prior
`campaign_review.yaml` — repetition does not substitute for the trigger firing.

## Reactivation-gated recommendations (`campaign_knowledge_base.yaml` findings)

A KB finding's `reactivation_condition` describes what would need to be true for that
mechanism to be worth re-testing — it is a CONDITIONAL gate, not a standing invitation.
Once a run actually satisfies that condition and reaches a verdict, the condition is
CONSUMED: the orchestrator stamps `reactivation_consumed_by: <run_id>` and clears
`reactivation_condition` to null on that finding (see `_write_kb_findings_entry`'s F09
hook). A finding with `reactivation_consumed_by` already set, or `exhausted: true` with
no open `reactivation_condition`, is CLOSED — proposing to reactivate it again is not a
new test, it is repeating a question that has already been answered.

**2026-07-06 incident this section exists to prevent:** `run_053`'s `campaign_review`
recommended `reframe` into reactivating both H-041-A (funding-rate mean-reversion) and
H-041-C (fear/greed contrarian) via `next_research_question`. Both had ALREADY been
closed by `run_050`/`run_048` (P1b, 2026-07-05/06) — but neither KB entry had been
written back with the closing verdict yet, so `reactivation_condition` still read as
open at review time. The orchestrator's own conformance gate (A5.4) now catches this
mechanically and pauses instead of scaffolding the run — but do not rely on that gate
as your only check; it exists as a backstop, not a substitute for reading the KB.

**Before citing any `campaign_knowledge_base.yaml` finding's `hypothesis_id` in
`recommendation_rationale` or `next_research_question`:**
1. Read that finding's `reactivation_consumed_by` and `exhausted` fields directly.
2. If `reactivation_consumed_by` is set, or `exhausted: true` with `reactivation_condition: null`:
   do not recommend reactivating it. State the terminal result instead (outcome,
   `exhausted_basis`, which run closed it) and, if a genuinely different formulation
   exists (different evidence_type, timeframe, mechanism, or an explicitly
   era-conditional/regime-gated variant), frame it as a NEW hypothesis registration
   (its own id, e.g. `H-041-C-v2`) — never as reactivating the closed entry.
3. If `reactivation_condition` is still non-null: verify the condition is ACTUALLY met
   by current campaign_state.yaml/campaign_knowledge_base.yaml evidence before citing
   it as satisfied — the same standard as the wishlist-gate check above.

## Fragment-pattern-motivated ideation (optional, 2026-07-10)

`fragment_patterns.yaml` (`strategy-research/tools/fragment_patterns.py`,
written to a completed run's `artifacts/` directory) is an ideation-only
diagnostic layer over LIFO trade fragments — forecast-bin outcome tables,
entry/exit component attribution, initial-entry-vs-scale-up cost comparison,
and duration/regime cross-tabs, all tagged `basis: lifo_fragment,
ideation_only`. It is an explicit, narrow exception to the Context rule
below: this skill may use a specific completed run's `fragment_patterns.yaml`
for the sole purpose of motivating a NEW candidate hypothesis — never to
read the campaign more broadly, and never as a substitute for
`campaign_state.yaml`'s diagnostics_log.

**You cannot open files (CUL-336, 2026-09-27).** You have no tools: you see
only the files pasted into your prompt. No handoff of this stage delivers a
`fragment_patterns.yaml`, so this section applies only if one appears among
your provided context files. If none does, skip fragment-pattern ideation —
do not describe or cite a fragment pattern you have not been given.

If a pattern in `fragment_patterns.yaml` motivates a candidate hypothesis:
- Draft it as a stub brief (`research_brief.yaml` shape, see
  `workflow_artifacts/templates/research_brief.yaml`) with `status: proposed`.
- Populate a `motivating_observation` field citing the EXACT pattern by
  table and value — e.g. `"fragment_patterns.yaml forecast_bin_table:
  fragments with entry forecast in [0,5) carried 70% of aggregate losses ->
  hypothesis: minimum-forecast entry gate"`. Do not paraphrase the pattern
  vaguely; cite the bin/cell and its numbers.
- The hypothesis still enters through FULL pre-registration — validation_gate,
  screening_backtest, walk_forward_validation, the works — exactly like any
  other hypothesis in this campaign's workflow (see
  `strategy-research/CLAUDE.md`'s Workflow stages). `motivating_observation`
  records WHY the hypothesis was proposed; it carries no evidentiary weight
  toward whether the hypothesis is correct. The pattern motivates. It never
  validates.
- Never cite `fragment_patterns.yaml` to argue an already-recorded verdict
  (protocol_verdict, status: kill/promote/refine/pivot) was wrong. That is
  verdict_interpreter's exclusive domain, and it explicitly excludes this
  artifact (see `workflow_artifacts/skills/verdict-interpreter/SKILL.md`'s Forbidden section).
  A fragment pattern is grounds for a NEW proposed hypothesis, never grounds
  to relitigate an old one.

## Checklist
- Read ALL diagnostics_log entries, not just the latest.
- If `recommendation_rationale` or `next_research_question` draws on a
  `detector_wishlist.yaml`/`feed_wishlist.yaml` entry, check and cite its trigger
  condition per the section above BEFORE recommending it as a run.
- If `next_research_question` names any `hypothesis_id` from `campaign_knowledge_base.yaml`,
  check its `reactivation_consumed_by`/`exhausted` fields per the "Reactivation-gated
  recommendations" section above BEFORE recommending it as a run.
- Compute the trend in forecast_return_corr across runs: improving / stable / worsening.
- Compute the trend in cost_drag_pct: falling / stable / rising.
- If same root cause across families: name it explicitly in pattern_evidence.
- Budget assessment: if runs_used > 0.6 × campaign_budget, recommend prioritizing the
  most informative remaining test (the one that would be hardest to replicate later).

## Forbidden
- Do not recommend terminate unless: instruments_tried ≥ 3 AND components_built ≥ 1
  AND all show no positive forecast_return_corr. Terminating prematurely wastes the
  campaign.
- Do not recommend reframe based on a single run's diagnostics. Require at least 2
  runs with the same root cause.
- Do not change the asset class or timeframe without citing a specific diagnostic
  reason (e.g. "all regimes uninformative on 1h → try 4h" not just "try something else").
- Do NOT populate next_research_question when recommendation=continue. Populating it
  on a continue output causes the pipeline to treat it as a reframe and overwrite the
  next run's brief, ignoring the verdict_interpreter's recommendation entirely.
- Do NOT recommend reframe (or any run) into a `detector_wishlist.yaml` or
  `feed_wishlist.yaml` family whose trigger_condition has not fired. (2026-07-04:
  this happened twice in the same campaign — both toward `daily_timeframe_er_overlay`
  / ADX overlay, per detector_wishlist.yaml `trigger_condition.status: not_triggered`
  at the time — see campaign_knowledge_base.yaml for the parked record.) Record it as
  wishlist support instead; see "Wishlist-gated recommendations" above.
- Do NOT recommend reframe (or any run) that reactivates a `campaign_knowledge_base.yaml`
  finding whose `reactivation_consumed_by` is already set, or whose `exhausted: true`
  with no open `reactivation_condition`. (2026-07-06: this happened with `run_053`,
  proposing to reactivate both H-041-A and H-041-C after P1b had already closed both —
  see "Reactivation-gated recommendations" above.) State the terminal result and, if
  warranted, propose a NEW hypothesis registration instead.
- Do NOT cite `fragment_patterns.yaml` to argue that an already-recorded
  verdict was wrong, to re-open a closed KB finding, or to justify a
  reframe/pivot of an EXISTING hypothesis. It may only motivate a NEW
  proposed hypothesis (`status: proposed`) via `motivating_observation` — see
  "Fragment-pattern-motivated ideation" above.

## Context rule
Read campaign_state.yaml and research_brief.yaml only. Do not read individual run
artifacts — the campaign_state diagnostics_log is the summarized truth. EXCEPTION:
a specific completed run's fragment_patterns.yaml, if it is among your provided
context files, may be used for the sole purpose of drafting a
fragment-pattern-motivated proposed hypothesis (see that section above) — this
does not broaden the rule to other per-run artifacts. You cannot open any file
yourself (CUL-336): only what is pasted into your prompt exists for you.
