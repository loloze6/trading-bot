---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
line: 7.d not profitable
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The heavier a coin's Saturday-Sunday volume against its mean volume over the preceding five weekdays, the further the coin continues its weekend move over the next 5 days.
Consequence: Weekend volume against the weekdays grades how strongly to follow every weekend move into the following week, with light-volume weekends leaning toward a fade.
Why:
- F2: The weekend move keeps extending well past the 48-hour hold. On the 463 Sunday-23:00 cases the signed return is +1.15 % at 48 h (t 2.65) and +2.13 % at 120 h (t 3.44). The increment from 48 to 120 h is +0.93 % (t 1.96, 453 cases). On the volume-gated weekends the unusual move doubles from +1.14 % at 48 h (t 2.49, 432 cases) to +2.37 % at 120 h (t 3.74, 422 cases).
- F5: Across all 2,219 Sunday-23:00 weekends, ungated, the effect is graded by weekend volume against the weekdays. The unusual 120 h move by volume-ratio quintile goes from −0.97 % (t −1.84) in the lowest to +2.46 % (t 3.72) in the highest. The ungated weekends together show nothing (u120 −0.08 %, t −0.30, 1797 cases).
- F6: Inside the gated cases, the size of the weekend move does not grade the outcome. The 48 h move by |move| quartile is +0.02 %, +2.81 %, +0.86 %, +0.81 %. Across all weekends, by vol-scaled move quintile, it is flat at about +0.4 % except −0.58 % in the fourth.
