# E-035 — External knowledge: let the loop propose an idea from outside its own history

**State:** new
**Owner:** Jeremy
**Updated:** 2026-08-27

## Why

Split out of **E-032** on 2026-08-27. E-032's own objective — stop the loop
proposing neighbours of what it already tried — is met and closed: the
exclusion digest, the anti-adjacency gate, the disposition, and the
retry-then-escalate wiring all landed (S1/S2a/S2b/S2c). What remains is a
**different capability**, not a loose end of that one, so it gets its own
epic rather than holding a finished epic open.

**The problem this solves.** E-032 S1 measured that the idea-generating
stages are closed-book: `hypothesis_generation` receives only
`research_brief.yaml` + `available_feeds.yaml` + `indicator_library.yaml`,
`innovation_expansion` only the brief plus the card it expands, and every
stage agent runs with `allowed_tools=[]`. E-032 fixed what the loop can
**remember** (it can now see what has been tried and refuse a repeat). It did
not fix what the loop can **reach**: every idea it proposes still comes from
inside its own history and the indicator library.

Operator framing (2026-08-23): *"it can read litteratures, take it from forum
(reddit), propose innovation from his knowledge. This part is very important
if we do not want to stay in the corner of 'exhausted ideas' that are too
much by the book."*

Supporting evidence, MEASURED: 59 runs produced **0 promotions across 38
graded verdicts**, and in that entire history the loop asked for exactly
**one** thing it did not already have (`feed_wishlist.yaml` holds 1 entry)
and built **zero** new components (`campaign_state.components_built` is
empty). The search stayed inside classic single-asset TA — the lane
`CLAUDE.fork.md` already calls a proven dead end.

## Done when

1. The idea-generation stage can dispatch to an external knowledge agent
   (literature, forums, model knowledge) when internal sources are exhausted.
2. That agent returns **mechanisms, not fitted rules** — anything imported
   must be re-expressible in the bot's core logic (forecast → allocation,
   regime detection, regime→strategy mapping), so nothing arrives
   pre-parameterised to someone else's backtest.
3. Every externally-sourced idea records its **source and date**. Not for
   lookahead — a mechanism is not a bar timestamp — but for **publication
   bias**: the ideas that get written up are the ones that appeared to work
   recently. The existing era-stability bar (sign-consistent across
   2018-20 / 2021-22 / 2023-25) is the control; the source field is what
   makes anyone remember to apply it.
4. Every generated idea that gets tested produces a trial row. Autonomous
   generation that does not count itself silently inflates N for every future
   deflated-Sharpe claim.
5. Off by default with a bit-identity proof, per the standing rule.

## Stories

- [ ] S1 — **Characterize and STOP.** What would it take for a stage to
      dispatch outward: where the grant lives, what triggers exhaustion of
      internal sources, and how a returned mechanism is shaped so the
      existing registration contract can accept it. E-032 S1's Task 4
      already sketched this — start from it, verify it against current code
      (E-032/E-034 changed things since), do not re-derive from scratch.
- [ ] S2 — The external-knowledge dispatch path, with source/date recording.
- [ ] S3 — Wire E-018's near-miss scoreboard in as the internal-source input
      it was explicitly built to be (`docs/CAMPAIGN_PROGRAM.md` Part 1: *"a
      ranked table ... that the idea-generation stage reads as raw material,
      and that promotion is forbidden to read"*). This is E-018's own S2 seen
      from the consumer side — coordinate, do not duplicate.

## Relationship to other epics

- **E-032** (closed 2026-08-27) — parent. Its gate is the filter that keeps
  an externally-sourced idea from being a repeat; this epic is the supply.
  Together: E-032 stops bad ideas, E-035 finds new ones.
- **E-018** (near-miss scoreboard, S1 done) — its S2 has been waiting for a
  consumer to wire read access to. This epic is that consumer.
- **E-031** (queue return edge, S3 unbuilt) — an idea from here still needs a
  path into the queue. E-031 S3 is that path; neither is sufficient alone.

## Success signal (pre-registered)

Within 60 days of S2: at least one registered hypothesis carries a recorded
external source and date, names a family absent from `failed_families` at the
time it was proposed, and reaches a graded verdict. An externally-sourced idea
REFUSED by E-032's anti-adjacency gate also counts as the system working, and
is logged.

## Log

- 2026-08-27 — `new`. Split out of E-032 so a finished epic could close.
  E-032's four stories delivered its stated objective (stop proposing
  neighbours); this is the separate capability of reaching outside the
  loop's own history, which that epic named but never built.
