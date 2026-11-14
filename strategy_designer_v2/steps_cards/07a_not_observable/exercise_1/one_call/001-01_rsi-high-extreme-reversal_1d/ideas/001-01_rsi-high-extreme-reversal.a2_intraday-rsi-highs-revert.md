---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal
line: 7.a not observable
backtest: 001-01_rsi-high-extreme-reversal_1d
instruments: BTC, ETH, BNB
bar: 4h
period: 2022 to 2025
---
Idea: On each of BTC, ETH and BNB, 4-hour bars where RSI(14) is high relative to its own past 60 readings are followed by a 5-bar return below that coin's average 5-bar return.
Consequence: A trader would stand aside from longs, or fade the move, over the next day after a 4-hour RSI high, where such readings occur often enough to be tested.
Why:
- F1: The plan's minimum of 30 non-overlapping cases could not be reached even in principle, because the backtest holds one coin (BTCUSD) in one window of 120 daily bars, which gives only 23 non-overlapping 5-bar blocks with a defined forward return. Even if every block had been extreme, the count would have been 23.
- F3: The situation itself is rare. Of the 120 bars, 15 had a forecast of −10 or lower, and they formed only 3 separate runs (median length 2 bars, longest 12), so the 5-bar grid caught just 3 cases. At other grid offsets the count was 2 to 4.
- F4: The "high extreme" in this window was a mild RSI rather than a true extreme. RSI(14) never reached 60 (0 bars at 60, 65 or 70; maximum 58.0), and the extreme bin covered RSI 54.0 to 58.0, so the 60-bar standardisation labelled ordinary readings as extremes in a calm period.
- F5: The outcome varies far more than the effect. At the 3 extreme grid cases the excess 5-bar return was −6.75% with a standard deviation of 6.35% (t −1.84). Over all 15 overlapping extreme bars it was −2.34% with a standard deviation of 5.66%, and the 5-bar return's overall standard deviation was 7.27%. At the milder −2 threshold, about 35 cases would be needed for t = −2 (6 available, mean −3.2%, t −0.83).
