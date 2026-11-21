---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-03_thin-cloud-upward-breakout.b2_cloud-breakout-after-a-fall
line: 7.d not profitable
backtest: 021-03_thin-cloud-upward-breakout.b2_cloud-breakout-after-a-fall_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily close that crosses up from below a coin's Ichimoku cloud to above it, the coin rises over the next 26 days, and the smaller the coin's rise over the past 26 days before the cross, the larger the rise, so a cross after a modest rise still carries most of it and only a cross after a large run-up carries little.
Consequence: Every upward cloud cross is a reason to go long for the next few weeks, sized larger when the past 26 days rose little or fell, and a cross after a large 26-day run-up is a reason to take little or none of that trade.
Why:
- F1: The book is almost never in the market, and that is why the mean daily return (1.0e-05), the Calmar (0.10) and the trades per day (0.0013) fail: it made 31 trades over 17,405 coin-days and held a position on 4.0 % of days, while cost was never the obstacle (the total move of +9.77 % per case is 50.6 times the 0.19 % cost of a trade).
- F2: The book traded so rarely because most crosses came after a rise, and the plan sized only crosses after a fall: of 163 upward cloud crosses with a known 26-day past return, 137 came after a rise and 26 after a fall, so only 34 had a positive forecast and 20 reached a forecast of 2 or more.
- F3: Upward crosses in general are followed by a larger rise than the coin's normal drift, and the plan threw that move away: counted once per 26-day grid cell, the 152 crosses had a mean unusual move of +4.9 % over 26 days (t 1.55, strength 0.146), and the 111 crosses that came after a rise had +4.7 % (t 1.23, overlapping cases).
- F4: What lowers the move after a cross is a large prior rise, not the lack of a fall: by tercile of the prior 26-day return, crosses after a fall or a flat stretch had +9.6 % (t 1.35, 36 cases), the middle tercile +10.9 % (t 1.14, 36 cases), and the largest prior rises −2.4 % (t −0.68, 36 cases).
- F5: Grading by the depth of the fall is not supported: in step 5 the larger-fall half minus the smaller-fall half was −7.9 %, and the fall and middle terciles above differ by only −1.3 %.
