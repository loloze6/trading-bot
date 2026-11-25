---
line: 7.d confirmed, not profitable
backtest: 042-01_low-close-next-day-rebound_1d
idea tested: 042-01_low-close-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5297 USD
---
## Findings
- **F1:** The book was too small and too constantly in the market to clear its costs. Its mean absolute position was 0.107 of the book, with a median of 0.096 and a 99th percentile of 0.33. It held a position on 99 % of the coin-days, and its position changed by 0.142 of the book per day. That gave a gross gain of 3.4 bp per coin-bar against 1.3 bp of fees, so its mean daily return on days in a position was 0.47 bp against the 5 bp the check requires, with a Calmar of 0.08. The average case moves +0.22 %, only 1.1 times the 0.19 % cost of a trade, so a version of the idea with larger cases is needed.
- **F2:** The effect is carried by closes near the low on days whose range is wide against the coin's last 20 days. A close in the bottom fifth of the range on a top-third range day gave a drift-removed next day of +142.6 bp (t 3.23 with each day's cases taken together; 505 cases on 215 days), 7.5 times the cost of a trade. The wide range alone gave +7.0 bp (t 0.28; 2127 cases), and a low close on a narrower range gave -7.5 bp (t -0.20; 666 cases). So the range is not an effect of its own: it measures how much urgent flow was left unabsorbed, which is the brief's own mechanism.
- **F3:** The low-close, wide-range case is graded and stable. On long cases scored by (close location - 0.5) x the range relative to its 20-day mean, the next-day excess return by score quintile was -18, +9, +30, +20 and +128 bp (about 718 cases each). In the low-close, wide-range cell, the mean was positive in all 12 explored windows (w7 to w18), from +0.65 % to +3.46 %.
- **F4:** The short side added little and lost in rising markets. The book's gross gain was 5.6 bp per bar when long against 1.3 bp when short. Closes in the top fifth of the range were followed by +45.9 bp in a rising 60-day trend (454 cases), against -35.8 bp in falling and -77.8 bp in choppy trends.
- **F5:** A close near the low pays mainly inside a falling 60-day trend. The next day gave +121.0 bp (t 2.10; 398 cases, 164 days) for low closes in a falling trend, against +24.5 bp (t 0.71; 773 cases) outside it. A falling trend without a low close gave -46.6 bp (t -1.94; 1665 cases), so the trend alone is not the effect. In a choppy trend, low closes gave -95.6 bp (77 cases). My agitation measure could not be computed inside the windows, so this finding speaks to the trend only.
- **F6:** The close's place in the range carries information beyond the day's own move, which answers the brief's falsification test. In a pooled regression with the day's return standardised by its 20-day swing, each unit of close location from high to low added +75 bp to the next-day excess return, while the standardised day return gave -15.5 bp. Within terciles of the day's standardised return, the close-location coefficient was +74 bp on down days, +88 bp on flat days and +8 bp on up days.

## Ideas
- `042-01.d1_wide-range-low-close-rebound` (from F1, F2, F3, F4, F6): A coin rises over the next day, more so the nearer that day's close sits to the day's low within its high-low range and the wider that range is against the coin's daily ranges of the past 20 days.
- `042-01.d2_falling-market-low-close-rebound` (from F1, F4, F5): In a falling market, a coin rises over the next day, more so the nearer that day's close sits to the day's low within its high-low range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
