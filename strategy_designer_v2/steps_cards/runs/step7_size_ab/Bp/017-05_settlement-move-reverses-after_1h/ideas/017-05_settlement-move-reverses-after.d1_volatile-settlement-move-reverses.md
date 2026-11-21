---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 8 hours after each funding settlement time runs opposite to the return over the 2 hours before it, only while the coin's 24-hour volatility is high. The larger the pre-settlement move against its usual size, and the higher that volatility, the larger the move back.
Consequence: A trader would fade only the large pre-settlement moves made in volatile markets and hold the bet for most of a funding interval, so that a move of 20 to 40 bps can pay a 22 bps round trip.
Why:
- F1: The book loses because each bet is far smaller than its cost. On settlement bars the forecast-signed move over 2 hours is +2.8 to +6.4 bps per coin, and +5 bps per case in the verdict, against a round trip of 22 bps. The book made 62,957 trades, about 3.6 a day, which lost -0.10 % each before fees and -0.20 % after. As a result the book's mean daily return is -0.23 %, while holding the coin earned +0.12 % a day.
- F2: The reversal is carried almost entirely by the largest pre-settlement moves. Over 2 hours it is 11.45 bps for the top fifth of 2-hour moves (mean size 267 bps), against -1.16 to 4.09 bps for the other four fifths. Over 8 hours it is 18.49 bps for the top fifth, against 0.6 to 4.9 bps for the rest. The book trades every settlement, sized in proportion, so most of its trades are in fifths that earn 0 to 4 bps.
- F3: High recent volatility adds to the effect. Settlement bars in the top fifth of both 2-hour move and 24-hour volatility reverse by 20.6 bps over 2 hours, 24.1 bps over 4 hours and 37.4 bps over 8 hours (t 5.01, 4.51 and 5.06; 4,757 cases). This group covers a round trip only when held about 8 hours, not 2.
- F4: Large moves in calm markets keep going instead of reversing. In the lowest two fifths of 24-hour volatility, the top fifth of pre-settlement moves is followed by -8.7 and -11.9 bps over 2 hours, and by -13.3 and -7.4 bps over 8 hours. In the top fifth of volatility the same moves reverse by +20.6 and +37.4 bps.
- F6: After large moves the reversal keeps building beyond 2 hours. For the top fifth, it grows from 17.0 to 51.7 bps between 2 and 24 hours at 00 UTC, and from 10.5 to 16.3 bps between 2 and 8 hours at 16 UTC.
