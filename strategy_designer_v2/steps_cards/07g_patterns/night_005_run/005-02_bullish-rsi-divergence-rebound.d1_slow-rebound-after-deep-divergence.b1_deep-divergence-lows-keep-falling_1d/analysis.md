---
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3695 USD
---
## Findings
- **F1:** When a coin closed at a new 30-day high, its excess return over the next 20 days was positive: +4.1% mean, t = 2.25 over 72 spaced events, with 57% of them up. Grid bars without a new high averaged −0.2% (t = −0.16, n = 257). The effect was strongest in ETH (+7.3%, t = 2.59, n = 33) and in windows w13–w24 (+7.7%, t = 2.35, n = 29), and weak in BTC (+1.4%, t = 0.61, n = 39).
- **F2:** The drift grew with the span of the high being broken. New 90-day highs were followed by +6.3% excess over 20 days (t = 2.22, n = 14), against +4.1% for new 30-day highs. On a 10-day horizon, new 30-day highs gave +2.2% (t = 1.97, n = 120).
- **F3:** Among new 30-day lows, a deeper 30-day decline went with a lower excess return over the next 20 days (r = −0.28, n = 61). The correlation was negative in all four coin-by-half subsets: BTC −0.28 and −0.44, ETH −0.07 and −0.32. Across all grid bars the 30-day return had no such link (r = −0.003, n = 179), so the effect is specific to new-low bars.
- **F4:** The RSI divergence added nothing at lows. Divergence lows averaged −4.4% excess (t = −1.03, n = 28) and non-divergence lows −3.3% (t = −1.12, n = 49), a difference with Welch t = −0.20.
- **F5:** The book's worst 2% of days came after the coin had fallen 4.6% over the prior 5 days (all days: +0.55%). On those days the coin itself rose 0.84% (all days: +0.13%). The short loses on rebound days that follow sharp drops.
- **F6:** Weekday and volatility patterns did not stand out once the number of angles is counted. Saturday's mean coin return was +0.28% (t = 2.78), but it held up only in ETH's first half (t = 2.21) and not in the other three subsets. Five-day returns by volatility quintile were all within |t| < 1.4.

## Ideas
- `005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling.g1_new-highs-drift-further-up` (from F1, F2): When a coin closes above its highest close of a past lookback, it rises more than its usual drift over the next 20 days, and the longer the lookback whose high it clears (30 days versus 90 days), the larger the rise.
- `005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling.g2_deep-lows-keep-falling` (from F3, F4): When a coin closes at a new 30-day low, it falls further than its usual drift over the next 20 days, and the deeper its 30-day decline into that low, the larger the further fall, whatever its RSI shows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
