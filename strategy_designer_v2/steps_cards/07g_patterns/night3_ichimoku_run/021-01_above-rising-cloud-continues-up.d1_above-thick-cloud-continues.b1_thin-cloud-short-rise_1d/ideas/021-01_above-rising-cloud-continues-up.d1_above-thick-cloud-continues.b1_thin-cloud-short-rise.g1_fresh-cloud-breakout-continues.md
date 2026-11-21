---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise
line: 7.g patterns
backtest: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its Ichimoku cloud (9/26/52), its return over the next 5 days is larger the fewer days have passed since its close first rose above the cloud.
Consequence: A trader would favour coins that have just broken above their cloud and give less weight to coins that have stood above it for weeks.
Why:
- F1: Among bars where a coin closes above its Ichimoku cloud, the fewer days since it crossed above, the larger its next 5-day return above its normal drift. The slope on the log of days since crossing is -0.0215 (t -3.65, 490 non-overlapping cases), and the pattern holds in both halves of the windows (w1-w12: t -3.11, n 282; w13-w24: t -2.07, n 208).
- F2: By terciles of days above the cloud, the excess 5-day return is +3.53 % for 1 to 9 days (total move +4.11 %, about 21 times the 0.19 % cost of a round trip), +0.57 % for 9 to 19 days and -1.23 % for 19 to 39 days (163 to 164 cases each).
- F3: The freshness effect survives controls: with cloud width, distance above the cloud top and the 20-day return in the same regression, log days since crossing keeps beta -0.0222 (t -3.16, n 490), while width (t -0.15), distance (t 0.14) and the 20-day return (t 0.42) carry nothing; freshness and width are nearly uncorrelated (-0.08).
- F5: The coins mostly agree on freshness: 5 of 6 coins have a negative slope (XRP t -2.86, LTC -1.70, ETH -1.63, ZEC -1.38, XMR -1.04), and BTC alone is flat (+0.0026, t 0.32, n 87).
- F6: The strategy's own record shows the same thing: active bars in their first 1 to 5 bars of the regime are followed by +2.76 % excess over 5 days (t 2.65, n 213), against -0.95 % to +0.29 % for later quartiles. The book, which holds through the whole stretch above the cloud, earns a mean daily return of 0.00046, just under the 0.0005 required.
