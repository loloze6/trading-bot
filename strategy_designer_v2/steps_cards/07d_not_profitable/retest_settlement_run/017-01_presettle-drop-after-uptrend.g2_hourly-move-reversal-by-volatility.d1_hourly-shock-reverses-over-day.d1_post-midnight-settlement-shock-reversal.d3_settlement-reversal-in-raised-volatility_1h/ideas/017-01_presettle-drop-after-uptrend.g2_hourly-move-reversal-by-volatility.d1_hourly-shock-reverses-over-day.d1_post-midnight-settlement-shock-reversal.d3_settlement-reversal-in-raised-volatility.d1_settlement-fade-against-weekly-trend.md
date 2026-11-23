---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-hour return in the first hour after the 00:00 UTC funding settlement relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way, and more so the higher its 24-hour volatility stands against its 30-day volatility, the more so the further that hour's move runs against the coin's 7-day return.
Consequence: A trader would fade the settlement-hour shock mainly when it pushed the coin against its week's trend, the crowded side's pre-payment exit, and would refuse the shorts that fight a falling week, which carry the book's losses for no gain.
Why:
- F1: The check failed on Calmar alone (0.57 against 0.75): the book made +25.2 % a year over 7.94 years, but its deepest fall was −44.3 %. That fall lasted 213 days across windows w5–w6, starting in 2023. The book lost 0.26 % a day in it while the coins' daily returns summed to +26 %, so this fall is the fade losing, not the coins falling.
- F6: The short side earned +0.17 % per case (t 3.13, 8,491 cases), below the cost of a trade; the long side earned +0.44 % (t 8.08, 8,532 cases). The shorts that lose are those against the coin's 7-day trend (a rise in the settlement hour while the 7-day return is negative): +0.07 % (t 0.86, 4,304 cases). Shorts with the 7-day trend earned +0.31 % (t 3.75, 3,681 cases).
- F7: Across all sides, fades that agree with the 7-day trend earned +0.39 % per case (t 7.12, 7,531 cases), against +0.20 % (t 3.51, 8,478) for fades against it. The 7-day trend alone, followed over the next 24 hours from the 00:00 bar, earns only +0.06 % to +0.10 % (t 0.99 to 1.52, about 5,400 cases per tercile). It is therefore not an effect of its own, but the brief's own reading of the crowded side: a settlement hour that moves against the recent trend recovers in the trend's direction.
