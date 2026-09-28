---
# ============================================================================
# research_brief_new_pipeline.md -- first-run brief template for the "new
# pipeline" (E-061 C1.7; config_direct_authoring / strategy_config_authoring,
# the config-direct path this delivery plan brought up -- see
# engineering/review_2026-09-27/A3_all_flags_on.md §1's target v26 flag set).
#
# RELATIONSHIP TO workflow_artifacts/templates/research_brief.yaml (moved
# here, second-round code review): that file is the general-shape template
# for the LEGACY (validation-gate) pipeline's research_brief.yaml artifact --
# it has no `machine_constraints`/`criteria_from` and is filled in by the
# `hypothesis_generation` stage, not copied verbatim by an operator. THIS
# file is a frontmatter .md, the format `register_hypothesis`'s CLI actually
# reads (run_campaign.py::_parse_brief_frontmatter: '---'-delimited YAML,
# then Markdown prose) -- it lives beside research_brief.yaml because both
# are "the shape of a research_brief", not because they're interchangeable;
# an operator starting a NEW pipeline brief copies THIS one, never
# research_brief.yaml directly.
#
# HOW TO USE
# ----------
# 1. Copy this file to strategy-research/briefs/<your_brief_name>.md (the
#    `register` CLI reads a frontmatter .md; the leading '---'-delimited
#    block below IS the research_brief.yaml content, exactly as
#    run_campaign.py::_parse_brief_frontmatter expects -- see RUNBOOK.md
#    "Start a campaign on the new pipeline").
# 2. Replace every "<FILL IN...>" placeholder below with your idea.
#    Registration REFUSES a copy that still carries the placeholder sentinel
#    ANYWHERE in the frontmatter -- not just the top-level fields named
#    below, also inside machine_constraints (run_campaign.py::
#    _parse_brief_frontmatter, code review fix; the raw template cannot be
#    registered by accident, whatever field the placeholder is left in).
#    Every field run_campaign.py::REFRAME_BRIEF_REQUIRED_KEYS requires
#    (strategy_domain, market_universe, timeframe, research_goal, venue,
#    product) must also be non-placeholder and non-empty.
# 3. If your idea needs a DIFFERENT universe or bar size than the default
#    below (BTCUSDT+ETHUSDT, 1h), change market_universe/timeframe AND
#    machine_constraints.protocol.symbols/timeframe TOGETHER. Under
#    orchestrator.config_direct_authoring.enabled, registration cross-checks
#    the two (by bar-size SECONDS and by base-asset-normalized symbol -- BTC
#    == BTCUSDT -- so "60m"/"1h" and "BTC, ETH"/"BTCUSDT, ETHUSDT" both agree)
#    and refuses a real mismatch; `venue` has no protocol-side counterpart
#    (no protocol file carries a venue/exchange field) and is not
#    cross-checked. This check, and the promotion check in step 4, run ONLY
#    at registration, and ONLY under config_direct_authoring -- a
#    launch/resume re-parsing an already-registered brief does not re-run
#    them (same review fix).
# 4. Do NOT add a `promotion` block (C5.6, decision D-043). Under the new
#    pipeline -- orchestrator.config_direct_authoring AND
#    orchestrator.verdict_routing_retired both on (the target flag set) --
#    nothing that decides reads one: the grid and the profit bars decide, so
#    a generated protocol needs none and none is invented for you (see the
#    long comment below). There, registration refuses the abolished generic
#    block (median_sharpe_gt 0 / max_abs_drawdown_pct_lt 30 /
#    min_trade_count_gte 20 / kill_median_sharpe_lt -1) and a present-but-
#    empty `promotion:`; any other block registers with a note and is DROPPED
#    (never copied into pre_registration.yaml or the generated protocol).
#    With config_direct_authoring on but verdict routing still live, the
#    legacy verdict still decides and a real pre-registered block is
#    REQUIRED (G7, refused at registration without one).
# 5. Register it: `python workflow/run_campaign.py register --brief
#    briefs/<your_brief_name>.md --priority <n> --notes "<n>"` (RUNBOOK.md
#    §1a-bis has the pre-launch checks to run before spending any LLM
#    budget). `brief_status` is NOT set here -- see the note below.
#
# WHY criteria_from IS PRE-FILLED
# --------------------------------
# `criteria_from: hypothesis_generation` (== the orchestrator's own
# PASS_RULE_PENDING_AT_1A / CRITERIA_FROM_1A constant,
# workflow/run_phase1_research.py) defers pass_rule authorship to step 1a
# (hypothesis_generation), which fits real criteria from
# config/criterion_menu.yaml to the idea actually generated -- this is the
# same mechanism the orchestrator's own campaign-review reframe briefs use
# (run_phase1_research.py::_write_reframe_brief). It means YOU do not have to
# hand-author a pass_rule to get a first run going; do not add one here, or
# _materialize_run's guard raises (a brief cannot both defer to step 1a and
# carry a pre-registered pass_rule).
#
# WHY THIS IS A GENERATED PROTOCOL, NOT A PIN (code-review correction)
# ----------------------------------------------------------------------
# An earlier version of this template pinned an EXISTING file,
# protocols/diagnostic_btceth_4h.json, via machine_constraints.protocol_ref,
# and described it as "safe" and covering "every non-holdout era". Neither
# claim survived a full check against all 13 files in protocols/:
#   * diagnostic_btceth_4h.json's 11 windows sit ENTIRELY inside 2024
#     (one era: era_2024_burned) -- sign_consistent_by_era would pass
#     trivially, one era can never demonstrate era-stability;
#   * its own `holdout` block is {start: 2025-01-01, end: null}.
#     tools/run_protocol.py's --holdout mode (~L1988-1991) reads the range
#     from the PROTOCOL's own holdout block, not campaign_data_policy.yaml's
#     holdout_range, and resolves a null end as "today" -- so that block
#     SPANS the sealed window if anyone ever runs --holdout against it, the
#     opposite of "safe" (filed as Linear CUL-339, not yet fixed -- unrelated
#     to whether this template's OWN generated protocol is safe, since it
#     omits `holdout` entirely and so inherits the policy's real range; see
#     below);
#   * it passes tools/protocol_resolution.py's D-3 check
#     (assert_promotion_ratified) only because min_trade_count_gte was
#     lowered from the abolished generic default's 20 to 10 -- median_sharpe_gt
#     stays at the generic default's 0. That is a byte-inequality technicality,
#     not a real pre-registered threshold.
# Checking all 13 protocols against five criteria (test windows entirely in
# train+validation; span >= 3 real eras with substantive coverage, not a
# calendar-boundary sliver; never touch the sealed window; a holdout block
# consistent with campaign_data_policy.yaml's holdout_range or none; D-3
# clean on a REAL registered threshold, not a technicality) found none that
# cleanly qualifies on all five -- see the E-061 C1.6+C1.7 code-review commit
# messages for the full 13-row table. So this template GENERATES its own
# protocol via machine_constraints.protocol (the OTHER, pre-existing
# mechanism run_phase1_research.py::_ensure_protocol_from_constraints
# provides -- see its own docstring, and K3/G7 in that file for how a
# generated protocol is validated) instead of pinning an existing file:
#
#   * symbols/timeframe: BTCUSDT + ETHUSDT at 1h -- both have full
#     ohlcv/fear_greed coverage from 2018-02-01 and funding_rate from
#     2019-09/11 (config/campaign_data_policy.yaml backward_extension);
#   * start/end: 2018-02-01 .. 2025-12-31 -- generates 95 monthly windows
#     (matching protocols/run_048_generated.json's own start/end, which used
#     the identical range), measured (not estimated) against
#     tools/protocol_resolution.py::era_id_for_timestamp on this checkout:
#     20 windows in era_2018_pre_funding, 51 in era_2019_2023_full_feed,
#     11 in era_2024_burned (its full 11 calendar months), 13 in
#     era_2024_2025_walk_forward_extension (its full 13 calendar months) --
#     genuinely spanning FOUR real eras with substantive per-era coverage,
#     not a one-day boundary artifact;
#   * holdout: deliberately OMITTED -- _ensure_protocol_from_constraints
#     defaults it to campaign_data_policy.yaml's own holdout_range when
#     absent, which is the one value that cannot silently drift out of sync
#     with the policy (and sidesteps CUL-339 above entirely, since there is
#     no protocol-local holdout block for --holdout to misread);
#   * promotion: deliberately ABSENT (C5.6, D-043). A protocol's promotion
#     block only feeds tools/run_protocol.py's legacy top-level
#     promote/kill/refine verdict, which nothing reads once
#     config_direct_authoring AND verdict_routing_retired are both on: the
#     G7 gate (`_require_pre_registered_promotion`) is then skipped, the
#     generated protocol carries no `promotion` key (the abolished generic
#     default is never substituted), and run_tool_worker passes
#     --legacy-verdict-retired, so the legacy verdict is recorded as null
#     with a reason. (config_direct_authoring alone, or flag OFF: G7 still
#     refuses a generated protocol with no block, exactly as before -- this
#     template is for the new pipeline only.)
#
# WHY brief_status IS NOT SET HERE (code-review correction)
# -------------------------------------------------------------
# An earlier version of this template set `brief_status: open` at the brief
# level. That field is never read there -- run_campaign.py's
# `_register_from_cli` (the `register` sub-command) sets it on the QUEUE
# ENTRY it creates (`{"brief_status": "open"}`, only when
# orchestrator.decide_next.enabled is on), not on the brief file itself; a
# brief-level copy was inert prose, not configuration. Nothing here to fill
# in or check -- decide_next's own registration path handles it.
# ============================================================================

