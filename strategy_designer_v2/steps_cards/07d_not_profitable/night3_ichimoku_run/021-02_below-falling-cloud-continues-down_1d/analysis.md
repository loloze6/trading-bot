---
line: 7.d not profitable
backtest: 021-02_below-falling-cloud-continues-down_1d
idea tested: 021-02_below-falling-cloud-continues-down
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4755 USD
---
## Findings
- **F1:** The book loses because it is short coins that rise on average. On its 7,398 short bars it earned -0.078 % per bar. Of that, -0.060 % came from the market's own rise and only -0.018 % from timing. The coins' normal drift against a short is -4.24 % per 26 days, which outweighs the +1.51 % unusual move (t 0.69, 156 cases). The total move per case is therefore -2.73 %, so the size of a trade's cost (0.19 %) is not what sinks it.
- **F2:** The idea's grading runs the wrong way. When the cloud has fallen slowly, the short pays; when it has fallen fast, the coin rebounds.
- **F3:** The inversion holds across coins and periods.
- **F4:** The short works when the coin is calm and fails when it is volatile.
- **F5:** Cloud thickness also grades the move.
- **F6:** When the coin has not itself fallen over the past 26 days but still sits below a falling cloud, it rises. In that quartile (26-day return -2 % to +16 %) the short-signed total move is -15.4 % (t -2.24, 30 cases). The quartile with returns of -20 % to -13 % gains +8.7 % (t 2.62).

## Ideas
- `021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud` (from F1, F2, F3, F4): When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative, and more negative the slower the cloud has fallen over the past 26 days and the calmer the coin's daily moves have been over the past 30 days.
- `021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud` (from F1, F5): When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative, and more negative the thinner the cloud is relative to the price.
- `021-02_below-falling-cloud-continues-down.d3_fast-cloud-fall-rebounds` (from F2, F3, F6): After a coin's Ichimoku cloud has fallen fast over the past 26 days, the coin's return over the next 26 days is positive, and larger the faster the cloud has fallen.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
