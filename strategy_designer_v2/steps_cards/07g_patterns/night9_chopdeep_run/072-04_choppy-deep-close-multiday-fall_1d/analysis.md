---
line: 7.g patterns
backtest: 072-04_choppy-deep-close-multiday-fall_1d
idea tested: 072-04_choppy-deep-close-multiday-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4061 USD
---
## Findings
- **F1:** The tested idea's effect appears only in the deepest closes and does not grow with depth. In the choppy bars, on the non-overlapping 3-day grid, the deepest fifth of closes below the 20-day high (mean depth −6.2 swings) was followed by an excess 3-day return of −2.80 % (t −2.76, 82 cases). The other four fifths sat between −0.54 % and +0.44 %, all with |t| < 0.9. The choppy deciles were not ordered either: −2.06 %, −3.53 %, then +0.53 % and +0.35 %. This matches step 5's flat slope (t −0.05) and the book's Sharpe of −0.22.
- **F2:** Deep closes below the 20-day high were followed by a continued fall mainly in falling, calm markets. Here falling means a 60-day return below −10 %, and calm is my stand-in for the profile: 30-day swing below the 90-day swing, not the profile's past-year median. Across the deepest two depth deciles of all bars, falling calm cases had an excess 3-day return of −2.38 % (t −4.03, 211 cases). Falling agitated cases had −0.34 % (t −0.21, 52), rising calm −2.74 % (t −1.50, 32) and choppy calm −5.63 % (t −2.50, 27).
- **F3:** A large 5-day fall continued in the same calm markets. In the lowest fifth of the 5-day return scaled by its usual swing, the excess 3-day return was −2.61 % in falling calm markets (t −3.63, 166 cases) and −7.43 % in choppy calm ones (t −3.67, 31 cases). In falling agitated markets it was +1.27 % (t 0.65, 33), so the continuation is a calm-market effect.
- **F4:** Over all bars the deep-close effect is weaker than its plain t suggests. The second-deepest depth decile had −2.34 % (t −4.23, 236 cases), but the deepest decile's t falls from −1.28 to −0.77 when its cases are taken together by day (107 days). The pooled effect is crowded into few days, which is why only the per-profile split in F2 stands out.
- **F5:** Other angles showed only patterns the portfolio already holds or chance-level ones. One-day reversal after the largest scaled down days was +0.85 % the next day (t 3.69, 718), which the rebound strategies already hold. The next day's excess return was +0.47 % on Thursdays (t 3.19) and +0.39 % on Fridays (t 2.87), and 045-01 already holds the late-week gain. Upward 5-day momentum in rising calm markets gave +2.35 % (t 2.24), which the rising calm continuation strategies hold.
- **F6:** The book lost mainly on the coins that rallied out of deep closes. Its daily return moved against the coins' average (correlation −0.51), and its mean net trade result was −6.44 % on ZEC (128 trades) and about −1.1 % on LTC and XRP. Its mean was positive in only 5 of the 12 windows shown.

## Ideas
- `072-04.g2_choppy-calm-deep-close-fall` (from F1, F2, F3): In a choppy, calm market, the further a coin's close sits below its 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next three days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `072-04.g1_falling-calm-deep-close-continuation` (from F2, F3, F4): In a falling, calm market, the further a coin's close sits below its 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
