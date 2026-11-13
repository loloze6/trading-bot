---
line: 7.f real and profitable
backtest: N4-01_breakout-drift-lasts_1d
idea tested: N4-01_breakout-drift-lasts
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3192 USD
---
## Findings
- **F1:** The book's compounded gain rests on one coin-window. Trades' summed net log return is 19.44, but without ZEC in w24 it is -0.31. Eight of the ten best trades (net +336% to +1159%, held 22–121 days) are ZEC w24, and the top 10 trades carry 41% of the summed net trade return.
- **F2:** The gain depends on a few rising years and moves with plain holding. Trade net sums are -4728 in 2018 and -2121 in 2022. Book Sharpe falls from 0.57 overall to 0.32 without 2020 and to 0.03 without 2020, 2024 and 2025. Yearly book Sharpe tracks holding's (2018: -1.23 vs -1.10; 2022: -0.56 vs -0.76; 2020: 2.15 vs 1.52).
- **F3:** The book earns only when the coin is above its close of 20 days earlier. Next-day book return there averages 0.0037 (7187 days, sum 26.7), against -0.0001 when it is below (7313 days, sum -0.82). The best cell is rising and volatile (mean 0.0061, 2256 days); the worst is falling and calm (mean -0.0013, 2408 days).
- **F4:** Two of six coins lose. LTC's net log sum is -11.40 and XMR's is -12.64, against ETH +16.47 and XRP +12.00. Per coin, the non-overlapping 10-bar excess return after new 20-day highs has no t above 2 (XRP 1.90 on 38 events; BTC -0.77 on 51; XMR -0.33 on 52).
- **F5:** The drift after a new 20-day closing high appears only when the coin's 60-bar return is negative. In that case the non-overlapping 10-bar excess return is +0.046 (87 events, t=3.32). When the 60-bar return is positive it is -0.0006 (198 events, t=-0.05).
- **F6:** Fees are small in simple terms but large in compounding terms. They take 2.3% of the summed gross trade return but 14.5% of the gross log return (22.73 to 19.44). The win rate is 41%, and the median trade is negative in every volatility tercile.

## Ideas
- `N4-01_breakout-drift-lasts.f1_breakout-after-longer-decline` (from F5, F4): In one coin's daily bars, a close at its highest close of the prior 20 days, made while the close is below its close of 60 bars earlier, is followed by a rise over the next ten bars larger than the coin's average ten-bar rise.
- `N4-01_breakout-drift-lasts.f2_breakout-drift-needs-volatile-uptrend` (from F3, F2): In one coin's daily bars, after a close at its highest close of the prior 20 days, the next day's rise is larger while the close stays above its close of 20 bars earlier and the coin's 20-day volatility is in its upper third.
- `N4-01_breakout-drift-lasts.f3_breakout-drift-on-other-coins` (from F1, F4, F6): In one coin's daily bars, a close at its highest close of the prior 20 days is followed by a rise over the next ten bars larger than the coin's average ten-bar rise, on coins other than those whose gain came from one rally window.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
