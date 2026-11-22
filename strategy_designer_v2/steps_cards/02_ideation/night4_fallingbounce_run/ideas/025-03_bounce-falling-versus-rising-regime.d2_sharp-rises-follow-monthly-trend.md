---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime
line: 7.d not profitable
backtest: 025-03_bounce-falling-versus-rising-regime_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, the 5-day return after a one-day rise of several usual daily moves is higher the higher its 30-day return, measured in usual daily moves.
Consequence: After a sharp up day, a trader would go long a coin whose last month rose strongly and short one whose last month fell strongly, sized by that month's move.
Why:
- F2: Inside short cases, the fade is graded by the coin's own 30-day return (in usual daily moves), not by the rise:
- F3: Among long cases (90-day return positive), the 5-day excess return also rises with the 30-day return. It goes −1.43 % (t −2.45), +0.56 %, +1.33 % (t 2.14) and +0.90 % from lowest to highest quartile, 279 cases each. Both sides together say the 5 days after a sharp rise follow the 30-day trend, with a spread of about 1.5 to 3 % per case between extremes, well above the 0.19 % cost of a trade.
- F6: Overall the idea's size barely covers its cost. Short cases lost the coin −0.41 % versus drift (t −1.58, 1319 cases), and long cases −0.07 % (t −0.21, 1510 cases). Per case the total move is 1.1 times the cost and the unusual move 0.9 times.
