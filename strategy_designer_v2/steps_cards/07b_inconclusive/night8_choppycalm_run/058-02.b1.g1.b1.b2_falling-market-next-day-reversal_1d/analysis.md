---
line: 7.b inconclusive
backtest: 058-02.b1.g1.b1.b2_falling-market-next-day-reversal_1d
idea tested: 058-02.b1.g1.b1.b2_falling-market-next-day-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3809 USD
---
## Findings
- **F1:** Inside the falling profile, the fade is strong when the coin is agitated and absent when it is calm. On folds B and C, agitation was read as the 30-day swing above the coin's median. The fade score −z × next-day unusual move averages +0.0082 with t 5.27 over 2059 agitated cases, against +0.0013 with t 0.78 over 1991 calm cases.
- **F2:** In agitated falling markets both sides pay, and the move per case is about three times a trade's cost. The move in the fade's direction is +0.68 % after down days (t 3.88, 1060 cases) and +0.73 % after up days (t 4.01, 999 cases). In calm falling markets it is −0.12 % (t −0.73) and +0.23 % (t 1.43). One trade costs 0.22 %.
- **F3:** Only the down side is graded by the size of the move. After down days, the next-day move in the fade's direction rises with |z| across the five quintiles: −0.63 % (t −2.35), +0.08 %, +0.39 %, +0.35 % and +1.01 % (t 3.17, mean |z| 1.91). After up days it is flat or even falls with size: +0.68 % in the smallest quintile (t 2.72) and +0.38 % in the largest (t 1.07). The up side mostly carries the falling market's own drift, not a graded reversal.
- **F4:** The effect lives at the one-day horizon only. The day-summed fade score in the falling profile has t 2.14 at 1 day, 1.06 at 2 days, −0.10 at 3 days and 0.38 at 5 days.
- **F5:** The tested result is on the predicted side but short of the bar. Overall t is 1.72; on the visible folds B and C the main measure has t 2.34 over 911 days. All coins, folds and 1d bars were already used, so no more data is available. The blend of an agitated half that works and a calm half with t 0.78 explains why the result is unclear.

## Ideas
- `058-02.b1.g1.b1.b2.b1_falling-agitated-next-day-fade` (from F1, F2, F4, F5): In a falling, agitated market, the larger a coin's one-day rise is against its usual daily swing over the last 20 days, the larger its fall over the next day, and the larger its one-day fall against that swing, the larger its rise over the next day.
- `058-02.b1.g1.b1.b2.b2_agitated-downtrend-sharp-fall-rebound` (from F1, F2, F3, F4): In a falling, agitated market, the larger a coin's one-day fall is against its usual daily swing over the last 20 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
