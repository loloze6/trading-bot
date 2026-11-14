---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the RSI reaches a high extreme on the coin -> adapted: the 14-bar RSI's distance above 50 is used as a graded measure. It is squared through `signed_power` so that high extremes get large positions and readings near 50 get nearly none. This replaces an on/off "extreme" threshold.
- Comparison: behaviour after neutral RSI readings -> kept: in the criterion, forward returns after the largest positions (high-extreme RSI) are compared with forward returns after bars whose recorded RSI is neutral (40 to 60).
- Outcome: price keeps rising over the following bars -> adapted: the long position is held for as long as RSI stays high and shrinks as RSI falls back. The outcome is read as the forward 5-bar return after each bar, so no fixed holding period is used in the config.
- Verdict transfer: yes: the test asks whether upward moves after high-RSI bars are larger than after neutral bars, before costs and net of the coin's own drift, which is exactly the idea's claim.
Forecast: The forecast starts from `RSIPullbackComponent` with period 14 (the convention), whose raw value is (50 − RSI) × 0.4. - It is standardised against its own previous 60 values (window 60, min_periods 20), which puts its average absolute value near 10. - It is then negated, so it is positive when RSI is above 50. - It is passed through `signed_power` with exponent 2 and pivot 10. Moderate readings shrink smoothly towards 0 (5 becomes 2.5) and strong readings grow (15 becomes 22.5). - Finally it is clipped at 0 from below. The forecast is 0 whenever RSI ≤ 50. It is positive and long when RSI is above 50. It grows roughly with the square of how far RSI sits above 50 relative to its recent typical distance. The final clip on the combined forecast caps it at +20 (200% long). It is never negative.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The forward 5-bar close-to-close return after "extreme" bars minus the forward 5-bar return after "neutral" bars. - Extreme bars are the top quintile of the forecast among bars where it is positive. - Neutral bars are those whose recorded RSI is between 40 and 60. RSI is recovered from the recorded raw value as 50 − raw / 0.4. - Results are pooled across BTC, ETH, BNB and all 6 windows. - Overlapping returns are counted once: within each coin and window, only the first qualifying bar of each non-overlapping 5-bar block is kept. - Because both groups are measured on the same coin and the same windows, the coin's own drift (the buy-and-hold return) cancels out of the difference.
- Supporting check: The portfolio's daily return minus (that day's allocation × the coin's daily return under buy-and-hold) should not apply, as written; the check is instead the strategy's mean daily return per unit of allocation minus the coin's mean daily return. It must be positive for the idea to hold.
- Confirm: Both conditions must hold: - The extreme-minus-neutral difference in mean forward 5-bar return is at least +1.0 percentage point, with a t-statistic of at least 2.0 on non-overlapping cases. - The difference is positive in at least 2 of the 3 coins.
- Reject: Either of these rejects the idea: - The pooled difference is 0 or below, with a t-statistic of −1.0 or below. - The pooled difference is negative in at least 2 of the 3 coins, which would mean high RSI is followed by weaker moves (no continuation, or reversal).
- Inconclusive: A positive difference below +1.0 percentage point, or a t-statistic between −1.0 and 2.0, or results where the coins disagree in direction, is inconclusive. A pooled count of fewer than 30 non-overlapping extreme cases or fewer than 30 non-overlapping neutral cases is also inconclusive, whatever the result.
