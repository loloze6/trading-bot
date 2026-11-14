---
line: 7.g patterns
backtest: N2-02_capitulation-rebound_1d
idea tested: N2-02_capitulation-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3165 USD
---
## Findings
- **F1:** After a daily close that fell between 1 and 2 of its own 20-day volatilities, the next day returned +0.69% on average (t 4.9, n=1386); after a fall of more than 2 volatilities it returned +0.67% (t 2.2, n=403). Over all bars the next day returned +0.13% (t 3.5, n=17022), and after rises of the same size it returned only +0.11% to +0.13% (t 0.9 and 0.5).
- **F2:** The next-day rebound after a fall of 1 volatility or more is concentrated in two places. Below the 200-day SMA it is +0.75% (t 5.5, n=1608), against +0.16% above it (t 0.4, n=181). In the high-volatility regime it is +1.20% (t 4.9, n=722), against +0.34% outside it (t 2.5, n=1067).
- **F3:** The rebound is positive in every coin: from +0.34% for BTC (t 1.4, n=292) to +1.09% for XMR (t 4.0, n=299). It is positive in 7 of 8 years, with 2024 the exception at -0.01%.
- **F4:** Over 3 days the rebound persists. After down days of 1 volatility or more, counted at least 3 bars apart, the mean 3-day return is +0.84% (t 3.7, n=1387), against a 3-day base of +0.39%.
- **F5:** The return over the bar after a Thursday or a Friday bar is higher than after other days. After Thursday it is +0.34% (t 3.7, n=2431) and after Friday +0.43% (t 5.3, n=2430). After Wednesday it is -0.18% (t -1.6, n=2437). The return after Thursday or Friday is positive for all 6 coins, and it beats the other weekdays in 6 of 8 years.
- **F6:** The idea's own signal does not sort outcomes. The 10-bar excess return is flat across the five quintiles of distance from the 200-day SMA (all |t| < 0.7, about 160 cases each). In-regime bars with a forecast of 0 to 5 are negative: -1.6% (t -2.1, n=233).
- **F7:** Trades held longer than 30 days lose: mean -0.6%, median -6.0%, n=60. Trades held 30 days or less gain +4.4% to +5.1% on average (n=528). The long holds lost most in 2018 (-26%, n=13) and 2022 (-14%, n=25).

## Ideas
- `N2-02_capitulation-rebound.g1_sharp-down-day-short-rebound` (from F1, F2, F3, F4, F6): When a coin's daily close falls by at least one of its own recent daily volatilities while it trades below its 200-day average, its next one to three days rise more than its usual drift. The rise is larger when recent volatility is above its usual level.
- `N2-02_capitulation-rebound.g2_late-week-daily-return-premium` (from F5): A coin's return over the daily bar that follows a Thursday or a Friday close is higher than its return over the bars that follow other weekdays.
- `N2-02_capitulation-rebound.g3_unrecovered-dip-keeps-falling` (from F7): When a dip-buying long position still has not closed after a month while the coin stays below its 200-day average, the coin keeps falling over the following weeks.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
