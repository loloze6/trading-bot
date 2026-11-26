---
line: 7.g patterns
backtest: 036-02_agitated-scaled-fall-delayed-rebound_1d
idea tested: 036-02_agitated-scaled-fall-delayed-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4139 USD
---
## Findings
- **F1:** In agitated markets the rebound after a one-day fall comes on the next day, which the tested idea left out. Next-day excess return rises with the fall measured in 30-day daily swings: slope +1.285 % per swing, t 4.62, 1439 cases. The fall-weighted mean excess is +1.40 %, t 2.19 with the cases of one day taken together (537 days). In calm markets the same slope is only +0.354 % (t 2.45, 1978 cases).
- **F2:** The next-day rebound is graded. In agitated markets, next-day excess returns are +6.12 % (t 3.34, 28 cases) after falls beyond 2.5 swings, +3.22 % (t 3.18, 25) after 2 to 2.5 swings, +1.20 % (t 1.94, 85) after 1.5 to 2, and +0.94 % (t 1.81, 207) after 1 to 1.5. The fall-weighted mean of +1.40 % is about 7 times the 0.19 % cost of a trade.
- **F3:** The agitated next-day rebound lives where the coin's 60-day trend is falling or choppy, not rising. The slope is +2.618 % per swing (t 6.82, 377 cases) in falling trends and +3.68 % (t 2.55, 61 cases) in choppy ones, but +0.016 % (t 0.02, 358 cases) in rising ones. It is positive on all 6 coins (slopes +0.91 to +1.85 %, t 1.25 to 2.42) and in all 4 years (slopes +0.49 to +1.79 %).
- **F4:** The delayed rise the brief claimed is not there. In agitated markets the slope of excess return on the day's scaled move is −0.591 % (t −2.46, 1463 cases) over 2 days and −0.747 % (t −2.02, 963) over 3 days, both carried by day 1. Over 5 days it is +0.022 % (t 0.03, 591), so the rebound ends on day 1. The tested days 2–3 slope had t 1.21, and its unusual move per case was +0.04 % (t 0.18), 0.2 times the cost.
- **F5:** In calm markets a coin's 5-day return, scaled by its 30-day daily swing times √5, predicts the same-signed excess return over the next 5 days. The slope is +1.991 % per unit (t 5.60, 773 non-overlapping cases), and the sign-aligned mean is +1.17 % (t 2.35 with the cases of one day together, 196 days).
- **F6:** This calm 5-day momentum holds on both sides and is graded. The slope is +2.11 % (t 3.04) after rises and +2.97 % (t 3.69) after falls. Excess returns go from −4.84 % (t −2.89, 40 cases) below −1.5 units to +3.53 % (t 2.09, 66) above +1.5 units. It is positive on all 6 coins (t 1.16 to 3.84) and in 3 of 4 years (2019: −0.28 %, t −0.41). The sign-aligned mean of 1.17 % is about 6 times the 0.19 % cost.
- **F7:** The book of the tested idea earned little: Sharpe 0.34 against holding's 0.57 (difference −0.23), Calmar 0.12, and +4.8 % a year. Its mean daily return by window stayed between −0.11 % and +0.29 %, while the coins' mean daily return ranged from −0.44 % to +1.26 %.

## Ideas
- `036-02.g1_agitated-fall-next-day-rebound` (from F1, F2, F3, F4): In a falling, agitated market, the larger a coin's one-day fall against its 30-day daily swing, the larger its rise over the next day.
- `036-02.g2_agitated-scaled-fall-bounce` (from F1, F2, F4): In an agitated market, the larger a coin's one-day fall against its 30-day daily swing, the larger its rise over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `036-02.g3_calm-five-day-momentum` (from F5, F6): In a calm market, the larger a coin's 5-day return against its 30-day daily swing, the further the coin moves in the same direction over the next 5 days, up after rises and down after falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
