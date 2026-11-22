---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a coin's 1-day fall that is large relative to its usual 1-day move over the past 30 days, the 3-day rebound that follows is larger the higher the coin's 5-day volatility against its 30-day volatility.
Consequence: A trader leans harder into the rebound after a sharp drop when the drop comes in a burst of volatility, and stays light when it comes in a quiet market.
Why:
- F3: Among the largest 1-day falls (lowest decile), the 3-day rebound is larger when 5-day volatility is high against its 30-day average. The upper volatility half earns +1.99 % (t 3.60, 234 cases, strength 0.23) and the lower half +0.86 % (t 1.80, 234 cases).
- F1: The coin's 1-day move, measured against its usual 1-day move over the past 30 days, predicts the next 3 days far better than the tested forecast does. In the top quintile of the move's size, falls are followed by a 3-day excess return of +1.27 % (t 3.50, 490 independent cases, strength 0.145), and the response is graded across the whole down side (Spearman 0.113, p 1.9e-8, n 2450). The tested forecast's active cases earn +0.24 % (t 0.73, 638 cases), and step 5 found -0.01 % per case.
