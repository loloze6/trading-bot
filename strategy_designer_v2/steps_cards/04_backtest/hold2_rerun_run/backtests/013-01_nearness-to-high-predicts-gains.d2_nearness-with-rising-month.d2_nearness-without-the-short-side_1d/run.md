# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d

- Plan: `../../../../03_test_plan/hold2_rerun_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.073766 | -3.737 |
| w2 | 6 | 0.053154 | -0.601 |
| w3 | 11 | -0.133932 | -6.412 |
| w4 | 15 | -0.055608 | 20.676 |
| w5 | 10 | 0.035194 | 3.393 |
| w6 | 21 | 0.022112 | 74.834 |
| w7 | 10 | -0.030646 | -4.839 |
| w8 | 17 | -0.012647 | 13.693 |
| w9 | 8 | -0.054829 | -9.537 |
| w10 | 34 | -0.009186 | 24.701 |
| w11 | 28 | -0.081303 | 29.371 |
| w12 | 15 | 0.025853 | 4.619 |
| w13 | 11 | -0.094714 | -6.724 |
| w14 | 7 | -0.108914 | -10.28 |
| w15 | 32 | -0.102111 | 24.412 |
| w16 | 21 | 0.006043 | 5.051 |
| w17 | 17 | 0.118724 | 175.925 |
| w18 | 12 | 0.062419 | 3.708 |
| w19 | 22 | 0.056248 | 51.436 |
| w20 | 25 | -0.1442 | -17.673 |
| w21 | 28 | -0.01521 | 58.746 |
| w22 | 16 | -0.088432 | -5.316 |
| w23 | 29 | 0.020868 | 10.651 |
| w24 | 9 | -0.016252 | -8.6 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.02202 | -4.846 |
| w2 | 11 | 0.074358 | 2.528 |
| w3 | 9 | -0.073902 | -7.217 |
| w4 | 13 | -0.073723 | 5.801 |
| w5 | 13 | -0.089857 | -10.863 |
| w6 | 27 | 0.000883 | 33.735 |
| w7 | 4 | 0.068153 | -2.591 |
| w8 | 18 | -0.226409 | -5.914 |
| w9 | 11 | -0.118498 | -14.136 |
| w10 | 18 | 0.056906 | 70.383 |
| w11 | 35 | 0.024731 | 98.627 |
| w12 | 26 | -0.045864 | -5.505 |
| w13 | 15 | 0.077844 | 19.136 |
| w14 | 4 | -0.17604 | -5.075 |
| w15 | 16 | 0.045598 | 7.634 |
| w16 | 19 | 0.001073 | 10.668 |
| w17 | 26 | 0.047045 | 26.88 |
| w18 | 17 | 0.006112 | 18.246 |
| w19 | 24 | 0.002099 | 32.542 |
| w20 | 11 | -0.009332 | -3.702 |
| w21 | 22 | -0.024363 | 15.281 |
| w22 | 2 | -0.047881 | -7.114 |
| w23 | 20 | -0.019963 | 51.414 |
| w24 | 14 | -0.040869 | -6.197 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.086747 | -8.172 |
| w2 | 8 | 0.023381 | 1.751 |
| w3 | 13 | -0.031836 | 2.781 |
| w4 | 26 | -0.122041 | -8.35 |
| w5 | 19 | -0.159653 | -19.923 |
| w6 | 15 | -0.178736 | -8.427 |
| w7 | 5 | -0.046094 | -4.219 |
| w8 | 19 | -0.11885 | 9.488 |
| w9 | 6 | -0.065882 | -2.752 |
| w10 | 16 | 0.011414 | 10.87 |
| w11 | 45 | -0.133758 | 19.477 |
| w12 | 14 | -0.03155 | -5.109 |
| w13 | 15 | -0.051733 | -4.029 |
| w14 | 4 | -0.137322 | -2.916 |
| w15 | 23 | 0.038652 | 4.935 |
| w16 | 13 | 0.034877 | 7.558 |
| w17 | 34 | 0.03387 | 30.562 |
| w18 | 13 | 0.016973 | 1.051 |
| w19 | 29 | -0.011979 | 10.758 |
| w20 | 3 | -0.141022 | -4.724 |
| w21 | 36 | -0.043457 | 16.43 |
| w22 | 20 | -0.128117 | -24.027 |
| w23 | 26 | -0.066224 | 5.608 |
| w24 | 9 | -0.271332 | -33.223 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.024394 | -4.164 |
| w2 | 11 | -0.042206 | -5.565 |
| w3 | 13 | -0.101229 | -10.085 |
| w4 | 17 | -0.032274 | -0.485 |
| w5 | 8 | 0.019255 | 0.754 |
| w6 | 41 | -0.171817 | -4.885 |
| w7 | 5 | -0.059448 | -5.097 |
| w8 | 18 | -0.059117 | 5.884 |
| w9 | 6 | -0.021651 | -4.617 |
| w10 | 23 | 0.010302 | 35.462 |
| w11 | 38 | -0.036128 | 50.302 |
| w12 | 7 | -0.113876 | -8.62 |
| w14 | 8 | -0.024462 | -6.186 |
| w15 | 18 | -0.080223 | -3.326 |
| w16 | 19 | 0.00803 | 7.578 |
| w17 | 36 | -0.100078 | 12.0 |
| w18 | 17 | -0.037662 | -6.109 |
| w19 | 9 | -0.284924 | -38.719 |
| w20 | 29 | -0.092309 | -4.78 |
| w21 | 31 | -0.040324 | -10.414 |
| w22 | 34 | -0.100573 | 20.168 |
| w23 | 18 | 0.123589 | 28.758 |
| w24 | 46 | -0.222488 | 1.036 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.128521 | -8.693 |
| w2 | 0 | 0.03686 | 0.0 |
| w3 | 0 | 0.046456 | 0.0 |
| w4 | 0 | -0.118458 | 0.0 |
| w5 | 1 | -0.127034 | -0.132 |
| w6 | 14 | -0.100948 | 0.668 |
| w8 | 17 | -0.214705 | -8.461 |
| w9 | 11 | 0.047506 | -4.196 |
| w10 | 12 | 0.06564 | 22.285 |
| w11 | 34 | -0.005723 | 55.928 |
| w12 | 18 | -0.097976 | -12.901 |
| w14 | 8 | -0.035931 | -4.364 |
| w15 | 7 | -0.032723 | -5.866 |
| w16 | 13 | 0.008143 | 6.087 |
| w17 | 26 | 0.170044 | 99.848 |
| w18 | 13 | -0.069059 | -2.282 |
| w19 | 16 | -0.077486 | -5.881 |
| w20 | 14 | -0.060068 | -0.667 |
| w21 | 25 | 0.261198 | 215.678 |
| w22 | 13 | -0.075656 | -3.731 |
| w23 | 28 | 0.050192 | 29.988 |
| w24 | 4 | -0.094757 | -11.001 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.016242 | 1.547 |
| w2 | 12 | -0.02312 | -2.438 |
| w3 | 6 | -0.060085 | -5.646 |
| w4 | 15 | -0.117717 | -4.549 |
| w5 | 7 | 0.005389 | -0.598 |
| w6 | 28 | -0.181032 | -10.075 |
| w7 | 11 | -0.038733 | -9.483 |
| w8 | 9 | 0.016222 | 10.329 |
| w9 | 1 | -0.043761 | -0.752 |
| w10 | 28 | -0.046467 | 10.681 |
| w11 | 40 | -0.114936 | 44.977 |
| w12 | 16 | -0.08438 | -7.848 |
| w14 | 5 | -0.110036 | -6.789 |
| w15 | 19 | 0.053856 | -1.109 |
| w16 | 13 | 0.139247 | 38.369 |
| w17 | 16 | -0.096596 | -8.161 |
| w18 | 9 | 0.021347 | 1.336 |
| w19 | 5 | 0.024707 | -0.629 |
| w20 | 20 | 0.029169 | 19.553 |
| w21 | 34 | -0.040358 | 19.894 |
| w22 | 8 | -0.150365 | -8.538 |
| w23 | 13 | -0.022262 | -1.547 |
| w24 | 34 | 0.167687 | 208.977 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

