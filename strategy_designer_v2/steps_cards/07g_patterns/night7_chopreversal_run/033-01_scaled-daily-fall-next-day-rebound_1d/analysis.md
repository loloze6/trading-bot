---
line: 7.g patterns
backtest: 033-01_scaled-daily-fall-next-day-rebound_1d
idea tested: 033-01_scaled-daily-fall-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4152 USD
---
## Findings
- **F1:** On down days with a fall beyond one usual 30-day move, the next-day excess return over drift depends on the day's volume against its past month: high volume (above 1.3 times the 30-day mean) +1.49 % (t 2.98, 167 days, 441 cases), normal volume +0.21 % (t 0.36), low volume +0.37 % (t 0.61). This is the strongest split of the roughly fifteen angles explored.
- **F2:** Fall size and volume grade the rebound together. In the top volume tertile the next-day excess rises from +0.19 % (falls under 1 usual move, t 0.53) to +0.78 % (1 to 2, t 1.62) to +1.88 % (over 2, t 2.07, 68 days). In the bottom tertile it stays at -0.04 % (t -0.15) and -0.20 % (t -0.26). Over two days on a non-overlapping grid, falls beyond one usual move on volume above 1.6 times the median gain +1.76 % (t 1.93, 88 days), against +0.16 % at 1 to 1.6 times.
- **F3:** Volume carries its own effect on down days: the slope of next-day excess on log relative volume is 0.0059 (t 2.17, 867 days), against 0.0060 (t 1.76) for the scaled fall alone.
- **F4:** The high-volume rebound after a fall beyond one usual move is positive in 11 of 12 windows; w9 is the exception at -0.61 %. It is positive on all 6 coins, from +0.66 % on BTC (t 1.25) to +1.53 % on XRP (t 1.86) and +1.28 % on XMR (t 2.48).
- **F5:** The rebound lives in agitated markets, where the 30-day swing is above its recent median. There, falls beyond 2 usual moves gain +3.21 % the next day (t 1.83, 30 days), falls of 1 to 2 gain +1.08 % (t 1.69), and falls under 1 gain +0.12 % (t 0.30). In calm markets the same buckets gain only +0.72 % (t 0.90), +0.10 % (t 0.24) and -0.15 % (t -0.69).
- **F6:** The book spends much of its exposure where the move is below the cost of a trade (0.19 %). Falls of under half a usual move get a mean allocation of 0.13 over 1702 bars, yet their next-day excess is +0.10 % (t 0.50) and they earn 0.47 of the 7.65 summed gain. Falls beyond one usual move (845 bars, allocation 0.78) earn 5.10, two thirds of it, with an excess of +0.88 % to +3.14 % per bucket.
- **F7:** Neither a long slide nor the market's trend is needed for the rebound. Large falls (beyond one usual move) after a 5-day rise gain +1.16 % (t 2.41) and after a 5-day fall of over 10 % gain +1.47 % (t 2.18). By 60-day trend, falls of 1 to 2 usual moves gain +1.13 % (t 1.78) in rising markets and +0.73 % (t 1.29) in falling ones.

## Ideas
- `033-01.g1_heavy-volume-outsized-fall-rebound` (from F1, F2, F3, F4, F6, F7): The larger a coin's one-day fall measured against the standard deviation of its daily returns over the past 30 days, and the heavier that day's volume against its median daily volume of the past 30 days, the larger its rise over the next day; a large fall on light volume is followed by no rise.
- `033-01.g2_agitated-market-scaled-fall-rebound` (from F5, F6): In an agitated market, the larger a coin's one-day fall measured against the standard deviation of its daily returns over the past 30 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
