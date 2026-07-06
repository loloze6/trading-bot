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
Read skills/quant-fundamentals/SKILL.md before assessing diagnostic trends across runs.
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
2. Check whether the trigger has actually fired, citing the specific campaign_state.yaml
   or campaign_knowledge_base.yaml evidence that would need to exist for it to have
   fired (e.g. a KB finding with `outcome` other than `no_edge_observed`/`inconclusive`/
   `invalidated_artifact`, showing genuine ungated edge).
3. If the trigger has NOT fired: do not set `recommendation: reframe` (or any
   recommendation) that converts the wishlist entry into a run. Instead, record it as
   **wishlist support** — a note that this campaign's evidence continues to support
   deferring to that wishlist entry, without recommending it be run now. `recommendation`
   in this case should be `continue` (or another value independently justified by the
   diagnostics), never a reframe whose `next_research_question` targets the untriggered
   wishlist family.
4. If the trigger HAS fired: cite the exact evidence (finding id, outcome, KB values)
   that satisfies it, in `recommendation_rationale`, before recommending the run.

This applies even when the same wishlist family has already been suggested in a prior
`campaign_review.yaml` — repetition does not substitute for the trigger firing.

## Checklist
- Read ALL diagnostics_log entries, not just the latest.
- If `recommendation_rationale` or `next_research_question` draws on a
  `detector_wishlist.yaml`/`feed_wishlist.yaml` entry, check and cite its trigger
  condition per the section above BEFORE recommending it as a run.
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

## Context rule
Read campaign_state.yaml and research_brief.yaml only. Do not read individual run
artifacts — the campaign_state diagnostics_log is the summarized truth.
