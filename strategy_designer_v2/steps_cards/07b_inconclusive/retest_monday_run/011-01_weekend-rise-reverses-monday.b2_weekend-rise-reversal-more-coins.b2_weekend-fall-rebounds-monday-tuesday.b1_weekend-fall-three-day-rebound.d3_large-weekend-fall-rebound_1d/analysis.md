---
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4789 USD
---
## Findings
- **F1:** The main measure is positive (forecast-weighted excess 3-day return +1.11 %, t 3.65, 1477 cases). The result is inconclusive only because the forecast is not graded: by forecast quartile the excess 3-day return is +1.62 % (t 3.6), +1.12 %, +0.68 % and +1.39 % (t 2.5). The top quartile sits at the cap (mean forecast 20.0), so the top-quartile check comes out at Welch t −1.80.
- **F2:** Deep Sunday falls measured in usual daily moves do not rebound most. Sunday z below −3 gives +5.7 % but on only 8 cases, and z from −3 to −2 gives −1.76 % (t −1.14, 63 cases). The rebound sits at z from −1.5 to −0.5: +2.40 % (t 3.35, 232 cases) and +1.28 % (t 3.75, 691 cases).
- **F3:** Measured in percent, the Sunday fall is cleanly graded. Excess 3-day returns are +0.95 % (t 2.7) for falls of 1.5–3 %, +1.85 % (t 3.8) for 3–5 %, +2.31 % (t 3.0) for 5–8 % and +3.11 % (t 2.3) beyond 8 %. Sunday's own return has the strongest reversal slope of any weekday on the next 3 days: −0.234 (t −7.6), against −0.10 to +0.07 on the other weekdays.
- **F4:** The rebound lives where the coin's 20-day usual daily move is high against its own median. Sunday falls by volatility quintile give −0.61 %, +0.47 %, +0.32 %, +1.64 % (t 3.6) and +3.02 % (t 5.1).
- **F5:** Inside the high-volatility third, Sunday falls grade with depth: +1.55 % (shallow), +3.15 % (mid) and +3.30 % (deep), with a slope on the fall size of 0.41 (t 3.5, 699 cases).
- **F6:** The effect is spread across coins: 17 of 19 coins have a positive mean excess return. DOGE is the exception (−2.08 %, t −2.3, 93 cases). No more data is available than the test used, which already covered all 19 coins on all four folds of daily bars.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound` (from F1, F4, F5): A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) by a large multiple of its usual daily move rises over the next 3 days (Monday to Wednesday), only while its usual daily move over the past 20 days is high against its own usual daily move over the past year. The rise grows both with the depth of the weekend fall and with how high that 20-day usual move stands against its past year.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b2_percent-weekend-fall-rebound` (from F2, F3, F6): A coin's Saturday-to-Sunday close-to-close fall, measured in percent of its price, is followed by a rise over the next 3 days (Monday to Wednesday), and the deeper the percent fall, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
