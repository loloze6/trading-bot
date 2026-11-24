---
line: 7.g patterns
backtest: 031-02.g1.b1_deep-down-day-bounce-more-coins_1d
idea tested: 031-02.g1.b1_deep-down-day-bounce-more-coins
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4055 USD
---
## Findings
- **F1:** The book never took a position: all 36768 recorded bars sit in regime "unknown" and 0 bars have a non-zero forecast. Recomputed from the prices, 1937 coin-days rank in the bottom 5 % of the coin's past daily returns, so the regime gate never fired on days where it should have. The verdict's 0 % and the book's zeros come from this, not from the market.
- **F2:** The day's range relative to the coin's past 20-day average range is followed by a larger rise over the next 3 days. Its slope on the 3-day excess return in usual moves is +0.107, t 2.98, over 10799 non-overlapping cases on 938 days. The sign is the same at 1 day (+0.050, t 1.41, 2634 days) and 5 days (+0.072, t 1.07, 544 days). It is the only reading near t 3 among about 60 looked at, so it is borderline after allowing for the search.
- **F3:** The tested idea's own situation shows no reliable bounce. After days below −3 usual moves the next-day excess is +0.89 %, t 0.74, over 99 days. After deep-fall days closing near the low it is +0.51 %, t 1.38, over 480 days. The graded slope on fall × close-near-low is +0.052, t 0.90, at 1 day, and turns negative at 3 days (t −0.82) and 5 days (t −0.19).
- **F4:** After falls below −2 usual moves the next-day excess was positive in 2020 (+4.14 %, t 1.89) and 2021 (+2.59 %, t 1.28). It was near zero or negative in 2022–2024 (−0.29 %, −0.10 %, −0.30 %, all |t| < 0.25), so any bounce is not stable across years.
- **F5:** The brief's pattern is not in the bars. On flat-bodied days (body under 25 % of the range), the 3-day excess return against the prior 3-day run is −0.32 % (t −0.49, 293 days) when the range is wide. It is −0.08 % (t −0.27, 462 days) when the range is narrow. The middle third, +0.82 % with t 2.17, stands alone and is not graded.
- **F6:** The other angles showed nothing that clears chance. By weekday, no |t| reaches 1.8 (Friday +0.26 %, t 1.73). By volatility quintile all |t| are below 1. The 1-day slope on the day's own move is −0.0045, t −0.22, with no year beyond |t| 1.4. The past 3-day return bins show no |t| above 1.2.

## Ideas
- `031-02.g1.b1.g1_wide-range-day-precedes-rise` (from F2, F5, F6): The wider a coin's daily high-to-low range is relative to its average daily range over the past 20 days, the more the coin rises over the next 3 days, whichever way that day closed.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
