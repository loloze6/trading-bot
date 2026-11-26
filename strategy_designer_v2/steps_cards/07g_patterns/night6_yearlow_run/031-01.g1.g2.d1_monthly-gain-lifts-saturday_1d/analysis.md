---
line: 7.g patterns
backtest: 031-01.g1.g2.d1_monthly-gain-lifts-saturday_1d
idea tested: 031-01.g1.g2.d1_monthly-gain-lifts-saturday
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4224 USD
---
## Findings
- **F1:** Across all coins, the 20-day gain at Thursday's close (UTC) predicts Friday's return as strongly as the tested idea's Friday close predicts Saturday's. Among 1011 Thursday closes after a 20-day gain, the slope of Friday's excess return on the 20-day gain has t 4.89 (raw). It keeps t 2.88 (day-clustered, 276 days) when the gain is scaled by 20-day volatility and returns are winsorised, with Spearman 0.116. On Saturday the same robust measure falls to t 1.05, Spearman 0.006.
- **F2:** The Thursday-close effect runs through to Saturday. Over the two days from Thursday's close, the volatility-scaled 20-day return has a positive slope on the excess return: t 3.14, 2052 cases, 342 days, Spearman 0.079. The book does not capture it: it earns −0.024 % a day on Fridays and +0.199 % on Saturdays.
- **F3:** The Thursday-close grading holds broadly. It is positive in 5 of 6 coins (ZEC t 3.12, XRP t 2.27, LTC 1.81, ETH 1.65, BTC 1.48; XMR −0.38). It is positive in 7 of 8 years (Spearman 0.04 to 0.25; 2018 flat at −0.0003).
- **F4:** The tested Saturday grading rests on extreme cases. With Friday closes after a 20-day gain, the raw slope has t 5.87 but the robust slope has t 1.05. Saturday's level does hold: the overall Saturday excess is +0.30 % (t 2.09, 414 days), and it is +0.89 % (t 2.19) in the top 20-day-gain quintile.
- **F5:** The book's weak years match the weak Saturday years. Saturday excess after a 20-day gain was −0.73 % in 2018 and −0.26 % (t −1.79) in 2023. The book's mean daily return was −0.002 % and −0.006 % in those two years and positive in all other years.
- **F6:** A one-day reversal after down days exists but is too weak to count after this many angles. Over 14500 cases, the slope of the next day on the previous day's volatility-scaled return has t −2.36 (2418 days). The bottom quintile of the previous day's return is followed by +0.46 % (t 2.49). On down days alone the slope has t −1.53.
- **F7:** Distance from the 60-day low gives no clear grading over the next 5 days: quintile means go from −0.32 % to +0.91 %, with no t above 2.1 in magnitude. The 20-day-fall side on Saturday is not robust either: robust slope t 1.37, with signs changing across years.

## Ideas
- `031-01.g1.g2.d1.g1_thursday-momentum-into-weekend` (from F1, F2, F3, F4): The larger a coin's 20-day gain at Thursday's close (UTC), relative to its usual 20-day move, the more it rises over the next two days, Friday and Saturday.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
