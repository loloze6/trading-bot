---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a down day, a coin's return over the next 1 day is higher the larger that day's fall was, measured against its 20-day volatility.
Consequence: A trader would buy a coin after a large standardised daily fall, sized by the fall, rather than follow the fall down.
Why:
- F6: A coin rebounds the day after a large down day. After the fifth of down days with the largest fall in units of 20-day volatility (mean −1.81), the next day's unusual return is +0.60 % (t 4.19, 1568 days). The next fifth gives +0.33 % (t 2.64), and the small falls give about 0. The slope across all down days is weaker: t 1.94 on 7837 days.
- F7: The rebound is uneven by coin and by year. By coin it is strongest on XMR, with a slope t of 3.53 and +0.88 % after big falls (t 4.09). By year it is clear in 2020 and 2021 (+1.45 % and +1.36 %, t about 4.1–4.2) and near 0 in 2019, 2022, 2024 and 2025.
- F8: Both one-day moves are large next to cost, but they cover one day, not 5. The +0.94 % weekend move and the +0.60 % rebound are 4.9 and 3.2 times the backtest's 0.19 % round trip. Across up to ~30 angles examined, F3 and F5 stand out most clearly; F6 is weaker.
