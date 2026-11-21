---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_volatile-settlement-move-reverses
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.d1_volatile-settlement-move-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 24 hours after each funding settlement runs opposite to the return over the 2 hours before it, and the move back is larger the larger that 2-hour move is in percentage terms, whatever the coin's usual size of move.
Consequence: A trader would fade settlement moves by their raw size, which naturally favours the coins and periods where these moves are large enough to pay a round trip, and would refuse the small moves typical of quiet coins.
Why:
- F3: The move back is concentrated in the largest pre-settlement moves. The top decile by size of the 2-hour move (a mean move of 486 bps) is followed by 48.8 bps over 8 hours and 78.8 bps over 24 hours, and deciles 7 to 8 (169 to 242 bps) by 12.7 to 19.3 bps over 8 hours. The bottom seven deciles (moves of 7 to 125 bps) give -5.3 to +7.2 bps over 8 hours and mostly negative values over 16 and 24 hours.
- F6: In the largest cases the move back lasts beyond 8 hours. The top decile gives 48.8 bps at 8 hours and 78.8 bps at 24 hours, and the top forecast decile 31.6 then 57.9 bps. Over all cases, though, 16 hours (-1.6 bps, t -0.50) and 48 hours (t 1.18) show no move.
- F7: BTC shows no reversal: -0.8 bps over 8 hours and -4.3 bps over 24 hours, on pre-moves averaging 90 bps. The other coins give 6.8 to 16.5 bps over 8 hours on pre-moves of 117 to 169 bps, so the coins with larger settlement moves reverse more.
