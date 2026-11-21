# Backtest of 022-02_combination-beats-best-single_1d

- Plan: `../../../../03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 44 | 0.011526 | 2.175 |
| w2 | 44 | 0.056123 | 11.337 |
| w3 | 34 | 0.06576 | 20.363 |
| w4 | 49 | -0.102582 | -57.687 |
| w5 | 64 | -0.142506 | -24.793 |
| w6 | 47 | -0.212661 | -37.692 |
| w7 | 44 | -0.148291 | -11.67 |
| w8 | 38 | -0.114376 | -49.567 |
| w9 | 48 | -0.018159 | -15.225 |
| w10 | 51 | 0.104624 | -28.425 |
| w11 | 55 | -0.018892 | 20.56 |
| w12 | 50 | -0.022422 | -3.685 |
| w13 | 25 | -0.034775 | -8.974 |
| w14 | 39 | 0.090264 | 24.259 |
| w15 | 54 | -0.017757 | 37.067 |
| w16 | 33 | -0.126629 | -20.43 |
| w17 | 52 | -0.020229 | -54.535 |
| w18 | 36 | -0.090397 | -21.666 |
| w19 | 57 | -0.101558 | -15.973 |
| w20 | 41 | -0.200717 | -38.931 |
| w21 | 46 | -0.048835 | -11.385 |
| w22 | 36 | 0.100499 | 12.913 |
| w23 | 67 | -0.045414 | -15.016 |
| w24 | 55 | -0.112181 | -8.936 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 70 | -0.120048 | -28.805 |
| w2 | 48 | 0.165612 | -11.624 |
| w3 | 31 | 0.02603 | 5.625 |
| w4 | 24 | -0.080975 | -46.25 |
| w5 | 45 | -0.041824 | -4.25 |
| w6 | 61 | 0.018419 | -22.026 |
| w7 | 54 | -0.065418 | 14.46 |
| w8 | 31 | -0.071202 | -28.603 |
| w9 | 43 | -0.108886 | -22.019 |
| w10 | 45 | -0.068591 | -38.63 |
| w11 | 58 | -0.159422 | -37.021 |
| w12 | 74 | -0.072883 | -12.573 |
| w13 | 57 | 0.065734 | 9.255 |
| w14 | 56 | 0.08658 | 47.313 |
| w15 | 56 | -0.196592 | -32.358 |
| w16 | 50 | 0.016374 | 18.261 |
| w17 | 54 | -0.058776 | -8.708 |
| w18 | 50 | 0.118747 | 8.353 |
| w19 | 52 | -0.113905 | -21.195 |
| w20 | 32 | -0.143303 | -21.245 |
| w21 | 56 | -0.054805 | -10.614 |
| w22 | 40 | -0.140466 | -8.117 |
| w23 | 40 | -0.114144 | 28.026 |
| w24 | 51 | -0.080243 | -5.779 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 46 | -0.062844 | -26.307 |
| w2 | 54 | 0.189876 | -8.796 |
| w3 | 60 | 0.050818 | 24.81 |
| w4 | 59 | -0.10593 | -52.374 |
| w5 | 47 | 0.075593 | 39.382 |
| w6 | 56 | 0.098368 | 26.033 |
| w7 | 53 | -0.198603 | -1.317 |
| w8 | 45 | -0.100762 | -37.383 |
| w9 | 38 | -0.162846 | 4.793 |
| w10 | 55 | -0.001118 | -19.841 |
| w11 | 59 | -0.024618 | 7.077 |
| w12 | 47 | 0.118553 | 15.794 |
| w13 | 48 | -0.164187 | -19.666 |
| w14 | 59 | 0.112262 | 26.534 |
| w15 | 49 | 0.09982 | 26.722 |
| w16 | 57 | 0.021636 | 8.437 |
| w17 | 48 | -0.116534 | -34.955 |
| w18 | 46 | -0.02161 | -23.954 |
| w19 | 54 | -0.028009 | -31.651 |
| w20 | 69 | 0.003731 | -9.147 |
| w21 | 53 | -0.133177 | -63.365 |
| w22 | 65 | -0.077214 | -12.203 |
| w23 | 60 | 0.075685 | -3.224 |
| w24 | 64 | 0.042211 | 19.268 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 67 | 0.030777 | -5.896 |
| w2 | 52 | 0.115112 | 25.766 |
| w3 | 49 | 0.259687 | 28.033 |
| w4 | 55 | 0.043809 | -13.906 |
| w5 | 63 | -0.014103 | -11.224 |
| w6 | 62 | 0.09077 | -12.611 |
| w8 | 38 | -0.035717 | -31.13 |
| w9 | 59 | -0.109156 | -35.559 |
| w10 | 29 | -0.106054 | -48.428 |
| w11 | 69 | -0.022024 | -5.596 |
| w12 | 76 | 0.045017 | -14.04 |
| w14 | 56 | 0.160647 | 50.429 |
| w15 | 48 | 0.00645 | -3.286 |
| w16 | 45 | 0.042054 | 18.313 |
| w17 | 44 | 0.074854 | -12.911 |
| w18 | 56 | 0.051114 | -15.854 |
| w19 | 53 | 0.299717 | 87.122 |
| w20 | 52 | 0.158437 | 12.248 |
| w21 | 58 | 0.121921 | -8.236 |
| w22 | 66 | 0.129635 | -3.318 |
| w23 | 62 | -0.239396 | -74.23 |
| w24 | 63 | -0.089322 | 11.949 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 483 warm-up bars -- required_bars=569. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=569. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 21 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | 0.015283 | -11.403 |
| w2 | 38 | 0.116394 | -9.3 |
| w3 | 0 | -0.060826 | 0.0 |
| w4 | 0 | 0.106723 | 0.0 |
| w5 | 0 | 0.058804 | 0.0 |
| w6 | 15 | 0.08829 | 2.357 |
| w8 | 32 | -0.004006 | -3.236 |
| w9 | 55 | 0.069668 | -5.286 |
| w10 | 58 | -0.127219 | -44.139 |
| w11 | 41 | -0.001736 | -47.98 |
| w12 | 21 | 0.018317 | -12.568 |
| w15 | 39 | -0.075865 | -33.034 |
| w16 | 56 | -0.032202 | -32.589 |
| w17 | 38 | 0.110845 | -49.6 |
| w18 | 42 | 0.031386 | 24.164 |
| w19 | 60 | 0.082324 | 1.094 |
| w20 | 52 | -0.057489 | -34.754 |
| w21 | 48 | -0.037174 | -16.965 |
| w22 | 66 | -0.151681 | -4.215 |
| w23 | 60 | -0.019617 | 12.452 |
| w24 | 69 | -0.097649 | -11.595 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=569. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=569. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 470 warm-up bars -- required_bars=569. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | -0.107174 | -19.191 |
| w2 | 63 | 0.091271 | -10.525 |
| w3 | 60 | 0.058864 | 4.224 |
| w4 | 58 | 0.075984 | 5.347 |
| w5 | 61 | 0.205112 | 49.596 |
| w6 | 58 | 0.070423 | -19.074 |
| w8 | 32 | -0.096551 | -33.57 |
| w9 | 55 | -0.155697 | -23.658 |
| w10 | 59 | -0.183211 | -12.406 |
| w11 | 63 | -0.013273 | -28.241 |
| w12 | 64 | 0.052658 | 26.792 |
| w14 | 38 | 0.168533 | -21.511 |
| w15 | 41 | -0.121369 | -9.601 |
| w16 | 62 | 0.08311 | 59.433 |
| w17 | 64 | -0.150474 | -36.67 |
| w18 | 57 | 0.12142 | 20.367 |
| w19 | 51 | -0.019187 | -21.111 |
| w20 | 54 | -0.080241 | -17.296 |
| w21 | 60 | -0.034175 | -13.912 |
| w22 | 60 | -0.190571 | -33.724 |
| w23 | 51 | 0.08125 | 15.511 |
| w24 | 52 | -0.044164 | -32.754 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 548 warm-up bars -- required_bars=569. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=569. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

