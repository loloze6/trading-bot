---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins
line: 7.e profitable but not proven
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin that has fallen over the past 30 days while its 30-day net move stayed small against its 30-day high-low range, the choppier that fall (the smaller the net move relative to the range), the further the coin keeps falling, beyond its normal drift, over the next 5 days.
Consequence: A trader would refuse to buy a coin sliding down through a wide, choppy 30-day range and would short it for the next 5 days instead of fading it toward the middle of the range.
Why:
- F6: The strongest continuation in the data is on bars the book never trades: coins that fell over 30 days outside the trending regime fall a further 1.43 % beyond their drift over the next 5 days (t 5.48, 1,593 cases, strength 0.11) and 2.10 % over 10 days (t 4.17). After a 30-day fall, the further fall over 5 days is +0.97 %, +1.84 % (t 4.6), +0.77 % and +0.14 % (t 0.30) from the lowest to the highest quartile of net-move-to-range. It holds with w21, w6, w19 and w20 left out (+1.13 %, t 5.11, 2,293 cases) and in 6 of 8 years.
- F7: After a 30-day fall, the further fall grows with the size of the fall up to the middle-to-upper quintiles of |30-day return| (+0.83 %, +0.96 %, +1.96 % t 4.65, +1.69 % t 4.05), then turns into a rebound of -0.80 % (t -1.38) in the deepest quintile. The overall slope of the unusual move on the 30-day return among falls is -0.064 (t -3.88, 2,711 cases).
- F1: The book's whole gain comes from its long bars: summed bar gains are 31.15 on 11,162 long bars against -0.001 on 11,722 short bars, and closed trades give +34,583 % long against -6,140 % short; on the short side, a timing gain of +9.18 is cancelled by -9.18 from shorting a rising market.
