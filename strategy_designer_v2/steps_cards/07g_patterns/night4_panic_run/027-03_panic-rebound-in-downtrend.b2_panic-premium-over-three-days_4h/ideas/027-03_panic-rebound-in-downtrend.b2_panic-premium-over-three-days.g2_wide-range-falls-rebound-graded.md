---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days
line: 7.g patterns
backtest: 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When the coin's 24-hour range is wider than its 30-day average, the larger its 24-hour fall measured in usual 24-hour moves, the higher its return over the next 3 days.
Consequence: A trader should buy wide-range sell-offs in proportion to the size of the fall, rather than waiting for an extreme range that is rare and pays less.
Why:
- F3: Among wide-range stretches (ratio at least 1.5), those with a 24-hour fall are followed by +2.72 % excess over 3 days (t 4.9, n 264), against +0.87 % (t 1.2, n 245) after a rise and +0.97 % (t 1.1, n 160) after a flat stretch.
- F4: The plan's panic level of at least 3× is past the sweet spot. For falls of at least 2 usual moves, the excess 3-day return is +1.68 % for ratio 1.5–2 (t 1.8, n 103), +4.31 % for 2–3 (t 3.5, n 38) and only +1.20 % above 3 (t 1.1, n 36), which fits the failed supporting check (−2.77 %).
- F1: Across all bars, not only panics, the coin's excess 3-day return rises steadily with the 24-hour mean bar range over its 30-day mean. It goes from −0.78 % (t −3.5, n 1389) when the ratio is at most 0.7, to −0.12 % for 0.7–1, +1.06 % for 1.5–2 (t 2.2, n 446) and +3.31 % for 2–3 (t 3.7, n 168). Regressing the 3-day excess on the log of the ratio gives a slope of 0.0148 (t 5.7, n 5436) while the scaled 24-hour return adds nothing (t −0.49).
