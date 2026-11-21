# Backtest of 022-02_combination-beats-best-single.d1_combination-only-in-downtrends_1d

- Plan: `../../../../03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single.d1_combination-only-in-downtrends_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 37 | -0.039861 | -5.134 |
| w2 | 44 | 0.046361 | 6.089 |
| w3 | 35 | 0.050019 | 19.708 |
| w4 | 6 | -0.13877 | -32.024 |
| w5 | 17 | -0.186121 | -6.993 |
| w6 | 18 | -0.032243 | -16.226 |
| w7 | 41 | -0.147011 | -10.591 |
| w8 | 20 | 0.00856 | -9.317 |
| w9 | 41 | -0.005357 | -10.586 |
| w10 | 10 | 0.05295 | -3.589 |
| w11 | 0 | None | 0.0 |
| w12 | 8 | -0.073429 | 0.537 |
| w13 | 18 | -0.000953 | -8.001 |
| w14 | 37 | 0.087901 | 9.256 |
| w15 | 0 | None | 0.0 |
| w16 | 24 | -0.077719 | -6.93 |
| w17 | 0 | None | 0.0 |
| w18 | 23 | -0.076287 | -16.792 |
| w19 | 0 | None | 0.0 |
| w20 | 21 | -0.070169 | -23.197 |
| w21 | 11 | 0.156103 | 20.638 |
| w22 | 25 | 0.094319 | 9.612 |
| w23 | 3 | -0.019064 | -3.451 |
| w24 | 38 | -0.093333 | -7.216 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 59 | -0.091781 | -23.429 |
| w2 | 45 | 0.151969 | -10.933 |
| w3 | 22 | 0.015604 | 5.123 |
| w4 | 10 | -0.130007 | -20.019 |
| w5 | 21 | -0.00414 | -2.474 |
| w6 | 36 | -0.071884 | -4.267 |
| w7 | 46 | -0.023349 | 17.493 |
| w8 | 20 | -0.07686 | -13.799 |
| w9 | 43 | -0.110129 | -22.017 |
| w10 | 9 | -0.043743 | -5.633 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 17 | -0.013789 | -11.333 |
| w14 | 56 | 0.08658 | 47.313 |
| w15 | 7 | 0.011173 | -6.107 |
| w16 | 20 | -0.175151 | -23.141 |
| w17 | 5 | -0.06537 | -9.447 |
| w18 | 19 | -0.012362 | -0.602 |
| w19 | 0 | None | 0.0 |
| w20 | 21 | -0.05079 | -0.191 |
| w21 | 21 | -0.008902 | 23.05 |
| w22 | 28 | -0.136343 | -10.61 |
| w23 | 9 | -0.03654 | 15.775 |
| w24 | 24 | -0.021691 | 4.189 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 46 | -0.062844 | -26.307 |
| w2 | 54 | 0.189876 | -8.796 |
| w3 | 27 | 0.065579 | 12.814 |
| w4 | 9 | 0.060849 | 9.092 |
| w5 | 39 | 0.009383 | 19.085 |
| w6 | 38 | 0.015672 | 10.258 |
| w7 | 49 | -0.212537 | 2.054 |
| w8 | 23 | 0.025469 | -15.909 |
| w9 | 38 | -0.162846 | 4.793 |
| w10 | 23 | -0.085097 | -26.605 |
| w11 | 0 | None | 0.0 |
| w12 | 10 | 0.010048 | 8.961 |
| w13 | 25 | -0.046719 | -5.243 |
| w14 | 59 | 0.112262 | 26.534 |
| w15 | 9 | 0.077901 | 11.988 |
| w16 | 31 | -0.093844 | -14.027 |
| w17 | 6 | 0.071848 | 12.622 |
| w18 | 31 | 0.066904 | 7.087 |
| w19 | 15 | -0.030741 | -4.266 |
| w20 | 56 | -0.053733 | -11.871 |
| w21 | 25 | 0.009179 | -0.979 |
| w22 | 35 | -0.040174 | -7.494 |
| w23 | 29 | 0.078648 | -2.844 |
| w24 | 38 | 0.001083 | 17.817 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 52 | 0.021504 | -9.667 |
| w2 | 34 | 0.018656 | 7.047 |
| w3 | 34 | 0.079919 | 7.187 |
| w4 | 15 | 0.086452 | 3.634 |
| w5 | 28 | -0.107844 | -22.138 |
| w6 | 25 | -0.001013 | -16.548 |
| w8 | 25 | 0.067894 | 8.864 |
| w9 | 59 | -0.109156 | -35.559 |
| w10 | 14 | -0.034628 | -5.763 |
| w11 | 0 | None | 0.0 |
| w12 | 45 | 0.139763 | -6.288 |
| w14 | 55 | 0.137874 | 37.449 |
| w15 | 3 | 0.020915 | -3.119 |
| w16 | 14 | -0.047947 | 2.383 |
| w17 | 0 | None | 0.0 |
| w18 | 36 | 0.228596 | 18.586 |
| w19 | 50 | 0.274379 | 33.55 |
| w20 | 9 | 0.155133 | -6.66 |
| w21 | 33 | 0.0419 | 8.687 |
| w22 | 7 | 0.121116 | 7.182 |
| w23 | 17 | -0.177113 | -34.12 |
| w24 | 24 | -0.051777 | -7.469 |

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
| w1 | 36 | -0.117377 | -14.773 |
| w2 | 38 | 0.104953 | -9.111 |
| w3 | 0 | 0.101781 | 0.0 |
| w4 | 0 | 0.130048 | 0.0 |
| w5 | 0 | 0.102812 | 0.0 |
| w6 | 0 | -0.013219 | 0.0 |
| w8 | 31 | -0.105168 | -14.016 |
| w9 | 55 | 0.049041 | -9.568 |
| w10 | 29 | -0.050515 | -16.921 |
| w11 | 10 | -0.013783 | -4.864 |
| w12 | 11 | -0.041446 | -20.429 |
| w15 | 15 | -0.01531 | -16.847 |
| w16 | 44 | -0.011542 | -23.456 |
| w17 | 8 | -0.047549 | -39.453 |
| w18 | 15 | 0.156657 | 16.165 |
| w19 | 36 | 0.035407 | 0.085 |
| w20 | 31 | -0.219934 | -35.333 |
| w21 | 14 | -0.057969 | 11.031 |
| w22 | 27 | -0.180068 | -12.469 |
| w23 | 29 | -0.146596 | -5.563 |
| w24 | 48 | -0.090808 | -12.022 |

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
| w1 | 23 | -0.042847 | -3.592 |
| w2 | 60 | 0.070472 | -9.156 |
| w3 | 55 | 0.091827 | 9.255 |
| w4 | 49 | 0.042541 | 7.806 |
| w5 | 61 | 0.205112 | 49.596 |
| w6 | 31 | -0.080152 | -36.571 |
| w8 | 27 | -0.023482 | -33.937 |
| w9 | 55 | -0.155697 | -23.658 |
| w10 | 19 | -0.112558 | -7.21 |
| w11 | 4 | 0.01628 | 21.475 |
| w12 | 21 | 0.114219 | 11.85 |
| w14 | 38 | 0.168533 | -21.511 |
| w15 | 11 | -0.032189 | -4.121 |
| w16 | 21 | -0.038067 | 21.361 |
| w17 | 35 | -0.153347 | -20.764 |
| w18 | 39 | 0.17718 | 18.633 |
| w19 | 36 | 0.003734 | -15.313 |
| w20 | 26 | -0.005481 | -3.971 |
| w21 | 2 | 0.172533 | -3.792 |
| w22 | 42 | -0.237868 | -33.515 |
| w23 | 18 | 0.158422 | 25.631 |
| w24 | 6 | 0.049373 | -0.279 |

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

