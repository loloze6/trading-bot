---
idea: 034-02_rising-break-swings-continues
brief: 034_rising-market-nearness-to-high-drift
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: f090b5ff5633
---
Fidelity:
- Situation: a daily close above the prior 20-day high, in a rising market -> kept: a regime holds only while the close is above the highest close of the prior 20 bars; code adds the rising profile.
- Comparison: how many of its own daily swings over the last 20 days the close stands above that high -> kept: distance above the prior 20-bar closing high over the 20-bar standard deviation of daily returns.
- Outcome: the price rises over the next 5 days, more the larger that distance -> kept: the position is graded by the distance and held 5 bars.
- Verdict transfer: yes: the book is long only on breakout bars, sized by the distance in swings, so its 5-day gains test the idea directly.
Forecast: One indicator, `VolatilityScaledDistanceFromHighComponent` (period 20, vol_period 20). It is (close − highest close of the prior 20 bars) / that high / the 20-day standard deviation of daily returns, so it counts the distance in usual daily moves. The regime detector selects `trending` only while this value is above 0, which is a close above the prior 20-day high. On every other bar the regime is `unknown` and the book is flat. Inside the regime the forecast is the same value standardised against its own last 60 values (window 60, min_periods 20). It is positive and starts from 0 at the high. It grows steadily the more swings the close stands above the high, capped at 20. It is never negative. The code adds the rising-profile vetoes.
Config: 034-02_rising-break-swings-continues_1d_config.json
Profile: rising (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: Take each case, a bet of the forecast on the non-overlapping 5-bar grid of each window. Measure the coin's 5-bar return from the case's close minus the coin's mean 5-bar return over all windows. Average these excess returns weighted by the forecast, and compute its t with the cases of one day taken together.
- Supporting check: Across the cases, the Spearman correlation between the forecast and the 5-bar excess return is above 0.
- Confirm: The forecast-weighted mean excess 5-bar return is above 0 with t ≥ 2, and the supporting correlation is above 0.
- Reject: The forecast-weighted mean excess 5-bar return is below 0 with t ≤ −2.
- Inconclusive: The result is inconclusive when t lies between −2 and 2. It is also inconclusive when t ≥ 2 but the correlation is at or below 0. At least 30 cases on at least 30 distinct days are needed; with fewer, the result is inconclusive.
