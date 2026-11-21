---
line: 7.b inconclusive
backtest: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins_1d
idea tested: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3906 USD
---
## Findings
- **F1:** The supporting check could not be computed because the forecast hits its cap: on 69 % of the cases it is at the cap of 20, and its median is 20, so the median split put all 3937 cases in the lower half and none in the upper half; this half of the test was never run.
- **F2:** The 5-day result is positive but sits inside the noise: on my recount the unusual move is +0.23 % per case (t 1.18, 3899 cases), against +0.29 % and t 1.34 in step 5. Longer horizons do not sharpen it: 1 day +0.02 % (t 0.30), 10 days +0.26 % (t 0.84), 20 days +0.58 % (t 1.14), with strength 0.004 to 0.024.
- **F3:** The effect has opposite signs depending on the coin's 30-day trend, which is why the pooled result is unclear. Breakouts while the coin's 30-day return is positive are followed by +1.27 % unusual move over 5 days (t 3.96, 1778 cases). Breakouts while it is zero or negative are followed by −1.16 % (t −3.70, 1069 cases).
- **F4:** The split by 30-day return is graded. By its quartiles, the 5-day unusual move is −1.30 % (t −3.27), −0.33 %, +1.05 % (t 2.63) and +1.94 % (t 3.07). Over 10 days it is −2.43 % (t −4.19), +0.11 %, +1.79 % (t 2.10) and +2.61 % (t 3.22).
- **F5:** Inside the rising-trend half, the size of the break adds to the move (touch count times the close's margin, the forecast's raw value). Breaks above the raw median earn +1.53 % (t 2.48) in the third 30-day-return quartile and +2.84 % (t 3.10) in the top one. Breaks below it earn +0.67 % and +0.63 % in the same quartiles.
- **F6:** The touch count alone grades weakly and not in order. The 5-day unusual move is +0.47 % at 1 touch (1786 cases), +0.11 % at 2, +0.25 % at 3 and +1.33 % (t 1.68) at 4 or more. Only the top quartile of the close's margin (+1.59 %, t 2.67) and of the raw value (+1.27 %, t 2.51) stand out; the other quartiles are near zero.
- **F7:** The years swing with the market, a sign that the move is drowned by the coin's own trend:
- **F8:** Size against cost: in the rising-trend half the unusual move of +1.27 % per case is about 5.8 times the 0.22 % round-trip cost. Pooled, it is only 1.3 times the cost. By finding F11 of the earlier runs, the conditioned idea is large enough to pay, and the pooled one is marginal.
- **F9:** No more data is available: the test already used all 19 coins over all four folds on daily bars. The answer is therefore the idea amended to where the effect shows (F3, F4, F5), not the same idea on more data.

## Ideas
- `020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend` (from F3, F4, F5, F7, F8): When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 5 days, only while its 30-day return is positive, and the more times the level held and the further the close clears it, and the stronger its 30-day rise, the larger the rise.
- `020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend` (from F3, F4, F7): When a coin closes above a price where it turned down several times in the past 90 days while its 30-day return is negative, it tends to fall back over the next 10 days, and the deeper its 30-day decline, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
