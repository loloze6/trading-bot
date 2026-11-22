---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days
line: 7.d not profitable
backtest: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, the 20-day return after a one-day rise of several usual daily moves (its day's return over the standard deviation of its last 20 daily returns) is lower when its 90-day return is negative than when it is positive, and the gap widens as the rise gets larger, only while its 30-day return is also negative, more so the more negative its 30-day return.
Consequence: A trader would fade a sharp bounce in a 90-day faller only while the coin is still falling over the past month, and more firmly the steeper that recent fall, and would refuse the fade once the month's return has turned up.
Why:
- F1: The short side carries the losses. Bars held short summed −2.44 in bar gains over 8081 bars, against +12.29 over 8577 bars held long. The 885 short trades lost 13.3 % net on average (median −8.1 %, 30.5 % winners), while the 675 long trades made +8.2 % (47 % winners).
- F2: The book fades bounces while the coin keeps rising. The coin's mean next-bar return was +0.12 % on bars held short, higher than the +0.09 % on bars held long, so the shorts were on the wrong side of the coin's own drift.
- F3: The short side won only in windows where the coins kept falling and lost in windows where they recovered:
- F5: The falls are deep. The chained book fell 86 % at its deepest (−80 % by w16, −86 % in w17), which gives a Calmar of 0.14. The book is almost never flat (4.2 % of bars), because trades last 35 to 42 days on average, so a short taken after one bounce stays on through the recovery that follows.
