# Campaign review under retired verdict routing — note to campaign-review (E-059 slice 6c S2b)

**When you see this file.** The orchestrator adds it to your inputs ONLY when
`orchestrator.verdict_routing_retired.enabled` is on AND this review was started
by that flag's trigger (`run_phase1_research._apply_retired_routing_review_context`).
If you are reading it, verdict routing is retired and this note governs how
your recommendation is used. Where it disagrees with SKILL.md, this note wins;
everywhere else SKILL.md stands.

## What changed

- **An idea's status comes only from the grid.** Every run in
  `artifacts/campaign_review_digest.yaml` carries its `idea_status`
  (`validated`, `refuted` or `inconclusive`). Cite it; never restate, override
  or re-grade it. An entry with `engineering_fault` is a broken run, not a
  finding.
- **The next run is chosen only by decide-next.** Your review never picks it.
- **Your inputs:** `artifacts/campaign_review_digest.yaml` (written by code
  from the campaign memory: every run since the last completed review in full,
  counts for the earlier runs), this run's `research_brief.yaml` and, when it
  exists, the KB (if it is absent, its input says so: answer the KB questions
  with "no KB yet", never invent KB content). `campaign_state.yaml`'s
  `failed_families`, `hypothesis_family`, altitude history, `diagnostics_log`
  and `verdict_interpretation.yaml` belong to the retired routing: do not ask
  for them and do not reason from them.
- **Why you were called:** at least `review_every_n_runs` (6) runs recorded
  in the memory without an engineering fault are not yet covered by a
  completed review -- they are the digest's `runs_since_last_review`.

## What each recommendation does now

| recommendation | effect |
|---|---|
| `continue` | Recorded only. The run ends with its grid status. Do NOT write `next_research_question` (it is ignored). |
| `reframe` | `next_research_question` becomes a brief, `campaign_record/candidate_briefs/<run_id>__reframe.md`, registered as a `ready` queue entry (origin `campaign_review`). decide-next then picks the next run; an operator entry still goes first. |
| `escalate_instrument` | Recorded only. |
| `escalate_component` | Recorded only; your `recommendation_rationale` is appended to `campaign_record/component_requests.yaml` for the operator. |
| `terminate` | The campaign stops for the operator (pause `campaign_review_terminate`). Use it only when the memory shows the search space is spent. |

## Rules for a reframe

- `next_research_question` is a complete `research_brief.yaml`: it needs
  `strategy_domain`, `market_universe`, `timeframe`, `research_goal`, `venue`
  and `product`. A key you leave out is taken from this run's
  `research_brief.yaml`; if it is missing there too, the run stops.
- Do NOT write `candidate`, `criteria_from`, `machine_constraints` or
  `evaluation.pass_rule` (the run stops if you do). The orchestrator adds
  them: the new idea's criteria are chosen at step 1a from
  `config/criterion_menu.yaml` (never inherited from this run), and its
  protocol is pinned to this run's.
- It is a NEW question: the wishlist and KB-reactivation rules of SKILL.md
  still apply, and the orchestrator still checks both.

## Rules for terminate

This replaces SKILL.md's escalation-era guard (`instruments_tried ≥ 3 AND
components_built ≥ 1`), whose fields no longer grow. Before recommending
`terminate`, cite the memory's `idea_status` counts (how many runs validated,
refuted and inconclusive) and the KB's untested cells, and say why none is
worth a run. Prefer `reframe` while an untested, non-exhausted cell remains.
