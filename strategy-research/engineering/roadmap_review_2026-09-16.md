# Engineering Roadmap — Coherence Review (2026-09-16)

Reviewed `engineering_roadmap.html` against the same lens applied to the protocol/variant
discussion earlier this session: for every step and every epic, does the separation of
concern actually hold, is any axis conflated with another, and does the step-by-step
walkthrough forget anything the ordered plan already knows about?

Six findings, all resolved and applied directly to the board (now at v24). This file is
the record of what was found and how it was closed — the roadmap itself is the current
source of truth, not this document.

---

## 1. Step 2 and Step 4 both claimed to "fix the repeat-idea checker" (E-036), unreconciled

Step 2's own change-list and Step 4's entire purpose both described fixing the same
checker, with no indication of whose repeat-check each was.

**Resolution:** one check, one owner. Step 2 only *generates* versions now — the
repeat-check line was removed from its change-list. Step 4 is the one place the check
runs, explicitly once per version (matching Step 3's own per-variant framing), with a
sentence stating plainly that Step 2 doesn't check anything, it only generates.

## 2. Protocol's own robustness axes were invisible in the 12-step walkthrough

Time-windows, cost-stress, and era-stability — the "protocol" axes established as
siblings to design-variants in the gaps-list insight — were never named in any step's
text, even though Step 5/6 are where they actually apply.

**Resolution:** Step 5's Objective now states explicitly that a "run" is a walk-forward
across several time periods plus cost-stress/era-stability checks, not one flat backtest,
and names this as the sibling axis to Step 2's variants. Step 6's Objective/After now says
it grades one variant across whatever windows the protocol required, and forwards
explicitly to Step 7 for the family-level view.

## 3 & 4. CUL-298 (variant agreement) had no walkthrough step, and its relationship to E-046b was unstated

CUL-298 existed only as an ordered-plan card and a gaps entry — never mentioned in any
step's Today/What-changes/After text — and nothing reconciled it against E-046b's
per-variant gate.

**Resolution:** decided the real shape — E-046b grades one variant at a time; CUL-298
runs immediately after, across the group, producing the family verdict that actually
feeds specialist reading and memory. Gave it its own walkthrough step, **new Step 7**
("Do the variants actually agree with each other?"), between per-variant grading (Step 6)
and specialist reading (now Step 8). This meant renumbering every step from the old
Step 7 onward (7→8, 8→9, 9→10, 10→11, 11→12) and every cross-reference to them
throughout the document — verified afterward by re-grepping every "Step N" mention against
the new sequence, both numerically and for semantic correctness (not just "does a Step 9
exist" but "does this sentence about Step 9 still say something true").

## 5. The ordered plan conflated "pipeline-narrative order" with "build/dependency order"

E-046a (explicitly "gated on nothing") and E-031's own core mechanism (only its
auto-trigger half depends on the not-yet-built regroup stage) sat well behind items they
don't actually depend on, with nothing saying whether the list was priority or a
dependency queue.

**Resolution:** added an explicit note under "The plan, in order" stating the sequence is
priority-of-effort (schema work leads because it's foundational), not a strict dependency
queue, and naming E-046a and E-031's core mechanism specifically as already unblocked and
runnable in parallel with earlier items.

## 6. E-033.1's "build as a protocol extension" requirement wasn't cross-linked to E-049

**Resolution:** added a pointer on E-033.1's card to read E-049's findings first, since
that's where the real state of protocol's resolution loop is already characterized.

---

## What did not turn up an issue

The three-branch structure itself (branch 1 pass/fail, branch 2 specialist patterns,
branch 3 campaign-wide bar, regrouping into memory, feeding "what's next") held up
cleanly. Every finding above was at the level of a step's wording, an epic's
cross-reference, or the ordered list's sequencing logic — not the overall design.
