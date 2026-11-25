---
line: 7.g patterns
backtest: 035-02_swing-wide-low-close-rebounds_1d
idea tested: 035-02_swing-wide-low-close-rebounds
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5727 USD
---
## Findings
- **F1:** The rebound lives in agitated markets. Where the coin's 20-day swing is above its own median, the slope of next-day excess return on the forecast is +10.1 bp per forecast unit (t 3.22, 3,630 bars), and the top fifth of forecasts is followed by +133 bp (t 2.51, 251 days). Where the swing is calm, the slope is +1.8 bp (t 0.90, 3,619 bars) and the top fifth earns +8 bp (t 0.28, 329 days). Two other agitation measures show the same split: the 20-day against the 60-day swing (agitated +8.8 bp, t 2.65, against calm +1.1 bp, t 0.48), and the 30-day swing against its own past (agitated +9.8 bp, t 2.02, against calm +1.2 bp, t 0.53).
- **F2:** The effect grows with the coin's recent swing. By the coin's 20-day swing in terciles, the slope is +1.2 bp per forecast unit in the lowest tercile (t 0.54), +5.6 bp in the middle (t 2.56) and +11.1 bp in the highest (t 2.57), about 2,400 bars each.
- **F3:** In agitated markets the agitated slope is positive in every year (2018 +12.2 bp, t 2.12; 2019 +11.6, t 2.36; 2020 +5.6, t 0.69; 2021 +10.7, t 1.88) and on every coin (from BTC +6.3, t 2.23, to XMR +14.5, t 3.65, and ZEC +14.1, t 3.29).
- **F4:** In agitated markets the move per case clears the cost of a trade. The top fifth of forecasts is followed by a total next-day move of +146 bp, 7.7 times the 0.19 % cost of a trade, against +40 bp in calm markets. On every bar together the idea's total move is +0.22 %, only 1.2 times that cost.
- **F5:** What carries the effect is the day's width times the close's nearness to its low, not the day's own return. In a joint day-clustered regression, the width × low-close product earns +46.6 bp per standard deviation (t 2.40), while the day's return in usual moves earns +0.5 bp (t 0.03). Among the widest third of days, those closing in the lowest third of their range are followed by +85.5 bp (t 2.46), against −49.6 bp (t −1.55) for wide days closing near their high.
- **F6:** The book does little more than ride the market. It is in a position on 100 % of the coins' days, its daily returns correlate 0.83 with the coins' own, and its mean allocation is 0.37. The forecast sits mostly above 0, so the book holds the coin almost every day rather than only after wide low-close days.
- **F7:** The other angles show nothing that stands out after so many looks:

## Ideas
- `035-02.g1_agitated-wide-low-close-rebound` (from F1, F3, F4, F5): In an agitated market, the larger a day's high-to-low range is as a multiple of the standard deviation of the coin's daily returns over the past 20 days, and the nearer its close sits to the day's low, the larger the coin's rise over the next day.
- `035-02.g2_absolute-high-to-close-drop-rebound` (from F2, F5): The larger the distance from a day's high down to its close, as a share of the close, the larger the coin's rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
