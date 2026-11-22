---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling
line: 7.g patterns
backtest: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The higher a coin's traded volume over the last day against its volume at the same weekday and hours over the past four weeks, the more the coin rises over the next one to three days.
Consequence: A trader treats volume above its usual level for that time of the week as a reason to hold the coin long over the next days, and volume below it as a reason to stay out.
Why:
- F1: Each coin rises more over the next 3 days the larger its last day's volume is against its 30-day average volume: the pooled slope of the drift-adjusted 3-day strength on the log volume ratio is +0.103 with t 4.91 over 5004 non-overlapping cases, it is positive in all six coins (t from 0.96 for XMR to 3.49 for XRP) and in all eight years, and it is positive in 75 % of the 24 windows.
- F3: Weekly seasonality does not explain the effect, and it shows over a shorter horizon too: with weekday dummies and the 3-day return in the same regression, the volume slope stays at +0.075 (t 3.40); against a same-weekday, same-hour volume baseline from the past four weeks the slope is +0.067 (t 3.65, 5292 cases); over the next 1 day alone the slope is +0.095 (t 4.45).
- F4: The effect does not depend on the direction of the recent move, which goes against the brief's fading-volume reversal: the slope is +0.098 (t 3.26, 2553 cases) after a rising 3-day return and +0.107 (t 3.61, 2451 cases) after a falling one, and volume times the sign of the move has a slope of -0.012 (t -0.58).
