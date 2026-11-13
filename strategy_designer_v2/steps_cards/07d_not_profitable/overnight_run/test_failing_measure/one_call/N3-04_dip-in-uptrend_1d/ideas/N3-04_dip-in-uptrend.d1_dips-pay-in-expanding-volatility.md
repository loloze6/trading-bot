---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-04_dip-in-uptrend
line: 7.d not profitable
backtest: N3-04_dip-in-uptrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day and 60-day returns are positive, a large one-day drop is followed by an above-average next-day return when the coin's 20-day volatility is above its 60-day volatility. When the 20-day volatility is below the 60-day volatility, the same drop is followed by a below-average next-day return.
Consequence: A trader buys dips only when short-term volatility is expanding, and refuses them in contracting-volatility uptrends, where large positions lose.
Why:
- F3: The large positions carry both the edge and the losses. Bars held at allocation ≥1 have a next-day excess return of +0.0069 (t 3.56, n 821), but their summed losses are -22.7 against -7.2 for all smaller positions (n 1949), and their P&L standard deviation is 0.102 against 0.019.
- F4: The edge depends on short-term volatility expanding.
- F6: The windows holding the drawdowns (w11–w17, w20–w23) give a held-bar excess of only +0.0012 (t 0.83, n 1403) with summed losses of -20.9. The other windows give +0.0032 (t 2.80, n 1367) with losses of -9.0.
