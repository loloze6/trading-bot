# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d

- Plan: `../../../../03_test_plan/hold_paying_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.073766 | -4.255 |
| w2 | 8 | 0.053154 | -2.048 |
| w3 | 10 | -0.133932 | -7.213 |
| w4 | 14 | -0.055608 | 20.806 |
| w5 | 11 | 0.035194 | 3.788 |
| w6 | 22 | 0.022112 | 74.819 |
| w7 | 10 | -0.030646 | -4.885 |
| w8 | 18 | -0.012647 | 14.726 |
| w9 | 9 | -0.054829 | -10.129 |
| w10 | 33 | -0.009186 | 24.562 |
| w11 | 31 | -0.081303 | 29.849 |
| w12 | 17 | 0.025853 | 1.003 |
| w13 | 11 | -0.094714 | -5.294 |
| w14 | 7 | -0.108914 | -9.928 |
| w15 | 32 | -0.102111 | 24.127 |
| w16 | 21 | 0.006043 | 5.042 |
| w17 | 17 | 0.118724 | 175.925 |
| w18 | 13 | 0.062419 | 3.583 |
| w19 | 22 | 0.056248 | 46.971 |
| w20 | 25 | -0.1442 | -15.949 |
| w21 | 28 | -0.01521 | 59.579 |
| w22 | 17 | -0.088432 | -5.706 |
| w23 | 31 | 0.020868 | 10.992 |
| w24 | 13 | -0.016252 | -9.13 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.02202 | -4.785 |
| w2 | 11 | 0.074358 | 2.184 |
| w3 | 9 | -0.073902 | -7.234 |
| w4 | 14 | -0.073723 | 4.94 |
| w5 | 14 | -0.089857 | -10.676 |
| w6 | 28 | 0.000883 | 33.571 |
| w7 | 4 | 0.068153 | -2.591 |
| w8 | 17 | -0.226409 | -4.521 |
| w9 | 12 | -0.118498 | -13.042 |
| w10 | 16 | 0.056906 | 71.107 |
| w11 | 36 | 0.024731 | 98.958 |
| w12 | 25 | -0.045864 | -6.248 |
| w13 | 16 | 0.077844 | 18.324 |
| w14 | 5 | -0.17604 | -5.002 |
| w15 | 14 | 0.045598 | 11.642 |
| w16 | 20 | 0.001073 | 11.024 |
| w17 | 26 | 0.047045 | 28.221 |
| w18 | 19 | 0.006112 | 19.473 |
| w19 | 24 | 0.002099 | 31.966 |
| w20 | 11 | -0.009332 | -3.701 |
| w21 | 24 | -0.024363 | 15.571 |
| w22 | 2 | -0.047881 | -7.114 |
| w23 | 20 | -0.019963 | 51.431 |
| w24 | 17 | -0.040869 | -7.986 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.086747 | -7.726 |
| w2 | 8 | 0.023381 | 0.477 |
| w3 | 14 | -0.031836 | 3.593 |
| w4 | 27 | -0.122041 | -7.615 |
| w5 | 20 | -0.159653 | -18.691 |
| w6 | 16 | -0.178736 | -6.713 |
| w7 | 6 | -0.046094 | -7.454 |
| w8 | 18 | -0.11885 | 12.356 |
| w9 | 6 | -0.065882 | -5.745 |
| w10 | 17 | 0.011414 | 14.096 |
| w11 | 45 | -0.133758 | 19.203 |
| w12 | 14 | -0.03155 | -5.761 |
| w13 | 15 | -0.051733 | -4.029 |
| w14 | 6 | -0.137322 | -7.861 |
| w15 | 24 | 0.038652 | 3.428 |
| w16 | 13 | 0.034877 | 5.988 |
| w17 | 32 | 0.03387 | 30.46 |
| w18 | 13 | 0.016973 | 1.045 |
| w19 | 27 | -0.011979 | 10.473 |
| w20 | 4 | -0.141022 | -4.638 |
| w21 | 35 | -0.043457 | 20.625 |
| w22 | 21 | -0.128117 | -23.364 |
| w23 | 26 | -0.066224 | 5.674 |
| w24 | 11 | -0.271332 | -32.887 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | -0.024394 | -3.247 |
| w2 | 12 | -0.042206 | -4.323 |
| w3 | 14 | -0.101229 | -9.35 |
| w4 | 19 | -0.032274 | 0.162 |
| w5 | 8 | 0.019255 | 0.207 |
| w6 | 37 | -0.171817 | -2.771 |
| w7 | 5 | -0.059448 | -7.661 |
| w8 | 21 | -0.059117 | 6.197 |
| w9 | 6 | -0.021651 | -4.308 |
| w10 | 24 | 0.010302 | 36.166 |
| w11 | 41 | -0.036128 | 50.236 |
| w12 | 10 | -0.113876 | -8.21 |
| w14 | 11 | -0.024462 | -9.312 |
| w15 | 21 | -0.080223 | -2.709 |
| w16 | 19 | 0.00803 | 5.844 |
| w17 | 34 | -0.100078 | 12.95 |
| w18 | 18 | -0.037662 | -6.05 |
| w19 | 10 | -0.284924 | -37.9 |
| w20 | 31 | -0.092309 | -3.972 |
| w21 | 30 | -0.040324 | -8.998 |
| w22 | 35 | -0.100573 | 19.958 |
| w23 | 19 | 0.123589 | 29.214 |
| w24 | 48 | -0.222488 | 3.282 |

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
| w1 | 14 | -0.128521 | -8.867 |
| w2 | 0 | 0.03686 | 0.0 |
| w3 | 0 | 0.046456 | 0.0 |
| w4 | 0 | -0.118458 | 0.0 |
| w5 | 2 | -0.127034 | -0.731 |
| w6 | 15 | -0.100948 | 1.333 |
| w8 | 13 | -0.214705 | -8.277 |
| w9 | 12 | 0.047506 | -7.198 |
| w10 | 10 | 0.06564 | 23.765 |
| w11 | 34 | -0.005723 | 54.544 |
| w12 | 18 | -0.097976 | -12.489 |
| w14 | 9 | -0.035931 | -4.008 |
| w15 | 9 | -0.032723 | -6.066 |
| w16 | 14 | 0.008143 | 3.412 |
| w17 | 28 | 0.170044 | 95.426 |
| w18 | 14 | -0.069059 | -1.002 |
| w19 | 17 | -0.077486 | -6.416 |
| w20 | 14 | -0.060068 | -0.281 |
| w21 | 26 | 0.261198 | 240.461 |
| w22 | 13 | -0.075656 | -3.895 |
| w23 | 27 | 0.050192 | 28.234 |
| w24 | 5 | -0.094757 | -11.201 |

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
| w1 | 16 | 0.016242 | 3.847 |
| w2 | 12 | -0.02312 | -3.29 |
| w3 | 6 | -0.060085 | -5.738 |
| w4 | 15 | -0.117717 | -4.61 |
| w5 | 7 | 0.005389 | -1.342 |
| w6 | 25 | -0.181032 | -9.22 |
| w7 | 11 | -0.038733 | -8.403 |
| w8 | 11 | 0.016222 | 10.62 |
| w9 | 2 | -0.043761 | -2.978 |
| w10 | 29 | -0.046467 | 11.178 |
| w11 | 40 | -0.114936 | 45.451 |
| w12 | 17 | -0.08438 | -8.081 |
| w14 | 6 | -0.110036 | -8.242 |
| w15 | 19 | 0.053856 | -1.123 |
| w16 | 15 | 0.139247 | 36.749 |
| w17 | 16 | -0.096596 | -7.521 |
| w18 | 9 | 0.021347 | -0.41 |
| w19 | 5 | 0.024707 | -0.629 |
| w20 | 19 | 0.029169 | 21.457 |
| w21 | 35 | -0.040358 | 20.141 |
| w22 | 8 | -0.150365 | -7.786 |
| w23 | 15 | -0.022262 | -0.302 |
| w24 | 35 | 0.167687 | 210.467 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

