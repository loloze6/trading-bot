---
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d2_tight-cluster-of-broken-lows
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: daily close just below several past-90-day turning-up lows, within a few percent above it -> adapted: graded as the number of swing lows bunched at the nearest low above the close, times that low's nearness.
- Comparison: several bunched, near lows against a lone or far-off low -> kept: the count and the nearness set the size, so a lone, far-off low gives a forecast near zero.
- Outcome: the price falls over the next 5 days, more when there are more and nearer lows -> kept: a short held 5 bars, larger as the count and nearness grow.
- Verdict transfer: yes: the graded short is the idea's own count-times-nearness relation at its own 5-day horizon.
Forecast: One component, `SwingHighClusterCountComponent`, with settings period 90, side 2, pivot "low", level "above", band 2 percent, form "proximity", power 1. It finds the nearest swing low at or above the close and counts the swing lows within 2 percent of it. It multiplies that count by 1/(1+D), where D is the close's percent distance below that low. It is zero when no past swing low sits above the close. The component is standardised over 90 bars and negated. The forecast is therefore never positive: it is zero with no low above, small for one far low, and a larger short as the lows bunch and the close nears them.
Config: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d2_tight-cluster-of-broken-lows_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use a non-overlapping 5-bar grid in each window, pooled over coins. On it, take each bar's 5-bar forward return minus the coin's mean 5-bar return over all windows. Regress that excess return on the short size, -forecast / 10.
- Supporting check: The 5-bar excess return over the cases in the largest third of short sizes has a mean below zero.
- Confirm: The slope is negative with t <= -2, and the supporting check passes.
- Reject: The slope is positive with t >= +2.
- Inconclusive: Any t between -2 and +2 is inconclusive. A negative slope with the largest-third mean at or above zero is also inconclusive. So is a test with fewer than 100 non-zero-forecast grid cases in total, or fewer than 30 in the largest third.
