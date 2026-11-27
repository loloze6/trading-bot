# Backtest of 067-02.b1.b1.b1_agitated-chop-downside-stretch-carries_1d

- Plan: `../../../../03_test_plan/night9_chopstretch_run/plans/067-02.b1.b1.b1_agitated-chop-downside-stretch-carries_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.130414 | -0.784 |
| w2 | 0 | None | 0.0 |
| w3 | 3 | 0.033411 | 0.628 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.085101 | -6.008 |
| w13 | 1 | 0.095013 | 4.144 |
| w14 | 0 | None | 0.0 |
| w15 | 9 | 0.032483 | -2.337 |
| w16 | 1 | 0.324095 | 27.653 |
| w17 | 8 | -0.038317 | -4.274 |
| w18 | 4 | -0.182056 | -7.303 |
| w19 | 5 | -0.044571 | -8.015 |
| w20 | 15 | -0.077317 | -5.785 |
| w21 | 8 | -0.012281 | -3.072 |
| w22 | 1 | 0.108841 | 2.599 |
| w23 | 0 | None | 0.0 |
| w24 | 20 | -0.092811 | -1.543 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 11 | 0.146032 | 4.076 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | 0.071091 | 1.62 |
| w9 | 4 | 0.019992 | -0.683 |
| w10 | 2 | 0.045078 | -0.609 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.046847 | -2.982 |
| w13 | 0 | 0.024651 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.017209 | 3.773 |
| w16 | 1 | 0.135025 | 2.669 |
| w17 | 4 | -0.144193 | -2.839 |
| w18 | 6 | 0.123546 | 4.188 |
| w19 | 9 | -0.046903 | -4.176 |
| w20 | 11 | -0.055995 | -5.323 |
| w21 | 0 | None | 0.0 |
| w22 | 8 | -0.152948 | 0.579 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.053247 | -2.01 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 8 | -0.001779 | -0.879 |
| w4 | 4 | -0.17772 | -5.018 |
| w5 | 12 | -0.060429 | -4.262 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 5 | 0.023963 | -2.467 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 7 | 0.016084 | -2.88 |
| w13 | 2 | -0.131628 | -0.454 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.099321 | -0.913 |
| w16 | 1 | 0.420008 | 13.044 |
| w17 | 6 | 0.003808 | -1.399 |
| w18 | 7 | 0.134317 | 2.137 |
| w19 | 20 | -0.052078 | -13.593 |
| w20 | 3 | -0.016503 | -0.087 |
| w21 | 7 | -0.045592 | -12.47 |
| w22 | 10 | 0.083848 | -1.72 |
| w23 | 5 | 0.011798 | -0.128 |
| w24 | 0 | None | 0.0 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 6 | 0.18328 | 15.296 |
| w3 | 6 | 0.057123 | -2.551 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.162162 | -8.44 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 7 | -0.097769 | -9.729 |
| w12 | 5 | -0.261313 | -8.967 |
| w14 | 0 | -0.026237 | 0.0 |
| w15 | 6 | -0.056654 | -2.773 |
| w16 | 1 | 0.3449 | 18.063 |
| w17 | 0 | None | 0.0 |
| w18 | 5 | -0.078902 | -4.853 |
| w19 | 25 | -0.043367 | -4.886 |
| w20 | 0 | -0.038746 | 0.0 |
| w21 | 4 | -0.000263 | -0.331 |
| w22 | 17 | -0.110682 | -10.305 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | -0.116118 | -8.279 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.052088 | -1.467 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | -0.18245 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 10 | -0.017007 | -7.098 |
| w6 | 6 | 0.094508 | 0.345 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | -0.035213 | -1.578 |
| w10 | 0 | None | 0.0 |
| w11 | 3 | -0.018912 | -2.749 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 6 | -0.047202 | 5.28 |
| w16 | 3 | 0.238309 | 18.085 |
| w17 | 7 | -0.153166 | -4.43 |
| w18 | 2 | 0.108323 | 0.653 |
| w19 | 10 | 0.05255 | 8.478 |
| w20 | 6 | -0.202369 | -14.026 |
| w21 | 12 | 0.059691 | -1.141 |
| w22 | 12 | -0.120003 | -16.946 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | None | -0.067 |
| w2 | 2 | -0.104576 | 0.816 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | -0.032707 | -0.275 |
| w6 | 4 | -0.035053 | -6.439 |
| w7 | 2 | 0.009563 | 1.257 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 7 | -0.056261 | -12.119 |
| w12 | 10 | -0.061742 | -5.788 |
| w13 | 4 | -0.219905 | -16.609 |
| w14 | 0 | None | 0.0 |
| w15 | 8 | 0.061599 | 8.345 |
| w16 | 0 | None | 0.0 |
| w17 | 16 | -0.024302 | -4.74 |
| w18 | 6 | -0.160963 | -6.356 |
| w19 | 7 | -0.074995 | -7.628 |
| w20 | 7 | 0.114198 | 14.976 |
| w21 | 2 | 0.018836 | -0.921 |
| w22 | 11 | 0.015439 | -2.8 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

