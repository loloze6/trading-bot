---
idea: 012-01_liquidation-flush-rebound
brief: 012_liquidation-flush-partial-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4a01343a8148
---
Fidelity:
- Situation: a bar closes sharply lower on volume far above its 30-day average, with a long lower wick -> adapted: "sharply" and "far above" become a graded fall-times-volume-ratio size, with the wick graded beside it.
- Comparison: volume against its own 30-day average -> kept
- Outcome: price rises over the next 3 days, more after bigger bursts and longer wicks -> kept
- Verdict transfer: yes: the forecast is long, it grows with fall, volume burst and wick, and it is judged on the 3-day rise against holding.
Forecast: The forecast is active only on bars where all three hold: - the bar fell (a negative 1-bar return in 20-bar usual moves), - volume is above its 30-bar mean, - there is a lower wick. On those bars it is the equal-weight mean of two parts. Each part is standardised over 60 bars and passed through signed_power with exponent 3 (the strongest dead zone): - the flush: the fall in usual moves times the volume ratio to its 30-bar mean, negated so that falls read positive, then clipped at 0; - the wick: the lower wick as a share of the bar's range. The forecast is never negative. It is near zero for mild falls, light volume bursts or short wicks. It grows steeply, up to the cap of 20, as the fall, the burst and the wick become extreme. On every other bar it is 0 (flat).
Config: 012-01_liquidation-flush-rebound_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Sample a non-overlapping 3-bar grid in each window. On grid bars with forecast >= 2, take the coin's 3-bar return minus that coin's mean 3-bar return over all windows (excess over holding), before costs. Test its mean with the t of the mean.
- Supporting check: On those same bars, the forecast-weighted mean excess return must exceed the unweighted mean excess return (a larger flush leads to a larger rise).
- Confirm: The mean excess return is > 0 with t >= 2, and the supporting check passes.
- Reject: The mean excess return is < 0 with t <= -2 (continued decline after flushes, beyond holding).
- Inconclusive: Any t between -2 and 2, or a confirming t with the supporting check failing. Fewer than 30 qualifying grid bars across all coins and windows is also inconclusive.
