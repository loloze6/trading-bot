---
line: 7.d confirmed, not profitable
backtest: 075-01.g1_heavy-volume-down-day-rebound_1d
idea tested: 075-01.g1_heavy-volume-down-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4533 USD
---
## Findings
- **F1:** The book fails on Calmar (0.54 against 0.75) because of one long fall: −22.3 % over 119 days from w8 into w9, while the coins themselves summed −43 % over the same stretch, and w9 was the worst window (book summed −10.8 %, coins −29.8 %). The book was long the coin's down days straight through a falling market, holding a position on 74 % of coin-days.
- **F2:** The effect lives in agitated markets, and the book's largest positions sit in calm ones. Down days in falling agitated markets were followed by +1.08 % excess next-day return (t 4.78, 737 cases) and in rising agitated ones by +0.63 % (t 1.69, 1265). Falling calm down days gave −0.12 % (t −0.83, 956) and choppy calm ones +0.02 % (t 0.09, 583). Yet the volatility targeting gave calm down days a mean position of 0.46–0.51 against 0.28–0.29 on agitated ones.
- **F3:** Agitation is not an effect of its own, which makes it a repair. Down days in the agitated profiles average about +0.73 % excess next day, against about +0.11 % in the calm profiles. The agitated days that are not down days average about −0.39 % (about 2,330 cases), and the falling agitated non-down days about −0.79 % (700 cases), derived from the all-day and down-day profile tables. The agitation therefore carries no gain without the idea's heavy-volume fall, and it fits the brief's theory: forced selling (liquidations, stop cascades) happens in swinging markets.
- **F4:** The volume grading is real but runs from loss to gain. Inside falling markets, down days in the light-volume tercile were followed by −0.32 % excess (t −1.90, 754 cases), the middle by +0.01 %, and the heavy by +0.97 % (t 4.40, 763). In rising markets the same three terciles gave +0.29 %, +0.42 % and +0.78 % (t 3.05). Across fall sizes, light-volume mid and small falls lost −0.44 % (t −2.13) and −0.30 % (t −2.00). The book still holds a long on every down day, so these light-volume falls are a steady drag at a cost of 0.22 % a trade.
- **F5:** The size of the move against the cost decides the book. Over all cases the total move is +0.23 % against a 0.22 % trade cost (1.0 times) and the unusual move only +0.08 % (t 0.69). In the heavy-volume tercile the move is much larger: falling markets +1.19 % total, about 5 times the cost, and falls in the largest tercile on heavy volume +1.49 % total (t of the excess 5.39, 1031 cases). The book can only pay if it concentrates on these strong cases.
- **F6:** The strong case is also the heavy-volume fall that ends a run of falls. Down days in the lowest tercile of 5-day return with heavy volume gave +1.38 % excess (t 5.23, 864 cases). Heavy-volume down days with a middling 5-day return gave +0.02 % (t 0.10, 426). The same low 5-day return on light volume gave +0.74 % (t 0.90). That condition carries part of the gain on its own, so it is not proposed as a repair.

## Ideas
- `075-01.g1.d1_agitated-heavy-volume-fall-rebound` (from F1, F2, F3, F5): In an agitated market, on a day a coin falls, the heavier its volume against its own average daily volume over the past 20 days, the larger its rise over the next day.
- `075-01.g1.d2_volume-graded-down-day-reversal` (from F1, F4, F5): On a day a coin falls, its return over the next day rises with its volume against its own average daily volume over the past 20 days, from a further decline after the lightest-volume falls to a rebound after the heaviest-volume falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
