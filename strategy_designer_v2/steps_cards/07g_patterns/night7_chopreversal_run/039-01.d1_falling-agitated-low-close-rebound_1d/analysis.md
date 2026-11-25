---
line: 7.g patterns
backtest: 039-01.d1_falling-agitated-low-close-rebound_1d
idea tested: 039-01.d1_falling-agitated-low-close-rebound
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3689 USD
---
## Findings
- **F1:** The close-location effect lives on days whose range is wide against the coin's last 20 days, not on narrow ones. The graded signal (location − 0.5) × next-day excess return averages +19.8 bp on wide-range days (t 3.24, 773 days), against +5.3 bp on mid days (t 1.23) and +0.8 bp on narrow days (t 0.22).
- **F2:** On wide-range days the next day is graded by where the close sits. A close in the lowest fifth of the range is followed by +129 bp of excess return (t 2.77, 195 days). A mid close is followed by +16 bp (t 0.51) and a close in the top fifth by −57 bp (t −1.63). On narrow days the low close is followed by −5 bp (t −0.12).
- **F3:** The wide-range effect needs at least ordinary swing, not the highest. The signal on wide days is +28.3 bp (t 3.91) in the middle volatility tercile and +38.7 bp (t 3.11) in the agitated one, but −4.8 bp (t −0.61) in the calm tercile.
- **F4:** On wide days the close location carries information beyond the day's own return. In a day-clustered joint regression, location keeps a slope of 252 bp (t 2.08) while the volatility-scaled day return has none (5.6 bp, t 0.21). Over all days neither term is separable (location t 1.23, return t −0.75).
- **F5:** Weighting location by the day's relative range gives a signal of +16.3 bp (t 2.80, 1,220 days). Its mean is positive in all 12 windows, w7 to w18, though no single window reaches t 2.2.
- **F6:** Among agitated bars, the effect sits in falling and choppy trends and is absent in rising ones. The signal is +32.8 bp (t 2.49) in a falling trend, +46.0 bp (t 1.97, 59 days) in a choppy one, and −4.9 bp (t −0.46) in a rising one.
- **F7:** Inside the tested profile only the long side pays. In-profile low closes are followed by +217 bp (t 2.67, 118 days), while high closes are followed by only −49 bp (t −0.76). The book's long trades net +2.30 % each (490 trades), its short trades +0.11 % (427 trades). The book earns 1.19 bp a day (t 2.79), with a correlation of 0.22 to holding the coins.

## Ideas
- `039-01.d1.g1_wide-day-low-close-rebound` (from F1, F2, F3, F4, F5): The lower a coin closes within its day's high-low range, and the wider that range is against its ranges of the last 20 days, the larger its rise over the next day.
- `039-01.d1.g2_falling-wide-day-low-close-rebound` (from F2, F6, F7): In a falling, agitated market, the lower a coin closes within a day's range that is wide against its last 20 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
