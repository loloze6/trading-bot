---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours. The larger that hour's rise relative to its typical move, the larger the further rise.
Consequence: A trader would buy, rather than fade, a surging-volume hourly rise and hold it for about a day, where the move per case is several times a trade's cost.
Why:
- F5: The brief's own side is present at a horizon long enough to pay. On a non-overlapping grid, rises above 2 times the usual hourly move with volume over 3 times its 30-day average carry on upward:
- F6: Within high-volume rises the effect is concentrated, and partly graded. The rise size times log volume ratio, in quintiles, gives 24-hour total moves of +0.13, +0.02, +0.04, +0.28 and +0.44 % (top quintile t 1.81). By volume ratio, the effect sits at 3–5 times volume (+0.64 %, t 3.29); at 5–8 and over 8 times it is weaker (t 0.61 and 0.45).
- F7: The effect holds in both coins but not in every period. Over 24 hours it is BTC t 1.78 (+0.42 %) and ETH t 2.39 (+0.68 %). It is weak in windows w1–w8 (t 0.57) and stronger in w9–w16 (t 1.85) and w17–w24 (t 2.96).
- F3: Large rises on quiet volume do not fade. Rises above 2 times the 30-day mean absolute hourly move, with volume 0.67–1.5 times its 30-day average, return only +0.019 % in the short direction over 2 hours (t 0.67, n 2388) and -0.021 % over 24 hours (t -0.24). The grading is not monotone: rises of 2–3 times give -0.009 %, 3–4 times +0.103 %, 4–6 times +0.104 %, over 6 times -0.273 % (n 10).
- F2: The forecast's per-case move is far too small to pay. The unusual move per case is +0.03 % over 2 hours (strength 0.026), against a trade cost of 0.11 %: 0.3 times that cost, with a total move of only 0.2 times it.
- F1: The book loses on costs and on gross. Its mean daily return is -0.140 % against +0.127 % for holding, with a Sharpe of -2.34, over 2898 days. Its 16844 trades, all short and with a median length of 120 minutes, average -0.173 % before fees (t -15.6) and -0.273 % after. Fees cost 0.178 %/day on BTC and 0.138 %/day on ETH, against bar gains before costs of only 0.026 % and 0.005 %/day, at a turnover of 3.5 and 2.5 times the book per day.
