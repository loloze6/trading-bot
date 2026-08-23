# E-032 — Proactive idea generation: the loop must be able to propose something it has not already tried

**State:** in-progress (S1 dispatched 2026-08-23)
**Owner:** Jeremy
**Updated:** 2026-08-23

## Why

The loop is **not** short of ideas. It generates them constantly — and every
one of them is a neighbour of the idea it is already holding.

Measured (2026-08-23, `research-system-evolution` review):

- **30 of 36 completed runs produced a follow-on idea** — 19
  `completed_refined`, 11 `completed_reframed` (counted from
  `pending_stage` across the 58 `runs/run_*/pipeline_state.yaml` files, 59 run
  dirs). The generating stages exist and fire: `hypothesis_generation` and
  `innovation_expansion` are both in `workflow/stages.yaml`, and
  `innovation_expansion` sits on both the initial and the refinement path.
- Every one of those follow-ons is **adjacent**: tweak a parameter, reframe the
  same family, adjust a threshold. They live inside a lineage and die when it
  terminates.
- **The curiosity deficit, in one number: in 59 runs the loop asked for exactly
  one thing it did not already have.** `campaign_record/feed_wishlist.yaml`
  holds a single entry (`liquidation_data`). `campaign_state.yaml`'s
  `components_built` is an **empty list**.
- Result: 59 runs stayed inside classic single-asset TA — the lane
  `CLAUDE.fork.md` already calls proven dead — and produced **0 promotions
  across 38 graded verdict files** (`protocol_verdict`: 26 refine, 10 kill, 2
  absent; `status`: 14 refine, 10 pivot, 7 escalate, 2 kill, 5 absent).

Operator framing (2026-08-23): *"another thing might be also to enhance the
'curiosity' and 'innovation' of the steps generating the run ideas backlog"* —
and, on sourcing, *"it can read litteratures, take it from forum (reddit),
propose innovation from his knowledge. This part is very important if we do not
want to stay in the corner of 'exhausted ideas' that are too much by the book."*

## What this epic is not

Not a strategy-search epic. It changes **who proposes**, never what passes.
Every generated idea goes through the same registration contract, validation,
prescreen, frozen pass rule and holdout discipline as an operator-authored one.
The bright line (frozen rule → one-shot holdout) is untouched.

## Done when

1. An idea-generation agent exists with a **custom disposition**: proactive,
   empowered to declare a direction exhausted and redirect, expected to propose
   non-adjacent ideas rather than the next parameter over.
2. **The anti-adjacency gate is mechanical, not aspirational.** A proposed idea
   is REFUSED at the gate if it collides with `failed_families`,
   `recent_parameter_dimensions_by_family`, `instruments_tried`, or
   `timeframes_tried` in `campaign_state.yaml`. "Propose clever ideas" is
   unfalsifiable prose; a refusal condition is testable. This is the criterion
   that makes the epic reviewable.
3. The agent can dispatch to an **external knowledge agent** (literature,
   forums, model knowledge) when internal sources are spent. That agent returns
   **mechanisms, not fitted rules** — anything imported must be re-expressed in
   the bot's core logic (forecast → allocation, regime detection,
   regime→strategy mapping), so nothing arrives pre-fitted.
4. Every externally-sourced idea records its **source and date**. Not for
   lookahead — a mechanism is not a bar timestamp — but for **publication
   bias**: the ideas that get written up are the ones that appeared to work
   recently. The existing era-stability bar (sign-consistent across 2018-20 /
   2021-22 / 2023-25) is the control; the source field is what makes anyone
   remember to apply it.
5. Off by default; fast suites green; no engine change.

## Stories

- [x] S1 — **Characterize and STOP.** What the generating stages can see today
      versus what they would need to propose something non-adjacent. Where the
      disposition lives (skill file / stage prompt / config). What the
      anti-adjacency gate can key on that already exists. No code.
- [x] S2a — **The exclusion digest + the deterministic anti-adjacency gate.**
      No disposition/persona prose (S1 measured that prose alone repeats an
      already-ineffective pattern). Build only.
- [ ] S2b — The disposition (skill-prose amendment on the two generating
      stages, instructing them to consult the digest).
- [ ] S3 — The external-knowledge dispatch path, with source/date recording.

## Relationship to other epics

