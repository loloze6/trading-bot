---
line: 7.d confirmed, not profitable
backtest: 070-01.g1.d2_run-break-fade-every-market_1d
idea tested: 070-01.g1.d2_run-break-fade-every-market
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4652 USD
---
## Findings
- **F1:** The book fails on Calmar (0.21) and on Sharpe against holding (-0.053) because its gain is spread unevenly. Short cases lose when the coin has been rising. Cases in a rising calm 60-day market have a mean short-direction unusual move of -1.25 % (t -2.93, 100 cases). Cases in falling agitated markets earn +2.24 % (t 4.33, 80 cases) and cases in falling calm markets earn +1.00 % (t 2.78, 195 cases). Held days in rising markets summed -0.38 of gain, against +1.26 in falling markets.
- **F2:** The losing windows are the ones where the coins rose. w11 had a coin mean of +1.26 % a day, the book summed -6.3 % and the cases' mean move was -1.23 %. In w10, w12 and w17 the book summed -0.8 %, -4.4 % and -1.1 %, and the deepest falls of the reconstructed chain were -13.4 % (w13) and -12.3 % (w12). By year, the book's mean daily return dropped from +0.068 % in 2018, when the coins fell (-0.35 % a day), to -0.010 % in 2021, when they rose (+0.41 % a day).
- **F3:** The run's count of down days grades the move poorly, but the depth of the run's fall grades it strongly. By count, runs of 2 earn +1.08 %, runs of 3 earn +0.80 % and runs of 4 earn +0.51 %. By the price fall over the run, the deepest quarter (beyond -13 %) earns +2.46 % (t 5.57, 263 cases) and the next quarter earns +1.38 % (t 4.09). The two shallow quarters earn -0.08 % and +0.37 %.
- **F4:** The coin's 20-day return decides where the fade works. Among cases, the most negative 20-day quarter earns +1.97 % (t 4.86) and the most positive quarter earns -0.30 % (t -0.97). Deep runs inside a negative 20-day return earn +2.90 % (163 cases), against +0.16 % for deep runs inside a positive one (57 cases).
- **F5:** Neither added condition is an effect on its own:
- **F6:** In a simplified rebuild of the book (fixed volatility sizing, 0.19 % cost per position-day), changing the sizing or adding the 20-day condition lifts Calmar:

## Ideas
- `070-01.g1.d2.d1_depth-graded-run-break-fade` (from F3, F5, F6): An up day that ends a run of down days is followed by a fall over the next day, and that fall is larger the more the price dropped over the run of down days it ends.
- `070-01.g1.d2.d2_falling-market-depth-run-break-fade` (from F1, F2, F4, F5, F6): In a falling market, an up day that ends a run of down days is followed by a fall over the next day, and that fall is larger the more the price dropped over the run of down days it ends.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
