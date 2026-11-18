---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its highest close of a past lookback, it rises more than its usual drift over the next 20 days, and the longer the lookback whose high it clears (30 days versus 90 days), the larger the rise.
Consequence: A close at a new multi-week high is a reason to hold or add a long rather than fade it, and more so the longer the high it breaks.
Why:
- F1: When a coin closed at a new 30-day high, its excess return over the next 20 days was positive: +4.1% mean, t = 2.25 over 72 spaced events, with 57% of them up. Grid bars without a new high averaged −0.2% (t = −0.16, n = 257). The effect was strongest in ETH (+7.3%, t = 2.59, n = 33) and in windows w13–w24 (+7.7%, t = 2.35, n = 29), and weak in BTC (+1.4%, t = 0.61, n = 39).
- F2: The drift grew with the span of the high being broken. New 90-day highs were followed by +6.3% excess over 20 days (t = 2.22, n = 14), against +4.1% for new 30-day highs. On a 10-day horizon, new 30-day highs gave +2.2% (t = 1.97, n = 120).
