# Backtest of 069-02.d2_agitated-below-high-up-day-fade_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/069-02.d2_agitated-below-high-up-day-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.017717 | 1.214 |
| w2 | 23 | 0.097979 | 17.08 |
| w3 | 19 | 0.000666 | 0.228 |
| w4 | 13 | -0.29526 | -17.153 |
| w5 | 0 | None | 0.0 |
| w6 | 25 | 0.139039 | 1.79 |
| w7 | 0 | None | 0.0 |
| w8 | 15 | 0.164976 | 5.4 |
| w9 | 12 | 0.050857 | 5.463 |
| w10 | 16 | -0.021168 | -3.443 |
| w11 | 41 | 0.081154 | -4.828 |
| w12 | 14 | -0.080705 | -10.925 |
| w13 | 26 | 0.060861 | 6.022 |
| w14 | 17 | 0.069908 | 12.984 |
| w15 | 46 | 0.027934 | -14.604 |
| w16 | 17 | 0.328003 | 49.24 |
| w17 | 32 | -0.094838 | -24.745 |
| w18 | 33 | 0.22031 | 33.512 |
| w19 | 37 | 0.13813 | 7.946 |
| w20 | 23 | 0.015959 | 0.977 |
| w21 | 20 | 0.010903 | -6.605 |
| w22 | 18 | 0.101457 | 5.307 |
| w23 | 2 | -0.092516 | -1.237 |
| w24 | 18 | 0.001496 | 2.227 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.050684 | -2.024 |
| w2 | 30 | 0.052564 | 14.629 |
| w3 | 20 | 0.119019 | 14.23 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 18 | 0.045813 | -0.992 |
| w7 | 0 | None | 0.0 |
| w8 | 11 | 0.12817 | 4.925 |
| w9 | 9 | 0.054854 | 4.06 |
| w10 | 14 | 0.047042 | -1.955 |
| w11 | 40 | 0.069571 | -12.771 |
| w12 | 12 | -0.070257 | -7.78 |
| w13 | 22 | -0.026246 | -6.336 |
| w14 | 29 | 0.063845 | 12.04 |
| w15 | 19 | 0.057503 | 5.125 |
| w16 | 23 | 0.071325 | -0.271 |
| w17 | 33 | 0.064632 | -5.559 |
| w18 | 28 | 0.188549 | 30.144 |
| w19 | 32 | 0.080146 | -0.303 |
| w20 | 33 | 0.07569 | 12.141 |
| w21 | 25 | 0.115319 | 7.972 |
| w22 | 28 | 0.006193 | 10.737 |
| w23 | 16 | 0.11709 | 3.671 |
| w24 | 20 | -0.119415 | -9.947 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 24 | 0.09866 | 15.559 |
| w3 | 13 | 0.087411 | 5.994 |
| w4 | 14 | -0.043113 | -5.084 |
| w5 | 23 | -0.122427 | -21.753 |
| w6 | 3 | -0.198365 | -6.72 |
| w7 | 0 | None | 0.0 |
| w8 | 31 | 0.108283 | -0.414 |
| w9 | 0 | None | 0.0 |
| w10 | 9 | 0.025867 | -1.391 |
| w11 | 37 | -0.04023 | -18.944 |
| w12 | 13 | 0.050638 | 8.13 |
| w13 | 16 | 0.035118 | 4.076 |
| w14 | 16 | -0.018766 | 0.111 |
| w15 | 25 | -0.042212 | -7.055 |
| w16 | 15 | 0.130156 | 11.032 |
| w17 | 31 | 0.038357 | -8.06 |
| w18 | 27 | 0.229909 | 27.522 |
| w19 | 30 | 0.053857 | 1.15 |
| w20 | 21 | -0.051669 | -5.883 |
| w21 | 32 | 0.148426 | 7.322 |
| w22 | 38 | -0.06097 | -9.314 |
| w23 | 8 | 0.063201 | 3.425 |
| w24 | 17 | -0.059923 | -6.064 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.052746 | -7.871 |
| w2 | 28 | 0.169579 | 23.241 |
| w3 | 11 | -0.007443 | -3.741 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 12 | -0.024814 | -7.781 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.067183 | 0.993 |
| w9 | 2 | 0.045308 | 2.334 |
| w10 | 5 | 0.080394 | 3.048 |
| w11 | 39 | -0.067217 | -26.796 |
| w12 | 11 | -0.014391 | -1.542 |
| w14 | 22 | 0.023694 | 4.488 |
| w15 | 21 | 0.056157 | 0.765 |
| w16 | 21 | 0.137565 | 12.229 |
| w17 | 24 | 0.082343 | -0.485 |
| w18 | 31 | 0.330541 | 73.337 |
| w19 | 45 | 0.032668 | 4.685 |
| w20 | 27 | 0.106281 | -0.027 |
| w21 | 24 | -0.019852 | -5.58 |
| w22 | 36 | -0.044996 | -18.831 |
| w23 | 23 | -0.114904 | -19.76 |
| w24 | 36 | -0.07346 | -17.651 |

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
| w1 | 5 | 0.014832 | 0.553 |
| w2 | 1 | 0.076229 | 16.414 |
| w3 | 0 | 0.015697 | 0.0 |
| w4 | 0 | 0.138246 | 0.0 |
| w5 | 15 | 0.035853 | -0.762 |
| w6 | 15 | 0.080308 | 4.17 |
| w8 | 3 | -0.002248 | -0.066 |
| w9 | 9 | -0.042158 | -2.202 |
| w10 | 8 | 0.063374 | 2.43 |
| w11 | 38 | -0.038748 | -25.401 |
| w12 | 1 | -0.083744 | -2.022 |
| w14 | 14 | 0.017559 | 1.178 |
| w15 | 14 | 0.016462 | 0.64 |
| w16 | 28 | 0.153988 | 18.904 |
| w17 | 24 | 0.062684 | 11.478 |
| w18 | 26 | 0.214426 | 23.382 |
| w19 | 20 | 0.04885 | 5.629 |
| w20 | 26 | -0.19189 | -20.972 |
| w21 | 29 | 0.122539 | -2.497 |
| w22 | 37 | -0.108478 | -22.648 |
| w23 | 5 | -0.169333 | -11.89 |
| w24 | 12 | -0.070039 | -4.783 |

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
| w1 | 4 | 0.079607 | 3.318 |
| w2 | 25 | 0.242553 | 32.56 |
| w3 | 9 | -0.054361 | -2.533 |
| w4 | 5 | 0.023064 | -0.17 |
| w5 | 14 | -0.10542 | -6.496 |
| w6 | 6 | 0.120439 | 6.468 |
| w7 | 6 | 0.088584 | 8.064 |
| w8 | 7 | 0.255746 | 4.558 |
| w9 | 13 | 0.016272 | 2.097 |
| w10 | 18 | 0.069145 | 0.569 |
| w11 | 39 | 0.049135 | -18.228 |
| w12 | 23 | 0.041216 | -0.46 |
| w13 | 20 | 0.123703 | 15.874 |
| w14 | 15 | 0.002536 | 1.703 |
| w15 | 18 | 0.169272 | 22.469 |
| w16 | 36 | 0.051963 | -6.462 |
| w17 | 28 | 0.066091 | 8.208 |
| w18 | 28 | 0.326244 | 59.078 |
| w19 | 33 | -0.008135 | -2.935 |
| w20 | 21 | 0.073242 | 3.406 |
| w21 | 34 | 0.010204 | -11.715 |
| w22 | 40 | -0.071826 | -9.693 |
| w23 | 11 | -0.032692 | -2.557 |
| w24 | 39 | -0.049059 | -37.074 |

