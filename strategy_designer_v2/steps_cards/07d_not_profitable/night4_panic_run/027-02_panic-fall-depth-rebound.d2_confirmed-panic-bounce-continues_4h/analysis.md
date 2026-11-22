---
line: 7.d not profitable
backtest: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues_4h
idea tested: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3560 USD
---
## Findings
- **F1:** The book's deepest fall is −52.2 %, from a peak in w17 to a trough in w20, against a Calmar of 0.49. Windows w18–w24 each fall −25 % to −52 % deep, against −9 % to −29 % in w1–w17. The book lost −27.6 % in w18 and −18.7 % in w20, while holding the coins earned −22.0 % and +10.3 % there.
- **F2:** Inside that fall both sides lost. Over w18–w20 the short bars summed −1.77 and the long bars −1.27 of per-bar gain. In w21–w24 the shorts still lost (−1.32) while the longs earned +4.98. In w1–w17 the shorts earned +4.80 and the longs +8.70.
- **F3:** The short side carries the instability. Cases where the coin kept falling after the panic (negative forecast) were followed by an 84-bar excess return of −3.53 % (t −3.59, 254 cases) in w1–w17, but +1.29 % (t 0.88, 95 cases) in w18–w24. Over all windows the 1133 short trades lost a mean −2.76 % net, while the 1248 long trades made +5.84 %.
- **F4:** Among cases with a positive bounce, the 84-bar excess return rises with the coin's prior 30-day return. The lowest tercile earned +0.29 % (t 0.20), the middle +1.80 % (t 1.02) and the highest +5.11 % (t 1.95), with 113 cases each. Long bar gains are also highest in the top prior-30-day quintile: 0.000557 per bar, against 0.000080–0.000454 in the others.
- **F5:** Long gains grow with the coin's 180-bar volatility. In the top volatility quintile long bars earned 0.000697 per bar, against 0.000149–0.000391 in the others. Short bars lost −0.000211 per bar in that same top quintile.
- **F6:** Cost is not the cause. The total move is +1.74 % per case, 9.0 times the 0.19 % cost of a trade, and the unusual move is +1.32 % (strength 0.057, 797 cases).

## Ideas
- `027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.d1_bounce-after-panic-in-uptrends` (from F1, F3, F4): Among 24-hour stretches where a coin's range is several times its 30-day average and the coin fell, the larger the coin's rise over the 24 hours after the stretch, the higher its return over the following 14 days. The effect is the stronger the higher the coin's 30-day return before the stretch.
- `027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.d2_panic-bounce-in-high-volatility` (from F2, F3, F5): Among 24-hour stretches where a coin's range is several times its 30-day average and the coin fell, the larger the coin's rise over the 24 hours after the stretch, the higher its return over the following 14 days. The effect is the stronger the higher the coin's 30-day volatility of 4-hour returns.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
