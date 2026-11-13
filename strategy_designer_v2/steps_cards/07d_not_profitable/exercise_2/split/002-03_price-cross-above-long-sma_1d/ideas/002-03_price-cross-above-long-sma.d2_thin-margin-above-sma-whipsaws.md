---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A close that sits only slightly above its 200-day SMA is followed by a 20-bar return below the coin's average 20-bar return, and the close often falls back under the SMA soon after.
Consequence: Stay out of bars that sit only slightly above the SMA, because that is where the signal turns on and off often and its short trades lose.
Why:
- F3: Being above the 200-day SMA barely separates good from bad bars: active bars earn 13.4 bp a day and 3.2% over 20 bars, against 12.4 bp and 2.6% on flat bars, and only 42.0% of active bars beat the coin's pooled 20-bar mean.
- F4: A larger forecast earns more over 20 bars only roughly: mean forward 20-bar returns are -0.25%, 2.4%, 4.4%, 3.9% and 7.8% across the buckets 0–5, 5–10, 10–15, 15–20 and 20; the 15–20 bucket earns just 2.0 bp a day; and the 0–5 bucket loses 3.6 bp a day on a 0.25 allocation with a 39% 20-bar hit rate.
- F5: The book's gain sits entirely in long holds: 2228 trades, all long, with a 29.7% gross win rate and a median hold of 11 days; every duration class up to 30 days loses on average (-6.1%, -6.4%, -5.7% and -2.3% gross, summing to about -8040%), while the 515 trades held over 30 days make +33.9% each, summing to +17472%.
