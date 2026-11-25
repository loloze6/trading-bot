# Backtest of 050-01_falling-calm-scaled-week-fall-continuation_1d

- Plan: `../../../../03_test_plan/night7_panic_run/plans/050-01_falling-calm-scaled-week-fall-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | 0.002969 | 6.449 |
| w2 | 15 | 0.092897 | 21.371 |
| w3 | 24 | 0.125091 | -2.923 |
| w4 | 2 | 0.015418 | -0.563 |
| w5 | 9 | 0.000398 | -1.681 |
| w6 | 9 | -0.035567 | -5.328 |
| w7 | 26 | -0.038254 | -0.911 |
| w8 | 8 | 0.006626 | -0.599 |
| w9 | 26 | -0.277387 | -44.267 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | 0.034784 | 5.477 |
| w12 | 13 | -0.064352 | -9.179 |
| w13 | 9 | 0.021392 | -2.997 |
| w14 | 8 | 0.176652 | 41.047 |
| w15 | 0 | None | 0.0 |
| w16 | 3 | -0.097993 | -5.623 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.079869 | 0.748 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.022724 | -4.229 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.09108 | 2.263 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.01162 | 6.023 |
| w2 | 2 | -0.088467 | 12.316 |
| w3 | 12 | 0.199558 | 1.433 |
| w4 | 2 | -0.011004 | -0.935 |
| w5 | 12 | 0.004194 | 4.022 |
| w6 | 20 | 0.020014 | -8.76 |
| w7 | 29 | 0.006705 | 24.983 |
| w8 | 0 | None | 0.0 |
| w9 | 31 | -0.09935 | -13.634 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.021444 | 1.194 |
| w13 | 17 | 0.146653 | 29.293 |
| w14 | 8 | 0.182176 | 35.507 |
| w15 | 16 | 0.045918 | 5.598 |
| w16 | 0 | -0.196135 | 0.0 |
| w17 | 4 | -0.056051 | -2.994 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | 0.033396 | 0.211 |
| w22 | 6 | -0.080917 | -3.016 |
| w23 | 0 | None | 0.0 |
| w24 | 18 | -0.015203 | 2.233 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | -0.025087 | 2.746 |
| w2 | 3 | 0.047531 | 4.916 |
| w3 | 10 | 0.012574 | 0.091 |
| w4 | 4 | -0.128184 | -18.871 |
| w5 | 4 | -0.01657 | 0.21 |
| w6 | 18 | 0.053204 | 0.723 |
| w7 | 50 | 0.030153 | 25.35 |
| w8 | 0 | None | 0.0 |
| w9 | 39 | -0.011406 | 6.952 |
| w10 | 11 | -0.058629 | -6.624 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.020563 | -0.372 |
| w13 | 25 | -0.005321 | -1.49 |
| w14 | 16 | 0.135531 | 43.386 |
| w15 | 10 | 0.068887 | 9.478 |
| w16 | 2 | -0.095401 | -6.361 |
| w17 | 8 | -0.098053 | -9.558 |
| w18 | 5 | -0.007632 | -1.237 |
| w19 | 2 | -0.110343 | -12.575 |
| w20 | 17 | -0.045456 | -4.719 |
| w21 | 3 | -0.047812 | -10.237 |
| w22 | 3 | 0.016948 | 2.26 |
| w23 | 0 | None | 0.0 |
| w24 | 10 | -0.026968 | -4.821 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.082438 | -6.081 |
| w2 | 4 | -0.081476 | -0.486 |
| w3 | 11 | 0.005447 | 0.018 |
| w4 | 7 | -0.23478 | -9.074 |
| w5 | 13 | -0.098534 | -0.69 |
| w6 | 9 | -0.109691 | -8.221 |
| w7 | 50 | -0.03046 | 14.176 |
| w8 | 7 | 0.024975 | -7.081 |
| w9 | 37 | 0.003154 | 7.014 |
| w10 | 3 | -0.268757 | -4.787 |
| w11 | 0 | None | 0.0 |
| w12 | 27 | -0.038297 | -8.245 |
| w14 | 10 | 0.200191 | 68.933 |
| w15 | 7 | 0.068185 | 4.499 |
| w16 | 0 | -0.081401 | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.009081 | -1.359 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | -0.161556 | -9.627 |
| w21 | 6 | -0.046573 | -7.779 |
| w22 | 2 | -0.05728 | -2.823 |
| w23 | 11 | 0.074306 | 18.498 |
| w24 | 3 | 0.008584 | -0.154 |

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
| w1 | 25 | 0.100449 | 19.326 |
| w2 | 8 | -0.109688 | 15.105 |
| w3 | 0 | 0.033987 | 0.0 |
| w4 | 0 | 0.005334 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 9 | 0.012623 | -4.626 |
| w8 | 28 | -0.171486 | -5.818 |
| w9 | 27 | 0.007733 | 0.821 |
| w10 | 6 | -0.022556 | -2.682 |
| w11 | 0 | None | 0.0 |
| w12 | 22 | -0.066421 | -7.762 |
| w14 | 19 | 0.02907 | 3.837 |
| w15 | 18 | 0.01246 | 0.538 |
| w16 | 0 | -0.194304 | 0.0 |
| w17 | 10 | -0.005764 | -2.025 |
| w18 | 11 | -0.006751 | -10.779 |
| w19 | 18 | -0.095639 | -13.519 |
| w20 | 21 | 0.0074 | 4.709 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.073529 | -0.447 |
| w23 | 4 | 0.001275 | -2.056 |
| w24 | 34 | -0.07916 | 13.072 |

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
| w1 | 25 | 0.073024 | 5.276 |
| w2 | 7 | -0.18654 | -12.564 |
| w3 | 38 | 0.03173 | 18.767 |
| w4 | 17 | -0.027131 | -10.137 |
| w5 | 18 | 0.05534 | 11.891 |
| w6 | 8 | 0.035782 | 3.517 |
| w7 | 38 | -0.052994 | 0.254 |
| w8 | 24 | -0.050543 | -1.853 |
| w9 | 29 | 0.047496 | 13.634 |
| w10 | 2 | -0.081071 | -1.879 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | -0.06579 | -2.012 |
| w13 | 19 | 0.065764 | 0.03 |
| w14 | 27 | 0.056166 | 22.974 |
| w15 | 12 | 0.018309 | 5.5 |
| w16 | 0 | None | 0.0 |
| w17 | 17 | 0.031316 | -9.718 |
| w18 | 3 | -0.023851 | -1.182 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | 0.023514 | -2.768 |
| w21 | 8 | -0.03862 | -5.944 |
| w22 | 0 | None | 0.0 |
| w23 | 16 | -0.02575 | -17.219 |
| w24 | 0 | None | 0.0 |

