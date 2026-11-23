---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr
line: 7.b inconclusive
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr_1h
instruments: BTC, ETH, LTC, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's Saturday-Sunday move continues in the same direction over the next 48 hours, the more so the heavier the weekend's volume against its mean over the preceding five weekdays.
Consequence: The heavier a weekend's volume against the prior weekdays, the stronger the reason to follow the weekend move into Monday and Tuesday, whatever the move's size.
Why:
- F1: The test missed its bar only on the size check, because the move does not grow with |forecast|: the 348 cases rose by +1.63 % (t 3.15), but across |forecast| quintiles the unusual move was +1.51 %, +2.73 %, −0.21 %, +2.63 % and +1.53 %; above-median minus below-median was −0.25 %, and the Spearman correlation of |forecast| with the move was 0.03.
- F2: The size of the weekend move does not grade the continuation, and the largest moves continue least: across move-size quintiles of the heavy-volume cases the unusual move was +0.12 %, +3.22 %, +3.11 %, +1.11 % and +0.61 %. Over all 1,901 Sunday closes the largest-move quintile gave −0.10 % (t −0.20), and the Spearman correlation of move size with the move was −0.05. Move size is the part that ties |forecast| to the case (correlation 0.73 against 0.49 for the volume ratio), so it is what makes F1's check fail.
- F3: The weekend-to-weekday volume ratio is what grades the continuation. Over all 1,901 Sunday closes, the volume-ratio sextiles gave −0.57 % (t −1.59), −0.50 %, +0.49 %, +0.27 %, +0.34 % and +1.95 % (t 3.55, ratio 1.04 to 9.09), with a Spearman correlation of 0.09. Inside the heavy cases, the top volume quintile (ratio 1.86 to 9.09) gave +3.27 % (t 2.64, 70 cases).
- F6: Weekends on lighter volume than the weekdays show nothing: 1,552 such Sunday closes gave +0.04 % (t 0.23), so the continuation sits only where weekend volume is heavy.
