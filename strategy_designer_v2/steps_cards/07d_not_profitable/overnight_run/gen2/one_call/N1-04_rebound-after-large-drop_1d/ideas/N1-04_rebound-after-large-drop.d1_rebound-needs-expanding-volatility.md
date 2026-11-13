---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-04_rebound-after-large-drop
line: 7.d not profitable
backtest: N1-04_rebound-after-large-drop_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, a daily close that falls far more than its recent typical daily move is followed by a higher next close mainly when its 20-day volatility is above its 100-day volatility, that is, when volatility is expanding.
Consequence: Take the rebound long after large drops only while the coin's volatility is expanding, and refuse it in calm or contracting-volatility markets, where it only adds drawdown.
Why:
- F1: The book fails only on Calmar (0.748 against 0.75) because its drawdowns are deep: the worst drawdown per coin runs from -46% (LTC) to -85% (XRP), the worst 1% of book days lose 10.2% or more, and on bars with forecast ≥16 the book holds about 2.0x while the next-day return has a standard deviation of 5.9% and a 5% quantile of -8.2% (n=1280).
- F2: The edge sits almost entirely in volatile markets: active bars in the top tercile of 20-day volatility earn a mean next-day +0.75% and add +16.2 to the summed book return, while the low-volatility tercile earns -0.04% and subtracts -2.8 (n=2361 each). Among forecasts ≥8, low volatility gives -0.06% (t -0.33, n=568) and high volatility gives +1.91% (t 5.55, n=477, hit 65%).
- F3: Among forecasts ≥8, the rebound holds only when volatility is expanding: where 20-day volatility is high relative to 100-day volatility, the next day earns +1.75% (t 6.03, n=398, hit 66%), while contracting volatility gives -0.12% (t -0.57, n=455).
- F8: The losses gather in calm years and the trend does not separate them. Active-bar mean next-day return is -0.05% in 2018, -0.05% in 2022 and +0.03% in 2025, against +0.86% in 2020 and +0.80% in 2021. Bars above and below the 50-day average earn alike (+0.27%, t 3.34, n=2987, and +0.28%, t 3.98, n=5442).
