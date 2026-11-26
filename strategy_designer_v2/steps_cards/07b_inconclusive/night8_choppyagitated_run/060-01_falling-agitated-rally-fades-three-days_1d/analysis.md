---
line: 7.b inconclusive
backtest: 060-01_falling-agitated-rally-fades-three-days_1d
idea tested: 060-01_falling-agitated-rally-fades-three-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3741 USD
---
## Findings
- **F1:** The tested idea's giveback lives on the first day and fades by the plan's 3-day horizon: in folds B and C, the 396 cases (on 177 days) have a short-signed unusual move of +1.26 % over 1 day (day-clustered t 2.56), but only +0.53 % over 2 days (t 0.70), +0.75 % over 3 days (t 0.97) and +0.73 % over 5 days (t 0.85). This matches step 5's 3-bar result of +0.43 % with t 1.01.
- **F2:** Over 1 day, the giveback is large enough to trade even with the coin's drift left in: the total short move is +1.08 % per case (t 2.20), about 4.9 times the 0.22 % cost of a trade. Over 3 days the total move is +0.27 % (t 0.35), below that cost.
- **F3:** The one-day reversal is broad across the falling-agitated days themselves: the 590 up days are followed by a short-signed unusual move of +0.98 % the next day, and the 614 other days by −1.10 % (Welch t 6.38). It is positive for 8 of the 10 coins seen, with ZEC +1.50 % (t 2.02), BTC +1.03 % (t 2.19) and ADA +2.49 % (t 3.55), and positive in all four years of folds B and C (+0.66 % to +1.66 %).
- **F4:** The grading the idea claims is not visible here. Over 1 day, the forecast quartiles give +1.76 %, +1.36 %, +1.23 % and +0.70 %, smallest for the largest forecasts. The top scaled-rise quintile (mean 1.53 usual moves) gives only +0.28 %, against +0.82 % to +1.82 % for the others. The slope on the scaled rise is −0.0024 (t −0.60, 590 up days) over 1 day and +0.0009 (t 0.10) over 3 days. So the 1-day test may still fail the slope check.
- **F5:** Over 3 days the effect varies a lot between periods: the w16 cases give −0.79 % (87 cases, 29 days) and the 2020 cases −0.78 % (t −0.49), against +2.02 % in 2018. This later-day noise is what drowns the first day's giveback at the plan's horizon.

## Ideas
- `060-01.b1_agitated-decline-rally-fades-next-day` (from F1, F2, F3, F4, F5): In a falling, agitated market, a coin's one-day rise that is larger against the standard deviation of its daily returns over the past 30 days is followed by a larger fall over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
