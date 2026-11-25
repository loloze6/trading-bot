---
line: 7.g patterns
backtest: 032-02.b2.g1_close-location-next-day-reversal_1d
idea tested: 032-02.b2.g1_close-location-next-day-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3956 USD
---
## Findings
- **F1:** The next-day reversal grows with the size of the day's range. The slope of the next-day return (coin mean removed) on (close location − 0.5) × (high − low)/close is 0.217 (t 10.99, n 8688), against t 5.37 for the location alone. In a joint fit the location × range term has beta 0.339 (t 10.83), and the location alone turns negative (beta −0.0173, t −5.03). The effect is a distance in percent of the close below the day's midpoint, not a place in the range.
- **F2:** The reversal is concentrated on days whose range is wide against the coin's past 20-day mean range. The directional next-day return by quartile of that ratio is +0.04 % (t 0.41), +0.12 % (t 1.12), +0.35 % (t 2.75) and +0.82 % (t 5.69), about 2000 bars each. The book's daily position gain is +0.095 % (t 5.18) in the top quartile against +0.004 % in the bottom. Only the top quartile's move per case is well above the 0.19 % cost of a trade.
- **F3:** The reversal also grows with the coin's 20-day volatility against its 60-day level. The directional next-day return by quartile is −0.23 % (t −1.90), +0.17 % (t 1.47), +0.37 % (t 2.97) and +0.94 % (t 6.22).
- **F4:** The wide-range reversal holds in every year and every coin. In the top range quartile, every year is positive, from +0.57 % to +1.36 % (t 2.28 to 3.74), and every coin is positive, from +0.37 % (BTC, t 1.62) to +1.35 % (XMR, t 3.86). It is stronger after closes near the low (long side +1.13 %, t 5.52, n 1012) than after closes near the high (short side +0.50 %, t 2.47, n 985).
- **F5:** A large down day against the coin's 20-day volatility is followed by a rebound the next day.
- **F6:** Over 5 days the close's place in the 5-day range carries on rather than reverses (non-overlapping 5-day grid).
- **F7:** The brief's own situation does not stand out. A new 30-day closing low while the 20-day return is negative and volatility is above its 60-day mean is followed by +0.25 % the next day (t 0.39, n 198) and −2.2 % over 5 days (t −0.78, n 41), not distinguishable from other bars.
- **F8:** Mondays are weak for the tested reversal. The directional next-day return is −0.34 % (t −2.17, n 1236) on Mondays against +0.41 % to +0.59 % (t 3.0 to 3.9) from Wednesday to Sunday. After many angles this is too weak to build on.

## Ideas
- `032-02.b2.g1.g1_close-distance-from-midpoint` (from F1, F2, F4): The further a coin's daily close sits below the midpoint of that day's high-low range, measured in percent of the close, the more the coin rises over the next 1 day. The further it closes above the midpoint, the more it falls.
- `032-02.b2.g1.g2_wide-day-close-reversal` (from F2, F3, F4): The wider a coin's daily high-low range is against its average range over the past 20 days, the more a close near that day's low is followed by a rise over the next 1 day.
- `032-02.b2.g1.g3_next-day-rebound-after-shocks` (from F5): The larger a coin's daily fall is against its standard deviation of daily returns over the past 20 days, the more the coin rises over the next 1 day.
- `032-02.b2.g1.g4_five-day-range-continuation` (from F6): The lower a coin's daily close sits within its high-low range of the past 5 days, the more the coin falls over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
