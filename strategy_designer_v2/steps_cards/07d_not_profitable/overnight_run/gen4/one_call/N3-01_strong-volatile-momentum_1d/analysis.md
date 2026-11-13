---
line: 7.d not profitable
backtest: N3-01_strong-volatile-momentum_1d
idea tested: N3-01_strong-volatile-momentum
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3813 USD
---
## Findings
- **F1:** Fees do not explain the failure: the 1118 trades, all long, earn 5.64% each on average before fees and pay 0.10% in fees (t of gross = 3.43). The Calmar failure comes from drawdowns: the deepest book drawdown is -86% on ZECUSD, -71% on both LTCUSD and XRPUSD, and -86% in 2021.
- **F2:** The gain rests on a few long winners. The 10 best trades make up 74% of the summed gross gain, the median trade loses 1.32%, and only 43.8% of trades win.
- **F3:** Short holds lose and long holds pay. Gross mean per trade is -3.36% for holds of 2 days or less (n=332), -2.95% for 2–5 days (n=223), -1.08% for 5–10 days (n=191), +4.30% for 10–20 days (n=195) and +43.0% beyond 20 days (n=173).
- **F4:** Trades give back much of their best excursion. Even trades held over 20 days give back 38 points from a mean peak gain of 81%. Trades exited while the forecast was still 15 or more lost 6.46% gross (n=131).
- **F5:** A larger forecast does not earn more. Mean excess 5-bar return (non-overlapping) is -3.4% in the 5–10 bucket (t=-1.53, n=35) and +0.97% at 10 or more (t=1.38, n=369). Trades entered at forecast 10–15 lose 0.18% gross (n=99).
- **F6:** Among forecast ≥10 cases, the largest run-ups do not continue. In the top 20-day-return tercile (above +37%), the excess 5-bar return is 0.0% (t=0.00, n=108). In the lowest tercile (+4% to +22%), it is +2.1% (t=1.64, n=107).
- **F7:** Volatility shapes both gain and loss. In-position days in the high-volatility tercile hold the largest allocation (0.74) and carry 39% of all losing-day losses, with an annualised Sharpe of 0.75 against 1.11 in the mid tercile. At forecast ≥10, the excess 5-bar return is +2.0% in mid volatility (t=1.64, n=116), +0.9% in high volatility (t=0.88, n=163) and -0.5% in low volatility (n=43).
- **F8:** Gains come early in a position. The book earns 1.31% per day in the first 2 days of a position (t=2.60, n=487) and loses 0.40% per day on days 5–10 (t=-1.26, n=598).
- **F9:** Losses cluster by period. Trades in 2018 lost 14.2% each (n=38) and those in 2019 lost 0.78% (n=115), while trades in 2025 earned 27.5% each (n=159). The trades by coin range from +0.23% per trade on LTCUSD (n=196) to +15.1% on ZECUSD (n=264).

## Ideas
- `N3-01_strong-volatile-momentum.d1_moderate-run-ups-keep-going` (from F5, F6, F1): When a coin is up over both 20 and 60 days and its 20-day rise is moderate rather than extreme by its own standards, the next 5 days rise more than the coin's average.
- `N3-01_strong-volatile-momentum.d2_mid-volatility-trends-persist` (from F7, F1): When a coin's 20-day rise above a rising 60-day trend happens with mid-range rather than the highest 20-day volatility, the next 5 days rise more than the coin's average.
- `N3-01_strong-volatile-momentum.d3_slow-trend-carries-the-gain` (from F2, F3, F4, F8): Once a coin has stayed up over both 20 and 60 days for several weeks, its rise continues over the next several weeks more than the coin's average. The persistence lives in the slow part of the trend, not in the next few days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
