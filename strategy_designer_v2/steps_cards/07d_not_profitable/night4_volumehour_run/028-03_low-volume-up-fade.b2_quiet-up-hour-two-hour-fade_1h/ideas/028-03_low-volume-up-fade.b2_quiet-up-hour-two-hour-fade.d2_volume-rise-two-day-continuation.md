---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next two days. The larger that hour's rise times its volume surge, the larger the further rise.
Consequence: A trader would keep a long opened on a surging-volume rise for two days, trading rarely enough that fees stay small against the move.
Why:
- F5: The brief's own side is present at a horizon long enough to pay. On a non-overlapping grid, rises above 2 times the usual hourly move with volume over 3 times its 30-day average carry on upward:
- F6: Within high-volume rises the effect is concentrated, and partly graded. The rise size times log volume ratio, in quintiles, gives 24-hour total moves of +0.13, +0.02, +0.04, +0.28 and +0.44 % (top quintile t 1.81). By volume ratio, the effect sits at 3–5 times volume (+0.64 %, t 3.29); at 5–8 and over 8 times it is weaker (t 0.61 and 0.45).
- F4: Most of the book's short exposure sits on ordinary hours, not on large rises. Only 14 % of bars are short, but the mean scaled rise on short bars is 1.04. 10572 of the 18268 short bars have a rise below 1 times the usual hourly move, and their 2-hour moves of +0.027 % and +0.050 % are too small to cover the fees.
- F1: The book loses on costs and on gross. Its mean daily return is -0.140 % against +0.127 % for holding, with a Sharpe of -2.34, over 2898 days. Its 16844 trades, all short and with a median length of 120 minutes, average -0.173 % before fees (t -15.6) and -0.273 % after. Fees cost 0.178 %/day on BTC and 0.138 %/day on ETH, against bar gains before costs of only 0.026 % and 0.005 %/day, at a turnover of 3.5 and 2.5 times the book per day.
