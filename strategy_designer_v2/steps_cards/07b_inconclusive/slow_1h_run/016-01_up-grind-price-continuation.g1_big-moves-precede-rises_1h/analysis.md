---
line: 7.b inconclusive
backtest: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises_1h
idea tested: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4363 USD
---
## Findings
- **F1:** The rise after big moves comes almost entirely from the largest moves: the 72-bar excess return by forecast quintile is -0.44%, -0.22%, -0.18%, 0.00% and +0.84%, and the top decile earns +1.56% against -0.17% for the rest (Welch t 4.10, 568 top cases). Meanwhile the held position grows evenly from 0.06 to 0.46 across the quintiles, so the book is long through the middle quintiles, where the excess return is negative.
- **F2:** The book's timing part is negative on every coin, from -0.00024 (XRP) to -0.00076 (XMR) a day, while its gain from the market's own rise is +0.00015 to +0.00041 a day. Hourly, the timing sum by forecast quintile is -0.10, -0.01, +0.15, +0.73 and -0.06, while the market part grows from 0.29 to 2.36. So the positive slope (t 3.67, 5,683 cases) does not become timing profit for a book sized linearly on the forecast.
- **F3:** After a 3-day fall, the slope is strongest at the shortest horizon: t 5.36 over 24 bars (2,881 cases), falling to 2.92 at 48 bars and 2.27 at 72 bars. After a 3-day rise, the 24-bar slope is only t 0.52 (2,926 cases) and builds to 2.82 at 48 and 2.88 at 72 bars, so the plan's 3-day horizon mixes a fast rebound after falls with a slow drift after rises.
- **F4:** The effect is uneven over time and by coin: the year slopes run from t 3.47 (2021) and 2.12 (2025) down to 0.01 (2020) and -0.55 (2022), and the coin slopes from t 2.45 (XRP) to 0.51 (ETH).
- **F5:** The move's size carries the signal, not its direction: the signed standardised 3-day return has a slope t of only 1.08 (5,539 cases), against 3.67 for the absolute size.

## Ideas
- `016-01_up-grind-price-continuation.g1_big-moves-precede-rises.b1_rebound-after-deep-falls` (from F3, F1, F5): The larger a coin's absolute 3-day return, the more the coin rises, only while that 3-day return is a fall, over the next 1 day.
- `016-01_up-grind-price-continuation.g1_big-moves-precede-rises.b2_largest-moves-precede-rises` (from F1, F2): The larger a coin's absolute 3-day return, whether up or down, the more the coin rises over the next 3 days, and the rise grows faster than the move's size, so the largest moves are followed by far larger rises than moderate ones.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
