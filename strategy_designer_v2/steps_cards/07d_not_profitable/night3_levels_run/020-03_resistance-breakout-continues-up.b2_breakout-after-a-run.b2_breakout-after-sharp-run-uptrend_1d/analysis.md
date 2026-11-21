---
line: 7.d not profitable
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend_1d
idea tested: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4200 USD
---
## Findings
- **F1:** Calmar fails because the falls are long and come with bear markets in the coins: the yearly return is 22.4 % against a deepest fall of 33.3 %. That fall took 226 days to its trough, from w1 to w3, while holding the coins lost 64 %. The next falls are 27.7 % (w16–w17, coins −44 %), 25.8 % (w12–w15, coins −76 %) and 23.1 % (w18–w21, coins −26 %).
- **F2:** The book loses in the windows where the coins fall: w2 −10.7 % (coins −44 %), w3 −16.6 %, w13 −9.5 % (coins −34 %), w14 −8.1 % (coins −49 %), w18 −14.5 % (coins −22 %). It is long in bear markets, with only the 60-day filter between it and them.
- **F3:** Held positions earn nothing once the coin has turned down, even with the 60-day return positive at entry. The daily gain on held bars is −3.0 bps (t −0.63, 1144 bars) when the coin's 20-day return is below −6 %, and +6.2 bps (t 0.69) between −6 % and +2 %. It is +28 to +38 bps (t 2.7 to 3.1) above +2 %.
- **F4:** The same split appears against the 50-day average, measured as the share the close sits above or below it. Held bars earn −7.5 bps (t −0.66, 791 bars) with the close more than 2 % below it, and +8.6 bps (t 1.10) within −2 % to +5 %. They earn +31 to +41 bps (t 2.6 to 3.1) above +5 %.
- **F5:** Held bars also earn nothing at the weak end of the 60-day return. Below +3 % they earn −3.6 bps (t −0.33). Between +3 % and +47 % they earn +32 to +44 bps (t 2.0 to 3.2).
- **F6:** The 10-day run-up the idea grades by does not grade the trades: mean net gain per trade by run-up quartile is 2.2 %, 3.1 %, 2.0 % and 3.8 % (452 trades each).
- **F7:** Calm, contracting volatility carries no gain. Held bars where the coin's 10-day volatility is below 0.65 of its 60-day volatility earn +4.6 bps (t 0.54, 666 bars). Above 1.27 of it they earn +53.6 bps (t 2.55).
- **F8:** Cost is not the cause. The unusual move per case (+0.44 %, 1205 cases, t 1.28) is 2.3 times the 0.19 % cost of a trade, and the total move (+1.02 %) is 5.3 times it.

## Ideas
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average` (from F1, F2, F4, F5): When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 5 days, only while its 60-day return is positive and its close is above its 50-day average, and the further its close stands above that average, the larger the rise.
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d2_breakout-after-strong-month` (from F2, F3, F6): When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 5 days, only while its 60-day return is positive, and the larger its 20-day return before the break, the larger the rise.
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d3_breakout-with-expanding-volatility` (from F6, F7): When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 5 days, only while its 60-day return is positive, and the larger its 10-day volatility relative to its 60-day volatility, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
