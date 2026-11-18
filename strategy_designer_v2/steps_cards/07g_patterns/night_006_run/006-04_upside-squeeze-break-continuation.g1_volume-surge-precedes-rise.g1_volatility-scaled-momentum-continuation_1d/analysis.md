---
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d
idea tested: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3694 USD
---
## Findings
- **F1:** Recent volume predicts the next 3 days' excess return across its whole range, even after allowing for the tested advance. On the 3-day grid, the bars in the top quintile of 10-day mean volume over 60-day mean volume returned +0.0104 above the coin's usual 3-day return (t 2.94, n 857). The bottom quintile returned −0.0072 (t −2.63, n 857). In a regression of excess return on both log volume ratio and the volatility-scaled 10-day return, the volume ratio's beta is 0.0140 (t 4.61), against the scaled return's t of 2.13. The Spearman correlation is 0.045 (p 0.003).
- **F2:** The volume pattern holds in every coin. The top volume quintile's excess is positive in all six coins, from +0.0032 (BTC, n 115) to +0.0188 (XRP, n 153). The bottom quintile's excess is negative in all six, from −0.0008 (BTC) to −0.0127 (ETH, t −2.36). The top quintile is positive in 6 of 8 years, with 2024 at +0.0322 (t 4.03, n 135) and 2020 at +0.0209 (t 2.27).
- **F3:** The pattern also holds on a 3-day volume ratio and partly on a 10-day horizon. A 3-day volume surge (3-day mean over 60-day mean, top quintile) is followed by +0.0100 excess over 3 days (t 2.83, n 857), against −0.0052 for the bottom quintile (t −1.90). At a 10-day horizon the top volume quintile gives +0.0174 excess (t 1.51, n 252), which is the same sign but weak.
- **F4:** Light volume is costly when the advance is weak. Bars in the lowest volume tercile give −0.0089 excess (t −2.65, n 485) when the scaled 10-day return is also in its lowest tercile, and −0.0093 (t −2.98, n 566) when it is in its middle tercile. Within the top scaled-return tercile, the middle volume tercile is where the gain sits, at +0.0106 (t 3.08, n 463).
- **F5:** Range compression did not precede larger moves, which goes against the brief. The size of the next 3-day move, as a multiple of the coin's mean, was 0.97 after the most compressed ranges (10-day mean range over 60-day, bottom quintile). The middle quintiles gave 0.91 to 0.92, and the most expanded ranges gave 1.22. Expanded ranges were also followed by a higher excess return, +0.0065 (t 1.92), against −0.0055 (t −2.01) after compressed ones.
- **F6:** Range compression combined with a falling 10-day return was followed by a further fall. Compressed ranges with a negative 10-day return gave −0.0092 excess (t −3.16, n 664). Expanded ranges with a positive 10-day return gave +0.0097 (t 2.69, n 684).
- **F7:** The book's mean daily return is 0.000765. Of this, 0.000312 (41%) is the market's own rise, carried on a mean position of 0.26, and the rest is timing. The tested signal's top group is positive in 6 of 8 years but negative in 2018 (−0.0153, n 78) and in 2022 (−0.0054, n 96). It is negative in LTC (−0.0001) and XMR (−0.0029).
- **F8:** Neither the weekday nor the 1-day return carries a pattern that stands out. The weekday excess has |t| ≤ 1.86 and the 1-day return quintiles have |t| ≤ 0.88, which is chance level given the many angles looked at.

## Ideas
- `006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation.g1_volume-ratio-predicts-drift` (from F1, F2, F3): The higher a coin's 10-day average volume relative to its own 60-day average volume, the more its price rises over the next 3 days relative to its usual 3-day return.
- `006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation.g2_quiet-decline-keeps-falling` (from F5, F6, F4): When a coin's 10-day return is negative, the narrower its 10-day average daily range relative to its 60-day average range, the more its price falls below its usual 3-day return over the next 3 days.
- `006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation.g3_expanding-range-advance-continues` (from F5, F6): When a coin's 10-day return is positive, the wider its 10-day average daily range relative to its 60-day average range, the more its price rises above its usual 3-day return over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
