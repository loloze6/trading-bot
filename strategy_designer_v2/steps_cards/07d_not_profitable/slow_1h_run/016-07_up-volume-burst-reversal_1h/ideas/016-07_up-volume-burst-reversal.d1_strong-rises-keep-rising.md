---
brief: 016_grind-versus-jump-moves
source-idea: 016-07_up-volume-burst-reversal
line: 7.d not profitable
backtest: 016-07_up-volume-burst-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day rise, the more the coin keeps rising over the next 3 days.
Consequence: A trader should not fade strong 3-day rises in these coins and could lean long in proportion to the size of the rise instead.
Why:
- F1: The book loses on every coin because it is short in rising markets. Mean daily book return runs from -0.0007 (XMR) to -0.0019 (BTC). Mean allocation runs from -0.18 to -0.36, with a short position on 46–52 % of bars, while the coins rose 0.0007–0.0016 a day. The market's rise alone costs the book 0.00015–0.00043 a day.
- F3: The bars the book shorts continue rather than reverse. Risen-regime grid bars have a mean excess forward 72-bar return of +0.0014 (n=2916, t=0.89), against -0.0015 for the non-risen bars (n=2767, t=-0.95).
- F4: The rise the book shorts is graded toward continuation at its strong end. Within risen bars, the top fifth of 72-bar past return has an excess forward 72-bar return of +0.0157 (n=573, t=3.37), the strongest cell in the data. Over all bars, the top fifth of past return (mean +11.8 %) is followed by +0.0055, against -0.0071 for the flat middle fifth.
