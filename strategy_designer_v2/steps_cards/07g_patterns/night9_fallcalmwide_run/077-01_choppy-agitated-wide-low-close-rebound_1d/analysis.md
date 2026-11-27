---
line: 7.g patterns
backtest: 077-01_choppy-agitated-wide-low-close-rebound_1d
idea tested: 077-01_choppy-agitated-wide-low-close-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3907 USD
---
## Findings
- **F1:** Inside the choppy agitated profile (the bars the code did not veto), wide days that close in the top quarter of their range are followed by a fall the next day. Relative to the coin's normal drift the move is −3.45 % at mid width (16 cases, t −1.95), −5.27 % at wide (14 cases, t −1.93) and −4.01 % at very wide (5 cases, t −0.83). Narrow high-close days in the same profile move only −0.71 % (32 cases, t −0.65).
- **F2:** Outside the profile the same high-close days barely fade. Very wide ones move −0.88 % (283 cases, t −1.54) and wide ones +0.13 % (519 cases, t 0.38), so the fall after a wide high close is about four times larger inside choppy agitated than elsewhere. No strategy on the map holds the choppy agitated short cell.
- **F3:** Outside the profile, wide low-close days rebound, and the rebound grows with width. Wide days gain +0.81 % the next day (360 cases, 175 days, t 2.01), very wide days +1.62 % (280 cases, 126 days, t 2.45). The very wide rebound is not spent within one day: +1.74 % over two days (t 2.49).
- **F4:** Across all bars, wide low-close days rebound more when the coin's 30-day swing is in its own top third, and the effect grows with the swing. The next-day gain is +2.06 % in the top third (209 cases, t 2.51), +0.96 % in the middle third (259 cases, t 2.26) and +0.57 % in the bottom third (196 cases, t 1.07). This is the agitated wide low-close rebound the map already holds (039-02, 044-01, 045-01), so it is not a discovery.
- **F5:** Inside the profile, the tested low-close side has too few cases to read. Very wide low closes gain +2.64 % (16 cases, t 1.22), and the book traded 0.006 times a day against the 0.01 required, so its failure is mainly a shortage of cases, not of size (the total move is 4.4 times the cost of a trade).
- **F6:** Other angles showed nothing that stands out after this many looks:

## Ideas
- `077-01.g1_choppy-agitated-wide-high-close-fade` (from F1, F2, F5): In a choppy, agitated market, a wide day that closes near its high is followed by a fall over the next day, larger the wider the day's range against its 30-day swing and the nearer the close sits to the high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
