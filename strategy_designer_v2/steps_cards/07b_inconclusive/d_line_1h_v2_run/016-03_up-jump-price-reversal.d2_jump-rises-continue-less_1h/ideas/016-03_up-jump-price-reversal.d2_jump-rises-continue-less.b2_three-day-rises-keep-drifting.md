---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less
line: 7.b inconclusive
backtest: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger that 3-day rise, the larger the coin's further rise over the next 3 days.
Consequence: A trader would hold long exposure after a coin's 3-day rises, sized up with the size of the rise, rather than fading them.
Why:
- F6: What carries the forward return is the rise itself, not how it was built. Grid bars after any 72-hour rise have a mean 72-hour forward return of 0.0125, against 0.0024 over 4,706 bars without a rise, while the grind-versus-jump split moves it by only 0.0047.
- F4: Part of the measure is the move's size, but controlling for size does not change the result. grind_residual has a Spearman correlation of 0.44 with the past 72-hour rise, and quintile mean past rises go from 0.077 to 0.168. With the past rise in the regression, grind_residual's coefficient is 0.0149 (t 0.82, n 967) and the past rise adds nothing (t 0.12). Within past-size terciles the difference is −0.0015 (t −0.19), +0.0112 (t 1.16) and −0.0016 (t −0.13).
