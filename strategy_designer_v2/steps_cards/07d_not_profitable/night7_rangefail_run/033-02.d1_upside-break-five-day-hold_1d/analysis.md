---
line: 7.d confirmed, not profitable
backtest: 033-02.d1_upside-break-five-day-hold_1d
idea tested: 033-02.d1_upside-break-five-day-hold
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4432 USD
---
## Findings
- **F1:** The book fails on its falls, not its gain: its Calmar is 0.71 against the rule's 0.75, from a +8.0 % yearly return and a deepest fall of −8.5 % in w17; 372 of the 474 days spent more than 3 % under the peak fall in w15 to w18 (90, 101, 103 and 78 days).
- **F2:** All of the book's gain comes from positions held while the coin's 60-day return was above +10 %. In that rising trend, 815 held bars earned +0.29 % each, +2.38 summed. Held bars in the other trends earned nothing: falling 716 bars at −0.006 % each (−0.05 summed), choppy 199 bars at −0.06 % each (−0.12 summed). So 915 of the 1,730 held bars added risk without gain.
- **F3:** Fresh 20-day-high breaks are followed by a much larger 5-day unusual move in a rising 60-day trend than in the others. Rising: +5.3 %, t 3.49, 109 cases. Choppy: +2.9 %, t 1.34, 32 cases. Falling: +0.5 %, t 0.27, 30 cases. A rising trend alone does not carry this move: grid bars without a break in a rising trend give +0.6 % (t 0.82, 288 cases), so the trend limits where the breakout effect holds and is not an effect of its own. This fits the brief's theory that breakout and trend-following flows add to a coin already being read as trending.
- **F4:** During the book's deep falls (more than 3 % under the peak), only 18 % of the held bars were in a rising 60-day trend, against 27 % of all held bars. The falls are made disproportionately by positions taken outside the rising trend.
- **F5:** The size of the move is not the problem: the total move per case is +2.34 %, 12.1 times the 0.19 % cost of a trade. Held bars 0 to 5 days after the fresh break earn +0.39 %, −0.13 %, +0.39 %, +0.25 %, +0.38 % and +0.23 % a bar. Bars 6 or more days after the break (1,093 held bars) earn about 0 (−0.04 % and −0.008 % a bar), so the aged positions only add swings.
- **F6:** Breaks out of a narrow range carry the effect and breaks out of a wide one do not. By the prior 20-day range width (high minus low, over price), the 5-day unusual move after a fresh break is +3.3 % (t 2.92) in the narrowest third, +4.1 % (t 2.56) in the middle third and +1.1 % (t 0.76) in the widest third, with 92 to 93 cases each. Without a break, the same thirds give +0.5 % (t 1.31), −0.6 % and −0.5 %, so a narrow range alone is not the effect.
- **F7:** Breaks made while the coin's recent swing is high against its longer swing (30-day over 60-day daily standard deviation) carry more. By thirds of that ratio, the unusual move is +2.3 % (t 1.50), +4.7 % (t 2.90) and +5.1 % (t 2.04), with 57 cases each. Held bars by the same thirds earn −0.01 %, +0.10 % and +0.30 % a bar. Without a break the ratio shows no pattern (−0.8 %, +1.1 %, −1.4 %), so the swing alone is not the effect.

## Ideas
- `033-02.d1.d1_rising-market-upside-break-hold` (from F1, F2, F3, F4, F5): In a rising market, when a coin closes above its 20-day high, it rises over the next 5 days, and it rises more the further the close sits above that high, with the rise completed within those 5 days of the break rather than continuing while the close stays above the range.
- `033-02.d1.d2_narrow-range-upside-break-hold` (from F1, F5, F6): When a coin closes above its 20-day high, it rises over the next 5 days, and it rises more the narrower its 20-day high-to-low range was against its price before the break, with the rise completed within those 5 days.
- `033-02.d1.d3_agitated-upside-break-hold` (from F1, F5, F7): When a coin closes above its 20-day high, it rises over the next 5 days, and it rises more the larger its last 30 days' swing is against its swing over the 60 days before the break, with the rise completed within those 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
