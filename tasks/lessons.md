# Lessons (appended after user corrections)

## 2026-09-18 — Don't propose a control that already exists as a step
Pattern: proposed a "requires new data, yes/no" flag for idea proposals; the operator pointed out E-054's
data-availability gate already does this, per variant, pre-backtest.
Rule: before proposing any new check/flag/score, grep the stage graph (STAGE_CONFIGS, USER_GUIDE §2.1)
and the existing gates; if a step already owns the concern, route to it instead of adding a sibling.

## 2026-09-18 — Component-gap detection belongs where words become config
Pattern: put the "requires new component" outlet at hypothesis design (Step 1); the operator corrected
that feasibility is checked at backtest_specification, where the design is turned into a bot config.
Rule: place a check at the earliest step that has the concrete information the check needs, not the
earliest step conceptually related to it.

## 2026-09-17 — Write for a new joiner
Pattern: first review reply was dense and jargon-heavy; the operator asked for the same content in plain
words.
Rule: default to plain language, short sentences, one idea per sentence; keep file paths and line refs
in the record file, not in the prose the operator reads.

## 2026-09-23 — Built two slices on the legacy verdict vocabulary the target design had retired
- **Pattern:** E-046a 5b-ii-A/B1 made the 5 readers' proposal scores decide refine/kill and fed a per-family circuit breaker. The agreed target (roadmap v26/v27 cards G/I, delivery_plan_v26.md slices 2, 6b, 6c) says: idea status = the grid (validated/refuted/inconclusive), reader scores only RANK the next candidate (decide_next, 6b), refine/pivot/escalate/kill + the circuit breaker are retired (6c), repeats are caught by an exact-match check (slice 8). I framed the 5b S1 question as "who synthesizes the readers into a routing decision", the operator answered the question as framed, and two builds followed. The operator caught it from the downstream questions ("why do we still have escalation?").
- **Rule:** before designing any slice that touches verdicts, routing or "what runs next", re-read the target cards and the delivery plan's LATER slices that retire things, and check the design does not re-create what a later slice deletes. When an S1 finding offers a choice, first ask "does the target design already answer this?" — never pose a question whose framing presupposes retired machinery.
