---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high
line: 7.b inconclusive
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day return, the larger its rise over the next 5 days, the more so the closer the coin's close stands to its highest close of the past 60 days.
Consequence: A trader leans long on monthly strength most when the coin is at or near its 2-month high, and trusts monthly weakness least when the coin has already fallen far from that high.
Why:
- F1: On the plan's 5-day grid the forecast's slope is on the predicted side but small and noisy (slope 0.000273, t 1.30, 3,419 cases). The same forecast is clear over shorter horizons (t 2.30 at 1 day on 17,380 cases, t 2.51 at 3 days on 5,723) and fades over longer ones (t 0.46 at 10 days, t −0.11 at 20 days), so the plan read the idea past the horizon where it shows.
- F3: The effect is mixed across years and coins, which keeps a pooled 5-day t short of the bar. By year the 5-day slopes run from t −2.07 in 2022 and −1.51 in 2018 to +1.79 in 2020 and +1.67 in 2025. By coin they range from t +1.44 (ETH) and +1.34 (XRP) to −0.77 (LTC), with no coin above t 2 on about 570 cases each.
- F5: The 30-day return alone already predicts the 5-day excess move (slope 0.0163, t 2.76, 2,555 cases). Its slope is positive only in the nearest-to-high third (t 1.38) and zero in the middle and far thirds (t −0.12, −0.08), so the nearness grading points the right way. The idea's per-case size is 0.087 of a usual move, with a total move of 1.13 % per case, 5.8 times the 0.19 % cost of a trade.
