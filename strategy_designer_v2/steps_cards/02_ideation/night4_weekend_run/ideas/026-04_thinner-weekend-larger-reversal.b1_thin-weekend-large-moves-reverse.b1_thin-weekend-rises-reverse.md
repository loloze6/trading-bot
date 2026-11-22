---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse
line: 7.b inconclusive
backtest: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's Saturday-Sunday rise is partly reversed over the next 48 hours (Monday and Tuesday), only while its weekend volume is lower than its mean volume over the preceding five weekdays; the larger the weekend rise and the lower the weekend volume against the weekdays, the larger the share reversed.
Consequence: After a large weekend rise on volume far below the week's, a trader shorts the coin into Tuesday, and refuses that short when the weekend traded nearly as heavily as the week or when the weekend move was a fall.
Why:
- F2: The reversal is graded by how thin the weekend was and shows only in the thinnest weekends. In the thinnest octile (weekend mean volume roughly a third or less of the weekdays', log ratio below -1.13) the 48-hour strength is 0.131 (t 2.68, 293 cases), an unusual move of 0.79 % and a total of 0.80 % in the reversal direction, which is 4 times the 0.19 % cost of a trade. Regressing the 48-hour reversal strength on thinness gives a slope t of 3.98.
- F4: Inside the thinnest weekend quartile, the reversal grows with the move's size. Small moves show a 48-hour strength of -0.017 (t -0.30), mid moves 0.107 (t 1.56) and large moves 0.224 (t 2.84, 196 cases), a 1.38 % unusual move per case, about 7 times the cost.
- F5: Inside the thinnest weekend quartile, the reversal comes from weekend rises. Up weekends show a 48-hour strength of 0.200 (t 3.55, 291 cases), an unusual move of 1.29 % and a total of 1.01 %. Down weekends show 0.010 (t 0.18, 295 cases).
- F6: The effect is specific to weekends. Wednesdays with equally thin volume relative to their own preceding five days do not reverse: the thinnest midweek quartile shows a 48-hour strength of 0.029 (t 0.71, 587 cases).
- F7: Inside the thinnest weekend quartile the reversal is positive in 5 of 6 coins at 48 hours, with ETH at 0.217 (t 2.26) and XRP at 0.172 (t 2.18); ZEC is the exception at -0.130 (t -1.09). It is positive in 6 of 8 years, with 2021 (-0.048) and 2023 (-0.026) the exceptions, so it is broad but not uniform.
