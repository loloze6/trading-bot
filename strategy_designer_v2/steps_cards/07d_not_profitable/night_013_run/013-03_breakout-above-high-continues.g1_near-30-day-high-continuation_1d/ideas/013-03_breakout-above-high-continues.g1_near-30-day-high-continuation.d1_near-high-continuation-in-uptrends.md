---
brief: 013_anchoring-to-recent-high
source-idea: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation
line: 7.d not profitable
backtest: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close is to the highest high of its prior 30 days, the larger the coin's return over the next 10 days, and the effect keeps growing for closes that clear that high, only while the coin's own 60-day return is positive.
Consequence: A trader would lean long on a coin pressing against or through its 30-day high for about 10 days when the coin has risen over the past 60 days, and would refuse that lean when it has fallen over the past 60 days.
Why:
- F2: Longs carry the whole gain and shorts lose it back. Summed daily gains are +2.13 on 4,273 long bars (mean 0.000499) and −0.63 on 4,035 short bars (mean −0.000157).
- F4: The effect holds only while the coin's 60-day return is positive. There, the slope of excess 10-day return on distance has t = 3.08 (423 independent cases), and the top tercile shows +0.030 excess against −0.029 for the bottom. When the 60-day return is negative, the slope has t = −1.30 (404 cases), and the near-high tercile shows −0.013 excess.
- F5: The book's losses concentrate where it bets against a rising coin. Shorts while the 60-day return is positive lose −0.545 summed (mean −0.000274 on 1,993 bars), while longs in that state earn +1.92 (mean 0.000843). Longs while the 60-day return is negative earn only +0.22.
