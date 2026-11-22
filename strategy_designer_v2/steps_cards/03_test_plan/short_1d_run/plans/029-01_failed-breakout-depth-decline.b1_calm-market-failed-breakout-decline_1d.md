---
idea: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 02605c0f0d60
---
Fidelity:
- Situation: a daily close above the prior 20-day high, then a close back below that old high within 3 days -> adapted: on/off made graded as the close's depth below the old high (`FailedBreakoutDepthComponent`, period 20, fail_window 3, exclude_current 1).
- Comparison: only while 20-day volatility of daily returns is low, and the lower it is, the larger the fall -> replaced: the "only while low" gate fits a regime, but the catalogue has nothing that scales the depth by the inverse of volatility.
- Outcome: the coin falls over the next 5 days -> kept: a short held 5 bars.
- Verdict transfer: no: without position size growing as volatility falls, the idea's "lower volatility, larger fall" claim is not tested.
Reason: The idea needs the failed-breakout depth multiplied by the lowness of 20-day volatility, but a forecast can only add its components. No catalogue component is that product. An added volatility term would give a position on bars with no failed breakout, and it could push the forecast long, breaking the brief's short-only rule. The vol-normalize transform uses the 24-bar standard deviation of price levels times the close squared, not the 20-day volatility of returns.
