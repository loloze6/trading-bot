# Backtest of 058-03.g1_calm-downtrend-weekly-continuation_1d

- Plan: `../../../../03_test_plan/night8_fallingcalm_run/plans/058-03.g1_calm-downtrend-weekly-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | 0.003252 | 20.521 |
| w2 | 22 | 0.168075 | 54.423 |
| w3 | 30 | 0.154461 | -1.9 |
| w4 | 3 | -0.019076 | 0.593 |
| w5 | 11 | -0.152449 | -3.794 |
| w6 | 12 | 0.021557 | -7.432 |
| w7 | 33 | 0.033657 | -2.067 |
| w8 | 6 | 0.0081 | -0.485 |
| w9 | 32 | -0.230102 | -39.888 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.034784 | -6.927 |
| w12 | 19 | -0.045673 | -5.957 |
| w13 | 18 | 0.020804 | 9.463 |
| w14 | 11 | 0.13798 | 41.226 |
| w15 | 0 | None | 0.0 |
| w16 | 9 | 0.106329 | -0.877 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | -0.083795 | -5.573 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | -0.022724 | -9.502 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | 0.066831 | -4.851 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | 0.06341 | 24.169 |
| w2 | 2 | -0.088467 | 7.566 |
| w3 | 14 | 0.230084 | 4.338 |
| w4 | 4 | -0.008298 | 3.009 |
| w5 | 12 | 0.002901 | 14.919 |
| w6 | 25 | 0.048113 | -14.1 |
| w7 | 48 | -0.019931 | -13.094 |
| w8 | 0 | None | 0.0 |
| w9 | 41 | -0.067677 | -5.875 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.031489 | 2.206 |
| w13 | 35 | 0.149543 | 23.222 |
| w14 | 12 | 0.169895 | 22.4 |
| w15 | 14 | -0.019201 | 3.794 |
| w16 | 8 | 0.006847 | 15.676 |
| w17 | 9 | -0.044745 | -4.089 |
| w18 | 5 | 0.039181 | 11.093 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | -0.002869 | -7.742 |
| w22 | 8 | -0.167193 | -13.362 |
| w23 | 0 | None | 0.0 |
| w24 | 23 | -0.058504 | -10.057 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 56 | 0.047936 | 36.956 |
| w2 | 12 | 0.067929 | 14.959 |
| w3 | 9 | -0.037022 | 0.993 |
| w4 | 5 | -0.127949 | -13.826 |
| w5 | 2 | 0.007097 | -1.068 |
| w6 | 18 | -0.03991 | -7.58 |
| w7 | 67 | 0.047096 | 9.194 |
| w8 | 0 | None | 0.0 |
| w9 | 62 | -0.030558 | 4.981 |
| w10 | 9 | -0.026874 | -2.294 |
| w11 | 0 | None | 0.0 |
| w12 | 12 | -0.009209 | 5.149 |
| w13 | 30 | 0.040462 | 0.721 |
| w14 | 22 | 0.016193 | 18.145 |
| w15 | 15 | 0.050969 | 1.597 |
| w16 | 17 | 0.040106 | 28.049 |
| w17 | 11 | 0.014134 | -12.94 |
| w18 | 18 | 0.077236 | 20.238 |
| w19 | 5 | -0.102028 | -17.277 |
| w20 | 18 | -0.100974 | -12.3 |
| w21 | 7 | 0.009801 | -1.796 |
| w22 | 2 | -0.024451 | 4.608 |
| w23 | 5 | 0.087887 | 0.615 |
| w24 | 14 | -0.075834 | -6.827 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.069879 | -26.86 |
| w2 | 13 | -0.012868 | 2.422 |
| w3 | 16 | 0.008414 | -2.634 |
| w4 | 13 | -0.141299 | -8.988 |
| w5 | 11 | -0.092494 | 18.495 |
| w6 | 8 | -0.058411 | -3.882 |
| w7 | 63 | -0.055342 | -10.297 |
| w8 | 3 | -0.012346 | -0.96 |
| w9 | 53 | 0.010573 | 29.65 |
| w10 | 2 | -0.163613 | 0.103 |
| w11 | 0 | None | 0.0 |
| w12 | 26 | 0.070705 | 12.815 |
| w14 | 13 | 0.191591 | 37.312 |
| w15 | 11 | 0.004278 | 6.697 |
| w16 | 8 | 0.106706 | 16.06 |
| w17 | 0 | None | 0.0 |
| w18 | 7 | 0.037484 | 12.841 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | -0.233629 | -6.63 |
| w21 | 6 | -0.013366 | -12.739 |
| w22 | 4 | 0.030469 | -1.113 |
| w23 | 15 | 0.067433 | 13.105 |
| w24 | 2 | 0.009994 | -0.928 |

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
| w1 | 33 | 0.147495 | 43.933 |
| w2 | 8 | 0.053426 | 25.255 |
| w3 | 0 | 0.004337 | 0.0 |
| w4 | 0 | -0.054668 | 0.0 |
| w5 | 0 | 0.027775 | 0.0 |
| w6 | 16 | 0.028058 | -6.943 |
| w8 | 26 | -0.203017 | -7.338 |
| w9 | 36 | 0.114593 | 12.402 |
| w10 | 9 | 0.123966 | 11.342 |
| w11 | 0 | None | 0.0 |
| w12 | 23 | 0.050505 | -3.621 |
| w14 | 34 | 0.125756 | 54.32 |
| w15 | 14 | -0.060803 | -3.354 |
| w16 | 6 | 0.063856 | 5.353 |
| w17 | 18 | 0.009267 | -8.478 |
| w18 | 21 | 0.062324 | 26.092 |
| w19 | 20 | -0.049944 | -4.338 |
| w20 | 22 | 0.034171 | 0.917 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | 0.021822 | 0.0 |
| w23 | 1 | 0.039872 | -2.055 |
| w24 | 36 | -0.081087 | 13.942 |

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
| w1 | 33 | 0.049125 | 39.842 |
| w2 | 19 | 0.02237 | -12.337 |
| w3 | 36 | 0.002179 | -6.622 |
| w4 | 30 | -0.003232 | 5.263 |
| w5 | 26 | 0.058297 | -1.851 |
| w6 | 25 | -0.014991 | -3.851 |
| w7 | 62 | -0.09855 | -30.2 |
| w8 | 25 | -0.0808 | -2.144 |
| w9 | 46 | 0.043792 | -7.234 |
| w10 | 2 | -0.081071 | 0.784 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | 0.029256 | -3.666 |
| w13 | 37 | 0.091993 | 2.039 |
| w14 | 34 | 0.071005 | 17.459 |
| w15 | 11 | -0.042987 | 8.291 |
| w16 | 0 | None | 0.0 |
| w17 | 13 | -0.040382 | -12.877 |
| w18 | 13 | 0.087702 | 15.331 |
| w19 | 0 | None | 0.0 |
| w20 | 14 | 0.087635 | 6.675 |
| w21 | 11 | 0.040895 | 3.592 |
| w22 | 2 | -0.180561 | -0.998 |
| w23 | 20 | -0.013752 | -17.104 |
| w24 | 0 | None | 0.0 |

