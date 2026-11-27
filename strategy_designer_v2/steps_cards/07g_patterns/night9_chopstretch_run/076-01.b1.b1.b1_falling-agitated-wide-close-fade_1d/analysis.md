---
line: 7.g patterns
backtest: 076-01.b1.b1.b1_falling-agitated-wide-close-fade_1d
idea tested: 076-01.b1.b1.b1_falling-agitated-wide-close-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5697 USD
---
## Findings
- **F1:** In the falling-agitated profile, wide high-closing days fall the next day but not reliably. The top two deciles of (close − mid-range) / 20-day mean range are followed by −1.75 % (t −3.32, 121 bars, unclustered) and −1.47 % (t −1.79, 72 bars). With cases on the same day taken together, the three terciles of wide high-closing days give +0.98 % (t 0.69), −2.61 % (t −1.72) and −1.76 % (t −1.39). The fall is not graded from the middle tercile to the top one, which fits step 5's inconclusive t of 1.76.
- **F2:** In choppy markets, the top tercile of wide high-closing days is followed by −1.89 % the next day (t −3.01, 59 cases on 41 days), while the lower terciles give −0.81 % and +1.13 %. Among choppy days in the top quartile of the product, the agitated ones fell −2.64 % (t −1.90, 34 cases on 29 days) and the calm ones rose +0.30 % (t 0.40, 74 cases).
- **F3:** In rising markets the pattern does not appear. Wide high-closing days are followed by −0.06 %, +0.78 % and +0.50 % by tercile, and the top quartile of the product by +0.65 % (t 1.17, 142 days). The Spearman correlation is +0.015 (p 0.61), so the brief's claim of a fade "in any trend" fails in rising markets.
- **F4:** The fade lasts one day only. Over two days, wide high-closing days in falling-agitated markets give +0.20 % (t 0.21, 86 days) and in choppy markets +0.54 % (t 0.89).
- **F5:** The largest and surest move in these bars is a rebound after wide low-closing days, not a fade after high closes. All profiles together, the widest range quintile with the lowest close location rose +1.73 % the next day (t 5.21, 301 bars, unclustered). In the falling-agitated profile, the widest tercile closing in its lower half rose +2.65 % (t 2.76, 182 cases on 90 days). This effect is already held on the map (039-02, 044-01, 045-01 in falling agitated), so it is not a discovery.
- **F6:** Wednesday's next-day move of −0.62 % (t −3.49 unclustered) falls to t −1.45 once same-day cases are taken together (175 days). Its sign holds in all four years, but only 2019 reaches t −2.72. Among the many angles looked at (weekday, volume, year, coin), it does not stand out from chance.

## Ideas
- `076-01.b1.b1.b1.g1_choppy-agitated-wide-close-fade` (from F2, F3, F4): In a choppy, agitated market, a day whose high-low range is wide against the coin's average range over the past 20 days and which closes near its high is followed by a fall over the next day. The fall is larger the wider the day's range and the higher in its range it closes, the two multiplying.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
