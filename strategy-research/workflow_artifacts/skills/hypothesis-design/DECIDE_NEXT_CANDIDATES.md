# Decide-next candidates — addendum to hypothesis-design (E-059 S2a)

**When you see this file.** The orchestrator adds it to your inputs ONLY when
`orchestrator.decide_next.enabled` is on AND this run's `research_brief.yaml`
carries `candidate.criteria_from: hypothesis_generation`, or is a fold child
with fixed criteria (below; `run_phase1_research._apply_decide_next_context`). If you are reading it, the
brief is a decide-next candidate and this file governs it.

**This is a deliberate EXCEPTION to IMPROVEMENT 08's four-field rule.**
IMPROVEMENT 08 says a candidate missing any of `config`, `manifest`, `criteria`,
`source` is not a pass-through and must be authored normally. A decide-next
candidate has no `criteria` on purpose (operator decision 2, 2026-09-24:
criteria are never inherited from the run the proposal came from). For this
candidate only, the rules below replace IMPROVEMENT 08; everywhere else
IMPROVEMENT 08 stands unchanged.

The candidate comes from a specialist reader's proposal after an earlier run
(`candidate.source.proposal`: a side finding, a patch from an older run, or a
new-block sketch, with its evidence). That proposal may be a different idea from the one the earlier run
tested. Write THIS idea's card:

- `hypothesis_id`: exactly `candidate.source.hypothesis_id` (a new idea linked
  to `candidate.source.parent_hypothesis_id`). The orchestrator stops the run
  before stage 1b if it differs.
- `edge_source`, `signal_concept`, `thesis`: for the proposed change, as
  IMPROVEMENT 01/04 require.
- `criteria`: REQUIRED. Pick from `config/criterion_menu.yaml` (IMPROVEMENT 07)
  for what the proposed idea claims. The live entries are `sign_consistent_by_era`,
  `whole_test_sharpe_positive` and `forecast_ic_median` (median over windows of the all-bars forecast/next-bar IC
  `>` 0.02, fixed threshold, D-134); `realized_edge_to_cost_ratio` is retired for blocks
  (`retired_for: [block]`, D-107/D-128/D-133) and a card naming it is refused. `residual_ic` (card A) is added by
  code to every forecast-block idea when composition runs are on; there you may name it (`{id: residual_ic}`, no
  overrides) and it stays one criterion, code's own; leaving it out removes nothing; elsewhere naming it is refused
  (D-137). Naming it gains nothing, so if unsure, leave it out; it never counts as the card's own criterion
  (still pick at least one live entry). Each item is `{id: <menu id>}` plus only
  the fields that menu entry lists under `card_overridable`; any other field is
  refused. The orchestrator writes `pre_registration.yaml`'s pass_rule from
  these right after this stage (and again on every re-run of it). Never copy
  the earlier run's criteria (except a fold child with fixed criteria, below).
- Kind `patch` (`candidate.config` and `candidate.manifest` present): copy both
  into the card verbatim and set `pass_through: true`; stage 1b passes the
  config through (stage 5a checks its hash) and code writes the manifest. When
  CLAIM_TESTS.md is in your inputs, the card still carries its own `claim`.
  Kind `new_block` (no
  `candidate.config`): do not set `pass_through`; 1b authors the config.
  Kind `side_finding` (`candidate.claim`, and `candidate.start_config` when the
  earlier run's config is carried): do not set `pass_through`; PREFILLED_CLAIM.md
  says how to write the card; 1b starts from `candidate.start_config`.

**Fold child with fixed criteria (D-121, `orchestrator.brief_criteria`).** A
fold child's brief may carry NO `candidate.criteria_from` and instead an
`evaluation.pass_rule` with the source run's criteria (menu ids). Then the
criteria are fixed: copy them into the card's `criteria` verbatim and do not
change them. The orchestrator does not rebuild `pre_registration.yaml`'s
pass_rule from your card in that case. Everything else above applies.
