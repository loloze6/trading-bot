---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: The forecast is the 14-bar Wilder RSI turned into a momentum reading, long only, with extremes emphasised. Start with RSI − 50, which is RSIPullbackComponent at period 14, negated. Divide it by the mean absolute value of its own previous 60 daily values and multiply by 10, capped at ±20. Clip it at 0, so it is zero whenever RSI ≤ 50; the brief does not limit the side, but this idea is only about high readings. Then apply signed_power with exponent 2 and pivot 10, so the position grows with the square of the standardised strength. Near-neutral readings just above 50 give almost no position, typical readings give about 10, and high extremes (RSI near 70 or above) give a large long, up to the +20 cap.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Confirm: Pool all three coins and all windows. Compare the coin's 5-bar forward close-to-close return after high-extreme bars (recorded RSI ≥ 70, raw component value ≤ −8) with the same return after neutral bars (RSI 40–60). Count only non-overlapping 5-bar blocks, so each block enters once. The idea is confirmed if the extreme mean exceeds the neutral mean by at least 1.0 percentage point, with t ≥ 2, from at least 30 non-overlapping extreme observations. Supporting check: the difference is positive in at least 2 of the 3 coins. All of this is before costs; comparing with neutral bars removes the market's own drift.
Reject: The idea is rejected if the pooled difference (extreme minus neutral 5-bar forward return) is zero or negative, with at least 30 non-overlapping extreme observations. A difference at t ≤ −2 would point to reversal rather than continuation.
Inconclusive: The test is inconclusive if the difference is positive but below 1.0 percentage point or has t < 2. It is also inconclusive if fewer than 30 non-overlapping extreme observations exist, or if the pooled result is positive but only 1 of the 3 coins agrees.
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, with a long sized by the squared distance". The config therefore holds small longs at moderate readings and its largest longs while RSI stays extreme, not for a set number of bars after the extreme. Low extremes are not traded. The extreme is also measured relative to the RSI's previous 60 daily values, not against a fixed level of 70.
