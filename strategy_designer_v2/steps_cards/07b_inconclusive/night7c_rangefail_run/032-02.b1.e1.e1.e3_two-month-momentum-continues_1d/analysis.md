---
line: 7.b inconclusive
backtest: 032-02.b1.e1.e1.e3_two-month-momentum-continues_1d
idea tested: 032-02.b1.e1.e1.e3_two-month-momentum-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3205 USD
---
## Findings
- **F1:** On folds B and C the tested slope is flat. At 20 days it is −0.000004 (t −0.00, 414 non-overlapping cases), at 5 and 10 days it is +0.00018 and +0.00035 (t 0.67 and 0.66), and at 40 days it is −0.0034 (t −1.55). The verdict's +0.0005 (t 0.61) is therefore close to zero at every horizon, not a positive effect cut short by the bar.
- **F2:** The effect is present only when the coin's last 20 days were quiet. In the within-coin lowest tercile of the absolute 20-day return, the slope is +0.0085 (t 4.09, 114 cases), against −0.0009 (t −0.36) and −0.0002 (t −0.11) in the two other terciles. Signed in the forecast's direction, the excess 20-day return is +8.7 % (t 4.17, 114 cases) when quiet and −1.0 % (t −0.58, 228 cases) otherwise.
- **F3:** The quiet condition grades the effect continuously. In a regression of the excess return on forecast, quietness (−log of the 20-day absolute return over the coin's median) and their product, the product's coefficient has t 3.00 and the forecast alone has t 2.02. A second measure of quiet agrees: in the lowest tercile of 20-day over 60-day volatility the slope is +0.013 (t 3.14, 66 cases), falling to +0.0023 (t 1.02) and −0.0011 (t −0.51) in the higher terciles.
- **F4:** Inside the quiet tercile both sides work and most coins agree. Cases after a 60-day fall go on to a −9.5 % excess (t −3.62, 57 cases) and cases after a rise to +8.0 % (t 2.43, 57 cases). The slope is positive on 5 of 6 coins (LTC t 3.11, XMR t 3.40, BTC t 1.99, ZEC t 2.00, ETH t 1.00; XRP t −0.45). On the raw 60-day return the slope is +0.27 (t 3.27, 73 cases).
- **F5:** Outside that regime the effect is mixed, which is what drowns the pooled test. Window slopes swing between +4.26 t (w8) and −4.28 t (w16), with years 2019 at +2.97 t and 2020 at −3.85 t. The largest forecasts reverse: the top quintile (mean forecast +17.9) has a −2.9 % excess at 20 days and −9.1 % at 40 days, while the fourth quintile has +5.2 %. Even inside the quiet tercile, years are not uniform (2018 t −1.88, 2019 t +2.98).

## Ideas
- `032-02.b1.e1.e1.e3.b1_momentum-after-quiet-weeks` (from F2, F3, F4, F5, F1): The higher a coin's 60-day return, the larger its rise over the next 20 days, only while the coin's own 20-day return is small against its usual 20-day moves. The quieter those last 20 days, the larger the rise that follows a 60-day gain and the larger the fall that follows a 60-day loss.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
