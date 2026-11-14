---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal
line: 7.a not observable
backtest: 001-01_rsi-high-extreme-reversal_1d
instruments: BTC, ETH, BNB
bar: 4h
period: 2022 to 2024
---
Idea: On each of BTC, ETH and BNB, after a 4-hour bar closes with its 14-bar RSI at a true high extreme, the coin's return over the next 5 four-hour bars is below its own average 5-bar return. This is the same reversal claim at a bar size where overbought episodes occur many times a year.
Consequence: A trader would avoid buying, or would fade, a coin for the next day after a 4-hour close in the overbought zone.
Why:
- F2: The forecast was 0 on the first 34 of 120 bars: no bar before 34 had RSI above 50, and the forecast needs at least 20 bars of history before it can be standardised. Only 39 bars (33 %) had any short forecast, and 81 bars had a forecast of exactly 0.
- F4: The 15 extreme bars fell in only 3 episodes, of 2, 1 and 12 bars. Sampling every 5th bar therefore yields only 2–4 cases whichever grid offset is used, and the episode count, not the grid, sets the limit.
- F5: Case-to-case outcomes are noisy and depend on where the 5-bar grid starts. The 5-bar forward return has a std of 7.3 %, and the mean excess return across the five grid offsets ranges from −6.8 % (t −1.84, n 3) to −0.2 % (t −0.10, n 3).
- F9: The observed rate was about 3 non-overlapping cases per 120 daily bars, and that was with extremes defined relative to the window rather than by absolute RSI. At that rate, 30 cases need about 1,200 coin-days, for example roughly 400 daily bars for each of the 3 coins. The run covered 120 coin-days, about a tenth of that.
