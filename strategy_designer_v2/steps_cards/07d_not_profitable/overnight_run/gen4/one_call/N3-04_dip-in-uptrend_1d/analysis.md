---
line: 7.d not profitable
backtest: N3-04_dip-in-uptrend_1d
idea tested: N3-04_dip-in-uptrend
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3361 USD
---
## Findings
- **F1:** The book fails on Calmar (0.52 against 0.75) because its drawdowns are deep, from -42% on BTC to -82% on LTC, while its mean daily return passes (0.00058); its worst 5% of active days sum to -17.7 against a total active gain of +11.5 over 2411 active days, so a few days decide the result.
- **F2:** The losses come from the largest positions. The 50 worst book days had a mean allocation of 1.92, 94% of them at 1.5 or more, with a mean next-day coin move of -11.1%. The book's daily standard deviation rises from 0.011 at allocations up to 0.5 (1251 days) to 0.111 at allocations of 1.8 to 2.1 (551 days).
- **F3:** A larger forecast earns more before fees, but noisily. The mean next-day coin return is +0.72% at forecast 3–8 (n=427, t=2.75), +0.05% at 8–14 (n=268, t=0.14), +1.30% at 14–20 (n=155, t=2.96) and +0.78% at the 20 cap (n=525, t=3.18). By drop size it reaches +1.49% for drops over 3 typical moves (n=53, t=2.77).
- **F4:** The edge is regime-dependent by year. After forecast > 0 bars, the next-day coin return was -1.59% in 2018 (n=99, t=-1.99) and -0.40% in 2022 (n=150, t=-1.01), the two years the coins fell (mean daily coin return -0.35% and -0.18%). In 2019–2021 it was +0.61% to +1.09% with t between 2.0 and 4.6.
- **F5:** Within the active days, the book earns little when the 20-day trend is weakest: +0.10% per day (n=715, t=0.78), against +0.65% (t=3.13) and +0.74% (t=2.63) in the middle and strongest 20-day-return terciles. Calm days are also weak, at +0.14% (n=780, t=1.34), against +0.67% and +0.78% in mid and volatile days.
- **F6:** The rebound lasts beyond the one-bar horizon. On non-overlapping dip signals (n=1362), the coin gains +0.24% on day 1 (t=1.78) and a further +0.63% over days 2–3 (t=3.06). A second consecutive dip day is followed by +0.63% (n=826, t=3.42), against +0.33% (n=1557, t=2.68) after a first dip.
- **F7:** Fees are not the problem; trade selection is. The 1613 trades are all long, with a median hold of 1 day. Their gross mean is -0.03% per trade (t=-0.16) against about 0.10% in fees. One-day trades gain +1.25% gross (n=1127), but trades held 1.5–3.5 days lose -3.37% (n=342) and those held 3.5–7.5 days lose -3.74% (n=79): these are the dips that kept falling.

## Ideas
- `N3-04_dip-in-uptrend.d1_dip-rebound-spans-days` (from F6, F7): In a coin whose 20-day and 60-day returns are both positive, a sharp daily drop is followed by a rise over the next two to three days, larger than the rise on the first day alone.
- `N3-04_dip-in-uptrend.d2_dip-bounce-needs-strong-trend` (from F4, F5): A daily drop in a coin is followed by a rebound when the coin's 20-day return sits clearly above zero, in the upper part of its range. The rebound is absent when the 20-day rise is marginal, as in a falling year.
- `N3-04_dip-in-uptrend.d3_big-dips-bring-big-variance` (from F1, F2, F3): In an uptrending coin, the next day's move after a drop of more than twice the typical daily move is much more dispersed than after a moderate drop, with a larger absolute size in both directions. The mean gain grows less than that dispersion.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
