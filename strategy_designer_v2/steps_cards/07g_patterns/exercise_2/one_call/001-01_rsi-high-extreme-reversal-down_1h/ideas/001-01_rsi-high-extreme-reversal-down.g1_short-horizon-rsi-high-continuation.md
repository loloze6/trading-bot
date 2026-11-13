---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal-down
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal-down_1h
instruments: BTC, ETH, BNB
bar: 1h
period: fold A
---
Idea: When a coin's hourly RSI sits at its highest level relative to its last 60 values, price keeps rising over the next few hours, roughly the first four, instead of giving the move back.
Consequence: A trader should refuse to short a coin just because its hourly RSI is unusually high for its recent history, and may lean with the move over the next few hours.
Why:
- F1: The short-only book lost in all 12 coin-windows (BTC from -0.12 to -1.12 log, ETH from -0.41 to -0.81). That includes the four windows per coin where the coin itself fell, for example ETH w2 with the coin at -0.57 and the book at -0.60. Twelve of twelve losing would happen by chance with probability below 0.001.
- F2: The trades lost before fees, not only after them. The mean gross P&L per trade was -0.47% on BTC (3829 trades) and -0.57% on ETH (3871 trades), with win rates of 48% and median holds of 240 minutes. The short entries on unusually high RSI were, on average, followed by further rises over the next few hours.
- F3: Losses grew with the size of the short. Bars holding a position above 1 lost a mean of -5.2 bp per bar, 7330 bars summing to -3.78 log. Flat bars lost -0.35 bp and bars at 0–0.25 lost -0.73 bp. The more extreme the RSI was relative to its own recent values, the more price kept rising in the following hours.
- F4: Over 12 hours the signal turned weak and changed sign depending on the cut, so the give-back the idea expects is not visible. Overlapping bars with RSI 60–70 were followed by +30 bp (n=962, overlap-adjusted t 1.26; BTC +35 bp, ETH +23 bp). The top RSI decile on the non-overlapping grid showed -19 bp excess (t -1.44, n=292).
