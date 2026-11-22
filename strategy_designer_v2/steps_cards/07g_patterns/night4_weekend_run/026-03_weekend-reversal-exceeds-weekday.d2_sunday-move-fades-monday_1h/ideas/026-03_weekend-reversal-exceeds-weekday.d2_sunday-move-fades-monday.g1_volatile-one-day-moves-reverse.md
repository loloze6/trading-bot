---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return is followed by an opposite move over the next 24 hours on any day of the week, and the higher the coin's 7-day volatility and the larger that 24-hour move, the larger the reversal.
Consequence: If confirmed, a trader can fade one-day moves every day rather than once a week, mostly when the coin is volatile, giving about seven times the cases the Monday bet gives; if rejected, it is a reason to refuse daily fades in calm or volatile markets alike.
Why:
- F1: On a 24-hour grid covering every start hour and every day, the next 24 hours reverse the past 24-hour return (slope −0.101 of a usual move per usual move, t −11.6, 13030 non-overlapping cases), and the reversal is the same size whether the past 24 hours cover the weekend or not (−0.105, t −5.4, 3764 cases, against −0.100, t −10.3, 9266 cases); the brief's own falsifier, that weekday moves of the same size are reversed just as much, is what the bars show.
- F2: The 24-hour reversal sits almost entirely in the coin's most volatile third of 7-day volatility (slope −0.151, t −10.9, 4344 cases), with none in the middle third (+0.006, t 0.4, 4341) or the calmest third (+0.027, t 1.3, 4345); inside the most volatile third it is the same on weekend and weekday cases (−0.151, t −4.8, 1245, against −0.152, t −9.8, 3099).
- F3: The 24-hour reversal holds on every coin (slopes −0.077 to −0.151, t −3.5 to −6.8) and in all 8 years (slopes −0.005 to −0.181), with t ≤ −2 in 6 of them (weakest 2024, t −0.2; 2022, t −1.2).
- F4: On the tested Monday 00:00 cases alone, the reversal also appears only in the most volatile third (slope −0.192, t −4.0, 676 cases; fade mean +0.257 of a usual move), against +0.011 (t 0.2) and +0.046 (t 0.8) in the other two thirds; its slope was positive in only 11 of 24 windows.
- F7: Over 48 hours there is no reversal of the past 48-hour return on any start day (slopes −0.021 to +0.053), and the 48-hour reversal of the 24-hour return is significant only from Monday (−0.179, t −4.6); otherwise the effect is spent within the first day.