- **E-031** (queue return edge) — the plumbing. E-032 is the quality. Neither
  is sufficient alone: E-031 without E-032 re-queues neighbours faster;
  E-032 without E-031 generates ideas that cannot reach the queue.
- **E-018 (near-miss scoreboard) is this epic's feedstock, and it is currently
  parked.** `docs/CAMPAIGN_PROGRAM.md` Part 1 describes it as *"a ranked table
  of every tested idea (IC, cost ratio, which criteria it failed and by how
  much, root cause, era behavior) **that the idea-generation stage reads as raw
  material**, and that promotion is forbidden to read."* It is parked behind
  Phase 2's gate, yet its input is 38 already-recorded verdicts, not the new
  data axes. **Unparking E-018 is an open operator decision (2026-08-23) and a
  dependency of this epic, not an action taken here.**
- **E-029 / E-027** (trade record carries the decision; exit-cause
  attribution) — feedstock that makes the agent smarter at *diagnosing* a
  failure. Not blocking: the campaign-level record (`failed_families`, 36
  recorded failure modes, `altitude_history`) is already enough to avoid
  re-proposing dead families, which is what this epic needs first. INFERRED,
  not measured.
- **E-025** (dual-writer ledger) — every generated idea that gets tested is a
  trial and must count toward N. See E-031 Done-when #3.

## Success signal (pre-registered, per the skill's A8)

Within 60 days of shipping: at least one registered hypothesis names a family
absent from `failed_families` AND an instrument or timeframe absent from
`instruments_tried` / `timeframes_tried` at the time it was proposed — and it
reaches a graded verdict. A generated idea that is refused by the
anti-adjacency gate also counts as the gate working, and is logged.

## Log

- 2026-08-23 — `new`. Opened from a `research-system-evolution` review,
  measured above. Split from E-031 at the operator's direction. The operator's
  own correction drove the framing: the loop is not idea-poor, it is
  adjacency-bound, and refill without curiosity just repeats dead families at
  higher throughput.

