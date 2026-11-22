---
line: 7.g patterns
backtest: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall_1d
idea tested: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4258 USD
---
## Findings
- **F1:** In coins whose 30-day return is positive, a one-day rise of more than 2 usual daily moves is followed by a 2-day move of +1.77 % beyond the coin's drift (t 3.16, 173 non-overlapping cases) and a 5-day move of +4.74 % (t 2.37, 62 cases). This is about 9 times the 0.19 % cost of a trade. It is positive in all six coins (ETH +2.50 % t 2.84, LTC +2.51 % t 2.04, XRP +2.63 %, BTC +1.03 %, ZEC +0.99 %, XMR +0.60 %) and in both halves of the windows (w1–w12 +0.88 % t 1.53, w13–w24 +2.65 % t 2.78).
- **F2:** The continuation in F1 grows only weakly with the size of the rise. Over all rises above 0.3 usual moves in rising months, the Spearman correlation between the rise and the 2-day unusual move is 0.063 over 1344 cases (t about 2.3). The buckets are not monotone: 0.3–1 moves give −0.17 %, 1–1.5 give +0.50 %, 1.5–2 give −0.30 %, 2–3 give +1.92 % (t 2.87) and above 3 give +1.26 %.
- **F3:** In coins whose 30-day return is negative, the bounces the tested forecast ignored are the ones that fade. A small one-day rise of 0.3 to 1 usual moves is followed by a 2-day unusual move of −0.80 % (t −3.37, 705 cases). It is negative in all six coins (XMR −1.47 % t −2.93, LTC −1.21 % t −2.51, ETH −0.68 %, XRP −0.87 %, BTC −0.23 %, ZEC −0.22 %) and in both halves (w1–w12 −0.36 % t −1.31, w13–w24 −1.18 % t −3.16).
- **F4:** In falling months the fade is not graded by the size of the rise, which is why the steep forecast found nothing:
- **F5:** Sharp rises are followed by opposite moves depending on the 30-day sign. Above 2 usual moves, the 2-day unusual move is −1.83 % (t −2.81, 78 cases) when the 30-day return is negative and +1.77 % (t 3.16, 173 cases) when it is positive. In the 5-day grid, rises of 1–2 moves give +0.89 % in falling months against +2.07 % (t 2.30) in rising months.
- **F6:** The book lost 0.0077 % a day (standard deviation 0.47 %, 2898 days). Its daily returns correlate −0.33 with the coins' returns, so its loss is mostly the short exposure paying the coins' rises. The largest 5 % of days by size sum to −6.9 % of a −22.2 % total.
- **F7:** The day of the week shows a pattern, but it is a condition, not a graded situation, so no idea is drawn from it. Thursday and Friday bars have unusual 1-day returns of +0.25 % (t 2.63) and +0.30 % (t 3.76); Monday has −0.24 % (t −2.53) and Wednesday −0.30 % (t −2.70). Thursday and Friday beat the other days in all six coins (LTC +0.54 % against −0.22 %).

## Ideas
- `025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall.g1_sharp-rises-continue-uptrends` (from F1, F2, F5): In a coin whose 30-day return is positive, a one-day rise of several usual daily moves is followed by a further rise over the next 2 days, and the larger the one-day rise in usual daily moves, the larger the rise that follows.
- `025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall.g2_small-bounces-fade-downtrends` (from F3, F4, F5): In a coin whose 30-day return is negative, a modest one-day rise is followed by a fall over the next 2 days, and the more negative the 30-day return, the larger that fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
