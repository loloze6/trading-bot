---
line: 7.b inconclusive
backtest: N3-01_strong-volatile-momentum_1d
idea tested: N3-01_strong-volatile-momentum
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2997 USD
---
## Findings
- **F1:** The pooled effect is a small mean carried by a few large winners: 369 non-overlapping cases at forecast ≥10 give a mean excess 5-bar return of +0.97% (sd 13.5%, t=1.38), but the median is −0.40% and the hit rate is 47%. Skew is 2.43, the top 5% of cases account for 186% of the total excess, and once the tails are winsorised at 5/95% the t falls to 0.97.
- **F2:** The market's own move drowns the effect: the excess return of the cases correlates 0.68 with the six-coin mean 5-bar move, and that move explains 46% of their variance. Net of the market the mean is only +0.28% (t=0.54, n=369). For altcoins, the excess is +6.7% (t=6.15, n=160) when BTC's next 5 bars rise and −5.5% (t=−5.34, n=146) when they fall.
- **F3:** Among altcoins, the effect appears only when BTC is itself in a strong run-up on the same bar: mean excess +2.74% (t=2.12, n=126, hit 51%) when BTC's forecast is also ≥10, against −0.50% (t=−0.47, n=180, hit 43%) when it is not. BTC's own cases give +1.63% (t=1.79, n=63, hit 54%).
- **F4:** The effect sits in run-ups that have already pulled back from their 20-day high. Excess is +2.68% (t=1.57, n=107) in the lowest tercile of distance to the 20-day high and +1.60% (t=1.75, n=107, hit 52%) in the middle tercile, against −0.88% (t=−1.01, n=108, hit 43%) for coins at or near their high. The same pattern holds for distance to the 50-bar average: lowest tercile +1.21% (t=1.41, n=76), highest −1.19% (t=−0.77, n=76).
- **F5:** The effect is not stable across coins, periods or forecast size. By coin it ranges from −0.21% (LTC) to +3.16% (ZEC, t=1.20), and no coin reaches t=2. Windows w1–w18 give about zero (each group |t|<0.4), while w19–w24 give +3.0% (t=1.77, n=111). The capped forecast-20 bucket (n=307) gives only +0.69% (t=0.94), and the highest third of 20-day returns gives −0.25%.

## Ideas
- `N3-01_strong-volatile-momentum.b1_alt-momentum-with-btc` (from F3, F2): When an altcoin is up over 20 and 60 days in high volatility with an unusually large 20-day run-up, and BTC on the same daily bar is in the same strong, volatile run-up, the altcoin rises more than its usual 5-day return over the next 5 days.
- `N3-01_strong-volatile-momentum.b2_momentum-after-pullback` (from F4, F1): When a coin is in a strong, volatile run-up over 20 and 60 days but its close has already fallen back below its 20-day high, it rises more than its usual 5-day return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
