---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's close stands above its highest high of the previous 30 days, the higher its return over the next 7 days.
Consequence: A trader would buy a clean break of the 30-day high, sized up the further price has cleared it, instead of fading the break as resistance.
Why:
- F5: Nearness to the 30-day high carries no information beyond the 14-day return: in a joint regression its t is -0.76, while ret14 keeps t 3.80 (n 1723).
- F6: Closes above the prior 30-day high are followed by a 7-day return 4.5 % above the coin's mean (t 2.28, n 108), against -0.2 % for other bars (t -0.60, n 1615). The excess holds in the two highest volume quintiles (+5.9 %, t 1.61, n 30; +5.4 %, t 1.92, n 62). Given how many angles were checked, this is marginal.
