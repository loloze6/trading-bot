---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the more efficient the path of that rise (a larger net move relative to the sum of its absolute hourly moves), the more the coin rises over the next 3 days.
Consequence: A trader would go long after efficient 3-day rises and size by path efficiency, and would refuse to buy rises built from choppy back-and-forth hours.
Why:
- F4: Among 3-day rises on the non-overlapping 72-bar grid, the next-3-day excess return rises with path efficiency (net log move over the summed absolute hourly log moves): −38bp, −27bp, +16bp, +23bp and +111bp (t 2.8, n 597) from the lowest to the highest efficiency quintile; efficiency also correlates with the next-3-day excess return over all moves (rho 0.044, t 3.3, n 5,539), while the 3-day return alone does not (rho 0.015, t 1.1).
- F5: The efficiency effect is not stable across years: the correlation of signed efficiency with the next-3-day excess return is positive and significant in 2018 (t 2.3), 2020 (t 2.2) and 2024 (t 2.8), but negative in 2019, 2021 and 2025 (t −1.1 to −1.3); across coins it is positive for 5 of 6 (t 1.0 to 1.4 each).
- F7: The tested grind measure (one minus the top-3 hourly gains' share of a 3-day rise) correlates with the next-3-day excess return (rho 0.058, t 3.1, n 2,865) only before the rise's size is accounted for; the plan's regression with the 3-day return included gives t 1.5.
