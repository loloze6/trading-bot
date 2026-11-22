---
line: 7.b inconclusive
backtest: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days_1d
idea tested: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3485 USD
---
## Findings
- **F1:** The test's result points the way the idea predicts but falls short of the bar: up-regime minus down-regime 20-day unusual return is +2.17 % with Welch t 1.08 (382 vs 362 cases), and my recomputation gives +1.93 %, t 0.97 (386 vs 362).
- **F2:** The gap is real in sign but small next to the noise: strength 0.048 of a usual 20-day move (21.24 %), so about 750 cases cannot reach t 2.
- **F3:** Cost is not the obstacle: the 1.07 % total move per case is 5.5 times the 0.19 % cost of a trade.
- **F4:** The gap comes almost entirely from the sharpest bounces. In the top quartile of |forecast|, the 20-day gap is +10.1 % (t 1.98; 98 up vs 77 down cases). The lower three quartiles give −0.6 % (t −0.22), +1.0 % (t 0.29) and −2.9 % (t −0.69). The supporting check passed (+3.0 %).
- **F5:** The gap is mixed across years and is drowned by market swings. 2020 runs strongly against the idea (−19.7 %, t −2.84, 61 vs 30 cases). 2025 (+10.9 %, t 1.62) and 2019 (+4.8 %, t 1.25) run with it. In 2018 both sides fall alike (−14.7 % and −12.6 %, gap t −0.37).
- **F6:** The idea holds in five of six coins at 20 days, with gaps of +2.0 % to +8.3 % (t 0.47 to 1.17), but none is significant on its own about 125 cases. XRP runs the other way (−8.6 %, t −1.34).
- **F7:** The fade itself is weak at 20 days. Bounces in 90-day fallers average −1.0 % against drift (t −0.81, 362 cases), while bounces in 90-day risers average +0.9 % (t 0.60). The gap needs both sides, and each is small alone.
- **F8:** The idea shows at shorter horizons too, on the same 20-day grid of cases: the up-minus-down gap in raw return is +1.2 % over 3 days (t 2.08, 437 vs 417) and +1.6 % over 5 days (t 2.27). On a 5-day grid of its own it is +0.5 % (t 1.14, 1248 vs 1052 cases). Again the top quartile carries it (+2.0 %, t 1.97).

## Ideas
- `025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins` (from F1, F2, F3, F4, F6): In one coin, the 20-day return after a one-day rise of several usual daily moves (its day's return over the standard deviation of its last 20 daily returns) is lower when its 90-day return is negative than when it is positive, and the gap widens as the rise gets larger.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
