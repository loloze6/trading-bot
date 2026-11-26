---
line: 7.b inconclusive
backtest: 061-02_calm-big-down-day-continues_1d
idea tested: 061-02_calm-big-down-day-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3463 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but short of the bar. The main measure was +0.0080 with a day-clustered t of 1.59 over 930 cases on 340 distinct days. Its size was an unusual move of +0.33 % per case (t 0.90), which is 0.035 of a usual 5-day move of 10.60 %. That is the right sign and too small for six coins to show clearly.
- **F2:** The effect is not graded, which is why the supporting check failed (Welch t -0.25). On calm down days at 5 days, the mean short-direction excess return is not ordered by the fall's size in swing units:
- **F3:** The effect is mixed across periods and drowned by the market's own moves. The calm down-day 5-day short excess return is:
- **F4:** The idea's side does carry something once each window's drift is removed. Against their own coin-window's mean 5-day return, calm down days were followed by a further fall of +1.28 % in the short direction (t 3.04, 408 cases). The calm up and flat days of the same trends were not: choppy -1.0 % (t -1.4), falling -0.5 % (t -0.5), rising -4.3 % (t -3.1).
- **F5:** The continuation is broad across coins but weak in each one, so more coins add evidence. All six coins are positive at 5 days in calm down cases, from +0.7 % (ETH, t 0.57) to +2.6 % (XMR, t 2.54). It is strongest in a falling trend (+3.0 %, t 3.1, n 116) and absent in a rising one (+0.2 %, t 0.25, n 85).

## Ideas
- `061-02.b1_calm-big-fall-more-coins` (from F1, F4, F5): In a calm market, the larger a coin's one-day fall against the standard deviation of its daily returns over the past 30 days, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
