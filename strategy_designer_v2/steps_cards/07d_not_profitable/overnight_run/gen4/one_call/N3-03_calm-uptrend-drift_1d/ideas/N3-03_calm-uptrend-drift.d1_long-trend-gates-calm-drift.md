---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-03_calm-uptrend-drift
line: 7.d not profitable
backtest: N3-03_calm-uptrend-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A calm, positive 20-day rise in one coin is followed by further upward drift only while the coin's price also stands above its own long-term moving average; in a coin trading below that average, the same calm rise is followed by falling prices.
Consequence: A trader would take the calm-uptrend long only when the coin is above its long-term average and refuse it when the coin is below.
Why:
- F1: Fees are not why the book fails: the 2332 trades are all long, with a mean gain before fees of 1.00% (t 4.23 over 2332 trades) against a mean fee of 0.10%, so the failure is the Calmar of 0.36 against a 0.75 bar, which comes from deep drawdowns (mean per-window maximum drawdown −14% to −22% by coin, a worst book day of −38%, and a 1% quantile of invested-day book returns of −13%).
- F2: The book's losses sit in falling-market years: trades entered in 2018 lost a mean −3.3% before fees (n 220, win rate 33%), in 2022 −2.1% (n 322, win rate 29%) and in 2019 −0.8% (n 277), while 2020 and 2021 earned +3.8% (n 374) and +5.4% (n 325); the active bars' non-overlapping 5-bar forward return was likewise −2.5% in 2018 (n 74) and −2.3% in 2022 (n 114), against +3.8% and +4.0% in 2020 and 2021.
