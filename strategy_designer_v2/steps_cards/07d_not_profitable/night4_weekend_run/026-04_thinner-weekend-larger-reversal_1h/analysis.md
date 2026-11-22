---
line: 7.d not profitable
backtest: 026-04_thinner-weekend-larger-reversal_1h
idea tested: 026-04_thinner-weekend-larger-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5285 USD
---
## Findings
- **F1:** The book loses because its forecast does not carry the graded effect that is in the data. The raw situation (weekend move in usual 48-hour moves × weekday/weekend volume ratio) predicts the next 48 hours with slope -0.038, t -2.78, on 2286 weekly cases. The traded forecast, standardised and negated, has a slope of -0.0003, t -0.18, despite a correlation of 0.85 with that raw product.
- **F2:** The reversal is carried only by the largest thin-volume weekend moves, and the small ones run the other way. Sorted by the size of the raw signal, the unusual move in the signal's direction over the next 48 hours is:
- **F3:** Thinness is what makes a weekend move reverse. The 48-hour slope on the weekend move is:
- **F4:** The reversal holds only when the coin is already volatile. The slope of the next 48 hours on the weekend move is +0.230 (t 4.67) in the lowest third of 30-day volatility and -0.068 (t -2.03) in the highest third. Among the top half of raw signals, the unusual move is:
- **F5:** Among the thinnest weekends, the reversal is by far strongest after a 30-day rise: slope -0.466, t -4.10, 197 cases. After a 30-day fall it is -0.117 (t -1.19), and in a flat month -0.113 (t -1.12).
- **F6:** Most of the losses fall on the two days the bet is held. Mean position is 0.50 on Monday and 0.48 on Tuesday, against about 0.02 on other days. The book's gain per bar is -0.04 bp on Monday and -0.14 bp on Tuesday.

## Ideas
- `026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse` (from F1, F2, F3): The lower a coin's weekend volume is compared with its volume over the preceding five weekdays, the larger the share of its Saturday-Sunday move that is reversed over Monday and Tuesday. This holds only for weekend moves that are large in the coin's usual 48-hour moves, and the reversal grows with the product of the move's size and the weekend's thinness.
- `026-04_thinner-weekend-larger-reversal.d2_thin-weekends-reverse-when-volatile` (from F3, F4): The lower a coin's weekend volume is compared with its volume over the preceding five weekdays, the larger the share of its Saturday-Sunday move that is reversed over Monday and Tuesday, the more so the higher the coin's hourly volatility over the preceding 30 days.
- `026-04_thinner-weekend-larger-reversal.d3_thin-weekend-reversal-after-rally` (from F3, F5): The lower a coin's weekend volume is compared with its volume over the preceding five weekdays, the larger the share of its Saturday-Sunday move that is reversed over Monday and Tuesday, the more so the more the coin has risen over the preceding 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
