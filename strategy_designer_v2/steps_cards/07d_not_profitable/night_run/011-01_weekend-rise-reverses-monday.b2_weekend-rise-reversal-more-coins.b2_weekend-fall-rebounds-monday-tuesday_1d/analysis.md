---
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3798 USD
---
## Findings
- **F1:** The book is flat on about 88% of days: only 12.2% of coin-days carry a non-zero book return, the mean position on active Sundays is 0.35, and every gain comes from Mondays (book mean 8.2e-4 on weekday 0, near 0 on the other days), so the mean daily return is 1.2e-4, under the 5e-4 needed.
- **F2:** The rebound after a weekend fall runs past the one Monday bar the book holds. On active Sundays the excess return is +0.14% over 1 day (t 1.20, n 2667), +0.24% over 2 days (t 1.62), and +0.65% over 3 days (t 3.37, n 2617).
- **F3:** Split by day after any weekend fall (n 2125), Wednesday adds as much as Monday: +0.37% Monday (t 2.87), +0.23% Tuesday (t 2.13), +0.40% Wednesday (t 3.35), and +1.00% over the 3 days (t 4.80).
- **F4:** Weekend rises reverse just as strongly, and the book ignores them. After a weekend rise the 3-day excess return is -1.00% (t -5.36, n 2186), with -0.52% Monday (t -4.33) and -0.61% Tuesday (t -5.50). On the Sundays the book left flat, the 2-day excess return is -1.07% (t -6.93, n 2584).
- **F5:** The size grading holds for falls but not for small ones. By forecast tercile the Monday excess return is -0.35% (low), -0.14% (mid) and +0.89% (high). By weekend-z sextile the 3-day excess return is +1.70% for the largest falls, +1.25% for the next, and +0.07% for the smallest.
- **F6:** The book's gain is thin in every year. Its mean daily return per year ranges from -1.7e-4 (2018) to 6.3e-4 (2020), and it is negative in 2018, 2022, 2023 and 2025.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.d1_weekend-fall-three-day-rebound` (from F1, F2, F3, F5): A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days (Monday to Wednesday), and the larger the weekend fall relative to the coin's usual daily move over the past 60 days, the larger the rise.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.d2_weekend-moves-reverse-both-ways` (from F1, F3, F4, F5): A coin's weekend move (its Saturday-to-Sunday close-to-close return, relative to its usual daily move over the past 60 days) is reversed over the next 3 days: after a weekend rise the coin falls and after a weekend fall it rises, and the larger the weekend move, the larger the reversal.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
