# Backtest of 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d

- Plan: `../../../../03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.005671 | -8.981 |
| w2 | 26 | -0.037368 | -22.613 |
| w3 | 27 | 0.158191 | 25.268 |
| w4 | 32 | 0.069768 | -22.687 |
| w5 | 26 | 0.092109 | 17.707 |
| w6 | 19 | 0.062286 | 20.912 |
| w7 | 17 | 0.118884 | 12.86 |
| w8 | 37 | 0.104946 | 57.911 |
| w9 | 22 | -0.080224 | -6.317 |
| w10 | 28 | 0.045085 | 37.1 |
| w11 | 7 | 0.049555 | 1.129 |
| w12 | 36 | 0.076689 | 13.943 |
| w13 | 33 | 0.007226 | -4.997 |
| w14 | 23 | -0.154867 | -14.844 |
| w15 | 32 | -0.116342 | -1.072 |
| w16 | 36 | 0.097152 | -3.929 |
| w17 | 8 | -0.16206 | 13.558 |
| w18 | 17 | -0.102217 | -34.784 |
| w19 | 53 | 0.088632 | 12.059 |
| w20 | 28 | 0.06383 | 16.984 |
| w21 | 35 | -0.020404 | -34.192 |
| w22 | 28 | 0.037693 | 4.322 |
| w23 | 32 | -0.06525 | 2.827 |
| w24 | 25 | 0.048479 | -1.093 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.11763 | -13.532 |
| w2 | 23 | -0.226047 | -34.212 |
| w3 | 29 | 0.047373 | 6.919 |
| w4 | 11 | 0.195562 | 2.299 |
| w5 | 19 | 0.128722 | 23.858 |
| w6 | 20 | 0.071018 | -5.159 |
| w7 | 34 | -0.004678 | -37.135 |
| w8 | 27 | 0.166197 | 31.756 |
| w9 | 23 | 0.014948 | 7.462 |
| w10 | 14 | 0.095285 | 42.76 |
| w11 | 13 | 0.076674 | 14.006 |
| w12 | 23 | 0.086249 | 12.112 |
| w13 | 40 | 0.231905 | 79.008 |
| w14 | 35 | -0.161733 | -51.175 |
| w15 | 37 | -0.023987 | -20.083 |
| w16 | 31 | -0.12479 | -52.499 |
| w17 | 5 | 0.022424 | 3.094 |
| w18 | 26 | -0.144868 | -51.604 |
| w19 | 35 | 0.09288 | 19.67 |
| w20 | 20 | 0.020305 | -0.791 |
| w21 | 36 | 0.009684 | -1.597 |
| w22 | 18 | 0.034497 | 13.416 |
| w23 | 25 | 0.03432 | 9.276 |
| w24 | 29 | -0.07334 | -14.903 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.088092 | 20.349 |
| w2 | 25 | 0.011653 | -4.978 |
| w3 | 29 | -0.008134 | -1.334 |
| w4 | 16 | 0.075686 | 18.61 |
| w5 | 24 | -0.017629 | -8.71 |
| w6 | 22 | 0.025951 | 14.854 |
| w7 | 14 | 0.122678 | 63.716 |
| w8 | 34 | 0.185252 | 25.451 |
| w9 | 25 | 0.150226 | 40.332 |
| w10 | 6 | -0.019932 | 1.36 |
| w11 | 19 | 0.232178 | 6.716 |
| w12 | 27 | -0.145478 | -35.93 |
| w13 | 10 | 0.061923 | 4.062 |
| w14 | 8 | -0.107923 | -14.586 |
| w15 | 14 | 0.018128 | 4.997 |
| w16 | 29 | -0.019059 | -21.407 |
| w17 | 23 | 0.114906 | 22.727 |
| w18 | 24 | -0.070314 | -35.342 |
| w19 | 18 | 0.004075 | 7.523 |
| w20 | 19 | 0.07382 | 20.095 |
| w21 | 24 | 0.165626 | 7.993 |
| w22 | 24 | 0.188694 | 11.828 |
| w23 | 27 | -0.094796 | -19.486 |
| w24 | 40 | 0.104862 | 32.733 |

- XMRUSD: 19 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.069156 | 2.326 |
| w2 | 25 | -0.00798 | -6.507 |
| w3 | 19 | -0.086215 | -20.989 |
| w4 | 13 | 0.11323 | 16.385 |
| w5 | 43 | 0.144618 | 30.876 |
| w6 | 28 | 0.115344 | 41.239 |
| w9 | 23 | 0.034081 | 20.568 |
| w10 | 19 | 0.037223 | 60.913 |
| w11 | 26 | 0.008157 | -7.089 |
| w12 | 10 | 0.094991 | 15.414 |
| w16 | 38 | -0.119605 | -57.48 |
| w17 | 3 | -0.040955 | 1.016 |
| w18 | 17 | -0.073691 | -50.266 |
| w19 | 35 | 0.013168 | 20.756 |
| w20 | 13 | 0.030496 | 1.465 |
| w21 | 20 | 0.107049 | 20.457 |
| w22 | 25 | 0.013805 | -25.373 |
| w23 | 34 | -0.085085 | -34.056 |
| w24 | 42 | 0.102914 | 38.599 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 483 warm-up bars -- required_bars=852. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w8 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 728 warm-up bars -- required_bars=852. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=852. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 606 warm-up bars -- required_bars=852. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w15 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 848 warm-up bars -- required_bars=852. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 18 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.001539 | -7.525 |
| w2 | 17 | 0.125106 | 3.14 |
| w3 | 0 | 0.020645 | 0.0 |
| w4 | 0 | 0.091976 | 0.0 |
| w5 | 0 | -0.045007 | 0.0 |
| w6 | 0 | -0.037825 | 0.0 |
| w10 | 19 | -0.049142 | 35.966 |
| w11 | 19 | -0.057283 | 46.572 |
| w12 | 12 | -0.043898 | 2.227 |
| w16 | 29 | 0.053933 | 5.646 |
| w17 | 14 | -0.12044 | -23.019 |
| w18 | 13 | -0.140755 | -24.542 |
| w19 | 0 | -0.051097 | 0.0 |
| w20 | 0 | 0.084337 | 0.0 |
| w21 | 20 | -0.041297 | -31.269 |
| w22 | 22 | 0.087536 | 6.89 |
| w23 | 4 | -0.084677 | -6.83 |
| w24 | 14 | 0.070195 | 11.189 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=852. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w8 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 592 warm-up bars -- required_bars=852. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w9 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 835 warm-up bars -- required_bars=852. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=852. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 470 warm-up bars -- required_bars=852. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w15 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 712 warm-up bars -- required_bars=852. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 20 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.167611 | 7.858 |
| w2 | 12 | 0.005881 | -10.132 |
| w3 | 19 | -0.132767 | -51.948 |
| w4 | 17 | 0.027441 | 2.656 |
| w5 | 33 | -0.120462 | -48.448 |
| w6 | 16 | 0.052425 | 22.64 |
| w9 | 34 | 0.288604 | 46.793 |
| w10 | 30 | 0.176708 | 74.14 |
| w11 | 26 | -0.010719 | 12.734 |
| w12 | 17 | -0.048686 | -13.03 |
| w15 | 28 | -0.115751 | -25.169 |
| w16 | 26 | -0.040553 | -36.586 |
| w17 | 9 | -0.01863 | -7.067 |
| w18 | 19 | -0.098824 | -44.543 |
| w19 | 27 | 0.056691 | 5.394 |
| w20 | 23 | 0.130246 | 38.561 |
| w21 | 38 | 0.10972 | 14.761 |
| w22 | 21 | -0.005633 | -4.027 |
| w23 | 26 | 0.002726 | -7.643 |
| w24 | 25 | 0.169072 | -19.072 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 548 warm-up bars -- required_bars=852. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w8 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 793 warm-up bars -- required_bars=852. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=852. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 671 warm-up bars -- required_bars=852. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

