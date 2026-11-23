---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 5-day rise, measured in its usual 5-day moves, the more it rises over the next 3 days, only while the coin's 20-day return is positive.
Consequence: A trader holds a coin for three days after a strong 5-day advance only while its last 20 days are up, and stays out of advances inside a falling month, which is where the long fall came from.
Why:
- F1: The Calmar failed because of one long fall: the book fell 33.7 % over 1114 days, from w1 to its trough in w10, while the coins fell 68.3 %. That fall alone sets the deepest fall against a yearly return of +25.0 %, giving a Calmar of 0.742 against a rule of 0.75.
- F2: The book's gain while held depends on the coin's own longer trend. On bars held when the coin's 60-day return was positive, the mean daily gain was +0.219 % (3095 bars, sum +6.79); when it was not, it was −0.020 % (2566 bars, sum −0.51). Above versus below the 50-day average it was +0.209 % (3829 bars) against −0.005 % (2851 bars).
- F3: The idea's grading exists only inside a rising 20-day trend. On the 3-day grid among signal cases, the slope of excess return on the forecast is 0.00083 when the 20-day return is positive (1508 cases, forecast-weighted excess +0.65 %). When it is not, the slope is 0.00014 (820 cases, weighted excess +0.14 %).
- F5: Held gain in the losing stretch w1–w10 shows where the fall came from. With the 20-day return at or below zero and a strong forecast, the mean daily gain was −0.045 % (285 bars). With a positive 20-day return and a strong forecast it was +0.075 % (980 bars). In w11–w24, the strong-forecast, positive-trend bars earned +0.582 % a day (1631 bars, sum +9.49), almost all of the book's gain.
- F7: Rebuilt books with costs show how much a trend filter improves the falls.
