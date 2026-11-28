---
line: 7.c no effect
backtest: 041-01.b1_rising-agitated-rise-continues_1d
idea tested: 041-01.b1_rising-agitated-rise-continues
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5543 USD
---
## Findings
- **F1:** Inside rising agitated, a scaled one-day rise does not predict the next day. The slope of next-day excess return on the scaled rise has a day-clustered t of 0.74 and a Spearman of -0.04 (572 cases, 361 days). The mean excess return is +0.06 % (t 0.21), and the verdict's own t is +0.015. The tested continuation is absent at its own horizon.
- **F2:** The next-day reaction to up days differs by coin and is mostly negative. Mean excess return after an up day is -0.36 % for ETH (147), -0.59 % for XMR (90) and -0.19 % for XRP (82). Only LTC is positive, at +0.61 % (253).
- **F3:** In the same profile, down days are followed by a rise but the rise is not graded. After a fall the next-day excess return is +0.40 % (t 1.15, 515 cases) and the 2-day excess return is +1.46 % (t 2.04, 275 cases). The 2-day slope on the fall's size has a clustered t of 0.19. By tertile of the fall, the middle third gains +2.75 % over 2 days, while the largest third gains +0.23 % and the smallest +0.14 %.
- **F4:** Over 4 days, the rebound after falls in rising agitated starts to grow with the fall's size. The mean is +2.08 % (t 1.39, 120 cases, 73 days), with a slope clustered t of 1.36 and a Spearman of 0.15, the strongest ranking seen on either side.
- **F5:** Outside the profile, the brief's one-sided reversal is clearly there and graded. Next-day excess return is +1.80 % after scaled falls below -2 (99 cases), +0.82 % after falls between -2 and -1 (282), +0.04 % after falls from -1 to 0, and -0.21 % to -0.42 % after rises. The book's profile filter removed the place where the theme's effect lives.
- **F6:** Up-day continuation over 3 days is fragile.

## Ideas
- `041-01.b1.c1_rising-agitated-fall-rebound-four-days` (from F3, F4, F5): In a rising, agitated market, the larger a coin's one-day fall measured against the standard deviation of its daily returns over the last 30 days, the larger its rise over the next four days.
- `041-01.b1.c2_rising-agitated-rise-continues-three-days` (from F1, F6): In a rising, agitated market, the larger a coin's one-day rise measured against the standard deviation of its daily returns over the last 30 days, the larger its rise over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
