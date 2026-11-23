---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises
line: 7.e profitable but not proven
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 14-day return relative to its own daily volatility over the past 30 days, the higher its return over the next 5 days.
Consequence: A trader should lean long in proportion to a coin's volatility-scaled two-week rise and refuse longs in coins whose recent two weeks were weak relative to their volatility.
Why:
- F1: The book's mean daily gain of 0.049 % splits into 0.019 % from the coins' own rise and 0.030 % of timing (t 1.88 over 2922 days), and that timing comes from the 30-day-return gate rather than from the idea's forecast. On the 5-day grid, cases with a positive 30-day return end +0.44 % above the coin's drift and the others −0.44 % (t 2.81, about 2440 cases each). Inside the gate, the forecast's slope has t 0.89. With the 30-day return in the same regression, the forecast's t is 0.83 and the 30-day return's t is 2.14.
- F3: Momentum scaled by the coin's own volatility predicts the next 5 days, and the shorter the lookback the stronger it is. On 2415 non-overlapping cases, the slope in strength units per unit of scaled return is 0.085 with t 4.46 for the 14-day return, 0.063 with t 3.54 for the 30-day return and 0.028 with t 1.61 for the 60-day return.
- F5: The effect is broad and not carried by a few trades. Rising-coin minus falling-coin 5-day excess is positive in 14 of 16 coins, for example XRP +3.13 %, SOL +3.11 %, ETH +2.47 % and BTC +1.04 %. The top 10 of 1798 trades carry 13.5 % of the summed trade result, the win rate is 55 %, and BTC carries the largest share of the gain at 21 %.
