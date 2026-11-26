---
line: 7.d confirmed, not profitable
backtest: 031-02.b1.d2_rebound-graded-by-turbulence_1d
idea tested: 031-02.b1.d2_rebound-graded-by-turbulence
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4375 USD
---
## Findings
- **F1:** The book fails only on Calmar (0.677 against 0.75). Its deepest fall is −39.4 %, lasts 204 days, spans windows w1 to w3 and has its trough in 2022. Inside it the book held a mean allocation of 0.39 while the coins lost 0.40 % a day, a forecast was positive on only 53 % of the coin-days, and the positions summed to −1.23 in bar gains. Every year from 2018 to 2025 had a fall of 18 % to 39 %, so the depth is not one isolated crash.
- **F2:** The signal pays only when the coin is turbulent; after a calm stretch it loses.
- **F3:** Turbulence alone does not earn, so it is part of the idea's own effect, not a separate one. On grid bars with no signal, the high-ratio third returns −0.25 % excess over 2 days (t −0.77, 1077 cases), against +0.69 % when the fall signal is also present.
- **F4:** Taking the book out of the market on days after a low-ratio bar (the lower third of the 10-day/60-day volatility ratio) lifts Calmar from 0.67 to 0.87. The yearly return rises from 26.4 % to 30.2 %, the deepest fall shrinks from −39.4 % to −34.7 %, and Sharpe goes from 0.77 to 0.88. Removing the high-ratio days instead cuts Calmar to 0.25.
- **F5:** Within the signal, the rebound grows with both the fall and the turbulence, and small falls lose everywhere.
- **F6:** The book carries positions far beyond the signal. 31.5 % of its position-days have a forecast at or below 0, with a mean allocation of 0.24. Those days earn little: summed bar gains are +1.03, +1.03 and −2.28 across the low, middle and high ratio thirds. Keeping only the 2 days after a signal lifts Calmar to 0.79, with a yearly return of 30.3 % and a deepest fall of −38.1 %.
- **F7:** In the turbulent case the rebound grows with the horizon, and the move then dwarfs the 0.19 % cost of a trade.
- **F8:** Trend gates do not answer the falls. Leaving the book out when the coin's 20-day return or its distance to the 50-day average is negative gives Calmar 0.30 and 0.38. The signal's 2-day excess is +0.06 % in down 20-day trends against +0.19 % in up trends, both with t under 1.

## Ideas
- `031-02.b1.d2.d1_rebound-only-in-turbulence` (from F2, F3, F4, F5): The larger a coin's fall on its latest day, measured against the size of its own daily moves over the past 60 days, the more it rises over the next 2 days, only while its daily moves over the past 10 days are larger than those of the past 60 days, and the more so the larger that excess of recent turbulence.
- `031-02.b1.d2.d2_turbulent-rebound-held-longer` (from F7, F2, F3): The larger a coin's fall on its latest day, measured against the size of its own daily moves over the past 60 days, and the larger its daily moves over the past 10 days against those of the past 60 days, the more it rises over the next 6 days.
- `031-02.b1.d2.d3_rebound-held-two-days-only` (from F6, F1): The larger a coin's fall on its latest day, measured against the size of its own daily moves over the past 60 days, and the more so the larger its daily moves over the past 10 days against those of the past 60 days, the more it rises over the next 2 days, with the whole rise completed within those 2 days of the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
