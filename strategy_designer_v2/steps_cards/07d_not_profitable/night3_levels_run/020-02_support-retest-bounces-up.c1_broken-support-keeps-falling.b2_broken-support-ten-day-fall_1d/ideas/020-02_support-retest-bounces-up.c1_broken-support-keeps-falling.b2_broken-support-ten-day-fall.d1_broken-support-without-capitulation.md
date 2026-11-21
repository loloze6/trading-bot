---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, except when its 90-day return is a deep fall, after which it rebounds instead.
Consequence: A close just under a support that held many times is a reason to refuse a long for ten days, but not after a deep 90-day fall, when the coin tends to rebound.
Why:
- F3: The effect is graded but too small for a short to earn. The drift-adjusted short gain climbs from -0.45 % in the smallest |forecast| quartile to +0.64 %, +0.75 % and +1.62 % (t 2.24) in the largest. The raw short gain is -1.61 % (t -2.03) in the smallest quartile and only +0.43 % (t 0.59) in the largest.
- F4: The small-forecast half of the shorts loses in every 30-day trend tercile (raw short -0.89 % to -1.27 %). The large half gains +0.25 % to +0.46 % in all three, so the trend does not explain the loss; the weak, distant-level cases do.
- F5: After a deep fall the short loses most. In the lowest quartile of the 90-day return (mean -48 %), the drift-adjusted short gain is -2.42 % and the raw gain -3.62 %. In the other three quartiles the drift-adjusted gain is +1.90 % to +2.93 % (64 to 65 cases each).
