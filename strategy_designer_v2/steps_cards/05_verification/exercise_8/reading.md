# Exercise 8: the chain after both fixes, run twice

**What ran.** The production chain after fix A (the situation check, step 5) and fix B (symmetric criteria, step 3):
- step 3 rewrote the 29 daily plans (one rerun, 002-03: see `../../03_test_plan/plans/REVIEW.md`);
- step 4 reran the 7 plans whose config changed (2 of them are now refused by the engine);
- step 5 ran twice side by side, on the 13 plans with a record: run 1 in `../verdicts/`, run 2 here.

Opus. Cost: 0.94 and 1.14 USD. No code refusal in either run.

## The results

| Plan | Run 1 | Run 2 | Situation check (1 / 2) |
|---|---|---|---|
| 001-01 RSI high, reversal | inconclusive, t -1.32 | inconclusive, t -1.32 | 1.0 / 1.0 |
| 001-02 RSI low, rebound | inconclusive, t 0.50 | inconclusive, t 0.60 | 1.0 / 1.0 |
| 001-03 RSI high, continuation | inconclusive, t -0.56 | inconclusive, t -0.56 | 1.0 / 1.0 |
| 001-04 RSI low, continuation | inconclusive, t -0.47 | inconclusive, t -0.14 | 1.0 / 1.0 |
| 002-01 up-cross drift | inconclusive, t -0.93 | inconclusive, t -0.82 | 1.0 / 1.0 |
| 002-02 down-cross drift | inconclusive, t 0.32 | inconclusive, t -0.27 | 1.0 / 1.0 |
| 002-03 price above long SMA | inconclusive, t 0.65 | inconclusive, t 0.65 | 1.0 / 1.0 |
| 002-04 price below long SMA | inconclusive, t -0.24 | inconclusive, t -0.24 | 1.0 / 1.0 |
| 002-05 up-regime drift | inconclusive, t 0.70 | inconclusive, t 0.70 | 1.0 / 1.0 |
| 002-06 down-regime drift | inconclusive, t -0.54 | inconclusive, t -0.53 | 1.0 / 1.0 |
| 003-03 heavy up move continues | inconclusive, t 0.17 | inconclusive, t 0.17 | 1.0 / 1.0 |
| 003-04 heavy down move continues | inconclusive, t -0.24 | inconclusive, t -0.24 | 1.0 / 1.0 |
| 003-05 up move retrace by volume | inconclusive, t -0.15 | inconclusive, t -0.15 | 0.98 / 1.0 |

**The same status for all 13 plans, and every situation check passes.**

- **The two faulty configs are fixed.** 002-02 now goes short when SMA50 is below SMA200 (its agreement was 0 % in exercise 7). 003-05 is now active on up bars only, split by volume (19 % before).
- **The criteria are symmetric.** The six "rejected" verdicts of exercise 6 rested on t between -0.76 and +0.24. All are inconclusive now.

## Where the two runs differ

The numbers differ in 4 plans, each from a detail the plan leaves open. None is near a threshold.
- **002-02:** the baseline of "excess" is each window's mean in run 1 and the pooled mean in run 2. The estimate is about ±0.01 either way, with |t| ≤ 0.32. This could matter near a threshold, because the sign decides the reject.
- **001-02:** the hold baseline is the window's grid mean in run 1 and the mean of all 5-bar returns in run 2.
- **001-04:** "neutral" bars are taken from the non-zero forecasts in run 1 and from all grid bars in run 2.
- **002-06:** an ordinary standard error in run 1, a sandwich one in run 2.

This is the open point already in the card: a plan should name its baseline and its test. It is not fixed here, since no status depends on it.

## The finding for the operator

**On the default data (BTC, plus ETH for the RSI ideas, daily bars, fold A), none of the 13 testable ideas shows evidence for or against: every |t| is below 1.4.** The chain now works as designed:
- the tests do what their plans say;
- a verdict says "rejected" only on evidence.

But the data cannot decide these ideas. That is the question for the next run: more bars (hourly, set in the brief), not more machinery.
