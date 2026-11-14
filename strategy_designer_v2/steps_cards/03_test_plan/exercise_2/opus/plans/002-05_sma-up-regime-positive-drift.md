---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Config: 002-05_sma-up-regime-positive-drift_config.json
Confirm: Use a 1-bar horizon (next-day close-to-close return), before costs. The idea is confirmed if, on bars where the forecast is above 0 (SMA50 above SMA200, the stretch from an upward cross to the next downward cross), BTC's mean next-day return and share of up days both exceed BTC's unconditional values. That excess must be significant against random stretches of the same lengths: p < 0.05 in a block-bootstrap or circular-shift test of the in-stretch bars. A corollary is that the portfolio's return per unit of average exposure beats buy-and-hold.
Reject: The idea is rejected if the mean next-day return and up-day share on in-stretch bars are equal to or below BTC's unconditional values. It is also rejected if the in-stretch mean return is significantly negative relative to random stretches, which would point to crosses marking exhaustion.
Inconclusive: The result is inconclusive if in-stretch returns exceed the unconditional ones but not significantly (p ≥ 0.05). It is also inconclusive if there are too few complete up-cross stretches (fewer than about 5 over the period) to separate the result from one or two dominant bull runs.
Deviation: The on/off "between an up-cross and the next down-cross" state becomes a graded long position equal to the standardised SMA50−SMA200 spread. The position is still nonzero exactly during the stretch, but it scales with the gap between the averages instead of being constant, so returns are tested as exposure-weighted. The test is long-only (down-cross stretches are flat), uses the conventional 50/200 periods because the source gives none, and leaves out the "price crosses the long average" variant from the brief.
