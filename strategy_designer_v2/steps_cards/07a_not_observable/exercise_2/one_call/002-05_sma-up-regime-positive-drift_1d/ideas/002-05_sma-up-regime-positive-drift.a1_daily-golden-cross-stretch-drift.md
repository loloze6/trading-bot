---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-05_sma-up-regime-positive-drift
line: 7.a not observable
backtest: 002-05_sma-up-regime-positive-drift_1d
instruments: BTC/USDT, ETH/USDT, SOL/USDT, BNB/USDT, XRP/USDT, ADA/USDT, DOGE/USDT, LTC/USDT, LINK/USDT, AVAX/USDT
bar: 1d
period: 2017-2025
---
Idea: On a coin's daily bars, the days on which its 50-day simple average is above its 200-day simple average are followed by a higher mean next-day close-to-close return than the days on which it is below, measured over many coins and many years so that dozens of up-cross stretches are covered.
Consequence: A trader would hold the coin long only through its 50-over-200 daily stretches and stand aside otherwise.
Why:
- F1: The plan needed at least 100 in-stretch bars and 3 up-cross stretches, but the backtest got 13 in-stretch bars and 1 stretch; it also had 107 out-of-stretch bars, so the shortfall is entirely on the side where the idea's situation holds.
- F2: The data is one coin (BTCUSD) and one window (w1) of 120 daily bars covering 119 days. That is shorter than the 200-day slow average itself, so a full cross-to-cross stretch of a 50/200 daily pair can hardly fit inside it.
- F3: The only up-stretch was already under way when the window opened, with a raw spread of +50.3 on the first bar. It ended at bar 12, the single down-cross. So the in-stretch sample is the tail of one stretch whose up-cross falls outside the data.
- F5: The outcome varies far more than the effect being measured. The next-bar return SD was 0.0233 in-stretch and 0.0342 out-of-stretch, against a mean difference of -0.0069 (Welch t -0.95). At a daily SD near 0.03, a true drift of 0.2% per day needs roughly 1,800 bars per side to reach t=2, which means many years of daily bars or many coins.
