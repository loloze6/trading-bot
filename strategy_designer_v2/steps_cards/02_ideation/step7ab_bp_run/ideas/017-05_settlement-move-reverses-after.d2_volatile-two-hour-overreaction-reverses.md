---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's large 2-hour move, made while its 24-hour volatility is high, is followed by a move the opposite way over the next 8 hours, at any hour of the day. The larger the 2-hour move against the coin's usual 2-hour move, the larger the move back.
Consequence: The reversal can be traded as a general overreaction in volatile markets rather than a funding-clock effect, which gives the trader roughly twice as many chances to take it.
Why:
- F2: The reversal is carried almost entirely by the largest pre-settlement moves. Over 2 hours it is 11.45 bps for the top fifth of 2-hour moves (mean size 267 bps), against -1.16 to 4.09 bps for the other four fifths. Over 8 hours it is 18.49 bps for the top fifth, against 0.6 to 4.9 bps for the rest. The book trades every settlement, sized in proportion, so most of its trades are in fifths that earn 0 to 4 bps.
- F3: High recent volatility adds to the effect. Settlement bars in the top fifth of both 2-hour move and 24-hour volatility reverse by 20.6 bps over 2 hours, 24.1 bps over 4 hours and 37.4 bps over 8 hours (t 5.01, 4.51 and 5.06; 4,757 cases). This group covers a round trip only when held about 8 hours, not 2.
- F4: Large moves in calm markets keep going instead of reversing. In the lowest two fifths of 24-hour volatility, the top fifth of pre-settlement moves is followed by -8.7 and -11.9 bps over 2 hours, and by -13.3 and -7.4 bps over 8 hours. In the top fifth of volatility the same moves reverse by +20.6 and +37.4 bps.
- F5: The reversal is not tied to funding settlement. At the non-settlement hours 04, 12 and 20 UTC, the top fifth of 2-hour moves reverses by 15.73 bps over 2 hours, against 11.45 bps at settlements, and by 13.04 against 18.49 bps over 8 hours. 12 UTC shows the largest reversal of any hour, 31.2 bps over 2 hours.
- F6: After large moves the reversal keeps building beyond 2 hours. For the top fifth, it grows from 17.0 to 51.7 bps between 2 and 24 hours at 00 UTC, and from 10.5 to 16.3 bps between 2 and 8 hours at 16 UTC.
