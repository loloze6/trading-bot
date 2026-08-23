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
- [ ] S2 — The disposition and the anti-adjacency gate.
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
