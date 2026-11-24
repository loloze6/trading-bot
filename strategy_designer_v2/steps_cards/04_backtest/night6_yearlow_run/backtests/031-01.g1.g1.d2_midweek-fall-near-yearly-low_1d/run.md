# Backtest of 031-01.g1.g1.d2_midweek-fall-near-yearly-low_1d

- Plan: `../../../../03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.d2_midweek-fall-near-yearly-low_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.037215 | 2.984 |
| w2 | 14 | 0.055041 | 4.378 |
| w3 | 15 | -0.014642 | -2.731 |
| w4 | 14 | -0.018268 | 1.067 |
| w5 | 6 | -0.069715 | -4.707 |
| w6 | 11 | -0.048905 | -0.53 |
| w7 | 17 | 0.038447 | 2.357 |
| w8 | 14 | 0.028698 | 2.177 |
| w9 | 10 | -0.023788 | -1.873 |
| w10 | 7 | 0.054277 | 7.411 |
| w11 | 11 | 0.048815 | 7.432 |
| w12 | 10 | 0.043788 | 2.409 |
| w13 | 13 | 0.067027 | 6.396 |
| w14 | 14 | 0.196522 | 26.035 |
| w15 | 7 | 0.192328 | 23.958 |
| w16 | 13 | 0.045415 | 2.37 |
| w17 | 10 | -0.015568 | 1.053 |
| w18 | 11 | -0.004254 | -0.762 |
| w19 | 4 | -0.017478 | -0.326 |
| w20 | 6 | 0.019198 | 1.121 |
| w21 | 11 | -0.06093 | -1.779 |
| w22 | 9 | -0.009085 | -1.468 |
| w23 | 10 | 0.03346 | 1.927 |
| w24 | 11 | -0.013741 | -3.221 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.069175 | 5.079 |
| w2 | 13 | 0.081404 | 7.538 |
| w3 | 15 | -0.008075 | -0.759 |
| w4 | 16 | -0.007198 | 0.731 |
| w5 | 6 | -0.122647 | -7.843 |
| w6 | 14 | -0.056674 | -6.194 |
| w7 | 16 | 0.032397 | 5.249 |
| w8 | 12 | -0.001692 | -1.221 |
| w9 | 12 | -0.048311 | -4.814 |
| w10 | 9 | 0.305957 | 32.563 |
| w11 | 9 | -0.146182 | -10.222 |
| w12 | 13 | 0.065502 | 5.444 |
| w13 | 10 | 0.096725 | 9.533 |
| w14 | 15 | 0.161205 | 26.148 |
| w15 | 12 | -0.037387 | -5.27 |
| w16 | 13 | 0.091742 | 10.075 |
| w17 | 8 | -0.046638 | -3.176 |
| w18 | 7 | 0.108241 | 10.503 |
| w19 | 6 | 0.018306 | 2.779 |
| w20 | 7 | 0.0228 | 0.785 |
| w21 | 12 | 0.070971 | 5.933 |
| w22 | 12 | -0.006016 | -1.825 |
| w23 | 14 | 0.085393 | 11.252 |
| w24 | 10 | -0.028222 | -2.794 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.096321 | 8.022 |
| w2 | 15 | 0.078101 | 5.836 |
| w3 | 18 | 0.049058 | 3.897 |
| w4 | 11 | 0.009593 | -0.392 |
| w5 | 10 | -0.036323 | -3.293 |
| w6 | 10 | -0.090132 | -7.939 |
| w7 | 17 | 0.064138 | 6.951 |
| w8 | 14 | 0.071035 | 6.14 |
| w9 | 12 | -0.094731 | -8.829 |
| w10 | 12 | 0.24818 | 29.927 |
| w11 | 11 | 0.02235 | 2.241 |
| w12 | 17 | -0.012146 | -3.414 |
| w13 | 9 | -0.098263 | -8.063 |
| w14 | 15 | 0.149376 | 20.141 |
| w15 | 9 | 0.013812 | 1.259 |
| w16 | 16 | 0.052668 | 2.202 |
| w17 | 12 | 0.118464 | 10.249 |
| w18 | 12 | 0.044644 | 3.479 |
| w19 | 12 | 0.110406 | 12.531 |
| w20 | 18 | -0.014799 | -5.127 |
| w21 | 12 | 0.041681 | 7.83 |
| w22 | 10 | -0.143115 | -9.614 |
| w23 | 13 | 0.16007 | 17.441 |
| w24 | 14 | -0.122544 | -12.985 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.168218 | 14.802 |
| w2 | 13 | -0.027274 | -5.786 |
| w3 | 16 | 0.030449 | 0.007 |
| w4 | 14 | -0.123035 | -16.097 |
| w5 | 12 | -0.099451 | -11.722 |
| w6 | 10 | -0.025111 | -3.204 |
| w7 | 17 | -0.021981 | -2.263 |
| w8 | 15 | -0.017247 | -2.871 |
| w9 | 11 | -0.004509 | -2.615 |
| w10 | 12 | 0.157271 | 21.719 |
| w11 | 9 | 0.139825 | 14.934 |
| w12 | 17 | -0.021334 | -5.632 |
| w14 | 15 | 0.102816 | 13.119 |
| w15 | 15 | 0.023138 | -0.201 |
| w16 | 14 | 0.02309 | -0.41 |
| w17 | 8 | 0.109698 | 9.263 |
| w18 | 12 | 0.041077 | 3.746 |
| w19 | 14 | 0.079377 | 6.01 |
| w20 | 12 | 0.083908 | 5.101 |
| w21 | 11 | -0.073595 | -11.681 |
| w22 | 10 | -0.133421 | -5.803 |
| w23 | 8 | -0.035782 | -10.261 |
| w24 | 9 | 0.065543 | 6.219 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.076607 | 9.363 |
| w2 | 1 | 0.171102 | 1.256 |
| w3 | 0 | -0.050976 | 0.0 |
| w4 | 0 | -0.023304 | 0.0 |
| w5 | 8 | -0.050147 | -6.656 |
| w6 | 14 | -0.025851 | -1.585 |
| w8 | 14 | -0.022539 | -3.18 |
| w9 | 15 | -0.052478 | -5.018 |
| w10 | 13 | 0.278751 | 37.87 |
| w11 | 10 | 0.093098 | 11.361 |
| w12 | 11 | 0.075827 | 5.095 |
| w14 | 15 | 0.09435 | 13.093 |
| w15 | 14 | -0.052704 | -8.136 |
| w16 | 15 | 0.040881 | 0.738 |
| w17 | 9 | 0.15967 | 32.297 |
| w18 | 10 | 0.119188 | 11.528 |
| w19 | 12 | 0.047088 | 2.292 |
| w20 | 11 | -0.013524 | -8.13 |
| w21 | 12 | 0.21385 | 30.524 |
| w22 | 9 | -0.010565 | -0.771 |
| w23 | 7 | 0.055034 | 4.27 |
| w24 | 10 | -0.074628 | -6.244 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.1134 | 9.449 |
| w2 | 15 | 0.021625 | 1.525 |
| w3 | 17 | -0.095144 | -9.951 |
| w4 | 15 | 0.020264 | 0.62 |
| w5 | 13 | -0.041614 | -3.781 |
| w6 | 13 | 0.01218 | -2.388 |
| w7 | 15 | 0.051532 | 4.546 |
| w8 | 15 | -0.002209 | -0.096 |
| w9 | 15 | -0.127908 | -13.966 |
| w10 | 10 | 0.090419 | 8.815 |
| w11 | 10 | 0.221395 | 28.117 |
| w12 | 17 | -0.008237 | -2.047 |
| w13 | 12 | 0.064415 | 4.334 |
| w14 | 15 | 0.107192 | 12.447 |
| w15 | 17 | -0.048601 | -11.385 |
| w16 | 15 | -0.044711 | -9.844 |
| w17 | 9 | -0.015087 | -3.46 |
| w18 | 15 | 0.046035 | 3.688 |
| w19 | 13 | 0.161716 | 14.841 |
| w20 | 13 | -0.045758 | -9.477 |
| w21 | 8 | -0.022902 | -3.724 |
| w22 | 13 | -0.101291 | -9.896 |
| w23 | 16 | 0.098452 | 9.945 |
| w24 | 8 | 0.097865 | 9.239 |

