---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-02_thin-volume-drop-rebounds
line: 7.g patterns
backtest: 003-02_thin-volume-drop-rebounds_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises sharply over one day relative to its own 20-day volatility, it keeps rising over the next 5 days, and the larger the volatility-scaled rise and the heavier its volume against the coin's 30-day average, the larger the further gain.
Consequence: A large up day on heavy volume is a reason to be long the coin for the following week rather than fade it.
Why:
- F1: Across all coins and windows, a coin's 5-day excess return rises with the size of its one-day move scaled by its own 20-day volatility. The slope is 0.0045 per unit of scaled move (t 2.49, 2555 non-overlapping cases). Days up by 1 to 2 usual moves are followed by +1.58% (t 2.21, n 255). Days up by more than 2 usual moves are followed by +2.47% (t 1.96, n 110). Days down by more than 2 usual moves are followed by only +0.35% (t 0.34, n 76), so falls show no rebound.
- F2: The continuation after up days of more than 1 usual move is positive in all six coins. It is largest in XRP (+5.3%, t 2.09) and ZEC (+3.4%, t 1.75). It is concentrated in the early years: +3.5% (t 3.14, n 147) in 2018–2021 against +0.9% (t 1.22, n 202) in 2022–2025.
- F3: Volume adds to the continuation of up days, but only weakly.
