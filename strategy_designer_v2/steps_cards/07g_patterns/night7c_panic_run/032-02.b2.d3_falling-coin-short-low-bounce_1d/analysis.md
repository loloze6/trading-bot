---
line: 7.g patterns
backtest: 032-02.b2.d3_falling-coin-short-low-bounce_1d
idea tested: 032-02.b2.d3_falling-coin-short-low-bounce
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3638 USD
---
## Findings
- **F1:** The next-day move runs against the day's own move, measured in units of the coin's past 60-day daily volatility. The decile with the largest standardised falls (mean z -1.80) is followed by a next-day excess over the coin's mean of +1.00 % (t 2.26, 718 cases). The next decile gives +0.43 % (t 1.41). From the fifth decile up, every decile is below 0, down to -0.34 % (t -1.08) for the largest rises (mean z +1.93).
- **F2:** This one-day reversal is concentrated in coins with wide swings that are falling. With 20-day volatility in the coin's top tercile and a 30-day return below 0, the slope of next-day excess on the day's standardised return is -0.0104 per unit of z (OLS t -6.84, 1201 cases). The other regimes are much weaker: low volatility and falling, -0.0017 (t -1.15); high volatility and rising, -0.0015 (t -0.91); middle tercile, about -0.004 (t -2.2 to -3.7).
- **F3:** The reversal slope is negative in all 6 coins, from -0.0012 (t -0.76, XRP) to -0.0067 (t -4.66, XMR). It is negative in 10 of the 12 shown windows, with t of -5.43 in w10 and -5.33 in w16. So it is not one coin's or one period's effect.
- **F4:** The tested trigger, a close below the prior 10-day low in a coin that fell over 30 days, adds little beyond the day's own fall. Only the deepest quintile of break depth stands out: +2.81 % next-day excess, t 1.46, 61 cases. The other quintiles are +0.02 % to +0.68 % with t under 0.8. Sorting the same cases by the day's return gives the same picture: +2.75 % (t 1.30) for the largest falls.
- **F5:** The book's gain rests on a few days. Its best 5 % of active days carry 145 % of its summed return over 757 active days, and its worst 5 % sum to -86 %.
- **F6:** The reversal lasts one day only. On non-overlapping 3-day stretches, quintiles of the day's return give excess moves between -0.45 % and +0.36 %, all with |t| < 0.8.
- **F7:** Several angles show no pattern that stands out against the number of angles looked at:

## Ideas
- `032-02.b2.d3.g1_volatile-decline-one-day-reversal` (from F2, F3, F1, F6): In a coin whose 30-day return is negative and whose daily swings over the past 20 days are wide, the day's return is followed by a move the opposite way over the next 1 day. The move is larger the larger the day's return is against the coin's typical daily move over the past 60 days.
- `032-02.b2.d3.g2_standardised-down-day-bounce` (from F1, F3, F4, F7): In any coin, a day's fall is followed by a rise over the next 1 day, larger the larger that fall is against the coin's typical daily move over the past 60 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
