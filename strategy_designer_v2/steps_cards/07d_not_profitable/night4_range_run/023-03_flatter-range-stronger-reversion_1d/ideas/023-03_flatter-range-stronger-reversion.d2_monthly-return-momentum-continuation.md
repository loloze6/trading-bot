---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day return, the larger its rise over the next 5 days.
Consequence: A coin up strongly over the past month is a reason to be long for the coming days rather than short.
Why:
- F7: A plain 30-day return carries the same signal. Coins in the top fifth of 30-day return (mean +50 %) show an unusual move of +1.26 % over the next 5 days (t 2.12, 511 cases).
- F8: The book's falls come from fading rising coins. Its worst coin-windows fall while the coin rose: ETH w11 lost 54 % while ETH rose 154 %, and BTC w17 lost 51 % while BTC rose 95 %. Across coin-windows the book's return correlates -0.17 with the coin's, and every year from 2018 to 2021 was negative.
- F1: The book loses its money on its shorts. Days held short average -0.130 % (8106 days, summed -10.53), while days held long average +0.029 % (9246 days, summed +2.67). On the 5-day grid, the cases where the book was short with the close above the range's middle lose -0.62 % each (1025 cases).
