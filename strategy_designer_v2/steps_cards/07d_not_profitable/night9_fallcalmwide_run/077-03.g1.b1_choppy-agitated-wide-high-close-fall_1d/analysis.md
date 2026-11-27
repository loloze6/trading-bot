---
line: 7.d confirmed, not profitable
backtest: 077-03.g1.b1_choppy-agitated-wide-high-close-fall_1d
idea tested: 077-03.g1.b1_choppy-agitated-wide-high-close-fall
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6399 USD
---
## Findings
- **F1:** The book fails because it barely holds anything, not because the effect is too small for its costs. It holds a position on 3 % of the coins' days, at a mean allocation of −0.30 (median −0.25). Its daily standard deviation is 0.126 % and its yearly return +1.3 %. The total move per case (+0.65 %) is 2.9 times the 0.22 % trade cost. Simulated at unit size with that cost, the same high-close short still fails both measures: Sharpe 0.73 against holding's 0.63, Calmar 0.53 (deepest fall −8.5 %).
- **F2:** The low-close side of the same situation carries the larger effect, and the tested idea leaves it out. In profile, days closing in the bottom quarter of their range rise over the next day by +1.82 % unusual move (82 cases, day-clustered t 2.68, 65 % hit), against +1.31 % for high-close shorts (126 cases, t 1.75). Long on low closes alone, graded by width, simulates to Sharpe 1.05 and Calmar 2.41 (fall −3.0 %). Trading both sides simulates to Sharpe 1.27 and Calmar 1.27, so both failing measures pass.
- **F3:** The profile belongs to the idea and is not an effect of its own. All in-profile bars show a next-day unusual move of −0.06 % (449 bars, t −0.11). In-profile days closing mid-range give +0.05 % in the short direction (241, t 0.07). Outside the profile the same closes are weak or wrong: choppy calm high-close short −0.07 % (181), choppy calm low-close long −0.28 % (118). This matches the brief's view that forced flow overshoots only when a trendless market is agitated.
- **F4:** The gain sits in days wider than the coin's own recent days, as the theory's grading says.
- **F5:** The tested short is not graded by how close the close sits to the high. High closes at 0.74–0.85 of the range give +1.82 % (60, t 2.37); those at 0.95–1.0 give −0.28 % (15). High closes after the smallest day returns (mean +1.1 %) give +2.69 % (42, t 2.26), against +0.71 % after the largest (mean +10.8 %). Losses gather in w11, w12 and w14 (summed P&L −0.020, −0.076 and −0.011), where narrow days dominate.

## Ideas
- `077-03.g1.b1.d1_choppy-agitated-two-sided-close-fade` (from F1, F2, F3): In a choppy, agitated market, a day closing near an end of its range moves back toward the other end over the next day: a day closing near its high falls and a day closing near its low rises, and the move is larger the wider the day's range against the coin's 30-day swing of daily returns.
- `077-03.g1.b1.d2_choppy-agitated-low-close-rebound` (from F2, F3, F4): In a choppy, agitated market, a day closing near its low rises over the next day, and the rise is larger the wider the day's range against the coin's 30-day swing of daily returns.
- `077-03.g1.b1.d3_widening-day-close-fade` (from F1, F3, F4): In a choppy, agitated market, a day closing near an end of its range moves back toward the other end over the next day, and the move is larger the more the day's range against the coin's 30-day swing exceeds that of the coin's past 60 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
