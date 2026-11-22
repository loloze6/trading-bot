---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days while its volume over those 3 days was low relative to its 30-day average, it keeps falling over the next 3 days; the lower the volume relative to its average, the larger the further fall.
Consequence: A trader should refuse to buy a rebound after a quiet, low-volume 3-day fall, and can expect the decline to continue.
Why:
- F6: Contrary to the brief, falls on fading volume keep falling. Over 3-day falls, the lowest tercile of 3-day volume against its 30-day average is followed by -0.109 usual moves (t -3.71, 898 cases). The highest tercile is followed by +0.022 (t 0.57).
- F7: The tested down-streak idea is tiny. Its unusual move is +0.05 % per case (strength 0.007, t 0.48, 5674 cases). On the bars, the most extreme down streaks (mean -3.4 usual moves) are followed by +0.075 (t 2.28), but the next quintile is followed by -0.089 (t -3.06), so the effect is not graded. A Sunday effect (-0.150, t -4.05 on the base grid) flips sign across grid offsets (+0.115 to -0.150), so it is not a finding.
