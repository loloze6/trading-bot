---
line: 7.g patterns
backtest: 034-01_rising-nearness-to-high-rises_1d
idea tested: 034-01_rising-nearness-to-high-rises
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4449 USD
---
## Findings
- **F1:** Across every bar, in all profiles, the coin's drift-removed 5-day return rises with how close the close sits to its 20-day high in units of its 20-day daily swing: the slope is 0.0087 per swing unit, t 2.09 (2016 grid cases, 256 days). On the bars with a known trend the slope is 0.0109, t 2.25 (1622 cases, 236 days). Inside the rising profile alone it is weaker: 0.0071, t 1.29 (906 cases, 168 days).
- **F2:** Over 10 days the same nearness slope is clearer than at the tested 5 days. Inside the profile it is 0.0184, t 2.28 (454 cases), and on all bars 0.0160, t 2.29 (996 cases). Outside the profile it is 0.0131, t 1.23 (542 cases).
- **F3:** Inside the rising profile the gain sits at and above the high, and the steps below it are not graded. Closes above the 20-day high are followed by +4.61 % over 5 days beyond drift (t 2.41, 127 cases, 56 days). The bins further below the high, nearest first, give +0.49 % (t 0.29), +1.81 % (t 1.53), -0.22 % (t -0.22) and +0.38 % (t 0.15).
- **F4:** In falling and choppy markets a close above the high is also followed by gains: +4.36 % (t 3.94) and +24.65 % (t 1.38). Both rest on few days (8 and 16), so they cannot be told from chance. Closes more than 3 swings below the high in a choppy market are followed by -6.40 % (t -2.00, 35 days).
- **F5:** The book's gain rests on rare days. Its best 2 % of days carry 114 % of its total gain and its worst 2 % take away 73 %. Its daily returns correlate 0.245 with holding the coins.
- **F6:** These angles showed nothing that stands out after day-clustering:

## Ideas
- `034-01.g1_rising-nearness-ten-day-drift` (from F2, F3, F1): In a rising market, the closer a coin's daily close sits to its 20-day high, and the further it stands above it, measured in units of its daily swing over the last 20 days, the more it rises over the next 10 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `034-01.g2_nearness-to-high-all-markets` (from F1, F2, F4): In any market, the closer a coin's daily close sits to its 20-day high, and the further it stands above it, measured in units of its daily swing over the last 20 days, the more it rises over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
