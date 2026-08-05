# E-018 — Near-miss scoreboard

**State:** parked
**Owner:** Jeremy
**Updated:** 2026-08-05

## Why

Source: `docs/ROADMAP.md` §3.2, verbatim: "**Near-miss scoreboard (your
ranking idea, adopted for ideation only).** Objective: failed-but-instructive
ideas feed the generator. Deliverable: a ranked, auto-updated table over all
tested ideas (evidence quality, failed-criterion margins, root causes),
readable by the idea-generation stage, firewalled from promotion decisions."

Also Part 1, verbatim, on why the firewall is the point and not an
afterthought: "we build both, firewalled: the **near-miss scoreboard** (new,
step 3.2) — a ranked table of every tested idea ... that the idea-generation
stage reads as raw material, and that promotion is *forbidden* to read. The
scoreboard inspires; only the gates decide."

**The difficult requirement is the firewall, not the table.** A ranked table
is a straightforward read-model over the knowledge base. Firewalling it from
promotion — ensuring the promotion decision path has no read access to it —
is the part that protects the frozen pass/fail gates from becoming, in
effect, a leaderboard. A scoreboard built first with the firewall added later
is a leakage vector: any interim state where promotion *can* read the
scoreboard defeats the reason it exists.

**Blocked on:** Phase 2 verdict, for the same reason as E-017 — §3.2 belongs
to Phase 3, which is "ongoing once Phase 2 delivers" per `docs/ROADMAP.md`.
Phase 2's gate: "≥2 new data axes on disk with provenance + a first
registrable indicator each; recorders running."

## Done when

1. A ranked, auto-updated table exists over all tested ideas, carrying
   evidence quality, failed-criterion margins, and root causes.
2. The table is readable by the idea-generation stage.
3. The table is firewalled from promotion decisions: the promotion decision
   path has no read access to it, verified by inspection of what promotion
   code/process actually consults.

## Stories

- [ ] S1 — (blocked behind Phase 2's gate) Build the ranked table over tested
      ideas (evidence quality, failed-criterion margins, root causes).
- [ ] S2 — Wire idea-generation read access and verify, by inspection, that
      the promotion path has no read access to the table — build the
      firewall as part of the same story, not a follow-up.

## Log

- 2026-08-05 — `new` → `parked`. Created from E-013 S1's audit of
  `docs/ROADMAP.md` §3.2 and Part 1 (dispatch W35). Parked on Phase 2's gate.
