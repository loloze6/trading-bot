---
idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 10d8cbead801
---
Fidelity:
- Situation: 30-day net move large against its 30-day high-low range, close below that range's middle, with a 10-day fall -> kept: a regime rule (net move / range >= 0.5, close below the range midpoint), and the forecast grows with the 10-day fall.
- Comparison: larger falls against smaller falls -> kept: the position grows with the size of the 10-day fall.
- Outcome: price rises over the next 5 days, more after larger falls -> kept: a long held 5 bars, sized by the fall.
- Verdict transfer: yes: the regime is the idea's condition, the graded size is its fall, and the 5-day rise is what the forecast earns.
Forecast: The regime detector selects the active regime when two things hold. First, the 30-bar net move over the 30-bar high-low range (NetMoveToRange, period 30, high_low) is at least 0.5. Second, the close sits below the midpoint of the 30-bar high-low range, read as the Ichimoku position with all spans 30, displacement 0, edge top and base close, below 0. On those bars the forecast is the 10-bar price change (PriceEvolution, period 10), standardised over 60 bars, negated and clipped at 0. It is positive and grows with the depth of the 10-day fall, and it is 0 when the coin rose over those 10 days. On every other bar the forecast is 0 (flat). It never goes short.
Config: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: On the non-overlapping 5-bar grid of each window, take the cells where the forecast is above 0. Regress each cell's 5-bar return, minus the coin's mean 5-bar return over all windows, on the forecast. Pool all coins and report the slope's t.
- Supporting check: The mean of the same excess 5-bar returns over those cells is above 0.
- Confirm: The slope's t is 2 or more and the mean excess return is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and 2, or a confirming t with a mean excess return of 0 or below. It is also inconclusive if there are fewer than 30 grid cells with a forecast above 0, pooled over coins.
