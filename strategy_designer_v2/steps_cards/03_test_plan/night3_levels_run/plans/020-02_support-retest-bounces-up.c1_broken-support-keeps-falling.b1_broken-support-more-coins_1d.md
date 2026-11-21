---
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: daily close just below past-90-day turning-up lows -> adapted: graded as the count of swing lows clustered at the nearest level above the close, weighted by how close the close is to that level.
- Comparison: the more such lows just above the close, the larger the fall -> kept: the forecast's size grows with that count and that nearness.
- Outcome: price falls over the next 5 days -> kept: short, held 5 daily bars.
- Verdict transfer: yes: the forecast is short in proportion to the idea's own situation, and its gains over 5 bars decide the claim either way.
Forecast: One component, `SwingHighClusterCountComponent`, set to swing lows (`pivot` "low") at the level above the close (`level` "above"). It uses a 90-bar window, 2 bars on each side of a swing, a 2 % band and the "proximity" form. Its value is the number of past swing lows within 2 % of the lowest swing low at or above today's close, times 1/(1+D), D being the close's percent distance below that level. It is 0 when no swing low lies above the close. It grows with more touches and with a close nearer under the level. It is standardised against its own past 90 values and then negated. The forecast is therefore 0 or negative (short), and larger in size the more turning lows sit just above the close.
Config: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The forecast is read on the non-overlapping 5-bar grid of each window. Each grid bar's 5-bar return is taken minus the coin's mean 5-bar return over all windows. The measure is the pooled regression slope of that excess return on the forecast, with its t, before costs.
- Supporting check: On grid bars with forecast below 0, the mean excess 5-bar return is below 0.
- Confirm: The slope's t is 2 or more (a more negative forecast is followed by a more negative excess return), and the supporting check passes.
- Reject: The slope's t is -2 or less (a more negative forecast is followed by a higher excess return).
- Inconclusive: A slope t between -2 and 2, or a confirming t whose supporting check fails. The test also needs at least 200 grid bars with forecast below 0 across all coins and windows; fewer than that is inconclusive.
