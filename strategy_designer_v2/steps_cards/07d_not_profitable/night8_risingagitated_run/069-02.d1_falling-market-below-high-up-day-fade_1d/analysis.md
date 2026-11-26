---
line: 7.d confirmed, not profitable
backtest: 069-02.d1_falling-market-below-high-up-day-fade_1d
idea tested: 069-02.d1_falling-market-below-high-up-day-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4024 USD
---
## Findings
- **F1:** The fade works only when the coin is agitated as well as falling: on signal bars in a falling, agitated market the short-direction excess next-day return is +1.44 % (t 2.12 with same-day cases summed, 267 cases on 90 days), against +0.24 % (t 0.70, 703 cases on 244 days) in a falling, calm market; on the book's held bars the agitated ones earn 0.64 % per bar against 0.15 % for the calm ones, with fees of 0.076 against 0.338 summed.
- **F2:** Agitation is not an effect of its own: in a falling, agitated market the bars without the signal (the down days) give a short excess of −1.85 % (t −2.21, 256 cases), and all falling, agitated bars together give −0.16 % (t −0.28, 524 cases), so the short gain there comes from the idea's up-day signal and not from the market state. This fits the theory: an agitated fall is the one that leaves the most recent buyers trapped above the price.
- **F3:** The effect grows with how far the coin's 30-day swing sits above its own norm: when that swing, relative to its expanding median, is above 1.25 the signal's short excess is +1.49 % (t 3.71, 212 cases); between 1.0 and 1.25 it is +1.03 % (t 3.29, 205 cases); between 0.8 and 1.0 it is −0.05 % (t −0.17, 268 cases); below 0.8 it is +0.02 % (t 0.07, 304 cases).
- **F4:** In calm falling markets the shallow third of signals loses: −0.70 % (t −1.38, 226 cases), while the deep third earns +0.95 % (t 1.51); overall the shallowest forecast fifth is −0.17 % (t −0.52), and these calm, mostly marginal bars carry 82 % of the book's fees (0.338 of 0.415 summed).
- **F5:** The book's weak years are calm-market years: the signal's short excess is +0.80 % (t 3.36) in 2018 and +0.57 % (t 3.43) in 2019, but −0.04 % (t −0.14) in 2020 and −0.01 % (t −0.02) in 2021; the windows with losing held bars (w11 −0.22, w12 −0.10, w17 −0.03, all calm) had no or almost no agitated held bars.
- **F6:** The effect needs the falling market: up days outside a falling market, sorted by depth below the 20-day high, give at most +0.22 % (t 0.69) in the deepest fifth, and +0.36 % (t 0.52) in the deepest third even when agitated, against +1.05 % (t 2.25) for the deepest fifth of up days inside a falling market.

## Ideas
- `069-02.d1.d1_agitated-fall-up-day-fade` (from F1, F2, F4, F5, F6): In a falling, agitated market, when a coin closes up on the day, the further that close sits below its 20-day high, measured in units of its 20-day daily swing, the larger its fall over the next day.
- `069-02.d1.d2_swing-graded-low-range-up-fade` (from F2, F3, F5): In a falling market, when a coin closes up on the day well below its 20-day high, the more its 30-day daily swing exceeds its usual swing over the past year, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
