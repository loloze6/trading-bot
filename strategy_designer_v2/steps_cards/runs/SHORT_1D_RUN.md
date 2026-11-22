# Short side, daily bars (2026-11-22, written before the run)

**The operator's request (2026-11-22, about 12:30 Paris):** "launch a research flow around 1d for finding a strategy that
would exploit short position". **Why:** every paying book so far is momentum, held long (the similarity register); the
only short leg measured (025-03.d2's, `runs/NIGHT4_RUN.md` test 1) is unrelated to momentum but small (t 1.25), and
combining pays only with books near zero correlation (test 2, topic 44).

**The brief:** `01_brief/briefs/029_failed-breakout-traps-late-buyers.md` (bar 1d, side short only), written by step 1
from the operator's theme ("on daily bars, a strategy whose profit comes from short positions"). Theory: a daily close back
inside the old range a few days after a break above the recent high is followed by days of decline (trapped breakout
buyers sell). Step 1's list of sides gained "short only" (the mirror of "long only"; step 3 builds it with a `clip`,
`max` 0, as it builds long only with `min` 0).

**Run:** `short_1d_run`, `run_brief` with the brief, budget 35 USD (model calls), one session on branch `short-1d`, the
night 4 rules (restart a loop the 2-hour limit cuts, resume after a usage-limit stop, commit along the way, no new idea
after 6 hours, the similarity register left to the designer).

**Measures:** ideas, plans, components built, confirmed, profitable enough, holding on the unseen dates; for each paying
book, its short side (every plan must be short only: checked on the plans), its nearest relative in the similarity
register and its correlation with momentum.

| Outcome | What the counts would show | Meaning |
|---|---|---|
| S1. A short book of its own | a paying book, short only, holding on the unseen dates, its nearest relative explaining under 0.1 of it | the second book topic 44 waits for: test it combined with momentum (method A) |
| S2. Momentum turned round | a paying book whose nearest relative is a momentum book with a large share explained, direction − | the short side of momentum, not a new profit |
| S3. Real but not paying | confirmed ideas, no profitable book | falls exist but do not pay after costs against the coins' long rise |
| S4. Not real, or blocked | few confirmed, or ideas waiting for components that cannot be built | recorded |

**Risk:** the account's 7-day usage limit is at its warning level; the run may stop early.
