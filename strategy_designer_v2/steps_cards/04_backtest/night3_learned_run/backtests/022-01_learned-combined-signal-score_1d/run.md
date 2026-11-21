# Backtest of 022-01_learned-combined-signal-score_1d

- Plan: `../../../../03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 41 | 0.01161 | 1.105 |
| w2 | 43 | 0.04414 | 4.761 |
| w3 | 37 | 0.05894 | 21.601 |
| w4 | 49 | -0.099618 | -57.232 |
| w5 | 61 | -0.139483 | -22.852 |
| w6 | 46 | -0.209421 | -36.428 |
| w7 | 43 | -0.15038 | -11.189 |
| w8 | 31 | -0.104583 | -50.814 |
| w9 | 45 | -0.017987 | -12.675 |
| w10 | 55 | 0.135375 | -28.605 |
| w11 | 53 | -0.019569 | 24.712 |
| w12 | 50 | -0.023938 | -4.191 |
| w13 | 29 | -0.033596 | -9.215 |
| w14 | 38 | 0.091355 | 24.598 |
| w15 | 54 | -0.007187 | 38.589 |
| w16 | 34 | -0.126147 | -20.17 |
| w17 | 50 | -0.014366 | -50.905 |
| w18 | 37 | -0.090323 | -24.16 |
| w19 | 59 | -0.100801 | -24.14 |
| w20 | 43 | -0.203244 | -38.824 |
| w21 | 44 | -0.048128 | -6.374 |
| w22 | 39 | 0.094691 | 11.966 |
| w23 | 68 | -0.05227 | -16.187 |
| w24 | 57 | -0.11601 | -5.951 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 70 | -0.118822 | -27.793 |
| w2 | 47 | 0.167231 | -10.807 |
| w3 | 30 | 0.027077 | 5.027 |
| w4 | 24 | -0.081398 | -45.771 |
| w5 | 43 | -0.04399 | -5.613 |
| w6 | 62 | 0.015863 | -21.387 |
| w7 | 57 | -0.068853 | 21.481 |
| w8 | 30 | -0.065694 | -24.602 |
| w9 | 44 | -0.110049 | -22.07 |
| w10 | 49 | -0.061665 | -38.495 |
| w11 | 59 | -0.15739 | -36.812 |
| w12 | 69 | -0.084769 | -13.627 |
| w13 | 56 | 0.05426 | 5.885 |
| w14 | 54 | 0.087122 | 42.081 |
| w15 | 57 | -0.19774 | -33.978 |
| w16 | 50 | 0.012785 | 16.641 |
| w17 | 54 | -0.056071 | -7.166 |
| w18 | 54 | 0.116161 | 5.172 |
| w19 | 50 | -0.131984 | -28.45 |
| w20 | 32 | -0.14809 | -20.636 |
| w21 | 55 | -0.053878 | -9.771 |
| w22 | 39 | -0.143086 | -8.848 |
| w23 | 38 | -0.115437 | 26.096 |
| w24 | 53 | -0.074783 | -5.235 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 45 | -0.057387 | -27.37 |
| w2 | 53 | 0.182985 | -5.722 |
| w3 | 57 | 0.052646 | 25.248 |
| w4 | 61 | -0.105308 | -53.622 |
| w5 | 47 | 0.073423 | 38.18 |
| w6 | 56 | 0.096954 | 25.149 |
| w7 | 62 | -0.218705 | -3.965 |
| w8 | 41 | -0.105215 | -43.302 |
| w9 | 29 | -0.153802 | 6.277 |
| w10 | 52 | 0.006135 | -18.891 |
| w11 | 64 | -0.022213 | 7.422 |
| w12 | 39 | 0.117939 | 14.798 |
| w13 | 45 | -0.180478 | -11.295 |
| w14 | 58 | 0.118212 | 23.666 |
| w15 | 46 | 0.10138 | 27.964 |
| w16 | 55 | 0.021805 | 8.732 |
| w17 | 48 | -0.112457 | -37.687 |
| w18 | 52 | -0.02253 | -26.318 |
| w19 | 61 | -0.0224 | -31.757 |
| w20 | 66 | 0.006068 | -6.98 |
| w21 | 58 | -0.131134 | -63.316 |
| w22 | 64 | -0.075639 | -12.958 |
| w23 | 58 | 0.075844 | -3.942 |
| w24 | 64 | 0.033505 | 15.791 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 68 | 0.034827 | -5.628 |
| w2 | 48 | 0.120752 | 28.251 |
| w3 | 50 | 0.25374 | 28.564 |
| w4 | 47 | 0.04358 | -14.241 |
| w5 | 54 | -0.018074 | -10.81 |
| w6 | 60 | 0.093977 | -13.052 |
| w8 | 38 | -0.035525 | -31.149 |
| w9 | 59 | -0.110513 | -33.922 |
| w10 | 29 | -0.084032 | -46.487 |
| w11 | 66 | -0.03443 | -13.106 |
| w12 | 77 | 0.045227 | -15.115 |
| w14 | 56 | 0.160647 | 50.429 |
| w15 | 45 | 0.008854 | -4.262 |
| w16 | 48 | 0.039221 | 16.628 |
| w17 | 46 | 0.077255 | -10.138 |
| w18 | 59 | 0.044352 | 18.245 |
| w19 | 49 | 0.305513 | 92.77 |
| w20 | 53 | 0.155 | 7.092 |
| w21 | 58 | 0.124895 | -8.345 |
| w22 | 67 | 0.12215 | -5.373 |
| w23 | 58 | -0.243888 | -74.48 |
| w24 | 63 | -0.08629 | 10.985 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 483 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 21 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | 0.010785 | -13.823 |
| w2 | 38 | 0.116359 | -15.013 |
| w3 | 0 | -0.048852 | 0.0 |
| w4 | 0 | 0.11703 | 0.0 |
| w5 | 0 | 0.056154 | 0.0 |
| w6 | 23 | 0.087034 | 10.009 |
| w8 | 32 | -0.004006 | -3.236 |
| w9 | 56 | 0.071702 | -4.4 |
| w10 | 58 | -0.11856 | -43.512 |
| w11 | 43 | -0.006988 | -49.916 |
| w12 | 19 | 0.016382 | -13.47 |
| w15 | 39 | -0.075835 | -33.035 |
| w16 | 56 | -0.027256 | -30.889 |
| w17 | 38 | 0.108714 | -49.48 |
| w18 | 42 | 0.032605 | 25.495 |
| w19 | 56 | 0.080711 | 4.569 |
| w20 | 52 | -0.056964 | -34.066 |
| w21 | 50 | -0.031393 | -13.973 |
| w22 | 62 | -0.159883 | -3.9 |
| w23 | 59 | -0.024247 | 11.07 |
| w24 | 68 | -0.088827 | -15.682 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 470 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 47 | -0.115696 | -18.992 |
| w2 | 62 | 0.09441 | -9.975 |
| w3 | 60 | 0.064261 | 5.999 |
| w4 | 55 | 0.077163 | 6.79 |
| w5 | 58 | 0.205502 | 46.656 |
| w6 | 55 | 0.068137 | -18.822 |
| w7 | 48 | 0.069033 | -15.831 |
| w8 | 32 | -0.095782 | -33.713 |
| w9 | 50 | -0.162776 | -29.843 |
| w10 | 64 | -0.19794 | -18.949 |
| w11 | 61 | -0.025962 | -34.367 |
| w12 | 60 | 0.051552 | 24.418 |
| w14 | 38 | 0.168533 | -21.511 |
| w15 | 42 | -0.11776 | -7.9 |
| w16 | 61 | 0.091468 | 69.285 |
| w17 | 62 | -0.147968 | -34.581 |
| w18 | 56 | 0.119758 | 20.555 |
| w19 | 51 | -0.018633 | -20.9 |
| w20 | 54 | -0.075981 | -14.211 |
| w21 | 59 | -0.035041 | -13.711 |
| w22 | 63 | -0.194609 | -39.263 |
| w23 | 51 | 0.080681 | 17.138 |
| w24 | 52 | -0.03932 | -32.015 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

