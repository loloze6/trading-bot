---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal
line: 7.b inconclusive
backtest: 026-04_thinner-weekend-larger-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's Saturday-Sunday move is partly reversed over the next 48 hours (Monday and Tuesday), only while its weekend volume is lower than its mean volume over the preceding five weekdays; the larger the weekend move and the lower the weekend volume against the weekdays, the larger the share reversed.
Consequence: After a large weekend move on volume below the week's, a trader leans against the move into Tuesday, and refuses that trade when the weekend traded as heavily as the week.
Why:
- F1: The pooled result is near zero because the effect has opposite signs by weekend volume, and the two cancel. On my 1,803 Sunday-close cases, the 48-hour unusual return regressed on the weekend's 48-hour move (in the coin's own move units) gives a slope of 0.00045 (t 0.26). Adding the interaction of the weekend move with the log weekday-to-weekend volume ratio gives a strongly negative interaction (−0.018, t −6.75), so reversal grows with thinness.
- F2: The reversal is graded across volume-ratio quintiles. The slope of the next 48 hours on the weekend move is +0.0094 (t 3.06) in the quintile where the weekend was busier than the weekdays (median ratio 0.81). It turns negative in the higher quintiles: −0.0044 (t −1.26), −0.0090 (t −2.12), −0.0064 (t −1.49), and −0.0192 (t −3.40) at a median ratio of 3.22.
- F3: Weekends that traded heavier than their weekdays carry the largest moves and these moves continue, which is what drags the test's supporting mean to −0.29 % per case. In the thickest volume tercile (mean absolute weekend move 5.4 %), the move in the reversal direction over the next 48 hours averages −1.07 % (t −3.19, 631 cases). In the thinnest tercile (mean absolute move 2.3 %), it averages +0.50 % (t 2.08, 631 cases).
- F4: Inside thin weekends the reversal sits in the largest moves. In the thinnest volume tercile, the 48-hour reversal is +1.36 % for the largest third of weekend moves (t 2.87, 211 cases), against +0.10 % (t 0.30) and +0.05 % (t 0.11) for the small and middle thirds.
- F5: The thin-weekend reversal is broad but not uniform across coins and years. In the thinnest tercile the slope is negative for 5 of 6 coins (LTC −0.025, t −2.24; ETH −0.015, t −1.80; BTC −0.0097, t −1.56; ZEC alone +0.009 on 32 cases). It is negative in 7 of 8 years (2024 −0.025, t −2.44; 2022 −0.013, t −2.18; 2023 alone +0.009, t 0.94).
