---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.g2_late-evening-rebound-after-falls
line: 7.g patterns
backtest: 017-04_postsettle-decline-after-downtrend.g2_late-evening-rebound-after-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin, the return over the 2 hours from 21:00 UTC is positive, and the deeper its fall in the hour before 21:00, relative to its 24-hour volatility, the larger that rise.
Consequence: A trader would hold a long into the late-evening hours chiefly after a down hour, and size it by how sharp that hour's fall was.
Why:
- F2: The 21:00 UTC lift does not depend on a 3-day fall. The excess 2-hour return from 21:00 was positive for all six coins, from 7.3 bp (t 2.6–4.1, about 2,900 cases each). By 72-hour-return tercile it was 9.5 bp (t 4.2) after falls, 2.2 bp (t 1.6) in the middle and 13.2 bp (t 6.8) after rises, so the idea's fall gradient does not explain it.
- F3: Inside the 21:00 cases, the lift depends on the last hour's move scaled by its 24-hour volatility. The 2-hour excess was 17.9 bp (t 8.9) after the most negative tercile, 8.9 bp (t 5.0) in the middle and −1.9 bp (t −1.0) after the most positive tercile (about 5,660 cases each).
- F1: The book lost because of fees, not because the signal failed. Summed bar by bar, the gross position return was 4.40 against 9.15 in fees, and fees were larger for every coin (BTC 0.99 vs 1.47, ZEC 0.47 vs 1.31). Active bars earned only 1.79 bp gross at a mean allocation of 0.34.
