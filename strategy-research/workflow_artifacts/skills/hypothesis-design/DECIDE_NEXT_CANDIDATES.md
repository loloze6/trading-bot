# Decide-next candidates — addendum to hypothesis-design (E-059 S2a)

**When you see this file.** The orchestrator adds it to your inputs ONLY when
`orchestrator.decide_next.enabled` is on AND this run's `research_brief.yaml`
carries `candidate.criteria_from: hypothesis_generation`
(`run_phase1_research._apply_decide_next_context`). If you are reading it, the
brief is a decide-next candidate and this file governs it.

**This is a deliberate EXCEPTION to IMPROVEMENT 08's four-field rule.**
IMPROVEMENT 08 says a candidate missing any of `config`, `manifest`, `criteria`,
`source` is not a pass-through and must be authored normally. A decide-next
candidate has no `criteria` on purpose (operator decision 2, 2026-09-24:
criteria are never inherited from the run the proposal came from). For this
candidate only, the rules below replace IMPROVEMENT 08; everywhere else
IMPROVEMENT 08 stands unchanged.

The candidate comes from a specialist reader's proposal after an earlier run
(`candidate.source.proposal`: a patch or a new-block sketch, with its
evidence). That proposal may be a different idea from the one the earlier run
tested. Write THIS idea's card:

- `hypothesis_id`: exactly `candidate.source.hypothesis_id` (a new idea linked
  to `candidate.source.parent_hypothesis_id`). The orchestrator stops the run
  before stage 1b if it differs.
- `edge_source`, `signal_concept`, `thesis`: for the proposed change, as
  IMPROVEMENT 01/04 require.
- `criteria`: REQUIRED. Pick from `config/criterion_menu.yaml` (IMPROVEMENT 07)
  for what the proposed idea claims. Each item is `{id: <menu id>}` plus only
  the fields that menu entry lists under `card_overridable`; any other field is
  refused. The orchestrator writes `pre_registration.yaml`'s pass_rule from
  these right after this stage (and again on every re-run of it). Never copy
  the earlier run's criteria.
- Kind `patch` (`candidate.config` and `candidate.manifest` present): copy both
  into the card verbatim and set `pass_through: true`; stage 1b passes the
  config through (stage 5a checks its hash) and code writes the manifest. The
  card still carries its own `claim`. Kind `new_block` (no
  `candidate.config`): do not set `pass_through`; 1b authors the config.
