---
idea: 002-06_down-cross-to-reverse-cross-loss
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: from the short MA's cross below the long MA until it crosses back above -> adapted: "after the down cross, until the up cross" becomes "while SMA50 is below SMA200", sized by the size of the gap.
- Comparison: random spans of the same length -> adapted: compared with the coin's own average move over the same bars, as a position held at random times would earn it.
- Outcome: price falls over the span, more often and further -> kept: the short position's return, summed over the span, is the span's fall.
- Verdict transfer: yes: a short held only while the short SMA is below the long SMA, judged against the coin's own drift, earns exactly when such spans fall more often and further than random spans.
Forecast: The percent spread of SMA50 over SMA200 on daily closes (the death-cross and golden-cross convention). It is standardised against its own past 200 values, then clipped at a maximum of 0. The forecast is negative (short) only while SMA50 is below SMA200. It starts at 0 at the cross, deepens as the gap widens, and is capped at -20. It is zero while SMA50 is above SMA200 and never goes long.
Config: 002-06_down-cross-to-reverse-cross-loss_1d_config.json
Criterion:
- Horizon: 1 bar (next-day close-to-close return; summed over a span, this gives the span's return).
- Main measure: Per bar, the excess return is position × (next-bar coin return − the coin's mean daily return over the same window). This removes the market's own drift that a random-timed short of the same size would face. The excess returns are pooled across coins and windows, and the mean is tested with a Newey-West t-statistic (lag 10), so autocorrelated bars are not counted as independent.
- Supporting check: For each completed down-cross span (SMA50 < SMA200), compare its price return with the median return of all same-length spans of that coin. The share of down-cross spans falling below that median should exceed 50%.
- Confirm: The mean excess return is above 0 with t ≥ 2, and the supporting share is above 50%.
- Reject: The mean excess return is below 0 with t ≤ -2, which means prices rise more than average after down crosses (reversal).
- Inconclusive: Any t between -2 and 2, or a confirming t with a supporting share of 50% or less. A verdict also needs at least 500 bars with a non-zero position and at least 10 distinct down-cross spans across all coins; with fewer, the result is inconclusive.
