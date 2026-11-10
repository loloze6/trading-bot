---
idea: 002-03_price-upcross-long-sma-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
---
Forecast: The forecast is the percent distance of the 1h close from its 200-bar simple moving average, (close − SMA200) / SMA200 × 100, where the average includes the current close. This distance is put on the forecast scale by dividing it by the mean absolute value of its previous 200 values and multiplying by 10, capped at ±20. It is then clipped at 0, because the idea is only about crossing up. The forecast is zero while the close is at or below SMA200. It turns positive on the bar the close crosses above SMA200, starting near 0 at the cross. It grows smoothly as the close moves further above the average, reaching about +10 at a typical distance and at most +20. It never goes negative.
Config: 002-03_price-upcross-long-sma-drift_1h_config.json
Confirm: The horizon is 24 bars. The bars are sampled every 24 bars so that forward returns do not overlap (about 120 per window, about 730 in total). On bars where the forecast is above 0, the mean forward 24-bar log return exceeds the mean forward 24-bar return over all sampled bars, which stands for holding the coin. The excess must be positive with a t-statistic of at least 2.0 on the pooled samples, and positive in at least 4 of the 6 windows. Supporting check: the strategy's return before costs exceeds the return of holding the coin at the strategy's average allocation in at least 4 of the 6 windows.
Reject: The pooled excess forward 24-bar return on forecast > 0 bars is zero or negative, or positive in 2 or fewer of the 6 windows. A negative excess with t ≤ −2.0 also rejects the idea, and indicates reversal after up-crosses, meaning the cross marks exhaustion rather than the start of a trend.
Inconclusive: The pooled excess is positive but with t between 0 and 2.0. Or the pooled excess has t ≥ 2.0 but is positive in only 3 of the 6 windows. Or the main measure confirms but the supporting check fails, so the gain comes only from market exposure.
Deviation: "After a cross from below" becomes "while the close is above SMA200". The position is held for the whole time price stays above the average, not only in the bars just after the cross. Its size grows with the distance above the average, not with how recent the cross is. The idea does not state the length of the long average, so the conventional 200 bars is used.
