---
line: 7.b inconclusive
backtest: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins_4h
idea tested: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4188 USD
---
## Findings
- **F1:** The supporting check could not be run because the forecast saturates. 95.7 % of the 258 cases sit at the cap of 20 (median 20, 25th percentile 20), so the median split put all 256 cases in the lower half and none in the upper half. The test passed its main measure (+4.47 %, t 2.56) and is inconclusive for this mechanical reason, not for lack of cases.
- **F2:** Inside the tested cases, the size of the raw forecast (fall depth times 90-day rise) does not grade the move. By raw tercile, the unusual move is +4.6 % (t 1.96), +4.9 % (t 1.41) and +3.6 % (t 1.19) from low to high, and the Spearman correlation of raw forecast with unusual move is −0.026 over 258 cases.
- **F3:** The fall-depth grading runs against the idea while the 90-day return is positive. Among the 261 panic-fall cells with a rising 90-day return, the unusual move falls from +5.6 % (shallow, n 85, t 1.76) to +3.9 % (mid, n 72, t 1.67) to +1.5 % (deep, n 33, t 0.78).
- **F4:** The 90-day trend is what separates panics that rebound from panics that do not. Among the 490 panic-fall cells of the panic regime, those with a rising 90-day return earn +3.97 % unusual move over 14 days (n 261, t 2.31). Those without earn +0.29 % (n 229, t 0.25).
- **F5:** The 90-day rise itself grades upward, but the evidence is thin. On the 46 cases where the 540-bar return could be measured inside the window, the unusual move is +1.2 %, +1.4 % and +7.8 % from the smallest to the largest rise tercile (t 0.66, 0.74, 0.79).
- **F6:** The effect is concentrated in recent years. Tested cases earn +6.3 % (t 2.18, n 42) in 2023, +12.0 % (t 3.30, n 56) in 2024 and +11.0 % (n 29) in 2025, against −20.8 % in 2018 (n 6) and roughly zero in 2019–2022 (between −1.0 % and +1.1 %, 125 cases). The effect is present in only part of the data, and the market's own regime drowns it in the earlier years.
- **F7:** The size is far above cost. The unusual move of +4.47 % per case (strength 0.198) is 20 times the 0.22 % cost of a trade, so the book's weakness does not come from cost. It comes from the missing grading and from the years where the move is absent.

## Ideas
- `027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins.b1_panic-rebound-graded-by-uptrend` (from F2, F3, F4, F5, F7): Among 24-hour stretches where a coin's range is several times its 30-day average and the coin falls over that stretch, the larger the coin's 90-day return, the higher its return over the next 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
