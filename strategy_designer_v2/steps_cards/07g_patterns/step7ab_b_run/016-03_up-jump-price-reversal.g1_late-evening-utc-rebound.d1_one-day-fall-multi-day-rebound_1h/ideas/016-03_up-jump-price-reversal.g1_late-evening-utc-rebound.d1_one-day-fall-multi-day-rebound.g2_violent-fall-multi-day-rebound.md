---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After a coin has fallen over its last 24 hours, the higher its hourly volatility over those 24 hours relative to its last 30 days, the more it rebounds over the next 3 days.
Consequence: A trader would buy a one-day fall in proportion to how violent the day was, and would not buy a calm fall, which kept falling.
Why:
- F3: The volatility pattern is concentrated after 24-hour falls. After a fall, the strength rises steadily from -0.111 in the lowest volatility quintile (t -2.66, 510 cases) to +0.153 in the highest (t 3.39, 537 cases). The highest quintile ends +1.32 % above drift, +1.68 % in total, and is already +1.15 % above drift after 24 hours. After rises the same quintiles go only from +0.022 to +0.058 (t 1.11).
- F5: The tested idea's graded relation is not in the bars. The 24-hour return quintiles give strengths of +0.094, -0.081, -0.006, -0.038 and +0.031, so only the deepest-fall quintile is positive (t 2.90). The correlation of the 24-hour return with the next 72 hours is between -0.072 and +0.003 on every coin. Overall the idea's unusual move is +0.06 % per case, 0.3 times the cost.
