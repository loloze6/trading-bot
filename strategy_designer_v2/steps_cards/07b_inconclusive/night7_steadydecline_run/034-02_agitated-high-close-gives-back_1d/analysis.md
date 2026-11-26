---
line: 7.b inconclusive
backtest: 034-02_agitated-high-close-gives-back_1d
idea tested: 034-02_agitated-high-close-gives-back
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4564 USD
---
## Findings
- **F1:** The test's own measure points the way the idea predicts but stays short of the bar. On all folds the mean is +0.00048 with t 1.02 (7,670 bars, 2,212 days). On folds B and C it is +0.00087 with t 1.19 (3,668 bars, 1,051 days). It is positive on every one of the 6 coins, from +0.00019 (LTC, t 0.23) to +0.00230 (XMR, t 1.99), but no coin reaches t 2. The effect is weak but consistent, not mixed.
- **F2:** In agitated bars the close's place in the day's range does predict the next day against it. The correlation of the close location with the next day's excess return is −0.079 (t −4.84, 3,691 cases), against −0.038 (t −2.58, 4,639 cases) in calm bars. The quintile nearest the high is followed by −0.58 % (t −2.62), and closes above mid-range by −0.48 % (t −3.37, 2,010 cases). The effect is there; the book's sizing and drift removal make it hard to show.
- **F3:** The correlation is negative in every year of folds B and C, from −0.050 (2021, t −1.80) to −0.117 (2019, t −3.23). It is negative on all 6 coins, from −0.063 to −0.162 (XMR, t −3.62). The effect is not confined to one period or one coin, so more instruments should strengthen it rather than dilute it.
- **F4:** Inside the agitated profile the short side depends on the trend. In a rising market the main measure is −0.10 % (t −0.69, 748 bars) and the high-close short −0.03 % (t −0.06). In a falling market the main measure is +0.17 % (t 1.18, 730 bars) and the high-close short +1.00 % (t 1.99, 357 cases). In a choppy market the main measure is +1.26 % (t 1.60, 120 bars). The rising-agitated bars, about a third of the cases, dilute the result.
- **F5:** The effect is spent after the next day, as the brief says. The agitated correlation is −0.079 (t −4.84) at 1 day, −0.044 (t −1.91) at 2 days and −0.018 (t −0.62) at 3 days, so the plan's 1-day horizon is the right one.
- **F6:** The idea's size is 0.044 of a usual move: an unusual move of +0.20 % per case (t 1.26, 1,369 days). Its total move of +0.07 % is 0.4 times the 0.19 % cost of a trade. However real the effect is, a short-only book on this idea cannot pay at this size on these coins.

## Ideas
- `034-02.b1_agitated-high-close-all-coins` (from F1, F2, F3, F5): In an agitated market, the nearer a coin's daily close sits to the day's high within its high-low range, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
