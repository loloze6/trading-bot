---
line: 7.d confirmed, not profitable
backtest: 060-02.d1_volume-growth-fall-still-running_1d
idea tested: 060-02.d1_volume-growth-fall-still-running
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5472 USD
---
## Findings
- **F1:** The Calmar of 0.33 fails because one fall is far deeper than the gain: the deepest fall is -26.4 % (yearly return +8.6 %), in w14 over about 16 days. The book lost 29.4 % summed there while its coins fell 37.1 %. Every coin was long at nearly full forecast in that episode (BTC +20.0, ETH +19.6, LTC +20.0, XMR +20.0, ZEC +20.0, XRP +10.4), with allocations of 0.37 to 1.09. Their 20-day returns were -30 % to -42 % and their 60-day returns -32 % to -54 %. The coins lost 11 % (XRP) to 38 % (ZEC) each. In that window the long side summed -0.37 and the short side +0.72.
- **F2:** The tested signal has no edge once the 20-day fall is a crash, on either side. On the 5-day grid, in the deepest third of 20-day returns, long cases earn +1.7 % (t 1.17, 87 cases) and short cases -0.3 % (t -0.21, 55 cases). In the middle third, long cases earn +3.7 % (t 2.18, 53 cases) and short cases +4.1 % (t 4.16, 89 cases). Long position-days in the deepest quarter of 20-day returns earn +0.017 % a day (404 days) with the largest swing (std 3.46 %), against +0.52 % a day in the third quarter. This condition only removes bars and adds no signal of its own: the signal exists on every bar of the regime, so it cannot be measured alone, and the deep bars earn about 0 rather than an effect.
- **F3:** The short side carries the graded effect and the long side does not. On the grid, short cases earn +4.4 % in the strongest third of shrinkage (t 3.69, 90 cases), against +0.9 % (t 0.86) in the weakest third and -0.1 % (t -0.08) in the middle third. Long cases earn +2.2 %, +2.1 % and +2.3 % across the three strengths, with t of 1.6 or less. Over all position-days the short side summed +2.39 against +1.52 for the long side. The deepest fall (F1) was made entirely on the long side.
- **F4:** The largest long allocations carry the risk without the gain. Long days in the top third of position size earn +0.019 % a day (463 days, std 4.14 %, worst day -14.2 %). Mid-size long days earn +0.30 % (std 2.40 %), and large short days earn +0.26 % (std 3.23 %).
- **F5:** Costs are not what fails. The total move per case is +1.16 %, 6.0 times the 0.19 % cost of a trade, and the Sharpe (0.60) and the gain over holding (+0.046) both pass. The book fails on how deep it falls, not on how much it earns.

## Ideas
- `060-02.d1.d1_volume-shrinkage-extends-running-falls` (from F3, F1, F4): In a falling market, while the coin's 20-day return is still negative, the more its trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 5 days.
- `060-02.d1.d2_volume-signal-outside-crash-falls` (from F2, F1): In a falling market, while the coin's 20-day return is still negative but its 20-day fall is moderate rather than a crash, the more its trading volume over the past 30 days has grown against the 30 days before, the smaller its fall, or the larger its rise, over the next 5 days.
- `060-02.d1.d3_shrinkage-short-in-moderate-falls` (from F2, F3, F1): In a falling market, while the coin's 20-day return is still negative but not yet a crash, the more its trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
