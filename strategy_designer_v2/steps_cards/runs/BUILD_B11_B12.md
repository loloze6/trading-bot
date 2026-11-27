# Build B11 and B12 (2026-11-27, branch `build-b11-b12`)

The operator's go: next steps B11 and B12 (`topics/NEXT_STEPS.md`), evidence `topics/47_review/night9_review.py`, `.txt`.

## Purpose
- **B11.** Money goes to ideas that may still prove real, not to effects the data shows absent: step 5 gets a third
  answer, **no effect** (enough cases, the effect near zero or pointing the other way), which goes to line 7.c;
  "rejected" joins it; "inconclusive" (unclear) keeps its meaning and goes to 7.b.
- **B12.** A repair is tried where it can reach the bar: line 7.d runs only on a confirmed, unprofitable strategy that
  fails at most 2 of step 6's 6 measures.

## Expected outcomes (written before the build)
- B11, step 5 rerun with each plan's stored `measure.py` on night 9's tested ideas (no model call): only the unclear
  answers with t below 1, and the rejected one, become "no effect"; nothing else changes. Night 9's count is checked
  against `night9_review.txt` part 3 (that part counts nights 7 to 9 together).
- B12, on night 9's tables: the 7.d calls the new entry condition would have skipped led to 0 profitable strategies.
- Both: `run_idea` on one seeded idea whose answers do not change gives the same files with the new code as without.
- The cards' tests and the bot's tests pass.
