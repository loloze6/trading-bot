---
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close above its 200-day average, and the close high in its 20-day close range -> adapted: the 200-day condition is a regime, and range position is graded.
- Comparison: an already extended 30-day return, where a larger return means a smaller rise -> adapted: the "extended" threshold becomes a graded cubic dead zone on the 30-day return, subtracted.
- Outcome: a larger rise over the next 10 days -> kept: 10 daily bars, judged against the coin's average.
- Verdict transfer: yes: the forecast scales with range position, is cut by an extended 30-day run, and is active only above the 200-day average, so the 10-bar outcome bears directly on the idea.
Forecast: The forecast is active only on bars where the close is at or above its 200-day SMA (regime `trending`). On other bars it is flat. - First part: the close's position in its 20-bar close range (Donchian, 20), standardised over 60 bars. It is positive in the upper half of the range and negative in the lower half. - Second part: the 30-bar return, standardised over 60 bars, then cubed with a pivot of 10 (the strongest graded dead zone), then clipped at 0. It stays near 0 unless the 30-day run is unusually large, and then it grows fast. - Combination: with weights 1 and -0.5, the forecast is 2 x range position minus the extension penalty, clipped to ±20. - Sign and size: it is larger the nearer the close is to its 20-day high, and it is cut back as the 30-day run becomes extended.
Config: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: On regime-`trending` bars, take a non-overlapping 10-bar grid in each window and pool all coins. Regress the forward 10-bar return minus that coin's mean 10-bar return over all windows on the bar's forecast, and report the slope's t.
- Supporting check: Over all windows, the book's timing gain (its mean daily return minus the gain from the market's own rise) is above 0, before costs.
- Confirm: The slope's t is 2 or more with at least 100 independent cases, and the timing gain is above 0.
- Reject: The slope's t is -2 or less with at least 100 independent cases.
- Inconclusive: A t between -2 and 2, or a t of 2 or more with a timing gain at or below 0, is inconclusive. Fewer than 100 independent cases is also inconclusive.
