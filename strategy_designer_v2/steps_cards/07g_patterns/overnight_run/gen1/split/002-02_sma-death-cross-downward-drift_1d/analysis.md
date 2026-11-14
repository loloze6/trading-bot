---
line: 7.g patterns
backtest: 002-02_sma-death-cross-downward-drift_1d
idea tested: 002-02_sma-death-cross-downward-drift
step 5: inconclusive
step 6: not profitable enough
mode: analyst then deducer
explorations: 2
cost: 0.3769 USD
---
## Findings
- **F1:** The bars do not drift down while the 50-day SMA is below the 200-day SMA; they drift up. Across all six coins the mean forward 10-bar return in the short state is positive: BTC +0.89%, ETH +0.57%, LTC +0.89%, XMR +1.05%, XRP +2.72%, ZEC +1.50%. The share of rising cases is 0.51–0.55, and for LTC and XMR the short state outpaces the non-short state (LTC +0.89% vs −0.25%, XMR +1.05% vs +0.84%).
- **F2:** The strongest forward drift sits in the band just around the cross. In the raw spread decile from −31 to +1 (short SMA barely below the long), the mean forward 10-bar return is +3.12% (t 3.47, 59.5% up), against +0.7% to +0.9% in the four deeper-below deciles.
- **F3:** The furthest-above deciles show the weakest drift. With the short SMA very far above the long (raw spread >206), the forward 10-bar return is −0.18% with 46% up. In the flat state with spread above 150, the mean is −0.36% / +0.18% (falling / rising) against about +2% for spreads between 0 and 150, which points to exhaustion at extreme stretch above the long average.
- **F4:** While short, a widening spread is followed by rebounds. When the spread fell over the past 10 bars, the forward 10-bar return is +1.91% (t 2.75, 4376 bars), against +0.48% (t 0.73) when the spread was rising.
- **F5:** The drift is concentrated early after the downward cross and fades with time in the short state. Forward 10-bar returns are +2.15% at 0–10 days since the cross, +2.19% at 10–30 days (t 2.25), +1.15% at 30–60 days and +0.13% at 60–120 days.
- **F6:** Up-moves continue rather than reverse. After the top quintile of past-10-bar returns (>+10.4%), the forward 10-bar return is +4.78% (t 2.48) in the flat state and +2.80% (t 2.44, 57% up) in the short state. After daily moves of +2 to +3 sigma, the forward 10-bar return is +4.94%, against +1.25% after moves within ±1 sigma.
- **F7:** Sign by year: the short state's forward 10-bar return is negative in the bear years and positive in recovery years.
- **F8:** The book's result is set by its window trend, not by the signal.
- **F9:** Leverage magnifies the book's losses. On short bars the allocation reaches −2.2 (5% quantile −1.72, mean −0.85), and the book's daily return is almost exactly allocation × coin return (corr 0.99999). This gives daily book tails of −58% (worst) and −14.9% (1% quantile). The worst 1% of book days coincide with a +11.6% coin day at a mean allocation of −1.56.
- **F10:** The 1273 short trades lose on price, not fees. The mean adverse price move is −11.2% against 0.20% mean commission, with a 23.6% win rate. The worst losses come from trades held 23–55 days (mean −19.1%) and from entries at a weak forecast of −5 to −2 (mean −16.6%, against about −10.5% for deeper entries).

## Ideas
- `002-02_sma-death-cross-downward-drift.g1_fresh-death-cross-rebound` (from F2, F5, F10): Shortly after the 50-day SMA crosses below the 200-day SMA, while the spread is still small (short average only slightly under the long), price over the next 10 days rises more often than not and further than the coin's usual drift.
- `002-02_sma-death-cross-downward-drift.g2_widening-gap-below-rebounds` (from F4, F1): While the 50-day SMA is below the 200-day SMA, a stretch where the spread widened downward over the past 10 days is followed by price rising over the next 10 days.
- `002-02_sma-death-cross-downward-drift.g3_big-up-moves-keep-running` (from F6, F9): After a coin's past 10-day return lands in its top fifth, or after a daily rise of two to three standard deviations, price keeps rising over the next 10 days more than after ordinary days, also while the 50-day SMA is below the 200-day SMA.
- `002-02_sma-death-cross-downward-drift.g4_extreme-stretch-above-exhausts` (from F3): When the 50-day SMA stands extremely far above the 200-day SMA, the coin's next 10-day return falls below its usual drift and rises less than half the time.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
