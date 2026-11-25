# Backtest of 032-03_low-volume-decline-continues-more_1d

- Plan: `../../../../03_test_plan/night7c_steadydecline_run/plans/032-03_low-volume-decline-continues-more_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | 0.035487 | 15.146 |
| w2 | 7 | 0.227476 | 28.744 |
| w3 | 6 | -0.017214 | -3.104 |
| w4 | 11 | 0.004109 | -36.464 |
| w5 | 17 | 0.07588 | 17.985 |
| w6 | 3 | 0.007171 | -18.513 |
| w7 | 9 | -0.037151 | -6.391 |
| w8 | 6 | -0.014582 | -4.656 |
| w9 | 16 | -0.017896 | 11.927 |
| w10 | 9 | 0.007095 | -7.393 |
| w11 | 7 | -0.019132 | -5.666 |
| w12 | 12 | 0.033602 | 2.755 |
| w13 | 5 | 0.091806 | 4.28 |
| w14 | 18 | 0.020024 | 62.032 |
| w15 | 1 | -0.003936 | 0.1 |
| w16 | 3 | 0.164475 | 14.308 |
| w17 | 3 | 0.19328 | 9.092 |
| w18 | 11 | -0.001734 | -1.333 |
| w19 | 7 | -0.081337 | -11.054 |
| w20 | 17 | -0.040153 | -16.412 |
| w21 | 8 | -0.037922 | -10.496 |
| w22 | 30 | -0.058745 | -3.812 |
| w23 | 20 | -0.033329 | -21.598 |
| w24 | 12 | -0.106302 | -9.586 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.124476 | 25.217 |
| w2 | 6 | 0.184315 | 32.117 |
| w3 | 9 | -0.01495 | -3.056 |
| w4 | 16 | -0.066893 | -18.766 |
| w5 | 21 | -0.100663 | 7.396 |
| w6 | 9 | 0.034214 | -6.812 |
| w7 | 17 | 0.159689 | 42.733 |
| w8 | 0 | -0.077202 | 0.0 |
| w9 | 23 | -0.174352 | -27.455 |
| w10 | 6 | -0.061012 | -19.596 |
| w11 | 2 | 0.015633 | -2.545 |
| w12 | 19 | -0.17661 | -24.818 |
| w13 | 10 | 0.165038 | 12.882 |
| w14 | 4 | 0.109333 | 9.851 |
| w15 | 11 | 0.093758 | 12.868 |
| w16 | 2 | -0.024212 | -12.861 |
| w17 | 4 | -0.02708 | -0.524 |
| w18 | 7 | 0.026093 | -6.925 |
| w19 | 8 | 0.010322 | -9.156 |
| w20 | 16 | -0.074285 | -10.802 |
| w21 | 15 | -0.122252 | -46.429 |
| w22 | 6 | 0.007204 | 2.056 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | 0.002351 | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.019409 | 10.01 |
| w2 | 23 | 0.117684 | 24.146 |
| w3 | 20 | -0.203549 | -38.183 |
| w4 | 12 | 0.108475 | 5.055 |
| w5 | 10 | 0.070495 | 9.541 |
| w6 | 20 | -0.161767 | -23.771 |
| w7 | 13 | 0.055933 | 56.569 |
| w8 | 2 | -0.353691 | -12.024 |
| w9 | 14 | -0.048382 | 5.678 |
| w10 | 19 | -0.088502 | -13.523 |
| w11 | 0 | None | 0.0 |
| w12 | 15 | -0.037639 | -2.147 |
| w13 | 4 | 0.051221 | -0.477 |
| w14 | 21 | -0.030188 | 41.626 |
| w15 | 0 | None | 0.0 |
| w16 | 3 | -0.06046 | -14.12 |
| w17 | 4 | -0.018423 | -4.645 |
| w18 | 10 | -0.063832 | -11.492 |
| w19 | 6 | -0.036158 | -0.992 |
| w20 | 27 | -0.144648 | 9.789 |
| w21 | 9 | -0.064562 | -32.179 |
| w22 | 7 | -0.201369 | -2.31 |
| w23 | 8 | -0.040482 | -6.351 |
| w24 | 12 | -0.026004 | -0.521 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.113339 | -18.637 |
| w2 | 9 | 0.08827 | 3.1 |
| w3 | 26 | -0.026666 | -5.665 |
| w4 | 10 | 0.021645 | -1.902 |
| w5 | 18 | 0.01779 | 3.725 |
| w6 | 9 | -0.080597 | -10.023 |
| w8 | 6 | -0.038716 | -3.158 |
| w9 | 20 | -0.079308 | 9.691 |
| w10 | 9 | -0.030778 | -10.75 |
| w11 | 0 | None | 0.0 |
| w12 | 7 | -0.132962 | -1.624 |
| w14 | 13 | 0.063287 | 41.113 |
| w15 | 7 | -0.011518 | 4.447 |
| w16 | 3 | -0.16319 | -26.17 |
| w17 | 6 | -0.153007 | -6.744 |
| w18 | 3 | -0.05334 | -3.566 |
| w19 | 0 | 0.051503 | 0.0 |
| w20 | 0 | 0.042867 | 0.0 |
| w21 | 6 | -0.007341 | -5.883 |
| w22 | 18 | -0.068154 | -23.068 |
| w23 | 11 | 0.027191 | 10.023 |
| w24 | 0 | None | 0.0 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 483 warm-up bars -- required_bars=491. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=491. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 21 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.021383 | 2.149 |
| w2 | 12 | 0.115033 | 25.333 |
| w3 | 0 | 0.014199 | 0.0 |
| w4 | 0 | -0.011016 | 0.0 |
| w5 | 0 | -0.149422 | 0.0 |
| w6 | 5 | -0.060387 | -2.684 |
| w8 | 9 | -0.049077 | -1.359 |
| w9 | 8 | -0.073023 | -1.141 |
| w10 | 9 | -0.026544 | -20.239 |
| w11 | 3 | -0.01422 | -11.187 |
| w12 | 11 | -0.020113 | 5.86 |
| w15 | 6 | 0.005892 | -5.222 |
| w16 | 2 | -0.079274 | -2.707 |
| w17 | 15 | -0.033891 | -18.89 |
| w18 | 8 | 0.011155 | -5.392 |
| w19 | 0 | -0.052866 | 0.0 |
| w20 | 17 | 0.042803 | 6.685 |
| w21 | 14 | 0.117866 | -8.974 |
| w22 | 0 | -0.016342 | 0.0 |
| w23 | 11 | 0.006916 | -20.215 |
| w24 | 18 | 0.061329 | 23.774 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=491. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=491. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 470 warm-up bars -- required_bars=491. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.160264 | -12.202 |
| w2 | 13 | -0.085304 | -5.755 |
| w3 | 8 | 0.015843 | 34.439 |
| w4 | 13 | -0.215595 | -24.917 |
| w5 | 12 | 0.154663 | 28.365 |
| w6 | 8 | -0.086698 | -20.017 |
| w7 | 12 | -0.096441 | -10.091 |
| w8 | 16 | -0.085984 | -11.99 |
| w9 | 16 | -0.157259 | -5.59 |
| w10 | 10 | -0.053955 | -16.712 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.067704 | -6.751 |
| w14 | 16 | -0.113608 | 1.344 |
| w15 | 5 | 0.08088 | 9.417 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.041641 | -4.951 |
| w18 | 6 | -0.077847 | -5.951 |
| w19 | 0 | -0.019098 | 0.0 |
| w20 | 5 | 0.132225 | 3.576 |
| w21 | 9 | -0.005014 | -14.117 |
| w22 | 13 | -0.05017 | -4.531 |
| w23 | 16 | -0.051734 | -16.849 |
| w24 | 0 | None | 0.0 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=491. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

