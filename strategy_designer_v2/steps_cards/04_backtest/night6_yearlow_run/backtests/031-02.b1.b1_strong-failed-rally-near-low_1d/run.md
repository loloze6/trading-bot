# Backtest of 031-02.b1.b1_strong-failed-rally-near-low_1d

- Plan: `../../../../03_test_plan/night6_yearlow_run/plans/031-02.b1.b1_strong-failed-rally-near-low_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.015889 | 7.097 |
| w2 | 2 | 0.117861 | 6.317 |
| w3 | 8 | 0.179466 | 21.976 |
| w4 | 3 | 0.006602 | -16.904 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 10 | 0.072759 | 15.037 |
| w8 | 13 | -0.156714 | -48.0 |
| w9 | 0 | 0.065425 | 0.0 |
| w10 | 14 | 0.028101 | -12.735 |
| w11 | 0 | None | 0.0 |
| w12 | 18 | 0.02502 | -1.532 |
| w13 | 0 | None | 0.0 |
| w14 | 8 | 0.080889 | 45.613 |
| w15 | 0 | None | 0.0 |
| w16 | 7 | 0.0529 | 1.839 |
| w17 | 4 | 0.079498 | -5.696 |
| w18 | 4 | -0.095971 | -4.339 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 14 | -0.225808 | -56.638 |
| w22 | 6 | 0.000851 | -3.97 |
| w23 | 23 | -0.000135 | -7.34 |
| w24 | 6 | 0.019974 | 27.448 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.02407 | 4.374 |
| w2 | 8 | 0.068516 | 29.505 |
| w3 | 10 | 0.027285 | 14.199 |
| w4 | 7 | -0.22494 | -25.758 |
| w5 | 1 | 0.298693 | 11.212 |
| w6 | 5 | -0.051756 | -14.72 |
| w7 | 8 | 0.029785 | 13.823 |
| w8 | 11 | -0.124716 | -17.368 |
| w9 | 0 | None | 0.0 |
| w10 | 6 | -0.09593 | -20.439 |
| w11 | 0 | None | 0.0 |
| w12 | 15 | 0.012856 | -2.852 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | 0.012279 | 5.709 |
| w15 | 0 | None | 0.0 |
| w16 | 10 | 0.042475 | -7.436 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | -0.095943 | -10.826 |
| w19 | 4 | 0.086334 | -5.77 |
| w20 | 0 | None | 0.0 |
| w21 | 17 | -0.046799 | -34.298 |
| w22 | 5 | -0.050369 | 8.641 |
| w23 | 4 | -0.066737 | -10.959 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.002833 | 5.357 |
| w2 | 3 | -0.034714 | 0.387 |
| w3 | 2 | -0.118623 | -4.211 |
| w4 | 0 | None | 0.0 |
| w5 | 5 | 0.062822 | 11.544 |
| w6 | 9 | 0.150745 | -1.683 |
| w8 | 8 | -0.157978 | -23.981 |
| w9 | 0 | None | 0.0 |
| w10 | 10 | -0.064923 | -29.643 |
| w11 | 0 | None | 0.0 |
| w12 | 11 | 0.065973 | 15.948 |
| w13 | 0 | 0.143956 | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 13 | 0.048341 | 1.901 |
| w17 | 4 | 0.053151 | -7.88 |
| w18 | 3 | -0.072459 | -1.055 |
| w19 | 12 | -0.112396 | -29.226 |
| w20 | 0 | -0.031194 | 0.0 |
| w21 | 13 | -0.009488 | -40.039 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.059647 | -0.874 |
| w24 | 0 | -0.075462 | 0.0 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 465 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 465 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XMRUSD: 20 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.008647 | -5.843 |
| w2 | 8 | 0.042295 | 5.333 |
| w3 | 6 | -0.132061 | 3.069 |
| w4 | 0 | None | 0.0 |
| w5 | 11 | 0.164316 | 25.404 |
| w6 | 19 | -0.016972 | -16.476 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 15 | 0.203716 | 41.455 |
| w15 | 0 | None | 0.0 |
| w16 | 11 | 0.090179 | -4.107 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | 0.000976 | 0.66 |
| w19 | 3 | 0.038507 | 2.269 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.066053 | -2.686 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 465 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w8 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 465 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 465 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 13 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.029245 | 12.548 |
| w2 | 0 | 0.07178 | 0.0 |
| w9 | 7 | -0.060015 | 8.211 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | -0.017986 | 0.0 |
| w16 | 0 | -0.009737 | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w21 | 14 | 0.104653 | -50.734 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- w3 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 465 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w4 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 465 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w5 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 465 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w6 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 465 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w8 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 465 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 465 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w15 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 465 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w19 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 465 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w20 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 465 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 21 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.076632 | 15.987 |
| w2 | 3 | 0.139398 | 8.657 |
| w3 | 5 | 0.055605 | 9.395 |
| w4 | 0 | 0.069104 | 0.0 |
| w5 | 3 | 0.197896 | 8.394 |
| w6 | 7 | -0.089237 | -10.032 |
| w8 | 2 | 0.06924 | -1.147 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.0042 | -12.342 |
| w12 | 18 | 0.029821 | -22.258 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | -0.061785 | -0.486 |
| w19 | 0 | 0.037246 | 0.0 |
| w20 | 3 | 0.085351 | 0.075 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | 0.02761 | 2.299 |
| w24 | 13 | 0.020328 | -99.539 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 465 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 465 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

