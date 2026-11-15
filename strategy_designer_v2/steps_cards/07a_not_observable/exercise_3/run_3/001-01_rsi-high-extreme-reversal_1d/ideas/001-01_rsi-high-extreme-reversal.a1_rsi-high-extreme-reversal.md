---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal
line: 7.a not observable
backtest: 001-01_rsi-high-extreme-reversal_1d
instruments: BTC, ETH (BNB is not available)
bar: 1d
period: all four folds A, B, C and D, every window
---
Idea: When a coin's 14-day RSI is at a high extreme, its price falls back over the next 5 days, the more so the higher the RSI reading.
Consequence: If confirmed on enough history, a trader has a reason to fade, or at least not chase, coins whose RSI is at a high extreme for the next five days; if rejected, a reason to refuse that fade.
Why:
- F1: The test ran on only one coin and one window: BTCUSD w1 (2022), with 120 daily bars and 23 non-overlapping 5-bar grid cases. ETH and BNB do not appear in the record at all, so "negative in at least 2 of the 3 coins" could not be met by construction.
- F2: The extreme situation is not rare. 15 of 120 bars (12.5%) carried a forecast of −10 or lower, and 3 of the 23 grid cases did (13%), so the shortfall to the plan's minimum of 30 cases comes from too little data, not from a rare situation.
- F3: The forecast is mostly flat and runs short only. 81 of 120 bars (67.5%) sat at exactly 0, the median was 0, 10 bars sat in (−20, −15] and the 5% quantile was the −20 cap. Only 32.5% of raw component values were negative, so roughly a third of bars are short and about a third of those are extreme.
- F4: Outcomes vary widely from case to case. The 5-bar forward return on the grid had a standard deviation of 0.076 against a window mean of −0.0050. The 3 extreme cases averaged an excess of −0.0675 (t −1.84). The 8 grid cases with any negative forecast averaged −0.0121. At about 13% extremes per grid case, 30 cases need about 230 grid cases, or about 1,150 daily bars per pooled sample.
