---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-05_sma-up-regime-positive-drift
line: 7.c rejected
backtest: 002-05_sma-up-regime-positive-drift_1d_minus1pct
instruments: BTC/USDT
bar: 1d
period: fold A
---
Idea: While BTC's 50-day SMA sits above its 200-day SMA, the next daily bar's open-to-close move is positive on average. Any loss in that stretch comes from the step between one bar's close and the next bar's open, not from trading within the bar.
Consequence: In an up-regime, judge the trend's persistence by the open-to-close move, not close-to-close returns, because the -1% step at the bar boundary is probably a data shift (the plan carries a "minus1pct" tag, and the coin falls throughout 2023) rather than market behaviour.
Why:
- F1: The whole in-stretch deficit sits in the gap from one bar's close to the next bar's open: that gap averages -0.99% on in-stretch bars against -0.0007% out of stretch, while the next bar's open-to-close move is +0.11% in-stretch against -0.03% out, so the -0.86% in-stretch mean next-bar return (vs -0.03% out, Welch t -4.14) comes from a near-constant -1% step between bars and not from intraday trading.
- F6: The in-stretch loss is a shifted centre rather than a fat tail: the in-stretch median is -1.06% against -0.06% out, the 75th percentile is +0.23% against +1.36%, and in-stretch bars are calmer, with a 3.4% next-bar high-low range against 4.4%.
- F9: The coin fell in every window (-17.9% to -72.9%) and the rejection rests on 2023, where 277 in-stretch bars averaged -0.85% against +0.76% for 85 out-of-stretch bars (t -5.96); 2022 adds only 13 in-stretch bars (-1.76% vs -0.22%, t -2.29).
- F10: The book records no trades, yet its value moves in four windows: +24.9% in w4 and +26.0% in w6 while the coin lost about 22% in each, and -8.1% in w1 and -8.9% in w5 against coin losses of -30.8% and -72.9%.
