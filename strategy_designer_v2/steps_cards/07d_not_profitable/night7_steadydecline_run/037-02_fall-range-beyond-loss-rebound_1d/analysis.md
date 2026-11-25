---
line: 7.d confirmed, not profitable
backtest: 037-02_fall-range-beyond-loss-rebound_1d
idea tested: 037-02_fall-range-beyond-loss-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4501 USD
---
## Findings
- **F1:** The check failed on Calmar (0.69 against 0.75), and the book's falls come from choppy markets. Leaving out the positions held while the coin's 60-day return was between -10 % and +10 % raises Calmar to 1.53 (deepest fall -24.6 % instead of -37.0 %, yearly return +37.7 % instead of +32.4 %, Sharpe 1.19 instead of 1.00, approximate book after a 0.19 % cost per change of position). In a choppy trend the cases' next-day unusual move is -0.37 % (t -1.16, 324 cases), against +0.25 % (t 1.65, 1107 cases) in a falling trend and +0.37 % (t 1.66, 747 cases) in a rising one.
- **F2:** The deepest fall, in w16, was made by agitated non-falling positions. Choppy agitated positions lost a mean of -8.4 % per bar (sum -0.92 over 11 bars) and rising agitated ones -3.1 % (sum -0.56 over 18 bars), while falling agitated positions in the same window earned +1.43 % per bar (sum +1.40 over 98 bars).
- **F3:** The choppy condition is not an effect the repair borrows, and it does not earn on its own. Choppy bars without a case have a next-day unusual move of -0.34 % (calm, n 225) and -1.13 % (agitated, t -2.24, n 115). Choppy agitated bars with a case have about the same, -1.03 % (t -1.45, n 115). So in a choppy market a wide falling day carries no rebound, and the book there only adds falls.
- **F4:** The effect lives in falling agitated markets (falling 60-day trend, 30-day swing above its past median). There the cases' next-day unusual move is +1.30 % (t 4.51, 411 cases, net +0.66 % per bar after cost), against -1.28 % (t -4.99, n 405) on the same profile's bars without a case. The profile alone loses, so the gain is the idea's own. In falling calm markets the cases lose -0.37 % (t -2.27, n 696).
- **F5:** In rising markets the cases' gain is mostly the trend itself. Rising calm cases have an unusual move of +0.43 % (t 1.72), and rising calm bars without a case have +0.63 % (t 2.86). The rising part of the book is not the forced-sweep rebound.
- **F6:** The effect is graded and sits in its strong part. Cases with forecast ≥15 have a next-day unusual move of +0.65 % (t 3.14, n 982) in calm markets and +0.74 % (t 2.54, n 550) in agitated ones, while weaker calm cases have -0.08 % (t -0.82, n 2211). By forecast band, the 0–5 cases lose before costs (gain -0.014 %, net -0.044 % per bar, n 1335), while the 15–20 cases net +0.46 % (n 1532).
- **F7:** A deep fall over the past 10 days strengthens the rebound. Cases after a 10-day return below -15 % have a next-day unusual move of +1.07 % (t 3.97, n 747), while the same 10-day fall without a case is followed by -1.21 % (t -3.63, n 464). The condition alone loses, so it adds to the idea rather than being an effect of its own. It fits the brief's theory that a sweep is a capitulation of forced sellers after a slide.

## Ideas
- `037-02.d1_wide-fall-rebound-outside-chop` (from F1, F2, F3): The larger a coin's one-day fall and the further that day's high-to-low range stretches beyond the size of the closing loss itself, taken together, the larger the rise over the next day, except in a choppy market, where the coin's 60-day return has gone neither clearly up nor clearly down.
- `037-02.d2_falling-agitated-sweep-rebound` (from F4, F2, F5): In a falling, agitated market, the larger a coin's one-day fall and the further that day's high-to-low range stretches beyond the size of the closing loss itself, taken together, the larger the rise over the next day.
- `037-02.d3_sweep-after-slide-rebounds` (from F7, F6): The larger a coin's one-day fall and the further that day's high-to-low range stretches beyond the size of the closing loss itself, taken together, and the deeper the coin's 10-day fall before that day, the larger the rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
