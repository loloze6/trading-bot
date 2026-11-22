---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound
line: 7.g patterns
backtest: 024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a 4-hour run that is large relative to the coin's typical 4-hour move over the past 30 days, in either direction, the coin rises over the next three days. The rise is larger the more the volume of the last 8 hours exceeds its 5-day average.
Consequence: A trader buys after big runs either way that come with heavy volume, more the heavier the volume, and refuses the same runs on fading volume.
Why:
- F2: Volume works against the brief. Deep down streaks (at least 2 usual moves) are followed by +2.17 % (t 3.72, 240 cases) when the last 8 hours' volume is in the top tercile against its 5-day mean, but only +0.30 % (t 0.47, 240 cases) when volume is fading. Deep up streaks show the same split: +2.26 % (t 2.92, 259 cases) with heavy volume against −0.31 % (t −0.59, 258 cases) with fading volume. So the coin rises after large runs in either direction when volume is heavy, and does not give back after fading volume.
- F1: The rebound is concentrated in the deepest down streaks. With the coin's 30-day return positive, streaks of more than 5 usual moves are followed by +6.45 % unusual 18-bar moves (t 4.23, 47 cases) and streaks of 3–5 usual moves by +2.21 % (t 2.13, 89 cases), while streaks of 0–3 usual moves give between −0.20 % and +0.23 % (all |t| < 0.3). With the 30-day return not positive, the deepest streaks still give +1.84 % (t 1.78, 72 cases).
