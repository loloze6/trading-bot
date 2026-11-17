---
line: 7.e profitable but not proven
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3695 USD
---
## Findings
- **F1:** The book earns a mean daily return of 0.000635. Of that, 0.000287 comes from the market's own rise and 0.000348 from timing, while holding the coins earned 0.001230 a day. The book therefore keeps only about half its gain from timing and trails holding in raw return.
- **F2:** The gain sits in a few days and periods. The 30 best of 2898 book days give 93% of the summed daily return (the 10 best give 42%), and four windows (w17, w21, w10, w11) hold 22 of those 30 days. By year the book made 0.002386 a day in 2020, 0.001077 in 2021 and 0.001137 in 2024, and lost in 2018 (-0.000270) and 2022 (-0.000236).
- **F3:** Timing comes from BTC (0.000651), ETH (0.000646), XRP (0.000617) and ZEC (0.000423); it is negative in LTC (-0.000061) and XMR (-0.000136). XMR's 7-day excess return while long is -0.00095 over 213 cases.
- **F4:** The edge is strongest at a shorter horizon than the plan's 7 bars. The Welch t of active bars minus flat bars is 2.91 at 3 bars (2798 active cases, active mean excess 0.00318, t 1.92), 2.58 at 7 bars and 1.83 at 1 bar. It fades to 0.98 at 14 bars and 0.70 at 30 bars.
- **F5:** Inside the rising-month regime, the 7-day excess return is carried by the top quarter of range position: 0.0254, t 2.62, n 300. The other three quarters give -0.0023, 0.0057 and -0.0013, so the gain sits nearest the 52-week high rather than growing smoothly along the range.
- **F6:** The 30-day return part is not graded upward. Its quarters give 7-day excess returns of 0.0007, -0.0014, 0.0239 (t 2.98) and 0.0044 for the strongest quarter.
- **F7:** Inside the rising-month regime, the gain follows heavy volume. On bars whose volume is in the top third relative to its 20-bar mean, the 3-bar excess return is 0.01265 (t 3.72, n 876) and the 7-bar is 0.0190 (t 2.17, n 362). The lowest third gives 0.0014 at 3 bars and -0.0043 at 7 bars.
- **F8:** Part of the book's edge is standing aside from falling coins. Bars with a 30-day return at or below 0 have a 3-bar excess return of -0.00322 (t -2.23, n 2768) and a 7-bar one of -0.00702 (t -1.96, n 1179).

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through` (from F7, F4, F1): While a coin's 30-day return is positive, the higher its daily volume relative to its own 20-day average volume, the higher its return over the next 3 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high` (from F5, F2): The nearer a coin's daily close sits to its highest close of the past 52 weeks, the higher its return over the next 7 days, with the effect concentrated in the closes closest to that high.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling` (from F8, F4): The more negative a coin's 30-day return, the lower its return over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
