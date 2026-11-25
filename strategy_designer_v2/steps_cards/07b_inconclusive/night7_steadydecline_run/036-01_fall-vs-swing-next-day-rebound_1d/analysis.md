---
line: 7.b inconclusive
backtest: 036-01_fall-vs-swing-next-day-rebound_1d
idea tested: 036-01_fall-vs-swing-next-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3461 USD
---
## Findings
- **F1:** The supporting check failed because the forecast barely grades the fall. The forecast is the fall re-standardised over 60 days and capped at 20, so it saturates: 487 of the 1,024 cases in folds B and C sit at exactly 20, falls of 2 usual moves or more all have a forecast of 20.0, and falls of 1.5 to 2 usual moves average 19.8. Its rank correlation with the next-day excess return is 0.003, and its top third beats its bottom third by only +0.12 % (Welch t 0.23).
- **F2:** Graded by the idea's own measure (the day's return over its 30-day swing), the effect does grow with the fall, in the predicted direction. The deepest third of falls is followed by +1.52 % excess next day against +0.83 % for the shallowest third (difference +0.69 %, Welch t 1.41, 290 cases each). The deepest quarter gives +1.62 %, against +0.41 % to +1.00 % for the other three. Falls beyond 3 usual moves give +3.55 % (34 cases), falls of 2.5 to 3 give +1.80 % (t 2.09), and falls of 1.2 to 2 give +0.5 % to +1.0 %.
- **F3:** The grading holds across periods but is too weak for this data to show clearly. The rank correlation between fall size and next-day excess return points the predicted way (deeper fall, larger rise) in 10 of 12 windows (83 %), but overall it is only -0.048 for the raw fall and -0.107 for the linear correlation.
- **F4:** The main effect is on the predicted side and does not rest on outliers. Cases are followed by a mean next-day excess return of +0.93 % (t 2.46, cases of one day together, 1,024 cases). The median is +1.03 %, 61 % of cases are positive, and with the top and bottom 1 % trimmed the mean is +0.88 % (t 2.93).
- **F5:** The move lives at the plan's 1-day horizon and fades after it. The mean excess return is +0.93 % at 1 day (t 2.46), +0.43 % at 2 days (t 0.97), +0.68 % at 3 days (t 1.25) and +0.17 % at 5 days (t 0.24).
- **F6:** The effect is spread across coins and profiles, not confined to one part of the data. All six coins are positive, from BTC at +0.28 % (t 0.79) to XMR at +1.58 % (t 3.51) and ZEC at +1.52 % (t 3.07). Agitated markets give +1.67 % (t 2.22) and calm markets +0.70 % (t 1.69). It shows in both falling agitated (+2.18 %, t 1.83) and rising calm (+1.49 %, t 2.44), so no single profile carries it.
- **F7:** The book can pay on this move, so the problem is the clarity of the test, not the cost. The total move per case is +0.60 %, 3.1 times the 0.19 % cost of a trade, and the unusual move of +0.49 % is 2.5 times that cost. The book's Sharpe is 0.69, beating holding by 0.14, but it failed on Calmar at 0.56.

## Ideas
- `036-01.b1_outsized-fall-rebound-all-coins` (from F2, F3, F4, F5, F6): The further a coin's one-day close-to-close fall exceeds the standard deviation of its daily returns over the past 30 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
