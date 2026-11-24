---
line: 7.d confirmed, not profitable
backtest: 031-01.g1_sharp-drop-next-day-bounce_1d
idea tested: 031-01.g1_sharp-drop-next-day-bounce
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3956 USD
---
## Findings
- **F1:** The check failed on Calmar, at 0.636 against a rule of 0.75. The book's deepest fall was -27.7 % over 119 days, from w8 into w9 (2019), while holding the coins lost -40.2 % over the same stretch; in w8–w9 the strongest forecasts (12 to 20) lost, with summed gain -0.188 and excess -0.06 % on 178 bars, while forecasts 8 to 12 gained (+0.503, excess +0.66 %).
- **F2:** The bounce depends on whether the coin's recent turbulence is fresh, measured as 7-day volatility against 30-day volatility. On signal bars in the top quarter of that ratio, the next-day excess return is +0.75 % (1573 bars) and the book's gain per bar is +0.55 %; in the calmest quarter they are -0.11 % and -0.075 % (1643 bars), so in calm conditions the signal loses money.
- **F3:** Within the falls, the same grading holds. For falls beyond 1 usual move in the hottest quarter, the next-day excess is +1.44 % (589 cases on 297 days, day-clustered t 3.48). The same size of fall in the calmest quarter gives -1.20 % (fall of 1 to 1.5 moves, 94 cases) and -0.33 % (1.5 to 2 moves, 15 cases), and the hot-quarter excess grows with the fall: +0.23 %, +0.50 %, +1.26 %, +1.75 %, +1.41 % from the smallest to the largest fall bins.
- **F4:** The turbulence condition is not an effect of its own. On hot-quarter bars without the signal (up days), the next-day excess is -0.36 % (1692 bars), against +0.75 % when the signal is present. It belongs to the theory because a sharp fall inside a fresh burst of turbulence is the forced selling and capitulation the brief names as overreaction.
- **F5:** A rebuilt book that holds the tested position only when the 7-day/30-day volatility ratio is above its median reaches Calmar 0.815 against 0.641 for the rebuilt base. Its deepest fall is -21.1 % against -27.6 %, its Sharpe 0.97 against 0.73, its yearly return 17.2 % against 17.7 %, and its mean per day in a position 0.27 % against 0.12 %. Raising the forecast threshold alone does not repair the failing measure: Calmar is 0.677 for forecast above 8 and 0.542 for forecast above 12.
- **F6:** Per case, the idea's total move is +0.30 % and its unusual move +0.18 %, against a cost of 0.19 % per trade (0.9 times the cost for the unusual move). In the hot-turbulence falls of more than 1 usual move, the excess of +1.44 % is about 7.6 times the cost, so the stronger case pays for its trades.
- **F7:** The weak forecasts carry no excess return: forecast 0–4 gives -0.03 % (2620 bars) and 4–8 gives -0.08 % (1996). Forecast 12–16 gives +0.44 % (885) and 16–20 gives +0.62 % (1601).

## Ideas
- `031-01.g1.d1_sharp-drop-in-fresh-turbulence` (from F1, F2, F3, F4, F5, F6, F7): The further a coin's one-day fall stands below its own usual daily move (its 30-day volatility), the more it rises back over the next day, and the more so the higher its 7-day volatility stands against its 30-day volatility, so that a sharp fall inside a fresh burst of turbulence is followed by the largest rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
