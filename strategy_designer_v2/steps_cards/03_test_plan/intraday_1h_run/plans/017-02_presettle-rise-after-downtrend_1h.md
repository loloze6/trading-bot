---
idea: 017-02_presettle-rise-after-downtrend
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin with a strong 3-day run down, in the 2 hours before a funding settlement (00:00, 08:00, 16:00 UTC) -> adapted: "strong" fall made graded by the size of the 72-bar fall; the clock window kept as a regime.
- Comparison: the stronger the 3-day fall, the larger the pre-settlement rise -> kept: the position grows with the size of the fall.
- Outcome: the return over the 2 hours before settlement is positive -> kept: a long position is held over the 2 one-hour bars before each settlement.
- Verdict transfer: yes: the test holds a long only in the pre-settlement hours, sized by the 3-day fall, so its 2-bar gains are exactly the idea's claim.
Forecast: A regime rule uses HoursToSettlementComponent. It selects bars whose coming bar starts 1 or 2 hours before a settlement, so the position is held through the bars stamped 06:00/07:00, 14:00/15:00 and 22:00/23:00 UTC. On all other bars the forecast is 0. On the selected bars, the forecast is built from the 72-bar price change (PriceEvolutionComponent, period 72 = 3 days): - It is standardised against its own past 72 values and negated. - It is clipped at 0. - So it is 0 after a 3-day rise and positive after a 3-day fall. - It grows linearly with the depth of the fall, up to the cap of 20. - It is long only.
Config: 017-02_presettle-rise-after-downtrend_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: Each case is one pre-settlement episode: a bar t where `regime` is trending and HoursToSettlement reads 2, with forecast > 0. - For each case, take the 2-bar return close[t+2]/close[t]-1 inside the window. - Subtract the coin's mean 2-bar return over all its windows (non-overlapping grid). - Regress this excess return on forecast[t], pooled over coins and windows. - The measure is the t of the slope.
- Supporting check: The mean excess 2-bar return over the same cases must be above 0 with t ≥ 2.
- Confirm: The idea is confirmed only if both hold: - the slope t is ≥ 2; - the supporting check passes (mean excess return t ≥ 2).
- Reject: The idea is rejected if either holds: - the slope t is ≤ -2; - the mean excess 2-bar return over the cases has t ≤ -2.
- Inconclusive: Any other result is inconclusive, including both t values between -2 and 2, or one ≥ 2 with the other between -2 and 2. At least 300 cases are needed pooled, with at least 20 per coin; with fewer, the result is inconclusive.
