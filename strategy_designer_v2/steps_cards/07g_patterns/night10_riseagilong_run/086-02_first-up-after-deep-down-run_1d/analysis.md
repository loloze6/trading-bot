---
line: 7.g patterns
backtest: 086-02_first-up-after-deep-down-run_1d
idea tested: 086-02_first-up-after-deep-down-run
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4872 USD
---
## Findings
- **F1:** The tested idea's effect runs the other way in this data. Its 5-day unusual move after the first up day is -0.11 % (t -0.13, 261 days, 389 cases), and its depth slope is negative (t -2.16): deeper down runs, relative to the coin's swing, are followed by weaker, not stronger, 5-day returns in rising agitated markets.
- **F2:** Inside the rising agitated profile, a coin's 3-day return scaled by its 30-day swing predicts its next days with the same sign.
- **F3:** The 3-day continuation holds on the rising side and is graded there.
- **F4:** The 3-day continuation is not carried by one period or one coin, but ETH does not share it.
- **F5:** Nearness to the 20-day high, scaled by swing, also predicts the next days with the same sign, with mean slope t 1.59 at 3 days, 1.75 at 5 days and 2.19 at 10 days. The map already holds this pattern in rising agitated long (034-01.b1 "nearness to high 10 days", 033-03.b2), so it is not a discovery.
- **F6:** Other angles did not stand out once the number of angles looked at is counted.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `086-02.g1_agitated-rise-short-burst-continuation` (from F2, F3, F4, F1): In a rising, agitated market, a coin's rise over the last 3 days continues over the next 3 days. The larger that 3-day return, measured against the standard deviation of the coin's daily returns over the past 30 days, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
