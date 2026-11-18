---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's close sits above the highest high of its prior 20 days, as a share of that high, the further its price rises over the next 10 days, only while the coin's 60-day return is positive, and the higher that 60-day return, the larger the rise.
Consequence: A trader would buy closes above the 20-day high only in coins already up over 60 days and keep the position for the 10 days, rather than selling when the close slips back under the high.
Why:
- F2: The plan dropped the 10-day hold, so the book sells as soon as the close slips back under the prior high. 384 of 519 trades last 1.5 days or less and lose -1.67% net each, while the 34 trades held 3.5 to 15 days earn +14.5% to +45.6% net. The median trade loses -0.60% and 44% of trades win.
- F3: The 10-day move after a breakout exists but is concentrated on the breakout bar itself. On the non-overlapping grid, a close above the prior 20-day high is followed by +7.4% excess 10-day return (t 2.29, n 51). Grid bars 1 to 10 days after a breakout show only +0.4% (t 0.43, n 209).
- F5: The breakout's continuation lives in coins already rising over 60 days. In that group, breakouts are followed by +9.0% excess 10-day return (t 2.50, n 42), against -0.4% (t -0.06, n 9) when the 60-day return is negative.