- 2026-08-23 — **S1 done.** See
  `engineering/roadmap/E-032/artifacts/s1_idea_generation.md` +
  `.../artifacts/s1_measure_idea_generation.py` (read-only, re-runnable).

  **Adjacency is structural, three independent layers, not a prose problem.**
  (1) `hypothesis_generation` (3 required_inputs: research_brief, available_feeds,
  indicator_library) and `innovation_expansion` (2: research_brief,
  hypothesis_card) never receive `campaign_state.yaml`, the KB, or the
  near-miss scoreboard — `run_claude_worker` builds the whole prompt from
  `stages.yaml`'s `required_inputs`/`optional_inputs` and nothing else
  (`workflow/run_phase1_research.py:686-761`). Only `campaign_review` reads
  `campaign_state.yaml`, once per 6 runs, and its output is orphaned
  (`next: []`). (2) `expanded_hypothesis_card.schema.json` requires
  `base_hypothesis_id` and has no field for an unrelated hypothesis — a
  schema-conformant expansion is definitionally a child of one parent.
  (3) Stage agents run with `ClaudeAgentOptions(model="claude-haiku-4-5",
  allowed_tools=[])` (`run_phase1_research.py:788`) — zero tools, closed-book.

  **Anti-adjacency gate: `instruments_tried`/`timeframes_tried` are confirmed
  stale, and confirmed WRONG at the grain a gate needs, not just outdated.**
  `instruments_tried` (4 symbols) predates XS_momentum's 19-pair ratification
  (2026-07-22). `timeframes_tried` (`1h, 4h, 15m`) is family-blind: direct
  scan of all 7 funding-family `hypothesis_card.yaml` files found timeframes
  `{1h, 1d}` only — the `'4h'` entry comes entirely from 11 unrelated
  `keltner`-family runs. **A gate keyed on the global list would wrongly
  REFUSE a funding-family 4h proposal.** Recommended fix: layer the gate
  KB-reactivation-clause-first (per-branch granularity, e.g.
  `funding_rate_continuous_mean_reversion_expanded_auto`'s `4h or daily`
  clause, correctly still open after the daily branch was killed as
  `run_059`/`funding_mr_daily_retest_killed`), refreshed per-family
  `(family, instrument, timeframe)` triples second, and never trust the flat
  `campaign_state.yaml` lists as a global veto.

  **Worked calibration case, traced through the recommended gate: ADMIT.**
  The funding-rate 4h retest matches the still-open, unconsumed 4h branch of
  `funding_rate_continuous_mean_reversion_expanded_auto` (the daily branch's
  closure explicitly does not close the parent, per the KB's own text). Had
  the gate checked the flat `timeframes_tried` list first, it would have
  produced a false REFUSE — the calibration case is exactly the trap the
  layering exists to avoid. A same-day reproduction of `run_059` under the
  post-two-bars-fix engine convention (`E-012/EPIC.md`, 2026-08-23) found
  BTCUSDT median Sharpe crosses -0.296 → +0.016, but the pass-rule kill is
  unchanged (still FAIL on drawdown both symbols) — strengthens confidence
  the daily-branch kill is real, without reopening it.

  **Disposition lands in three places, not one:** a new `required_input` on
  the two generating stages (a small exclusion-digest artifact, not raw
  `campaign_state.yaml`), an additive SKILL.md prose section on both skills
  (matching the project's existing "IMPROVEMENT NN" convention), and a new
  deterministic `tool:` stage for the refusal itself (`tools/anti_adjacency_gate.py`,
  same pattern as `signal_prescreen`) — prose alone repeats the existing,
  measured-ineffective pattern (this project already has prose refusal rules
  in `hypothesis-design/SKILL.md`; 30 of 36 completions were adjacent anyway).

  **External-knowledge dispatch (Task 4, characterization only):** needs its
  own stage/tool grant (current stages have `allowed_tools=[]` by deliberate
  design, not oversight), a trigger keyed to gate-exhaustion (mirroring
  E-031's "zero admissible candidates" terminal state), and MUST route its
  output through the SAME `edge_source`/A1.3 anti-confabulation check
  internally-generated ideas already clear — no parallel, weaker gate for
  imported ideas.

  **Near-miss scoreboard (E-018 S1) fitness:** usable as raw material but
  thin (numeric margin recovered 24/59, IC 7/59, cost ratio 5/59) and its
  `worst_fail_margin_frac` column mixes the pre/post two-bars-fix engine
  convention (58 of 59 run dirs are pre-fix) — a consuming skill must check a
  row's run date against 2026-08-09 before treating its margin as current,
  demonstrated concretely on run_059's own row in this story. Not wired as an
  input anywhere today (no `stages.yaml` entry references it); E-018 S2 and
  this epic's gate stage should land together.

- 2026-08-23 — **S1 reviewed by the dispatching session; two load-bearing
  claims verified by execution, one gap added, one of the dispatcher's own
  claims retracted.**

  VERIFIED. The generating stages are closed-book, and this is the whole
  explanation for adjacency. `stages.yaml`: `hypothesis_generation` receives
  only `research_brief.yaml` + `available_feeds.yaml` +
  `indicator_library.yaml`; `innovation_expansion` only the brief + the card
  it is expanding. Neither ever receives `campaign_state.yaml`, the KB, or the
  scoreboard. And `run_phase1_research.py:788` runs every stage agent as
  `ClaudeAgentOptions(model="claude-haiku-4-5", allowed_tools=[])` — zero
  tools, by explicit design comment ("prevent it from wandering off").
  **The idea generator cannot know that 59 runs happened.** It is not
  conservative; it is amnesiac and blindfolded. Only `campaign_review` gets
  `campaign_state.yaml`, once per 6 runs, and its output is orphaned
  (`next: []`).

  Consequence for scoping: **E-032 is primarily an INPUT problem, not a
  disposition problem.** Prose telling a closed-book agent to be adventurous
  cannot work; it has nothing to be adventurous about. S2 must land the
  exclusion digest as a `required_input` before any disposition text is worth
  writing.

  GAP ADDED — precedence between disagreeing artifacts. S1's gate admits the
  4h funding retest by reading the KB's parent `reactivation_condition` and
  the explicit closure note that the child's kill "does NOT itself close the
  parent." That is well-evidenced and the dispatching session accepts it. But
  the daily brief's own pre-registered pass rule says the opposite in its own
  text — *"the mechanism's LAST escalation ... no further timeframe exists
  under it"* — and registered `lineage_routing: terminate`. Two binding
  artifacts disagree on their face; S1 resolves it by preferring the KB and
  does not say that it is doing so. **S2 must state a precedence order
  explicitly** (proposal: a registered `lineage_routing: terminate` closes the
  lineage it names, and only the KB's parent entry can keep a sibling branch
  open — which is what happened here). Left implicit, the gate will one day
  re-open a genuinely terminated lineage and no rule will have been broken.

  RETRACTED, dispatching session's own error. The dispatch brief and the
  operator-facing summary both claimed "cost has killed this family twice
  (1h edge_to_cost_ratio 0.2425; daily cost_ratio 2.2927)" and used it as an
  argument against 4h. Wrong: 2.2927 was a **PASS**. `run_059`'s
  `prescreen_result.yaml` records `safety_factor_required: 2.0`,
  `pass: true`; `run_044`'s records the same threshold with `pass: false` at
  0.2425. Cost killed the 1h branch once; the daily branch cleared the cost
  gate comfortably and died on Sharpe and drawdown. The a-priori case against
  4h is therefore weaker than the dispatcher stated, and S1's ADMIT verdict is
  better founded than the brief that commissioned it.

- 2026-08-23 — **S2a done (build only, no disposition prose).** Two new
  tools, both read-only over runs/, no LLM call:

  `tools/build_exclusion_digest.py` -- Task 1, the exclusion digest.
  Family-scoped `(family, instrument, timeframe)` triples, re-derived FRESH
  from `runs/run_*/artifacts/hypothesis_card.yaml` every regeneration, never
  from `campaign_state.yaml`'s stale flat lists. `classify_family()`
  prioritizes `library_lookup.indicator_id` (structural), then
  `edge_source.evidence_type`, then a keyword match bounded to
  `hypothesis_id` + `edge_source.specific_mechanism` + thesis's FIRST
  SENTENCE ONLY -- never rationale, never full thesis. That restriction is
  load-bearing, not defensive posture: while building this, S1's own
  measurement script's free-text "mentions funding" search was found to
  mis-classify run_048/run_058 (Fear & Greed hypotheses whose rationale
  incidentally discusses "funding rate availability" as an unrelated
  structural cause) as funding-family evidence. `classify_family()` correctly
  separates them (`tests/test_build_exclusion_digest.py::
  test_classify_family_never_scans_rationale_the_run048_058_false_positive`).
  Re-derived fresh against the real repo: funding_rate_extreme's triples are
  exactly `{1h, 1d}` (run_041/044/047/050 at 1h, run_059 at 1d) -- never 4h;
  keltner_channel is the actual source of the 4h entry. Regenerated snapshot
  committed at `campaign_record/exclusion_digest.yaml` (46 runs scanned, 2
  pre-existing unparseable cards skipped gracefully, 12 families, 30 triples).

  `tools/anti_adjacency_gate.py` -- Task 2, the deterministic gate, `tool:`
  stage documented in `stages.yaml` (declarative only -- `stages.yaml` is not
  read by the live orchestrator; see the stage's own comment and the scoping
  note below). Two layers, KB first, digest second, exactly as S1
  recommended, with one correction found while implementing: **Layer 1 must
  match at MECHANISM grain (hypothesis_id containment), never at FAMILY
  grain.** A first implementation attempt matched Layer 1 on the same family
  classifier as Layer 2 and immediately mis-fired on the calibration case
  itself -- `funding_rate_mean_reversion_inconclusive` (H-041-A, exhausted,
  no reactivation_condition) sits in the SAME family bucket
  (`funding_rate_extreme`) as `funding_rate_continuous_mean_reversion_
  expanded_auto` but is a wholly unrelated, independently-closed mechanism;
  matching Layer 1 at family grain let H-041-A's closure wrongly refuse the
  4h candidate before the correct finding was ever reached -- the exact
  failure mode this gate exists to prevent, relocated one layer down.
  Caught by testing against the real KB before writing the fixture tests,
  not found later.

  **Precedence rule, implemented as specified.** A registered
  `lineage_routing: terminate` (read from a run's own
  `pass_rule_evaluation.yaml`) closes only the branch the terminating run
  itself tested, on a KB entry that explicitly, textually references its
  parent (`_finding_references_parent`, a literal substring check -- this KB
  schema has no structured parent-id field). `funding_mr_daily_retest_killed`
  references `funding_rate_continuous_mean_reversion_expanded_auto` in its
  own `exhausted_basis` text and its evidence run (run_059) carries
  `lineage_routing: terminate` -- closes the DAILY branch of that parent
  only. The 4h branch, never tested by any run, is untouched. A first
  implementation pass wrote `_finding_references_parent` but never called
  it (`_branches_closed_by_lineage_routing` only scanned the candidate's own
  matched-finding set, which never includes the child that does the
  closing) -- caught immediately by the calibration-case REFUSE test failing
  where it should have passed, fixed same session.

  **Verified, both directions, against the real repo (not mocked):**
  the 4h candidate ADMITs (`test_calibration_case_admits_the_4h_funding_
  retest`); the identical candidate would be wrongly REFUSED by a naive gate
  keyed on `campaign_state.yaml`'s flat `timeframes_tried` list, which still
  contains `4h` from the unrelated keltner runs
  (`test_calibration_case_naive_flat_list_gate_would_refuse_the_same_
  candidate` -- asserts the two gates DISAGREE, not just that the real one
  passes); the daily candidate REFUSEs via the precedence rule
  (`test_precedence_rule_refuses_the_daily_branch_terminated_by_run_059`);
  and the 4h/daily branches are proven independent
  (`test_precedence_rule_never_touches_the_sibling_4h_branch`).

  **Required-input wiring (Task 1's "delivered as a new stage input"),
  off by default.** `config/campaign_config.yaml`'s new
  `orchestrator.exclusion_digest_input.enabled` (default false, same shape as
  E-030 S2a's `halt_policy.quarantine_enabled`), read by
  `run_phase1_research._exclusion_digest_input_enabled()`. When on,
  `_apply_exclusion_digest_input()` unions `campaign_record/
  exclusion_digest.yaml` into `hypothesis_generation`/`innovation_expansion`'s
  `optional_inputs`, mirroring the existing B7 mandatory-input-union pattern.
  Off-by-default is proven against the actual assembled PROMPT TEXT, not just
  "the code path is skipped": `run_claude_worker`'s prompt-building logic was
  extracted verbatim into a new pure function, `_build_stage_prompt()`, so
  tests can assert flag-off produces a prompt byte-identical to a baseline
  that never calls the union function at all
  (`tests/test_exclusion_digest_input.py::
  test_flag_off_prompt_is_byte_identical_to_never_calling_the_union_at_all`,
  plus the absent-key/section case). Flag-on is proven to actually change the
  prompt and carry digest content through to both generating stages.

  **Also found, incidentally, while tracing the input path:** the ALREADY-
  EXISTING optional_input for `campaign_knowledge_base.yaml` in
  `workflow_artifacts/templates/handoffs/research_brief_to_hypothesis.yaml`
  (`path: "../../campaign_knowledge_base.yaml"`) has never once resolved --
  the real file lives at `campaign_record/campaign_knowledge_base.yaml`,
  two directories further down than the template's path reaches. Since
  `run_claude_worker` treats a missing `optional_input` as silent absence
  (no error, no log), this has been a no-op for every run to date, on top
  of S1's structural finding that neither generating stage sees campaign
  history at all. Noted in `_apply_exclusion_digest_input()`'s own docstring;
  not fixed here -- fixing an unrelated pre-existing path bug is out of this
  story's scope, flagged for S2b or a follow-up.

  **Deliberately left out of S2a's scope, stated plainly, not silently
  narrowed:** the gate is NOT wired into the live orchestrator's stage
  dispatch (`STAGE_CONFIGS`/`run_tool_worker`/the `next:` routing state
  machine) -- only documented declaratively in `stages.yaml`, which the
  orchestrator does not read at runtime. Wiring live dispatch means deciding
  what happens on REFUSE (loop back to `hypothesis_generation`? terminate the
  run? how many retries?) -- a real orchestration design decision, and this
  session's hard constraints forbid running a campaign to verify any such
  wiring behaves correctly. Also not built: a `family` field on
  `hypothesis_card.schema.json` (S1's build-list item 1) -- the classifier's
  structural-field-first, keyword-bounded-fallback design does not require
  it, and adding an unused schema field without a consumer felt like scope
  creep against "prefer minimal code changes."

  Verification: strategy-research fast suite 954 passed (was 910; +44 new,
  all in the three new test files, zero regressions). trading-bot fast suite
  383 passed / 2 skipped, unchanged from the session's own reference figure
  (nothing under `trading-bot/` was touched). No campaign or backtest run;
  no LLM call made; `local_data/holdout_sealed/` never read.