strategy_domain: "<FILL IN: e.g. momentum, mean_reversion, funding_carry, breadth>"
market_universe: [BTCUSDT, ETHUSDT]
timeframe: "1h"
venue: "<FILL IN: e.g. kraken -- must be a (venue, product) pair marked
  tradable: true in config/venue_tradability.yaml, or the run is auto-flagged
  research_only>"
product: "<FILL IN: e.g. spot or perp -- see config/venue_tradability.yaml
  for which pairs are currently tradable>"
research_goal: >
  <FILL IN: one paragraph. What edge are you testing, and why do you expect
  it to survive fees and slippage at your size? (CLAUDE.fork.md's three
  HYPOTHESIS.md questions -- who is on the other side, why the edge survives
  costs, why it hasn't been arbitraged away -- are the bar this needs to
  eventually clear, even though this brief itself defers formal criteria to
  step 1a via criteria_from below.)>
constraints: []
available_data: []

criteria_from: hypothesis_generation

machine_constraints:
  protocol:
    symbols: [BTCUSDT, ETHUSDT]
    timeframe: "1h"
    start: "2018-02-01"
    end: "2025-12-31"
    # holdout: intentionally omitted -- defaults to campaign_data_policy.yaml's
    #   own holdout_range (see the long comment above).
    # promotion: intentionally omitted -- not needed under
    #   config_direct_authoring + verdict_routing_retired (C5.6, D-043; see
    #   the long comment above).
---

# <FILL IN: a short human title for this brief>

Prose below the closing `---` is for human readers only -- the orchestrator
never reads it (run_campaign.py::_parse_brief_frontmatter only parses the
leading frontmatter block above). Use this space to record the idea's
motivation, links, and any context that does not belong in a machine field.
