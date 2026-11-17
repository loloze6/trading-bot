---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days (Monday to Wednesday), and the larger the weekend fall relative to the coin's usual daily move over the past 60 days, the larger the rise.
Consequence: A weekend fall is a reason to stay long from Sunday's close through Wednesday's close, sized by the fall, rather than for Monday alone.
Why:
- F1: The book is flat on about 88% of days: only 12.2% of coin-days carry a non-zero book return, the mean position on active Sundays is 0.35, and every gain comes from Mondays (book mean 8.2e-4 on weekday 0, near 0 on the other days), so the mean daily return is 1.2e-4, under the 5e-4 needed.
- F2: The rebound after a weekend fall runs past the one Monday bar the book holds. On active Sundays the excess return is +0.14% over 1 day (t 1.20, n 2667), +0.24% over 2 days (t 1.62), and +0.65% over 3 days (t 3.37, n 2617).
- F3: Split by day after any weekend fall (n 2125), Wednesday adds as much as Monday: +0.37% Monday (t 2.87), +0.23% Tuesday (t 2.13), +0.40% Wednesday (t 3.35), and +1.00% over the 3 days (t 4.80).
- F5: The size grading holds for falls but not for small ones. By forecast tercile the Monday excess return is -0.35% (low), -0.14% (mid) and +0.89% (high). By weekend-z sextile the 3-day excess return is +1.70% for the largest falls, +1.25% for the next, and +0.07% for the smallest.
