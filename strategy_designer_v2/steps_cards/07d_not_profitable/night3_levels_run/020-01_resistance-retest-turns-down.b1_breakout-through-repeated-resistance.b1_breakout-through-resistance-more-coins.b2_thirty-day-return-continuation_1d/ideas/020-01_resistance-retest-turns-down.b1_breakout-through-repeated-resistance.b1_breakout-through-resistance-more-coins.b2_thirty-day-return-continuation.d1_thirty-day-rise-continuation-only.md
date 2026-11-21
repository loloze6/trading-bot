---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b2_thirty-day-return-continuation
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b2_thirty-day-return-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day return, the larger its rise over the next 10 days, only while that 30-day return is a rise.
Consequence: A coin's strong 30-day rise is a reason to buy it for 10 days, more so the stronger the rise, and a 30-day fall is no reason to sell it short.
Why:
- F1: The short side earns nothing and carries the deepest fall, so it is why Calmar fails. Before costs, the long legs alone earn 0.088 % a day with Sharpe 1.16, deepest fall -25 % and Calmar 1.30. The short legs alone earn -0.001 % a day with Sharpe -0.01 and deepest fall -53 %. Short bars lose on average (-0.014 % per bar over 18,873 bars), while long bars gain +0.20 % per bar over 17,958 bars.
- F2: The book's deepest fall is -36.7 % and lasts 478 days, through windows w2 to w6, while the coins' daily returns summed to +41 %. Of the fall's -0.35 bar gain, the short legs lost -0.27 and the long legs only -0.08. The worst single stretch is w4, where the coins rose +51 % and the shorts lost -0.14.
- F3: The deepest 30-day falls are not followed by further falls. On the non-overlapping 10-day grid, the most negative forecast sextile (forecast about -16) has a 10-day excess return of only -0.5 % (t -0.79, 447 cases). The next two sextiles show -2.1 % (t -3.04) and -1.7 % (t -2.60).
- F4: On the long side the effect is graded. The two highest forecast sextiles show +1.5 % (t 1.67) and +2.1 % (t 2.30) of 10-day excess over 447 cases each. Long-bar gains rise from -0.004 % in the lowest 60-day-return quartile to +0.42 % and +0.25 % in the top two.
- F6: The move is large against the cost of a trade. Per case it is 6.4 times the 0.22 % round trip (total move +1.43 % over 10 days), so costs are not the cause. Book and bar gains correlate at 0.999, with 0.082 % against 0.088 % a day.
