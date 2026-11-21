---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_volatile-settlement-move-reverses
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.d1_volatile-settlement-move-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 24 hours after each funding settlement runs opposite to the return over the 2 hours before it, only while the coin's 24-hour volatility is high against its 30-day average. The move back grows faster than the pre-settlement move itself, so the largest 2-hour moves into settlement, in the most volatile markets, are followed by moves back of several tenths of a percent.
Consequence: A trader would fade only the largest pre-settlement moves made in strongly volatile markets and hold each bet about a day, so that the move back covers a round trip several times over instead of half of it.
Why:
- F2: Across all cases, the move in the forecast's direction is 9.6 bps over 8 hours (t 4.05, 20,203 cases). The cost of a round trip is 19 bps, so the average case pays only half its trade, as the idea's size of 0.6 times the cost also shows.
- F3: The move back is concentrated in the largest pre-settlement moves. The top decile by size of the 2-hour move (a mean move of 486 bps) is followed by 48.8 bps over 8 hours and 78.8 bps over 24 hours, and deciles 7 to 8 (169 to 242 bps) by 12.7 to 19.3 bps over 8 hours. The bottom seven deciles (moves of 7 to 125 bps) give -5.3 to +7.2 bps over 8 hours and mostly negative values over 16 and 24 hours.
- F4: The same holds by forecast size: forecast deciles 0 to 4 give -4.3 to +9.9 bps over 8 hours and -25 to -2 bps over 24 hours. Deciles 6 to 9 give 15 to 32 bps over 8 hours and 20 to 58 bps over 24 hours (top decile 57.9 bps).
- F5: Volatility carries the effect only at its top. The quintile whose 24-hour volatility is 2.4 times its 30-day average gives 22.3 bps over 8 hours and 35.9 bps over 24 hours. The quintiles at 1.0 to 1.3 times give 0.7 to 7.5 bps over 8 hours and -13 to 0 bps over 24 hours, so the "at or above average" regime admits mostly cases that do not pay.
- F6: In the largest cases the move back lasts beyond 8 hours. The top decile gives 48.8 bps at 8 hours and 78.8 bps at 24 hours, and the top forecast decile 31.6 then 57.9 bps. Over all cases, though, 16 hours (-1.6 bps, t -0.50) and 48 hours (t 1.18) show no move.
