---
line: 7.g patterns
backtest: 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high_1d
idea tested: 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4034 USD
---
## Findings
- **F1:** Across all 6 coins, a day's fall measured against the coin's past-20-day daily volatility is followed by a next-day rebound that grows with the size of the fall. On down days, the slope of the next-day excess return on that standardised move is negative for every coin. It is significant on three: XMR (t −3.88, 1247 cases), XRP (t −2.71, 1326) and ZEC (t −2.08, 1328).
- **F2:** The rebound after falls holds on non-overlapping 2-day stretches: slope −0.0047, t −2.83 over 3885 cases. The next-day excess return is +0.69 % after a fall of 1 to 1.5 standard deviations and +0.75 % after a fall beyond 2. Both are several times this backtest's 0.19 % round-trip cost. After falls of under half a standard deviation it is −0.06 %. With cases averaged by date, the 1 to 1.5 band keeps t 2.95, while the beyond-2 band drops to t 1.48, so part of the effect is shared across coins on the same days.
- **F3:** The rebound after falls is not steady over time. It is strong in 2020 (t −4.23), 2021 (t −3.91) and 2018 (t −2.25), and close to zero in 2022, 2023 and 2024 (t from −0.77 to +0.04). On up days there is no such effect, except for XRP (t +3.05, with the opposite sign: continuation).
- **F4:** The book cuts its position just before these rebounds. Its average allocation is 0.46 after falls of under half a standard deviation and 0.35 after falls beyond 2 standard deviations, which are the days followed by the largest next-day excess return.
- **F5:** The raw nearness to the 90-day high, before standardisation, is U-shaped against the next 5 days' excess return. The two nearest deciles earn +1.61 % (t 2.33) and +1.18 % (t 1.55). The middle deciles are negative: decile 2 is −1.61 % (t −3.01) and decile 4 is −0.99 % (t −2.01). The deepest decile earns +1.23 % (t 1.68). The nearest decile is positive in all 6 coins, from +0.11 % (XMR) to +1.89 % (XRP).
- **F6:** The book mostly carries the market. Its daily return correlates 0.78 with the coins' mean return. Its best 2 % of days hold 150 % of its total gain and its worst 2 % hold −139 %. It falls less than holding in losing windows (w7: −0.28 against −0.58; w2: −0.22 against −0.44), but its Calmar is 0.72.
- **F7:** The weekday pattern does not stand out from chance once cases are averaged by date. Pooled, Thursday and Friday look positive (t 2.63 and 3.76), but averaged by date their t is only 1.03 and 1.85. The other angles also showed nothing that stood out after this many looks: the past 5-day return, the past 20-day return, the volatility level, the day's high-low range and the position in the 60-day range.

## Ideas
- `020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high.g1_rebound-after-outsized-daily-falls` (from F1, F2, F3, F4): The larger a coin's fall on the day, measured against its typical daily move over the past 20 days, the more it rises over the next 1 to 2 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
