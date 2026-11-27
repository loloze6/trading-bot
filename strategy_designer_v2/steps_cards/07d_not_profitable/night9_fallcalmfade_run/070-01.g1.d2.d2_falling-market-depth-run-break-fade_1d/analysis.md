---
line: 7.d confirmed, not profitable
backtest: 070-01.g1.d2.d2_falling-market-depth-run-break-fade_1d
idea tested: 070-01.g1.d2.d2_falling-market-depth-run-break-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4058 USD
---
## Findings
- **F1:** The effect lives almost entirely in deep runs. In a falling market, up days that end a run losing more than 15 % are followed by a next-day fall of +3.87 % beyond drift in the short direction (t 6.1, 58 cases). Runs losing 10 to 15 % are followed by +2.89 % (t 5.1, 75 cases). Runs losing 7 to 10 % give +0.89 % (t 1.5, 82), 4 to 7 % give +0.10 % (t 0.2, 138), and 0 to 4 % give +0.55 % (t 1.7, 208). So 428 of the 561 falling breaks carry a move about the size of the 0.19 % trade cost or below it, and they dilute the deep cases.
- **F2:** The book barely sizes its bets and does not grade them by depth. The mean forecast on active bars is −4.0 out of 20, and the mean absolute allocation is 0.15. The deepest fifth of run losses (mean −17.6 %) gets a forecast of −5.0 and an allocation of 0.19. The middle fifth (−5.2 %) gets nearly the same, −4.77 and 0.197, although it earns only 0.14 % against 2.43 %. The 60-bar standardisation and the weight-3 zero companion flatten the grading. This leaves the book at a mean daily return of 0.0108 % with a daily standard deviation of 0.21 %, below the 0.05 % per position day the check needs, even though trades earn 0.57 % net on average (783 trades).
- **F3:** The run's depth alone is not the effect. In falling markets, a down day that extends a run past a 15 % loss is followed by a rise: −2.23 % in the short direction (97 cases). For runs at −10 to −15 % the figure is −0.29 % (130 cases). So the short needs the up close that ends the run, as the idea says.
- **F4:** The fall is a one-day move:
- **F5:** Deep run breaks fall outside the falling profile too. Outside it, breaks after runs losing more than 15 % are followed by +1.95 % (157 cases) and runs losing 10 to 15 % by +1.31 % (178 cases). Shallow runs there give −0.22 % to +0.16 % (1,256 cases). The depth grading therefore holds in every trend, and the falling profile mainly adds size.
- **F6:** The deep-run effect is broad, not one period's:

## Ideas
- `070-01.g1.d2.d2.d1_falling-deep-run-break-fade` (from F1, F2, F3, F4, F6): In a falling market, an up day that ends a run of down days is followed by a fall over the next day that grows steeply with how much the price dropped over the run, so that nearly all of the fall comes after runs that took several of the coin's usual daily moves off the price, and the fall is larger in proportion to that drop itself.
- `070-01.g1.d2.d2.d2_deep-run-break-fade-anywhere` (from F1, F3, F4, F5): An up day that ends a run of down days is followed by a fall over the next day, and that fall grows steeply with how much the price dropped over the run, appearing mostly after runs that took several of the coin's usual daily moves off the price.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
