# Backtest of 060-01.g1.d1_wider-than-usual-high-close-fade_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/060-01.g1.d1_wider-than-usual-high-close-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 11 | 0.017421 | 5.053 |
| w3 | 9 | 0.098337 | 8.009 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.064816 | -1.265 |
| w9 | 2 | -0.159044 | -8.49 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | 0.001593 | 0.253 |
| w14 | 6 | 0.155979 | 15.337 |
| w15 | 0 | None | 0.0 |
| w16 | 7 | 0.049725 | 2.249 |
| w17 | 0 | None | 0.0 |
| w18 | 12 | -0.064753 | -9.07 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.006844 | -2.19 |
| w21 | 0 | None | 0.0 |
| w22 | 7 | 0.074837 | 4.282 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | 0.07053 | 5.66 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.027352 | -1.177 |
| w2 | 12 | -0.033442 | -3.435 |
| w3 | 4 | 0.034573 | 1.782 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | 0.12573 | 3.105 |
| w9 | 3 | -0.028798 | -1.548 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 17 | 0.100138 | 18.192 |
| w15 | 0 | None | 0.0 |
| w16 | 5 | 0.082792 | 3.815 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | 0.058087 | 1.565 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | 0.086781 | 8.579 |
| w21 | 6 | 0.051438 | 1.205 |
| w22 | 13 | 0.300075 | 46.175 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | -0.046891 | -1.94 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 8 | 0.054671 | 7.217 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | 0.009709 | 1.094 |
| w6 | 2 | -0.006925 | -1.042 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.052074 | -3.124 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.045408 | -1.852 |
| w14 | 12 | 0.029288 | 3.787 |
| w15 | 1 | -0.000973 | -0.085 |
| w16 | 5 | 0.090854 | 4.622 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | -0.1013 | -3.252 |
| w19 | 0 | None | 0.0 |
| w20 | 11 | 0.065586 | 4.72 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | 0.111149 | 8.028 |
| w23 | 1 | 0.031273 | 0.825 |
| w24 | 4 | 0.060602 | 3.563 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.036507 | 1.451 |
| w2 | 5 | -0.1001 | -8.346 |
| w3 | 2 | 0.000386 | -0.341 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.089725 | -6.171 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.153898 | 2.747 |
| w9 | 1 | -0.011145 | -0.135 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 6 | 0.121066 | 9.074 |
| w15 | 0 | None | 0.0 |
| w16 | 7 | 0.012932 | -1.303 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 8 | -0.007477 | -2.129 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.256566 | -16.547 |
| w24 | 1 | -0.009284 | -0.831 |

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
| w1 | 2 | 0.111109 | 3.985 |
| w2 | 1 | 0.012744 | 13.471 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.013245 | 0.071 |
| w8 | 0 | None | 0.0 |
| w9 | 4 | 0.054923 | 3.189 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.100303 | 4.929 |
| w12 | 0 | None | 0.0 |
| w14 | 2 | 0.028878 | 1.144 |
| w15 | 1 | -0.066589 | -1.785 |
| w16 | 8 | 0.12266 | 9.874 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | 0.08943 | 4.216 |
| w19 | 2 | -0.075744 | -2.191 |
| w20 | 1 | -0.021193 | -1.714 |
| w21 | 1 | 0.000951 | -1.522 |
| w22 | 7 | 0.139952 | 9.389 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.019717 | 1.886 |

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
| w1 | 0 | None | 0.0 |
| w2 | 8 | 0.080285 | 6.04 |
| w3 | 4 | -0.103339 | -5.238 |
| w4 | 1 | 0.139423 | 3.078 |
| w5 | 4 | -0.099717 | -6.821 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.046663 | 0.498 |
| w9 | 8 | 0.118647 | 10.176 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 6 | 0.242316 | 17.818 |
| w15 | 0 | None | 0.0 |
| w16 | 11 | 0.112867 | 7.066 |
| w17 | 3 | 0.008814 | 0.527 |
| w18 | 2 | -0.069573 | -2.545 |
| w19 | 10 | -0.097039 | -10.385 |
| w20 | 4 | -0.20445 | -18.505 |
| w21 | 1 | -0.013639 | -2.353 |
| w22 | 9 | 0.020097 | 0.228 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

