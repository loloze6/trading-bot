---
line: 7.b inconclusive
backtest: 046-02_calm-scaled-rise-two-day-continues_1d
idea tested: 046-02_calm-scaled-rise-two-day-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4883 USD
---
## Findings
- **F1:** The plan's two-day measure adds two opposite moves: on the 2-day grid of calm up days, the top fifth of scaled rises (mean z 1.98) gives -0.79 % excess on the first day (t -2.06, 203 cases) and +0.73 % on the second day alone (t 2.76), so the two-day excess is -0.08 % (t -0.20); this is why step 5's slope t is 0.39 and the unusual move is -0.04 %.
- **F2:** On every calm up bar (2,004 one-day cases), the second-day excess return rises with the scaled rise, with a slope t of 2.20 (1.63 with the cases of one day taken together; 2.42 when the outcome is measured in the coin's usual daily swings), while the first-day slope is -0.72; by fifth the second day is flat to rising, ending at +0.71 % (t 3.13) in the top fifth, against -0.35 % (t -1.35) on the first day and -0.17 % (t -0.73) on the third.
- **F3:** The top-fifth second-day move is +0.71 % per case with a t of 2.35 over 204 days with the day's cases taken together, which is 3.7 times the 0.19 % cost of a trade, but it leans on window w10 (+2.43 %, t 4.53): without w10 it is +0.42 % (t 1.70) and the slope t falls to 1.26.
- **F4:** The second-day effect is positive in all six coins' top fifth (from +0.30 % for BTC to +1.50 % for ETH, t 3.37) and in three of four years (2020 +1.55 %, t 3.11; 2018 -0.08 %), and it is weaker in agitated markets (top fifth +0.59 %, t 1.50), as the brief's calm reading predicts.
- **F5:** Within the calm top fifth, the second-day rise mostly follows a down first day: +1.08 % (t 4.20, 229 cases) when the first day fell, against +0.22 % (t 0.54, 172 cases) when it rose. This fits the brief's account of a day of selling into the jump, followed by the late buyers.

## Ideas
- `046-02.b1_calm-rise-second-day-follow-through` (from F1, F2, F3, F4, F5): In a calm market, the larger a one-day rise is against the coin's 30-day daily swing, the larger the coin's rise over the second day after it, from the close of the next day to the close of the day after.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
