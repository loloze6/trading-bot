---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.d2_support-retest-fails-downtrend
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.d2_support-retest-fails-downtrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's price falls back to a price where it turned up several times in the past 90 days while its 90-day return is negative, it tends to fall further over the next 5 days, and the higher its 20-day return at that retest (a calm return to the lows rather than a crash into them), the larger the further fall.
Consequence: In a coin that has fallen over 90 days, a slow drift back to old lows would be a reason to sell, and a crash into them would not.
Why:
- F1: The book loses mainly because it is short coins that drift upward. Its mean position is -0.186 and it is short on 30 % of bars. Its gain from the market's own rise is -0.022 % a day, more than its whole mean daily return of -0.011 %, so its timing is slightly positive (+0.011 % a day). Holding the coins earns +0.067 % to +0.155 % a day depending on the coin. Per case the total move is -0.13 % against a cost of 0.19 %, while the unusual move is +0.45 % (2.3 times the cost) but is eaten by a drift of -0.58 % in the short's direction.
- F2: The forecast's grading runs the wrong way, so the larger shorts do not fall more. The larger-forecast half minus the smaller half is -0.95 %. Active grid cases in the deepest 90-day-fall quartile end +0.16 % over 5 days, against -0.88 % in the second quartile. The four touch-strength quartiles show no order (-0.39 %, -0.14 %, +0.29 %, -0.34 %).
- F3: Shorts taken after a steep short fall lose the most.
- F4: Active grid cases fall further the less the coin has fallen over the past 20 days. The 20-day-return quartiles go from +0.69 % (mean -22 %) to -0.80 %, -0.45 % and -1.09 % (mean +6 %). The top quartile's 1.09 % short gain is 5.7 times the cost and above the coin's 5-day drift.
