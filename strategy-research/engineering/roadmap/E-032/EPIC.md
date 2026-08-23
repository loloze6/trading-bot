# E-032 — Proactive idea generation: the loop must be able to propose something it has not already tried

**State:** new
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

- [ ] S1 — **Characterize and STOP.** What the generating stages can see today
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
