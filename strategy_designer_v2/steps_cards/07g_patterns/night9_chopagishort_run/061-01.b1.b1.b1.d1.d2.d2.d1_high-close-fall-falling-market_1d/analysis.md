---
line: 7.g patterns
backtest: 061-01.b1.b1.b1.d1.d2.d2.d1_high-close-fall-falling-market_1d
idea tested: 061-01.b1.b1.b1.d1.d2.d2.d1_high-close-fall-falling-market
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4603 USD
---
## Findings
- **F1:** The tested situation is not graded the way the theory says. Over 2 days, closes at 0.75–0.9 of the day's range were followed by an unusual move of −0.90 % (t −2.27, 1021 cases, 392 days). Closes nearest the high (above 0.9) were followed by +0.05 % (t 0.11, 644 cases, 246 days). Inside a falling market, closes at or above 0.75 were followed over 5 days by only −0.75 % (t −0.50, 111 cases, 35 days). Neither nearness to the high nor the falling profile adds the fall the idea claims.
- **F2:** In a choppy market (60-day return between −10 % and +10 %), the coin's 20-day return continues over the next 5 days. The unusual 5-day move rises 7.07 % per unit of the 20-day return scaled by its 30-day swing (t 2.57, 189 cases, 76 days). The same slope is 0.82 % in falling markets (t 0.71, 527 cases) and 1.05 % in rising ones (t 0.99, 484 cases).
- **F3:** The continuation in choppy markets also shows on the short side. After a negative 20-day return in a choppy market, the next 5 days' unusual move averaged −5.05 % (t −2.31, 97 cases, 50 days). In choppy agitated markets it averaged −8.82 % (t −2.10, 36 cases, 24 days), against +0.59 % in falling agitated markets (t 0.27, 149 cases).
- **F4:** The book's 5-day 20-day-return slope is not driven by one period: it is positive in both halves of the shown windows (w7–w12: 0.93 %, t 1.01; w13–w18: 1.33 %, t 1.44). It reaches a t above 2 only inside the choppy profile (choppy calm 6.74 %, t 2.30, 125 cases).
- **F5:** The largest 1-day falls (below −6.15 %) were followed by a +1.53 % unusual move the next day (t 2.49, 1222 cases, 323 days). In choppy agitated markets the rebound grows with the scaled fall (slope −2.26 % per unit, t −2.85, 180 cases). The profile map already holds this as agitated-market fall rebounds (long), so it is not a discovery.
- **F6:** Weekday effects do not hold across halves. Monday's next-day unusual move is −0.36 % over all windows (t −2.59), but +0.13 % in w7–w12 (t 0.26). Friday's is +0.39 % (t 2.94), but −0.05 % in w13–w18 (t −0.12).
- **F7:** The book's small gain comes from one window. When held, the book's positions gained 0.15 % per bar before costs over 1554 bars, while the coins fell 0.09 % on those bars. Window w14 alone averaged +0.27 % a day, against between −0.03 % and +0.04 % for every other window but w13.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `061-01.b1.b1.b1.d1.d2.d2.d1.g1_choppy-market-twenty-day-continuation` (from F2, F3, F4): In a choppy market, a coin's 20-day return, measured against its usual 30-day swing, continues over the next five days, and the larger that scaled 20-day move, the larger the move in the same direction that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
