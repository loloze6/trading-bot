# Backtest of 061-01.g1.d1.d1_calm-big-rise-convex-follow-through_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/061-01.g1.d1.d1_calm-big-rise-convex-follow-through_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.082006 | -28.515 |
| w2 | 4 | -0.160188 | -34.621 |
| w3 | 7 | 0.019794 | -36.502 |
| w4 | 1 | 0.164233 | 39.251 |
| w5 | 9 | -0.037911 | -18.876 |
| w6 | 8 | -0.090622 | 7.765 |
| w7 | 7 | -0.028206 | 6.925 |
| w8 | 5 | -0.160385 | -2.344 |
| w9 | 10 | -0.067413 | -8.527 |
| w10 | 5 | 0.151554 | 28.915 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 1 | -0.130214 | -2.227 |
| w14 | 2 | 0.01971 | -0.782 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.048799 | 10.712 |
| w17 | 2 | 0.02169 | 29.446 |
| w18 | 2 | 0.162299 | 17.898 |
| w19 | 0 | None | 0.0 |
| w20 | 11 | 0.042746 | 0.642 |
| w21 | 5 | -0.033705 | 16.235 |
| w22 | 10 | -0.130926 | -35.217 |
| w23 | 5 | 0.129661 | 15.955 |
| w24 | 6 | 0.135626 | -8.76 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.014287 | 2.246 |
| w2 | 4 | -0.112127 | -15.248 |
| w3 | 6 | 0.005894 | -38.401 |
| w4 | 3 | -0.078546 | 24.523 |
| w5 | 9 | -0.047666 | -2.094 |
| w6 | 7 | 0.00028 | -0.791 |
| w7 | 1 | -0.112578 | 2.592 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | 0.00145 | -13.824 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | -0.004185 | -0.184 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | 0.010654 | 8.036 |
| w17 | 5 | 0.007798 | 1.791 |
| w18 | 2 | 0.048405 | 13.161 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.117543 | -0.141 |
| w21 | 6 | -0.063062 | -23.905 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | 0.127603 | 11.054 |
| w24 | 2 | 0.036336 | 12.153 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.068869 | -18.333 |
| w2 | 10 | -0.073456 | -31.18 |
| w3 | 10 | -0.007259 | 34.428 |
| w4 | 4 | 0.089386 | -5.128 |
| w5 | 7 | 0.104372 | -10.479 |
| w6 | 10 | 0.045553 | 21.404 |
| w7 | 3 | -0.056778 | -7.424 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.077579 | 1.035 |
| w10 | 9 | -0.018932 | -4.972 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.020323 | 11.655 |
| w13 | 1 | -0.143956 | -5.936 |
| w14 | 4 | -0.029069 | -6.848 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | -0.044289 | -4.395 |
| w17 | 4 | -0.022022 | -12.099 |
| w18 | 2 | -0.034004 | 6.06 |
| w19 | 9 | 0.075934 | -2.199 |
| w20 | 5 | 0.007738 | -21.448 |
| w21 | 5 | 0.037679 | 12.325 |
| w22 | 0 | None | 0.0 |
| w23 | 11 | 0.037786 | 31.409 |
| w24 | 3 | -0.223656 | -26.203 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.073052 | -16.62 |
| w2 | 4 | -0.040896 | -2.789 |
| w3 | 5 | 0.042003 | -8.806 |
| w4 | 11 | -0.070484 | -19.114 |
| w5 | 11 | 0.115366 | -10.873 |
| w6 | 8 | 0.079307 | -2.104 |
| w7 | 6 | -0.041428 | -6.912 |
| w8 | 7 | -0.062607 | -1.479 |
| w9 | 4 | -0.163816 | -19.794 |
| w10 | 5 | -0.067669 | 5.324 |
| w11 | 0 | None | 0.0 |
| w12 | 7 | 0.026792 | -29.378 |
| w14 | 6 | 0.07875 | -21.751 |
| w15 | 0 | None | 0.0 |
| w16 | 3 | -0.078413 | -4.619 |
| w17 | 0 | None | 0.0 |
| w18 | 7 | 0.057047 | 14.686 |
| w19 | 2 | -0.017154 | -19.827 |
| w20 | 3 | -0.04547 | -14.289 |
| w21 | 10 | 0.016438 | 4.648 |
| w22 | 6 | 0.002548 | 15.054 |
| w23 | 6 | -0.039502 | -19.654 |
| w24 | 1 | 0.042574 | -1.066 |

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
| w1 | 8 | -0.017661 | 1.322 |
| w2 | 0 | -0.00554 | 0.0 |
| w3 | 0 | 0.083024 | 0.0 |
| w4 | 0 | 0.015508 | 0.0 |
| w5 | 0 | -0.04649 | 0.0 |
| w6 | 3 | -0.019803 | 18.824 |
| w8 | 6 | -0.064748 | -5.175 |
| w9 | 2 | -0.096732 | -18.791 |
| w10 | 2 | -0.050335 | -4.788 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.033099 | 6.858 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.305107 | 18.519 |
| w16 | 1 | -0.018224 | -0.897 |
| w17 | 6 | 0.001312 | 27.104 |
| w18 | 2 | -0.006738 | 38.881 |
| w19 | 10 | 0.032113 | -14.048 |
| w20 | 4 | -0.101182 | -2.183 |
| w21 | 6 | -0.005962 | 94.229 |
| w22 | 0 | None | 0.0 |
| w23 | 9 | 0.110308 | 35.027 |
| w24 | 3 | -0.035066 | -0.504 |

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
| w2 | 0 | None | 0.0 |
| w3 | 2 | -0.129919 | -11.706 |
| w4 | 7 | -0.168086 | -7.551 |
| w5 | 2 | -0.00179 | -2.992 |
| w6 | 5 | -0.12475 | -10.288 |
| w7 | 2 | 0.036208 | -0.623 |
| w8 | 9 | -0.189882 | 3.291 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | 0.070421 | 12.593 |
| w13 | 0 | None | 0.0 |
| w14 | 2 | 0.023177 | 8.219 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.05182 | 17.4 |
| w18 | 2 | -0.018707 | 8.813 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | -0.114322 | -19.254 |
| w21 | 6 | -0.01161 | 9.169 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | 0.107232 | -1.621 |
| w24 | 0 | None | 0.0 |

