---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin rises over the two hours from 20:00 to 22:00 UTC, and the more it fell over the preceding 24 hours, the larger that rise.
Consequence: If confirmed, it is a reason to buy a falling coin into the UTC evening or to delay a sale until after it, though the move per case (about a tenth of an hourly move per hour) is smaller than a trade's cost on its own; if rejected, it is a reason to ignore the hour of day.
Why:
- F5: Hourly returns from 20:00 and 21:00 UTC are positive (+0.053 and +0.043 of an hourly standard deviation, t 6.9 and 5.9, about 17400 bars each; Welch t 8.3 against all other hours). The pattern holds on all 6 coins (t 3.0 to 4.4), on every weekday (t 2.4 to 4.0), in 7 of 8 years (2022: −0.021, t −1.5) and in 110 of 144 coin-windows. With 24 hours examined, it still clears any reasonable bar for chance.
- F6: The 20:00–22:00 UTC rise is graded by the coin's prior 24-hour return on the falling side: +0.113 (t 6.8) after the lowest fifth, then +0.041, +0.022 and +0.010 through the fourth fifth. The highest fifth breaks the pattern (+0.055, t 4.0).
