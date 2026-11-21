---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the more that fall was made of back-and-forth hourly swings (net 3-day move small relative to the sum of its absolute hourly moves), the more the coin keeps falling over the next 3 days.
Consequence: Refuse dip-buys after choppy, whipsawing 3-day declines, and lean short in proportion to how choppy the decline was.
Why:
- F3: Falls built from choppy, back-and-forth hours keep falling rather than reversing: among 3-day falls, the lowest-efficiency tercile is followed by −0.0091 excess 72-bar return (t −3.38, 890 cases), while the middle and grind terciles are flat (+0.0010 and +0.0001).
- F4: The tested rebound lives only in the top fifth of the forecast: active cases in the top forecast quintile earn +0.0112 excess 72-bar return (t 3.30, 553 cases), while the 2nd and 3rd quintiles lose −0.0065 (t −1.79) and −0.0082 (t −2.14), and active cases overall return −0.0015 against +0.0014 for inactive ones.
