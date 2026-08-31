# E-037 S5 — Anchor migration: `file:line` → `file::symbol`

**State:** scheduled — to run **after** S4's remaining items and **before**
Jérémy's review (his sequencing, 2026-08-31)
**Why it is its own stage:** two automated attempts were reverted mid-S3. It
needs a plan written before code runs, not a session-end rewrite.

---

## 1. The case for doing it

Line numbers rot on every edit above them. Measured during S2: **nine of
roughly forty anchors were wrong on the day they were written** — before any
refactor. `run_phase1_research.py` is over 6,000 lines and changes often.

A symbol is better on every axis that matters:

| | `run_phase1_research.py:5383` | `run_phase1_research.py::_route_holdout_evaluation` |
|---|---|---|
| Survives an edit above it | no | yes |
| Greppable | no | yes |
| Says *what* you are looking for | no | yes |
| Machine-verifiable | only "in range" | "this symbol exists" |

**Every anchor has a stable name available**, confirmed by dry run: 67 of 78
explicit anchors sit inside a top-level function or class; the other 11 sit in a
module-level named constant (`STAGE_CONFIGS`, `_SIG_THRESHOLD`, `_SKILL_MAP`,
`VALID_METHODS`). Exactly one — a section comment — has neither, and resolves to
the function immediately below it.

## 2. Why the first two attempts failed

Neither failed on the explicit anchors. Both failed on the **163 bare `:N`
shorthands** used inside a stage block that has already named its file.

- **Attempt 1** resolved a bare `:N` to "the last `.py` filename mentioned
  anywhere in the text". Prose between the block header and the anchor mentions
  other files, so anchors were attributed to `deflate_sharpe.py`,
  `timeframe.py` and others. It wrote before validating, and corrupted
  `FINDINGS.md` with `::run_tool_worker` credited to `prescreen_signal.py`.
- **Attempt 2** added a refuse-on-doubt gate, which correctly refused: 47
  unresolved. Nothing was written. But it left the corpus half-converted from
  attempt 1, which had to be reverted by hand.

**Lesson, and the rule for S5:** a mechanical rewrite of prose must validate
before it writes, and a half-converted document is worse than an unconverted
one.

## 3. The plan

**Rule for bare `:N` — block scope, not text scope.** Each `#### Stage N` block
declares its file in the **Engine** line and again in **Owned by which code**. A
bare `:N` inside a block resolves against *that block's* declared file, and
against nothing else. Prose mentioning another file does not change the scope.
Anchors outside a stage block must be explicit or are left alone.

**Steps.**

1. Parse the guide into stage blocks; extract each block's declared file(s).
   **Refuse to proceed** if a block declares zero or more than one candidate
   without an explicit anchor to disambiguate.
2. For every anchor — explicit or bare — resolve line → enclosing top-level
   symbol via `ast`, as the dry run already does.
3. **Validate the whole plan in memory.** Any unresolved anchor, any symbol not
   found in the target file, any block with ambiguous scope → **abort, write
   nothing, print the list.**
4. Only on a fully clean plan, write.
5. Re-run `tests/test_doc_anchors.py`, which validates `::symbol` anchors
   against the file's real top-level names.
6. Run the information-loss check. Anchors are identifiers, so a `:N` → `::sym`
   conversion **will** register as identifier churn — expected, and itemised in
   the S5 inventory rather than waved through.

**Out of scope:** anchors in `FINDINGS.md` prose that quote a line number as
*evidence for a finding* (e.g. "raises at `:1320`"). Those are measurements
taken on a dated commit, not navigation. They stay as-is, and S5 records which
they are.

## 4. Acceptance

- [ ] `tests/test_doc_anchors.py` green, with the reported split showing
      **0 by line number** for navigation anchors
- [ ] every `::symbol` resolves — enforced by that test, not by inspection
- [ ] loss check run; identifier churn itemised
- [ ] no partial state: the change lands whole or not at all
- [ ] S5 inventory committed, same shape as S2's and S4's

## 5. Estimated blast radius

~78 explicit anchors and ~163 bare ones across 6 documents. **No code changes.**
Reversible by `git revert` of a single commit, which is the main reason to do it
as one atomic change rather than incrementally.
