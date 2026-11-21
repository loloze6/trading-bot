---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: daily close near its 52-week high, far above its 52-week low, while the 30-day return is positive -> kept: the 365-bar range position of the close, gated by a regime on the sign of the 30-day return.
- Comparison: closer to the high and higher 30-day return versus farther below the high, with far-below meaning stand aside rather than short -> adapted: graded long size, with the lower half of the range set flat and never short.
- Outcome: higher return over the next 7 days -> kept: 7-bar forward return against the coin's own average.
- Verdict transfer: yes: the forecast grows with exactly the high, low and 30-day quantities the idea names, only inside its stated state, judged on 7-bar returns.
Forecast: The forecast is computed only on bars where the 30-day price change is above 0, the trending regime; on all other bars it is flat. Inside that regime it is the equal-weight mean of two parts: - Range position. Where the close sits in its 365-close range, from -20 at the low to +20 at the high. It is standardised over 365 bars and clipped at 0, so it grows as the close nears the 52-week high and moves away from the low, and is 0 in the lower half of the range. - Momentum. The 30-day percent price change, standardised over 60 bars and clipped at 0, so it grows with the 30-day return. The forecast is never negative. It is largest when the coin is at its 52-week high after a strong 30-day rise.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: Use non-overlapping 7-bar grid bars in each window where the forecast is above 0. On each, take the forecast/10 times the coin's 7-bar forward return minus that coin's mean 7-bar return over all windows. The measure is the t of the mean of that product.
- Supporting check: On the same bars, the top-half-forecast mean excess 7-bar return minus the bottom-half one is above 0.
- Confirm: The main t is 2 or more, with at least 100 cases, and the supporting check is above 0.
- Reject: The main t is -2 or less, with at least 100 cases.
- Inconclusive: Any t between -2 and 2, a confirming t whose check fails, or fewer than 100 non-overlapping cases with a forecast above 0.
