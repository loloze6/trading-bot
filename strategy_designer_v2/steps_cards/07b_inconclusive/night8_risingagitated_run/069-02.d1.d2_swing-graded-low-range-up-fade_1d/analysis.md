---
line: 7.b inconclusive
backtest: 069-02.d1.d2_swing-graded-low-range-up-fade_1d
idea tested: 069-02.d1.d2_swing-graded-low-range-up-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4197 USD
---
## Findings
- **F1:** The agitation grading the idea names is not in the cases: step 5's slope on the forecast's size is -0.00032 with t -0.61 over 378 cases. In folds B and C the slope is t -0.91 over 230 cases. The forecast terciles do not rise in order, with low +0.80 %, mid +1.46 % and high +0.02 % next-day excess in the short direction. The raw 30/365 volatility ratio has slope t -1.52, which points the wrong way.
- **F2:** The plain fade is on the side the idea predicts but small. Over all cases the next-day excess in the short direction is +0.76 % (t 1.93, 230 cases, folds B and C). Step 5's unusual move is +0.99 % (t 2.08, 198 days), 0.206 of a usual move and 5.1 times the 0.19 % cost of a trade.
- **F3:** The fade is graded by the coin's fall over the past few days, not by its agitation. Across the cases, the slope of the next-day short excess on the 5-day return is -0.248 (t -5.06, 205 cases, Spearman -0.31). Winsorising the returns at 2 % leaves it at t -5.14. The 3-day return gives t -4.27. The grading fades at longer lookbacks: the 10-day return gives t -0.67 and the 20-day t +0.75.
- **F4:** The gain sits in the deepest 5-day falls. Among falling-market up days low in the range, the quartile with the largest 5-day fall gives back +5.40 % the next day (t 5.77, 37 cases). The other three quartiles give -0.60 %, -0.27 % and -1.14 %, all with t near or under 1.
- **F5:** The 5-day grading points the same way on every coin. All six slopes are negative: BTC t -2.09, ETH -1.37, LTC -2.99, XMR -2.01, XRP -1.01 and ZEC -3.19.
- **F6:** The 5-day grading lives in the falling profile. Inside it, the slope over all up days low in the range is t -4.78 (147 cases). Outside it, the slope is +0.098 with t +0.89 (75 cases).
- **F7:** The 5-day grading is uneven over time, which is the main risk on the held-out folds. In 2018 it is t -4.96 (107 cases), while 2019 shows t +0.39 (69 cases). By window, w14 gives t -4.23, while w15 gives t +1.59 and w8 gives t +0.35.
- **F8:** How low the close sits in its 20-day range does not grade the fade inside the lower fifth (slope t -0.18, 205 cases). A smaller 1-day rise fades more: the lowest tercile of the day's rise gives +1.64 % with t 2.75, against +0.08 % and +0.62 % for the other two.

## Ideas
- `069-02.d1.d2.b1_five-day-fall-graded-up-day-fade` (from F1, F3, F4, F5, F6, F7): In a falling market, when a coin closes up on the day well below its 20-day high, the more it has fallen over its past 5 days, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
