---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin that has fallen over the past 30 days, the larger its 30-day net fall is against its 30-day high-low range (the steeper and cleaner the fall), the more it rises back, relative to its normal drift, over the next 5 days.
Consequence: A trader would refuse to short a coin after a clean, steep 30-day slide, and would keep shorts for choppy declines only.
Why:
- F5: The tested short side only works in the middle of the falls. Choppy falls (signed ratio −0.35 to 0) are followed by −1.84 % (t −4.25) and −1.16 % (t −2.58) over 5 days. The cleanest falls (ratio below −0.656) are followed by +0.13 % (t 0.25), so steep, clean declines stop continuing.
- F1: Measured over all coins on the 5-day grid, the 30-day net move divided by the 30-day high-low range, kept with its sign, grades the next 5 days' unusual move in the trend's direction (slope of strength on the signed ratio 0.113, t 4.35, 5434 cases); on rising coins alone the slope is 0.227 (t 2.95, 2723 cases).
