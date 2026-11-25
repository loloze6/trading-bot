# Backtest of 034-01.d1_wide-range-low-close-rebound_1d

- Plan: `../../../../03_test_plan/night7_steadydecline_run/plans/034-01.d1_wide-range-low-close-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.008566 | -4.11 |
| w2 | 44 | 0.026613 | -12.976 |
| w3 | 42 | 0.206613 | 23.287 |
| w4 | 23 | 0.076336 | 13.063 |
| w5 | 0 | None | 0.0 |
| w6 | 46 | 0.229181 | 71.572 |
| w7 | 0 | None | 0.0 |
| w8 | 28 | -0.037314 | -0.409 |
| w9 | 26 | -0.00431 | -4.859 |
| w10 | 33 | 0.004574 | 6.218 |
| w11 | 70 | -0.014739 | 19.926 |
| w12 | 33 | 0.157809 | 17.798 |
| w13 | 65 | -0.001067 | -3.201 |
| w14 | 38 | 0.080637 | -3.114 |
| w15 | 79 | -0.116904 | -0.786 |
| w16 | 44 | 0.092532 | 8.887 |
| w17 | 47 | 0.044913 | 26.23 |
| w18 | 70 | 0.008898 | -7.539 |
| w19 | 73 | -0.021261 | 8.724 |
| w20 | 72 | 0.103987 | 10.646 |
| w21 | 34 | 0.070384 | 29.749 |
| w22 | 47 | 0.161497 | 19.298 |
| w23 | 3 | -0.018604 | 0.038 |
| w24 | 51 | 0.002349 | -13.898 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.124589 | -14.643 |
| w2 | 85 | 0.080552 | -8.874 |
| w3 | 42 | 0.258831 | 30.367 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 40 | 0.04194 | 13.806 |
| w7 | 0 | None | 0.0 |
| w8 | 27 | 0.025765 | 3.437 |
| w9 | 20 | 0.063243 | 4.392 |
| w10 | 37 | 0.015291 | 10.53 |
| w11 | 70 | 0.081177 | 56.958 |
| w12 | 20 | 0.060502 | 6.071 |
| w13 | 38 | -0.004997 | -2.584 |
| w14 | 66 | 0.187908 | 14.296 |
| w15 | 45 | 0.029898 | 3.918 |
| w16 | 60 | -0.090476 | -19.911 |
| w17 | 50 | 0.004408 | 3.396 |
| w18 | 63 | 0.013614 | 6.646 |
| w19 | 66 | -0.158522 | -20.484 |
| w20 | 78 | 0.064804 | -6.694 |
| w21 | 59 | 0.089648 | 29.499 |
| w22 | 69 | 0.119746 | -5.75 |
| w23 | 40 | 0.071105 | 35.599 |
| w24 | 37 | 0.018947 | -6.585 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 49 | 0.025357 | -11.223 |
| w3 | 39 | 0.135262 | 23.639 |
| w4 | 26 | 0.023198 | 2.209 |
| w5 | 47 | 0.06876 | 1.71 |
| w6 | 4 | 0.168798 | 8.191 |
| w7 | 0 | None | 0.0 |
| w8 | 81 | 0.083693 | 36.882 |
| w9 | 0 | None | 0.0 |
| w10 | 17 | 0.032263 | 5.192 |
| w11 | 85 | -0.155864 | -4.575 |
| w12 | 40 | -0.07046 | -13.859 |
| w13 | 39 | 0.00999 | -0.433 |
| w14 | 44 | 0.123984 | 3.334 |
| w15 | 52 | 0.109087 | 11.468 |
| w16 | 37 | 0.016009 | -4.209 |
| w17 | 61 | 0.069301 | 27.236 |
| w18 | 48 | 0.074922 | 6.291 |
| w19 | 60 | 0.112162 | 30.535 |
| w20 | 54 | 0.104606 | 2.304 |
| w21 | 64 | 0.002983 | 19.751 |
| w22 | 87 | -0.005434 | -5.743 |
| w23 | 19 | 0.055718 | 6.261 |
| w24 | 40 | -0.047062 | -11.473 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | -0.067644 | -16.679 |
| w2 | 48 | -0.039387 | -10.994 |
| w3 | 24 | 0.10317 | 9.466 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 21 | 0.019682 | 2.594 |
| w7 | 0 | None | 0.0 |
| w8 | 16 | 0.002063 | -0.333 |
| w9 | 4 | 0.000527 | -1.092 |
| w10 | 9 | 0.085643 | 7.642 |
| w11 | 72 | 0.060047 | 49.003 |
| w12 | 24 | 0.01699 | -2.337 |
| w14 | 47 | 0.075113 | -5.399 |
| w15 | 49 | 0.002392 | -0.528 |
| w16 | 50 | 0.002831 | -5.771 |
| w17 | 46 | -0.071471 | -7.919 |
| w18 | 62 | 0.169676 | 19.391 |
| w19 | 86 | 0.236262 | 16.957 |
| w20 | 64 | 0.188799 | 38.621 |
| w21 | 42 | 0.032688 | 2.711 |
| w22 | 58 | 0.06347 | 18.626 |
| w23 | 49 | -0.154848 | -23.275 |
| w24 | 74 | -0.066888 | 5.194 |

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
| w1 | 9 | 0.007256 | -2.46 |
| w2 | 23 | -0.038723 | -17.339 |
| w3 | 0 | 0.070213 | 0.0 |
| w4 | 0 | 0.003966 | 0.0 |
| w5 | 40 | -0.085759 | -3.799 |
| w6 | 29 | -0.034245 | -2.243 |
| w8 | 6 | 0.060881 | 1.766 |
| w9 | 23 | 0.05105 | 1.76 |
| w10 | 12 | 0.003412 | 1.683 |
| w11 | 85 | -0.005332 | 45.333 |
| w12 | 4 | -0.001102 | -0.667 |
| w14 | 35 | 0.11773 | 18.879 |
| w15 | 37 | 0.093354 | 9.332 |
| w16 | 74 | -0.01353 | -4.339 |
| w17 | 47 | 0.028958 | 9.065 |
| w18 | 44 | 0.080207 | 4.968 |
| w19 | 52 | -0.054691 | -13.5 |
| w20 | 46 | 0.022129 | 10.593 |
| w21 | 57 | 0.091676 | 102.258 |
| w22 | 84 | 0.019284 | -0.381 |
| w23 | 15 | 0.08211 | 9.183 |
| w24 | 24 | 0.019719 | -4.333 |

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
| w1 | 28 | 0.203837 | 28.099 |
| w2 | 45 | -0.001649 | -9.548 |
| w3 | 22 | 0.215059 | 17.556 |
| w4 | 12 | -0.002916 | -0.196 |
| w5 | 36 | 0.167481 | 20.431 |
| w6 | 16 | 0.034268 | 2.749 |
| w7 | 11 | -0.066227 | -7.389 |
| w8 | 13 | 0.085486 | 1.987 |
| w9 | 40 | 0.058042 | -2.476 |
| w10 | 35 | -0.149161 | -14.51 |
| w11 | 72 | -0.018886 | 35.197 |
| w12 | 51 | 0.039287 | 8.052 |
| w13 | 45 | 0.028251 | 3.335 |
| w14 | 37 | 0.093661 | 1.855 |
| w15 | 44 | 0.070072 | 3.68 |
| w16 | 87 | 0.060398 | 45.827 |
| w17 | 57 | -0.079117 | -21.213 |
| w18 | 58 | 0.165348 | 26.536 |
| w19 | 93 | 0.109021 | 0.49 |
| w20 | 67 | -0.052617 | -0.112 |
| w21 | 72 | -0.066893 | 8.407 |
| w22 | 84 | -0.016718 | -14.499 |
| w23 | 25 | -0.094838 | -9.569 |
| w24 | 72 | 0.054016 | 78.777 |

