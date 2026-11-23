---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d1_absorption-rebound-in-stressed-markets
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d1_absorption-rebound-in-stressed-markets_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's volume on a day relative to its prior 20-day average, the larger that day's fall, and the nearer that day's close sits to its low, the more the coin rises over the next day. This holds while its 20-day volatility is high against its volatility over the past 4 months, and the more so the higher that ratio.
Consequence: A trader buys heavy-volume down days in proportion to how close to the low they ended, taking little on such days that closed back up in their range, which cuts the size carried into crash stretches like the deepest fall.
Why:
- F1: The check failed on Calmar alone (0.64 against 0.75), and the fall that sinks it is one 19-day stretch inside w16: the book lost 34.6 % (deepest fall −35.0 %) while its six coins fell 50–60 % each, the book holding about 0.19–0.64 of its value long in every coin, with a signal on 58–79 % of the coins' days. The book's other windows never fell deeper than −28.8 %.
- F3: Where the down day closed in its range carries the effect: signal days that closed in the lowest third of their range (mean close location 0.12) had a next-day excess return of +0.367 %, against +0.058 % for the rest (2838 against 5675 cases, Welch t 2.69). This held in both halves of the windows: +0.20 % against +0.06 % in w1–w12, and +0.54 % against +0.06 % in w13–w24.
- F4: Days with a low close but no signal are too rare to be an effect of their own (101 cases, excess +0.60 %; the next bin, 604 cases, gives −0.31 %). Close location belongs to the brief's own absorption-versus-last-push reading of where the day closes.
- F5: Re-weighting the tested book's positions by 1.5 × (1 − close location) gives a proxy book with a Calmar of 0.86 against 0.64 as tested. The other measures move with it: yearly +28.7 % against +22.4 %, deepest fall −33.4 % against −35.0 %, Sharpe 0.91 against 0.82, at the same 45 % of days held. This proxy charges half the trade cost on the change in position.
- F6: Turning positions off rather than grading them did worse on Calmar: requiring the volatility ratio ≥ 0.75 gave 0.46, requiring a previous-day signal gave 0.30, and requiring a low close with vol ratio ≥ 0.75 gave 0.58. Requiring a low close alone (close location ≤ 0.4) gave 0.73. The effect is graded, not a switch.
