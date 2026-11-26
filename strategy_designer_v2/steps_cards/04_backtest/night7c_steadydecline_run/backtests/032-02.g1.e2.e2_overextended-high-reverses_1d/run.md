# Backtest of 032-02.g1.e2.e2_overextended-high-reverses_1d

- Plan: `../../../../03_test_plan/night7c_steadydecline_run/plans/032-02.g1.e2.e2_overextended-high-reverses_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.086168 | 2.391 |
| w2 | 7 | -0.037794 | 3.834 |
| w3 | 3 | 0.078963 | 18.336 |
| w4 | 18 | 0.132473 | -36.045 |
| w5 | 5 | 0.132577 | 10.018 |
| w6 | 19 | -0.169461 | -45.159 |
| w7 | 6 | -0.025103 | -0.689 |
| w8 | 12 | -0.017735 | -24.291 |
| w9 | 5 | -0.029246 | 3.476 |
| w10 | 16 | 0.010581 | -5.323 |
| w11 | 13 | -0.062843 | -28.854 |
| w12 | 10 | 0.056773 | -0.109 |
| w13 | 4 | 0.037618 | 4.394 |
| w14 | 1 | 0.180822 | 3.143 |
| w15 | 16 | -0.113562 | -47.977 |
| w16 | 18 | 0.058499 | -3.646 |
| w17 | 23 | -0.107178 | -59.082 |
| w18 | 10 | 0.041096 | 0.135 |
| w19 | 15 | -0.095426 | -33.142 |
| w20 | 5 | 0.067489 | 5.896 |
| w21 | 23 | -0.041184 | -34.599 |
| w22 | 6 | 0.038395 | 1.101 |
| w23 | 17 | -0.029856 | -14.867 |
| w24 | 5 | -0.037433 | 0.37 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.067813 | 0.34 |
| w2 | 6 | 0.036652 | -17.667 |
| w3 | 6 | 0.030384 | 23.995 |
| w4 | 22 | 0.049077 | 4.527 |
| w5 | 4 | 0.141685 | 12.465 |
| w6 | 14 | 0.061 | -21.233 |
| w7 | 2 | -0.039783 | 2.149 |
| w8 | 11 | 0.143826 | 8.534 |
| w9 | 3 | -0.065603 | 1.425 |
| w10 | 12 | -0.121625 | -34.256 |
| w11 | 24 | 0.030017 | -30.917 |
| w12 | 7 | -0.001035 | -3.2 |
| w13 | 11 | -0.154688 | -10.493 |
| w14 | 3 | 0.04628 | -0.251 |
| w15 | 11 | -0.117945 | -25.292 |
| w16 | 14 | 0.011373 | -37.203 |
| w17 | 18 | -0.010746 | -0.903 |
| w18 | 10 | 0.009844 | -24.075 |
| w19 | 12 | -0.03325 | -27.663 |
| w20 | 8 | -0.020419 | 2.23 |
| w21 | 9 | 0.093483 | -23.185 |
| w22 | 0 | None | 0.0 |
| w23 | 17 | -0.090157 | -27.777 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.081351 | -1.577 |
| w2 | 4 | -0.000682 | 3.436 |
| w3 | 9 | -0.12087 | -3.127 |
| w4 | 18 | 0.200218 | 22.201 |
| w5 | 6 | 0.106323 | 13.91 |
| w6 | 8 | 0.0618 | 10.042 |
| w7 | 3 | -0.000758 | 9.688 |
| w8 | 12 | 0.047436 | -3.586 |
| w9 | 5 | 0.031725 | 6.852 |
| w10 | 6 | -0.020336 | -11.673 |
| w11 | 16 | -0.080881 | -13.912 |
| w12 | 6 | 0.093545 | 17.116 |
| w13 | 1 | 0.084051 | 0.538 |
| w14 | 0 | 0.249452 | 0.0 |
| w15 | 10 | -0.048165 | -11.653 |
| w16 | 8 | 0.068844 | -7.764 |
| w17 | 12 | 0.061819 | -19.097 |
| w18 | 7 | 0.104044 | 3.16 |
| w19 | 10 | -0.049601 | -5.743 |
| w20 | 1 | 0.009028 | 0.728 |
| w21 | 11 | -0.022978 | -24.635 |
| w22 | 7 | 0.022829 | 5.316 |
| w23 | 12 | 0.050504 | -23.47 |
| w24 | 3 | 0.179741 | 9.106 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.041342 | 0.726 |
| w2 | 8 | 0.0424 | -1.585 |
| w3 | 5 | 0.006202 | 7.244 |
| w4 | 11 | 0.047301 | 3.725 |
| w5 | 5 | 0.023693 | -1.378 |
| w6 | 16 | -0.027503 | -15.383 |
| w8 | 13 | 0.002723 | -14.046 |
| w9 | 6 | 0.034339 | 6.869 |
| w10 | 20 | 0.084349 | -12.064 |
| w11 | 18 | 0.147585 | -15.574 |
| w12 | 2 | 0.040463 | 3.371 |
| w14 | 4 | 0.191596 | 7.038 |
| w15 | 9 | -0.021365 | -10.031 |
| w16 | 14 | -0.010858 | -23.018 |
| w17 | 9 | 0.190848 | -1.385 |
| w18 | 11 | -0.000287 | 6.337 |
| w19 | 1 | 0.033486 | 25.728 |
| w20 | 12 | 0.026547 | -14.671 |
| w21 | 9 | 0.290704 | -1.272 |
| w22 | 11 | -0.133926 | -13.414 |
| w23 | 8 | -0.178765 | -36.328 |
| w24 | 12 | 0.279717 | 38.703 |

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
| w1 | 3 | -0.011936 | 0.155 |
| w2 | 0 | 0.074919 | 0.0 |
| w3 | 0 | 0.083413 | 0.0 |
| w4 | 0 | 0.038055 | 0.0 |
| w5 | 0 | 0.161861 | 0.0 |
| w6 | 8 | -0.182645 | -17.997 |
| w8 | 4 | 0.199559 | 1.618 |
| w9 | 5 | 0.135252 | 26.704 |
| w10 | 9 | -0.194185 | -27.944 |
| w11 | 12 | -0.021358 | -30.407 |
| w12 | 1 | 0.17592 | 5.74 |
| w15 | 3 | -0.025439 | 6.152 |
| w16 | 8 | -0.009634 | -13.618 |
| w17 | 13 | -0.182504 | -79.225 |
| w18 | 5 | -0.056847 | -7.575 |
| w19 | 6 | 0.161323 | 13.733 |
| w20 | 6 | 0.03574 | 10.738 |
| w21 | 15 | -0.466958 | -80.701 |
| w22 | 3 | 0.017437 | 2.672 |
| w23 | 10 | -0.165225 | -8.455 |
| w24 | 0 | 0.073148 | 0.0 |

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
| w1 | 6 | -0.028022 | -8.803 |
| w2 | 5 | -0.062241 | 1.406 |
| w3 | 1 | 0.029387 | 4.498 |
| w4 | 8 | -0.049427 | 7.296 |
| w5 | 1 | 0.050778 | 1.79 |
| w6 | 11 | 0.178039 | -2.264 |
| w7 | 4 | 0.064169 | 2.841 |
| w8 | 7 | -0.028374 | -14.653 |
| w9 | 1 | 0.06167 | 3.074 |
| w10 | 15 | 0.015498 | -21.101 |
| w11 | 14 | -0.06016 | -25.154 |
| w12 | 11 | 0.054327 | 18.759 |
| w14 | 2 | 0.021771 | 4.98 |
| w15 | 9 | 0.091113 | -2.749 |
| w16 | 16 | 0.014566 | -23.705 |
| w17 | 7 | 0.096283 | 3.393 |
| w18 | 10 | -0.010591 | -2.899 |
| w19 | 9 | -0.00407 | -5.315 |
| w20 | 13 | -0.007982 | -21.556 |
| w21 | 11 | -0.104819 | -29.885 |
| w22 | 4 | 0.187602 | 6.595 |
| w23 | 9 | -0.055567 | -4.451 |
| w24 | 17 | -0.141104 | -78.639 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=491. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

