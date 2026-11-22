---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse
line: 7.d not profitable
backtest: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's Saturday-Sunday move continues over the next 96 hours when its weekend volume is higher than its mean volume over the preceding five weekdays, and the continuation is larger the larger the move and the heavier the weekend volume against the weekdays.
Consequence: A trader follows a weekend move made on heavy volume into the week instead of fading it.
Why:
- F3: Weekends traded heavily against the week continue rather than reverse. The slope on the weekend move is +0.075 (t 3.13) at 12 h and +0.175 (t 2.85) at 96 h (n 432).
- F4: Inside the thin regime the reversal holds only on the thinnest weekends. By weekend-to-weekday log volume-ratio quartile, the 48 h reversal is +0.57 % on the thinnest quartile (mean -1.20) and -0.40 %, -0.14 % and -1.04 % on the other three.
