# 7.g exercise 4: the corrected definition and the new component (2026-11-15)

**Changes** (operator, 2026-11-15): the shared definition of an idea says that a regime may limit where an effect
holds but the effect inside it is graded; `VolatilityScaledReturnComponent` (a move in units of the coin's usual
move) added.

**Two runs on 002-03** (`run_1/`, `run_2/`, 0.68 USD): no calendar-only idea any more; every idea graded, most of them
on a move against the coin's own volatility.

**Through steps 3 to 6:**

| Idea | Step 3 | Step 5 | Step 6 |
|---|---|---|---|
| exercise 3 run 1 g1: in a calm coin, a day's move large against its 20-day volatility continues over the next 5 days | plan (blocked before: missing component) | main measure t 3.31 (1,793 cases), but **inconclusive**: the supporting check found 0 high-volatility cases | not profitable (Sharpe -0.66) |
| exercise 4 run 2 g1: the larger a one-day fall against the coin's 20-day volatility, the more it rises over the next 1 to 3 days | plan (exact) | inconclusive (t 0.20) | not profitable |

**Why the first is "inconclusive".** Its plan compares calm and volatile days on the component's recorded value. The
engine records a strategy's components only on the bars where their regime is active (calm bars here), so the
volatile side had no value, the check could not be computed, and the rule "a confirm needs its supporting check"
made the result inconclusive. Step 3 wrote a check the record cannot hold: it is not told what the record holds (step 5
is: `05_verification/helper/record_description.md`).

**Not validated yet**: its strongest idea is blocked by the record gap, not by the market.

## After the shared record description (2026-11-15)

`common/backtest_record.md` (what a backtest records, its limits included) is now read by steps 3, 5 and 7, in place
of step 5's and step 7's own copies. Step 3 re-planned the calm-coin idea: its comparison of calm and volatile days
now measures the day's move from the prices, which exist on every bar.

| Idea | Step 5 | Step 6 |
|---|---|---|
| in a calm coin, a day's move large against its 20-day volatility continues over the next 5 days | **confirmed** (t 3.34; 1,806 calm cases, 1,033 volatile cases) | not profitable (Sharpe -0.58): for 7.d |

**Validated**: one of its ideas, taken through steps 3 to 6, was confirmed.
