---
# research_brief.yaml — FUNDING_MR_4H_RETEST
#
# The 4h branch of campaign_knowledge_base.yaml's
# funding_rate_continuous_mean_reversion_expanded_auto reactivation_condition:
# "re-test the identical mechanism (FundingRateMeanReversionComponent,
# threshold=0.0) at 4h or daily bars". The DAILY branch ran as run_059 and was
# killed. The 4h branch is explicitly recorded in the KB as DEFERRED and
# untouched, and the parent entry still reads exhausted: false.
#
# Custody: source: operator_ratified. Registration approved by the operator
# 2026-08-27 ("yes to launch a run"); the pass_rule below is presented for
# explicit ratification BEFORE any launch, per the H-041-C-v2 precedent
# (2026-07-15) that pass rules are operator-ratified, never stage-invented.
# Authored 2026-08-27.

brief_id: FUNDING_MR_4H_RETEST

strategy_domain: structural_forced_flow
market_universe: [BTCUSDT, ETHUSDT]
timeframe: "4h"

# E-015 S1b: venue+product are required at registration and fail-closed.
# Binance is NOT listed in config/venue_tradability.yaml, so this resolves to
# research_only = True BY DESIGN. That is correct and deliberate: the funding
# series this mechanism reads is Binance's, the same source runs 044 and 059
# used, so the honest declaration is the venue the DATA comes from, not the
# venue we would eventually trade on. research_only keeps this run away from
# the sealed holdout, which is the right posture for a mechanism retest.
venue: binance
product: perp

constraints:
  - "One variant only - a closure run for a named KB branch. Expand exactly the
     registered mechanism (FundingRateMeanReversionComponent, threshold=0.0,
     4h bars). No parameter sweep, no additional variants."
  - "Thresholds are INHERITED from the daily sibling, not re-derived. Any
     proposal to move them is post-hoc selection and must be refused."

research_goal: >
  Re-test the continuous (threshold=0.0) 8h funding-rate sign mean-reversion
  mechanism on 4h bars - the last untested branch of the parent
  reactivation_condition, after 1h (run_044) and daily (run_059) both failed
  for DIFFERENT and individually-diagnosed reasons.

lineage:
  relation: reactivation
  parent_kb_entry: funding_rate_continuous_mean_reversion_expanded_auto
  parent_status: "exhausted: false; reactivation_condition names 4h AND daily"
  sibling_branch_outcome: >
    The daily branch ran as run_059 and was killed by its own pre-registered
    pass rule (median_sharpe -0.296 BTCUSDT / -0.979 ETHUSDT; max drawdown
    34.9% / 49.6%). Its lineage_routing was `terminate`. The KB's own closure
    note states explicitly that this does NOT close the parent entry, and that
    "the 4h branch of the parent reactivation_condition remains DEFERRED and
    is untouched."

hypothesis:
  mechanism: >
    Perpetual funding settles every 8 hours (00:00 / 08:00 / 16:00 UTC). A
    non-zero funding rate is a scheduled, non-economic cash transfer that
    forces one side of the book to pay the other. The claim is that the
    crowding which produces an extreme funding print mean-reverts around the
    settlement, and that the reversion is tradable net of cost.

  why_4h_specifically: >
    This is the strongest form of the argument and is the reason the branch is
    worth spending a run on, rather than a generic "try another timeframe".

    A DAILY bar spans three funding settlements. An 8h-periodic impulse sampled
    once per 24h is aliased - the three settlements inside one bar average
    against each other, so the mechanism is structurally invisible to a daily
    bar regardless of whether it is real. run_059's failure is therefore weak
    evidence against the MECHANISM: it is consistent with a mechanism that
    exists but cannot be resolved at that sampling rate.

    A 1h bar resolves the cycle but, per run_044's own recorded root cause
    (`lag_mismatch_to_regime_persistence`, confidence high), closes the
    position before the reversion materialises.

    4h is the only granularity that both resolves an 8h cycle (two samples per
    period - the Nyquist minimum) and holds long enough for the impulse to play
    out. If the mechanism is real, 4h is where it should be visible; if 4h also
    fails, the mechanism is dead across every granularity its own reactivation
    clause named, and the parent entry can be closed for good.

  falsifiable_statement: >
    On 4h bars over the pass-gated window set, the continuous funding-sign
    mean-reversion signal produces median per-window Sharpe > 0.8 on BOTH
    BTCUSDT and ETHUSDT, with max absolute drawdown < 30% on both.

  null_expectation: >
    Median Sharpe indistinguishable from zero on at least one symbol, i.e. the
    settlement impulse carries no tradable directional information at 4h either.

prior_evidence_honest_statement:
  run_044_1h: >
    ic_all_bars -0.008706, ic_active_bars +0.016737 (p=0.881, NOT significant),
    n_eff 83, activation 12.5%. Cost gate FAILED: edge_to_cost_ratio 0.2425
    against a required safety factor of 2.0. verdict_interpreter root cause
    `lag_mismatch_to_regime_persistence`, status escalate, target=timeframe -
    explicitly NOT a kill of the mechanism, only of the 1h execution grain.
  run_059_daily: >
    ic_active_bars 0.037802 (p=0.0406, significant). Cost gate PASSED:
    edge_to_cost_ratio 2.2927 against the same 2.0 floor. Killed on the pass
    rule: median_sharpe -0.296 / -0.979, max drawdown 34.9% / 49.6%.
    CORRECTION ON RECORD: an earlier characterisation in this project claimed
    "cost has killed this family twice". That is FALSE - cost killed the 1h
    branch only; the daily branch cleared its cost gate comfortably and died on
    return and drawdown.
  a_priori_risk_for_4h: >
    4h turns over roughly six times more than daily. Cost per trade is
    unchanged, so edge_to_cost_ratio scales down with trade count. The daily
    branch cleared the 2.0 floor at 2.2927 - a margin of ~15%. It is therefore
    entirely plausible that 4h fails the deterministic prescreen cost gate
    BEFORE any backtest runs. That is a legitimate, informative outcome and is
    pre-registered here as an expected failure mode, not a surprise: the
    existing signal_prescreen cost_check enforces it automatically and no new
    machinery is needed.

