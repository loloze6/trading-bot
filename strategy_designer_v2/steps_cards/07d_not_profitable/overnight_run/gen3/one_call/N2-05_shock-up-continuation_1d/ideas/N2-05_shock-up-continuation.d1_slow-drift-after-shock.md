---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-05_shock-up-continuation
line: 7.d not profitable
backtest: N2-05_shock-up-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin closes up by an outsized amount against its recent daily moves, its price keeps drifting up over the next one to two weeks. The drift comes mostly after the first day, not on the day after the shock.
Consequence: A trader should hold a long taken on a big up day for days, not exit it the next day, and should not expect a gain on the first day.
Why:
- F1: The book barely earns before fees and pays about four times that in fees. Over 17,380 bars its gross is 0.00006 per bar, its fees 0.000227 per bar and its net −0.000167 per bar. It turns over 0.207 of capital per bar while its average exposure is only 0.13 and it is in the market 30% of bars.
- F2: The book holds each shock for about one day, which is the day the effect is absent. The median trade lasts 1 day and the 75th percentile 3 days, over 2,692 trades, all long. The next-bar return after the largest shocks (forecast 20) is −0.24%, t −0.75, hit rate 43%, over 322 non-overlapping events.
- F3: The gain the book misses arrives over the following days and grows with the horizon. After forecast-20 shocks the mean return is +1.56% over 5 bars (t 2.00, n 322) and +3.44% over 10 bars (t 2.81, n 317). Forecast 5–10 events give +1.10% over 5 bars and +2.70% over 10 bars (t 2.50, n 323). So a larger forecast earns only slightly more, while a longer hold earns clearly more.
- F7: Full-size positions earn nothing and pay the most. On 795 bars at allocation above 1.0 the gross is 0.00009 per bar and the fees 0.00175 per bar. These are the bars right after the biggest shocks, when the next day is flat.
