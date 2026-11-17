---
brief: 013_anchoring-to-recent-high
source-idea: 013-02_follow-through-stronger-near-high
line: 7.d not profitable
backtest: 013-02_follow-through-stronger-near-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's past 30-day rise carries on into the next 30 days more strongly the closer the coin closes to its 52-week high, and the follow-through weakens as the coin's 30-day volatility grows relative to its 90-day volatility.
Consequence: A trader would cut long exposure near the high when short-term volatility is expanding, because the follow-through there turns into losses.
Why:
- F5: The long gain is concentrated near the 52-week high: longs in the shallowest depth quintile earn +0.00274 per bar (n=2166), falling steadily to +0.00077, +0.00023, +0.00011 and -0.00008 (n=650) in the deepest quintile.
- F8: Longs lose when recent volatility is rising. In the top quartile of 30-day over 90-day volatility, long bars average -0.00079 per bar (n=724), against +0.0016 per bar (n=491) in the lowest quartile.
