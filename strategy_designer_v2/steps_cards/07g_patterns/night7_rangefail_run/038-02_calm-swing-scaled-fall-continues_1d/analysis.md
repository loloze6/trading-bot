---
line: 7.g patterns
backtest: 038-02_calm-swing-scaled-fall-continues_1d
idea tested: 038-02_calm-swing-scaled-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3919 USD
---
## Findings
- **F1:** Over all signed 5-day moves, not falls alone, a coin's 5-day excess return in a calm market rises with its 5-day return scaled by its 20-day daily swings: slope +1.89 % per swing unit, t 2.80 with same-day cases summed, 904 grid cases on 200 days. In an agitated market the same slope is -0.22 % (t -0.19, 718 cases on 186 days). So the effect lives in the calm profile, and the brief's two-sided claim holds where the tested fall-only short did not reach significance (t 1.48).
- **F2:** The calm two-sided slope is consistent. It is positive in all 10 coins (BTC +1.10 %, t 1.63; ETH +1.64 %, t 2.13; XMR +2.05 %, t 2.48; ZEC +1.99 %, t 2.05; ADA +2.58 %, t 1.95; XRP +3.88 %, t 1.73), in all four years (2018 +1.53 %, 2019 +0.14 %, 2020 +2.05 %, 2021 +1.68 %) and in 8 of 12 windows.
- **F3:** The calm slope keeps its sign across ways of measuring and horizons. At 3 days it is +0.85 % (t 2.10, 1519 cases). At 5 days the 10-day scaled move gives +1.73 % (t 2.88), and the 60-day standardised score gives +1.72 % (t 2.66). At 10 days the 10-day scaled move gives +2.91 % (t 2.44, 442 cases on 98 days). The agitated slopes stay between -0.24 % and +1.41 % with every |t| below 0.7.
- **F4:** The rise side carries much of the calm effect.
- **F5:** After 5-day falls the result is mixed. Calm falls of 0.5 to 2 swing units are followed by excess returns of -2.86 % (t -2.19, 111 cases) and -3.85 % (t -2.01, 82 cases). The deepest calm falls, below -2 units, are followed by +1.12 % (t 0.45, 19 cases). The fall side alone is not graded clearly enough to stand by itself.
- **F6:** Weekday returns, the coin's volatility level and its day-range ratio show nothing beyond chance across this many angles. The day-averaged Saturday return is +0.63 % with t 2.43 and Friday's is +0.56 % with t 1.81, but no volatility quintile or range quintile reaches |t| 1.5.

## Ideas
- `038-02.g1_calm-swing-scaled-move-continues` (from F1, F2, F3): In a calm market, the more of its 20-day daily swings a coin's 5-day move spans, the further the coin keeps moving the same way over the next 5 days, upward after rises and downward after falls.
- `038-02.g2_calm-swing-scaled-rise-continues` (from F4, F3): In a calm market, the more of its 20-day daily swings a coin's 5-day rise spans, the more the coin rises over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
