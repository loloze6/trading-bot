---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day rise relative to its usual 3-day move, the further it keeps rising over the next 3 days.
Consequence: A trader rides a coin's strongest multi-day rises instead of fading them, with a follow-through several times the cost of a trade.
Why:
- F2: The book loses before costs, and it loses on the short side. Its gross gain per bar is +0.08 bps overall: -0.35 bps per bar on its 215874 short bars and +0.55 bps per bar on its 199974 long bars. The mean gross result per trade is negative on 5 of 6 coins (-0.14 % to -0.38 %).
- F3: The reversal exists only after falls. On non-overlapping 24-hour grid cases, drift-adjusted, the next 24 hours after the 10 % deepest 24-hour falls (in units of the coin's usual move) average +0.71 % (t 4.69, 1639 cases). After the 10 % largest rises they average -0.20 % (t -1.62), a continuation the book is short against. Over 72 hours those top-decile rises go on to +0.72 % (t 3.14).
- F7: Rises in the high-volatility state continue rather than reverse. In the top rise decile with high volatility, the forecast-signed 24-hour move is -0.85 % (t -2.51, 377 cases), so the coin kept rising. Over longer runs, the top decile of 3-day rises is followed by +1.46 % over 72 hours (t 5.99), and the top decile of 7-day rises by +2.06 % over 168 hours (t 4.98). That is 7 to 11 times the cost.