# Pins the protocol explicitly, exactly as the daily sibling does
# (briefs/FUNDING_MR_DAILY_RETEST.md:213). WITHOUT THIS the prescreen cannot
# resolve which protocol to run: it falls through run_context.yaml ->
# machine_constraints.protocol_ref -> campaign_state.last_escalation, and the
# last of those is a STALE entry claimed by run_049 (escalation_tf_15m.json).
# The B10 guard correctly refuses to run against another run's protocol rather
# than silently using it -- run_060 halted on exactly that on 2026-08-27
# (stale_escalation_unclaimed), because this block was omitted when the brief
# was first authored. The dry run had already said "brief has no
# machine_constraints" and that warning was not acted on.
machine_constraints:
  protocol_ref: protocols/funding_mr_4h_retest_v1.json
  protocol_ref_content_hash: "sha256:4fda1f39858295b06b81634b474eecb4a0c37c554e94689ec7a54e4204e4ecf9"
  significance_methodology: episode_blocked_a851a

evaluation:
  pass_rule:
    statement: >
      PASS iff, evaluated per symbol over the PASS-GATED windows only
      (protocols/funding_mr_4h_retest_v1.json, 49 monthly windows
      2019-12-01 to 2023-12-31), BOTH BTCUSDT AND ETHUSDT satisfy:
      (a) median Sharpe > 0.8; (b) max abs drawdown < 30%.
      ANY criterion FAIL on EITHER symbol -> kill, terminate.
      This is the mechanism's LAST named branch: the parent
      reactivation_condition names 4h and daily, and daily is spent. A kill
      here closes the parent entry - no refine, pivot, or escalate exists in
      this mapping.
    window_set_ref: protocols/funding_mr_4h_retest_v1.json
    criteria:
      - id: a
        metric: median_sharpe
        metric_basis: bar_level
        comparator: ">"
        per_symbol_threshold: {BTCUSDT: 0.8, ETHUSDT: 0.8}
        null_handling: fails_threshold
        source: >
          INHERITED VERBATIM from the daily sibling
          (briefs/FUNDING_MR_DAILY_RETEST.md criterion a), which sourced it to
          the operator's 2026-07-18 registration ruling and the H-041-C-v2
          precedent. Deliberately NOT re-derived: the sibling branch has
          already reported results, so choosing a new threshold now would be
          selecting one after seeing data. Same mechanism, same universe, same
          window set, same bar.
      - id: b
        metric: max_abs_drawdown_pct
        metric_basis: bar_level
        comparator: "<"
        per_symbol_threshold: {BTCUSDT: 30, ETHUSDT: 30}
        null_handling: fails_threshold
        source: >
          INHERITED VERBATIM from the daily sibling (criterion b), same
          provenance and same reasoning as criterion a.
    outcomes:
      # List-of-branches shape, matching the daily sibling verbatim. The map
      # shape written first was rejected by the B11 total-mapping lint at
      # materialization (2026-08-27): the lint iterates outcomes expecting a
      # dict per branch. promote carries lineage_routing: null because promote
      # never routes -- the holdout gate is a separate, standing gate, not a
      # lineage route, and naming it here is exactly what B11 rejects.
      - branch: PASS
        hypothesis_verdict: promote
        lineage_routing: null
      - branch: FAIL-a
        hypothesis_verdict: kill
        lineage_routing: terminate
      - branch: FAIL-b
        hypothesis_verdict: kill
        lineage_routing: terminate

honesty_notes:
  - id: i
    text: >
      The daily sibling's own pass_rule statement claimed daily was "the
      mechanism's LAST escalation ... no further timeframe exists under it".
      That parenthetical was factually wrong about the KB it cited - the
      reactivation_condition names 4h AND daily - and the KB's closure note,
      written at the same time, says the opposite and keeps 4h open. This
      brief proceeds on the KB's own explicit record. Flagged rather than
      buried because the two artifacts genuinely disagree and a future reader
      will find both.
  - id: ii
    text: >
      No threshold in this brief is new. Both criteria are copied from the
      daily sibling with their original provenance intact. The protocol's
      window set was copied programmatically from
      funding_mr_daily_retest_v1.json (verified identical, 49 windows) rather
      than retyped, so the two branches are compared on the same ground.
      min_trade_count_gte is 5 rather than the daily's 0, applying the standing
      A3.4 per-window floor (operator ruling 2026-08-22); at 4h that is
      trivially satisfied and is conformance, not a tightening.
  - id: iii
    text: >
      research_only resolves to True because binance is unlisted in
      venue_tradability.yaml. This run therefore cannot reach the sealed
      holdout. That is intended for a mechanism retest and is not a defect to
      route around.
---

# FUNDING_MR_4H_RETEST - the last named branch

See the frontmatter for the full registration. In one paragraph: perpetual
funding settles every 8 hours; a daily bar spans three settlements and cannot
resolve the impulse at all; a 1h bar resolves it but closes the position before
it materialises. 4h is the only granularity that both resolves an 8h cycle and
holds long enough to capture it. If it fails here, the mechanism has failed at
every granularity its own reactivation clause named, and the parent knowledge
base entry closes for good.
