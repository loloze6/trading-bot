---
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3598 USD
---
## Findings
- **F1:** When the 20-day volatility is above its 100-day mean, the next day's excess return falls steadily with where the day closed within its range: closes in the bottom fifth average +0.0058 (t 2.04, n 333) and closes in the top fifth average −0.0046 (t −2.32, n 560), a low-minus-high Welch difference of 0.0117 (t 3.23); outside that regime the same split shows nothing (−0.0019 vs +0.0004).
- **F2:** Inside the high-volatility regime, the close's place in the range carries the effect within each side of the day: down days closing in the lower third gain +0.0050 next day (t 2.46, n 527), and up days closing in the upper third lose −0.0046 (t −2.87, n 696); but in a joint regression with the day's sized move, the close-location slope is not separate (t −1.05) while the move's slope is (t −2.07).
- **F3:** The mirror of the tested idea holds: in the high-volatility regime, a day rising more than 2 usual moves (rise / 60-day mean absolute daily move) is followed by a mean excess next-day return of −0.0060 (t −2.35, n 193), and rises of 0.6 to 1.2 usual moves are followed by −0.0048 (t −1.85, n 250); outside the regime, rises above 2 usual moves give −0.0010 (t −0.29).
- **F4:** The fade after up days is graded but modest: on high-volatility up days, Spearman rho between the sized rise and the next-day excess return is −0.072 (p 0.019, n 1050); it is negative in both halves of the period (large rises −0.0038, t −1.28 early and −0.0046, t −2.29 late) and stronger in ETH (−0.0078, t −2.79) than in BTC (−0.0011, t −0.49).
- **F5:** The book's gain comes almost entirely from high-volatility bars (summed position gain 2.997 against 0.027 elsewhere); it is in the market only 27.6 % of bars at a mean allocation of 0.40, so its mean daily return of 0.000378 trails holding's 0.00128; timing makes up most of its gain (BTC 0.000436 of 0.000580, ETH 0.000326 of 0.000464).
- **F6:** Other angles showed nothing clear given how many were tried: bar range quintiles (all |t| < 1.4), 5-day reversal on a non-overlapping grid (all |t| < 1.2), the 2-day close-location grid (|t| < 1.5), and a lone Wednesday dip (−0.0039, t −2.38, one of seven weekdays).

## Ideas
- `005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound.g1_volatile-rise-next-day-fade` (from F3, F4, F5): In a coin whose 20-day volatility is high relative to its last 100 days, a sharp one-day rise is followed by a fall over the next day. The larger the rise relative to the coin's 60-day mean absolute daily move, the larger that next-day fall.
- `005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound.g2_volatile-close-location-next-day-reversal` (from F1, F2): In a coin whose 20-day volatility is high relative to its last 100 days, the higher the day closes within its own high-low range, the lower its return over the next day, and the lower it closes, the higher that return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
