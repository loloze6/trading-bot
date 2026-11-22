---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall, measured in its usual move over the past 30 days, and the heavier its volume over that day against its 30-day average, the larger its rise over the next three days.
Consequence: A trader buys heavy-volume capitulation days, not quiet falls, sizing up with both the fall and its volume.
Why:
- F3: After the largest one-day falls (the 6-bar move in usual moves), the coin's next 3 days beat its normal drift: +1.43 % (t 2.80, 265 non-overlapping cases) in the bottom 5 %, and +1.11 % (t 3.21, 530 cases) in the bottom 10 %. The middle vigintiles lie between -1.0 % and +0.4 %.
- F4: Inside those bottom-10 % one-day falls, the rebound grows with the volume of the falling day, not with its fading: +2.34 % (t 3.79) in the top volume tercile, +1.21 % (t 2.07) in the middle one and -0.04 % (t -0.07) in the lowest, about 177 cases each. It is positive in five of six coins (LTC +2.18 %, t 2.61; BTC -0.30 %).
- F5: The brief's volume fade adds nothing: among the largest down-streaks, those with rising volume gave back +1.28 % over 3 days (t 2.19, 226 cases) and those with fading volume +1.20 % (t 1.72, 155 cases). The tested idea's own measure was +0.02 % (t 0.14, 4334 cases).
