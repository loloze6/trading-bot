---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises
line: 7.e profitable but not proven
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 30-day return, the higher its return over the next 5 days, with the effect fading by 20 days.
Consequence: A trader should hold rising coins for about a week, in proportion to their month's rise, rather than for weeks.
Why:
- F1: The book's mean daily gain of 0.049 % splits into 0.019 % from the coins' own rise and 0.030 % of timing (t 1.88 over 2922 days), and that timing comes from the 30-day-return gate rather than from the idea's forecast. On the 5-day grid, cases with a positive 30-day return end +0.44 % above the coin's drift and the others −0.44 % (t 2.81, about 2440 cases each). Inside the gate, the forecast's slope has t 0.89. With the 30-day return in the same regression, the forecast's t is 0.83 and the 30-day return's t is 2.14.
- F4: The 30-day return is graded at 5 days. By quintile of the 30-day return, the 5-day excess move runs −0.38 %, −0.87 %, −0.57 %, +0.40 %, +1.09 % (729 cases each; slope t 3.23, n 3645). At 20 days the slope's t is only 0.36. The rising-minus-falling split has t 2.49 at 1 day, 2.81 at 5 days, 2.13 at 10 days and 0.31 at 20 days.
- F6: The gain depends on the market state. Rising coins' strength was −0.23 in 2022 and −0.65 in 2018, the two years the book's timing lost (−1.77 and −0.44 summed). It was +0.42 in 2020, +0.40 in 2021 and +0.12 in 2024, years when timing earned +1.66, +2.39 and +3.56.
