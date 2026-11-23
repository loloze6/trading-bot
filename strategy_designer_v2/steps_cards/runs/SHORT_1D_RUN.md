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

## Reading (2026-11-22, about 14:50 Paris; 35.74 USD; 11:43 to 13:44 UTC, nothing lost)
**Outcome: S3, real but not paying.**

| Ideas written | Run | Plans tested | Components built | Confirmed | Profitable enough | Unseen dates |
|---|---|---|---|---|---|---|
| 66 (5 by step 2, 61 by the step 7 lines) | 17 | 13 (3 waiting for components, 1 untestable) | 7 new classes (and settings added to the first), every check passed | 2 | 0 | not run (no paying book) |

The two real effects, both short only:
| Idea | Step 5 | Step 6 (what failed) |
|---|---|---|
| 029-05.b1 the failed breakout's depth, in usual moves | an 8-day fall beyond usual of 0.0200, t 2.94, 389 cases | Sharpe 0.39 but 0.17 below holding's; mean daily return 0.016 % (needs 0.05 %); Calmar 0.19 |
| 029-03.d1 a failed breakout after a small run-up | a 5-day fall of 0.0283, t 2.73, 50 cases | Sharpe 0.53 but 0.03 below holding's; mean 0.005 % a day; Calmar 0.22; too few trades |

**What it shows:** the brief's theory is real: after a failed breakout, the coin falls more than usual over the next days. But the
fall is too small and too rare to pay on the short side against the coins' long rise (holding them earns more, Sharpe for
Sharpe). The same as test 1's short leg: a short profit on these coins exists, unrelated to momentum, and does not pay on
its own.

**Short only, checked on the backtests' own files:** every one of the 13 books had 0 bars with a forecast above 0 and 0
long trades (89 to 1,312 short trades each). It held because every component used is 0 or more, then negated; only 2
configs add a `clip` with `max` 0. A component that can go below 0 would have let a book go long: step 3 has no rule
that enforces the brief's side.
