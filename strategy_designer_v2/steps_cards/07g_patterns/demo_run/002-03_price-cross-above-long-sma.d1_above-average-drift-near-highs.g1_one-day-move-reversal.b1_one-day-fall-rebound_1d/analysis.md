---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b1_one-day-fall-rebound_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b1_one-day-fall-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3910 USD
---
## Findings
- **F1:** The tested rebound after a fall only appears when the coin's volatility is high. Among down days, the mean of (fall in sigma × next-day excess return) in the top tercile of 20-day volatility (ranked against the coin's past 120 days) was 0.0050 (t 2.22, n 752) in windows w1–w12 and 0.0089 (t 2.89, n 910) in w13–w24. The low tercile was negative in both halves: −0.0011 (t −0.68) and −0.0020 (t −1.22).
- **F2:** The grading by fall size sharpens with volatility. The correlation of the scaled fall with the next-day excess return is −0.013 in the low-volatility tercile, 0.041 in the middle and 0.097 in the high (n 1762, 1314, 1662). Multiplying the fall by the volatility rank lifts the correlation from 0.042 to 0.093 over 4738 down days.
- **F3:** In the high-volatility tercile the rebound is positive in all six coins. The mean of (fall × next-day excess) runs from 0.0054 (ZEC, t 1.20) to 0.0105 (XRP, t 1.84), with 238 to 316 bars per coin, so no single coin carries it.
- **F4:** Up days are followed by a below-average next day. The mean next-day excess return was −0.0021 (t −2.95, n 3801) in w1–w12 and −0.0018 (t −2.19, n 3874) in w13–w24, and it was negative in all six coins. It does not grow with the size of the rise: the 0–0.5 sigma bin gave t −2.55 and the 0.5–1 bin t −2.93, while the 1.5–2.5 bin gave t −0.11 and the >2.5 bin t −0.45. It is not graded, so I draw no idea from it.
- **F5:** The 5-day excess return after a top-quintile up day depends on which grid of non-overlapping samples is used, so it does not count as a finding. On the base grid it was 0.0162 (t 3.35, n 598). On the other four starting offsets it was 0.0024, 0.0101, −0.0011 and 0.0060 (t 0.54, 2.01, −0.22, 1.18).
- **F6:** The rebound after falls is positive at both ends of the coin's 20-day return and not in the middle, so I draw no graded idea from it. The bottom quartile gave 0.0070 (t 2.53) and the top quartile 0.0047 (t 3.74). The middle quartiles gave −0.0021 (t −1.43) and 0.0011 (t 0.93).
- **F7:** The weekday effects do not hold across years, so they are not findings. Pooled, Friday's next-day excess was +0.0030 (t 3.76) and Wednesday's −0.0030 (t −2.70). By year, Friday's t ranged from −1.01 to 2.67, and Wednesday's pooled effect leans on a single year, 2019 (t −6.99).
- **F8:** The book moves largely with the coins but with much less risk. Its mean daily return was 0.000446 against 0.00118 for holding the coins, with a correlation of 0.63 and daily standard deviations of 0.0146 against 0.0407. Window means ranged from −17.3 to +30.2 basis points per day, and 11 of 24 windows were negative.

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b1_one-day-fall-rebound.g1_volatile-regime-fall-rebound` (from F1, F2, F3): The larger a coin's one-day fall relative to the standard deviation of its daily returns over the past 20 days, the larger its rise over the next day. The rise grows further the higher that 20-day volatility stands relative to its own level over the past 120 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
