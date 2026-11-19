---
line: 7.d not profitable
backtest: 016-07_up-volume-burst-reversal_1h
idea tested: 016-07_up-volume-burst-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2962 USD
---
## Findings
- **F1:** The book loses on every coin because it is short in rising markets. Mean daily book return runs from -0.0007 (XMR) to -0.0019 (BTC). Mean allocation runs from -0.18 to -0.36, with a short position on 46–52 % of bars, while the coins rose 0.0007–0.0016 a day. The market's rise alone costs the book 0.00015–0.00043 a day.
- **F2:** Timing does not rescue it. The position's gain before fees is negative on 5 of 6 coins (-0.0004 to -0.0012 a day; only XMR is +0.0003). Fees of 0.0006–0.0010 a day, at about 0.97 trades a day, roughly double the loss.
- **F3:** The bars the book shorts continue rather than reverse. Risen-regime grid bars have a mean excess forward 72-bar return of +0.0014 (n=2916, t=0.89), against -0.0015 for the non-risen bars (n=2767, t=-0.95).
- **F4:** The rise the book shorts is graded toward continuation at its strong end. Within risen bars, the top fifth of 72-bar past return has an excess forward 72-bar return of +0.0157 (n=573, t=3.37), the strongest cell in the data. Over all bars, the top fifth of past return (mean +11.8 %) is followed by +0.0055, against -0.0071 for the flat middle fifth.
- **F5:** Volume concentration carries no graded reversal. Across fifths of the raw top-3 volume share among risen bars, excess forward returns run -0.0004, +0.0070, +0.0004, +0.0019, -0.0035 (n=573 each), with no order. Fifths of the standardised forecast value run +0.0006, -0.0030, -0.0014, +0.0083, +0.0007. Step 5's top-minus-bottom third was -0.0044 with t=-1.10, and the top third's mean was +0.0007, above 0.

## Ideas
- `016-07_up-volume-burst-reversal.d1_strong-rises-keep-rising` (from F1, F3, F4): The larger a coin's 3-day rise, the more the coin keeps rising over the next 3 days.
- `016-07_up-volume-burst-reversal.d2_grinding-rises-continue` (from F3, F4, F5): When a coin has risen over the past 3 days, the larger the share of the past 3 days' hours that closed up, the more the coin keeps rising over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
