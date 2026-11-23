---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: In the hours around midnight UTC, a coin's 2-hour move reverses over the next 8 hours on both sides. The larger the 2-hour move against the coin's usual 2-hour move, the larger the opposite move, and the largest after a rise.
Consequence: A trader fades the midnight 2-hour move, up or down, sized by its size, where the per-case move is large enough to beat the cost.
Why:
- F1: Around the midnight UTC settlement (bars closing at 00:00–02:00 UTC), the 2-hour move reverses over the next 8 hours on both sides and in proportion to its size. The lowest decile of the scaled 2-hour return (z −2.74) is followed by +22.7 bp drift-removed (strength +0.078). The highest decile (z +2.85) is followed by −33.9 bp (strength −0.121), monotone across deciles, about 4,740 cases per decile. At the 01:00 close, the product of the reversal and the move is positive in all 6 coins (t 2.0 to 2.8, about 2,650 cases each). It is positive in 2018–2021 and 2023 (t 2.3 to 5.5) and faded in 2022, 2024 and 2025 (t 0.1, −0.3, 0.9).
- F2: The rise side of the midnight reversal is the strongest single reading in the hour scan. After a 2-hour rise, the 8-hour product t is −6.81 at the 01:00 close, −5.14 at 02:00 and −3.89 at 00:00 (about 7,500–8,000 cases each). This short side is not in the tested long-only idea, and its top-decile move (−33.9 bp) is about 1.8 times the 0.19 % trade cost.
