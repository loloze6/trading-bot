---
line: 7.d not profitable
backtest: N2-05_shock-up-continuation_1d
idea tested: N2-05_shock-up-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3145 USD
---
## Findings
- **F1:** The book barely earns before fees and pays about four times that in fees. Over 17,380 bars its gross is 0.00006 per bar, its fees 0.000227 per bar and its net −0.000167 per bar. It turns over 0.207 of capital per bar while its average exposure is only 0.13 and it is in the market 30% of bars.
- **F2:** The book holds each shock for about one day, which is the day the effect is absent. The median trade lasts 1 day and the 75th percentile 3 days, over 2,692 trades, all long. The next-bar return after the largest shocks (forecast 20) is −0.24%, t −0.75, hit rate 43%, over 322 non-overlapping events.
- **F3:** The gain the book misses arrives over the following days and grows with the horizon. After forecast-20 shocks the mean return is +1.56% over 5 bars (t 2.00, n 322) and +3.44% over 10 bars (t 2.81, n 317). Forecast 5–10 events give +1.10% over 5 bars and +2.70% over 10 bars (t 2.50, n 323). So a larger forecast earns only slightly more, while a longer hold earns clearly more.
- **F4:** The continuation exists only when the coin is already in an uptrend. Shocks with the close above its 50-bar mean give +2.06% over 5 bars (t 2.87, n 314), against −0.03% below it (t −0.04, n 196). Shocks after a positive 20-bar return give +1.87% (t 3.01, n 452), against +0.68% (t 1.18, n 424) after a negative one.
- **F5:** The book's losses sit in the downtrend state. Bars below the 50-bar mean (12,258) net −0.000294 per bar, against +0.000137 on bars above it (5,122). Bars with a negative 20-bar return net −0.000309, against +0.000034 with a positive one.
- **F6:** The losing years are falling-market years where shocks reversed. In 2022 the 5-bar return after shocks was −2.56% (t −1.98, n 97) and the book's gross was −0.000135 per bar. 2018 gave −0.17% (n 98). The rising years 2021 and 2024 gave +4.11% (t 2.65, n 106) and +3.89% (t 3.23, n 104).
- **F7:** Full-size positions earn nothing and pay the most. On 795 bars at allocation above 1.0 the gross is 0.00009 per bar and the fees 0.00175 per bar. These are the bars right after the biggest shocks, when the next day is flat.

## Ideas
- `N2-05_shock-up-continuation.d1_slow-drift-after-shock` (from F1, F2, F3, F7): After a coin closes up by an outsized amount against its recent daily moves, its price keeps drifting up over the next one to two weeks. The drift comes mostly after the first day, not on the day after the shock.
- `N2-05_shock-up-continuation.d2_shock-continuation-in-uptrends` (from F4, F5, F6): A coin's outsized up day is followed by further gains over the next days when the coin closes above its 50-day average and is up over the prior 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
