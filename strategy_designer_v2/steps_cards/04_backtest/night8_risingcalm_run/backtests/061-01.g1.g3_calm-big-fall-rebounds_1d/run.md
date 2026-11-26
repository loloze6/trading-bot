# Backtest of 061-01.g1.g3_calm-big-fall-rebounds_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/061-01.g1.g3_calm-big-fall-rebounds_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.005799 | -18.062 |
| w2 | 14 | -0.028715 | -46.294 |
| w3 | 16 | -0.207744 | -24.0 |
| w4 | 12 | -0.069022 | 60.519 |
| w5 | 13 | -0.004972 | -12.52 |
| w6 | 11 | -0.108736 | 36.548 |
| w7 | 15 | 0.071535 | -18.013 |
| w8 | 17 | 0.062016 | 61.003 |
| w9 | 9 | 0.050762 | -7.394 |
| w10 | 6 | 0.091987 | 34.637 |
| w11 | 6 | -0.077044 | 1.293 |
| w12 | 11 | -0.116155 | -31.03 |
| w13 | 9 | -0.008972 | 4.328 |
| w14 | 16 | -0.144062 | -67.642 |
| w15 | 6 | 0.187178 | 18.869 |
| w16 | 7 | 0.021533 | -41.808 |
| w17 | 15 | -0.104415 | 93.234 |
| w18 | 5 | 0.097243 | 13.001 |
| w19 | 6 | 0.012159 | 17.64 |
| w20 | 5 | -0.07882 | -1.632 |
| w21 | 14 | -0.130685 | 53.394 |
| w22 | 7 | -0.076866 | -15.197 |
| w23 | 12 | 0.005901 | 2.966 |
| w24 | 13 | -0.08027 | -34.607 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.017597 | -26.541 |
| w2 | 6 | -0.042404 | -36.915 |
| w3 | 20 | -0.138411 | -18.599 |
| w4 | 14 | 0.07819 | 36.474 |
| w5 | 13 | 0.052661 | -19.64 |
| w6 | 14 | 0.027356 | 58.772 |
| w7 | 11 | 0.088644 | -47.411 |
| w8 | 10 | 0.016014 | 25.304 |
| w9 | 16 | -0.064377 | -31.99 |
| w10 | 13 | 0.124691 | 70.196 |
| w11 | 6 | -0.008882 | 25.862 |
| w12 | 17 | 0.095052 | -16.116 |
| w13 | 11 | -0.011706 | -8.915 |
| w14 | 7 | -0.167661 | -46.607 |
| w15 | 12 | -0.016434 | 14.373 |
| w16 | 5 | 0.141003 | 72.541 |
| w17 | 8 | 0.072588 | 67.655 |
| w18 | 2 | 0.125433 | 24.313 |
| w19 | 4 | 0.218599 | 19.982 |
| w20 | 4 | -0.089512 | -10.688 |
| w21 | 11 | -0.107675 | 34.435 |
| w22 | 11 | 0.095816 | -23.275 |
| w23 | 14 | -0.127095 | 56.112 |
| w24 | 17 | -0.101719 | -22.599 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.03081 | -27.302 |
| w2 | 12 | 0.056349 | -29.697 |
| w3 | 13 | -0.108095 | 13.946 |
| w4 | 12 | -0.029387 | -1.628 |
| w5 | 14 | -0.08909 | -32.151 |
| w6 | 13 | 0.043895 | 37.2 |
| w7 | 9 | 0.154345 | -51.735 |
| w8 | 10 | -0.002394 | 31.498 |
| w9 | 8 | -0.029183 | -37.95 |
| w10 | 9 | 0.235751 | 60.804 |
| w11 | 4 | 0.081541 | 32.47 |
| w12 | 20 | -0.058081 | 0.924 |
| w13 | 9 | 0.074968 | -7.978 |
| w14 | 10 | -0.00064 | -29.047 |
| w15 | 22 | -0.153048 | -3.123 |
| w16 | 12 | 0.086885 | 57.123 |
| w17 | 5 | 0.036828 | 65.625 |
| w18 | 8 | 0.132037 | 27.864 |
| w19 | 7 | -0.081885 | 47.604 |
| w20 | 9 | -0.027234 | -20.982 |
| w21 | 10 | -0.055406 | 33.872 |
| w22 | 3 | -0.109656 | -4.76 |
| w23 | 16 | 0.114108 | 26.298 |
| w24 | 12 | 0.032749 | -9.855 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.094525 | -23.646 |
| w2 | 10 | 0.121963 | -18.182 |
| w3 | 13 | 0.083252 | -7.932 |
| w4 | 14 | 0.190809 | -10.672 |
| w5 | 9 | -0.019433 | -22.982 |
| w6 | 12 | 0.163465 | 28.651 |
| w7 | 8 | 0.195277 | -27.805 |
| w8 | 8 | 0.169398 | 32.648 |
| w9 | 15 | 0.041885 | -35.407 |
| w10 | 16 | 0.30628 | 71.372 |
| w11 | 7 | 0.09533 | 45.275 |
| w12 | 8 | 0.017089 | -12.638 |
| w14 | 17 | 0.033211 | -45.482 |
| w15 | 14 | -0.050107 | -6.15 |
| w16 | 11 | 0.088314 | 4.474 |
| w17 | 14 | 0.241928 | 27.906 |
| w18 | 4 | 0.103876 | 16.501 |
| w19 | 2 | -0.144092 | -9.462 |
| w20 | 8 | 0.163332 | 31.83 |
| w21 | 13 | -0.036186 | 17.176 |
| w22 | 11 | 0.045799 | 21.402 |
| w23 | 8 | 0.039912 | 1.363 |
| w24 | 7 | -0.013745 | 2.052 |

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
| w1 | 11 | 0.016299 | -24.11 |
| w2 | 4 | 0.096727 | -34.466 |
| w3 | 0 | 0.103059 | 0.0 |
| w4 | 0 | 0.284615 | 0.0 |
| w5 | 10 | 0.030984 | 68.342 |
| w6 | 8 | 0.124794 | 53.715 |
| w8 | 13 | 0.193909 | -4.141 |
| w9 | 16 | -0.067279 | -44.874 |
| w10 | 12 | 0.177108 | 52.7 |
| w11 | 0 | None | 0.0 |
| w12 | 19 | 0.090854 | -16.006 |
| w14 | 12 | -0.019058 | 14.533 |
| w15 | 13 | 0.001254 | -7.803 |
| w16 | 7 | 0.065191 | 11.215 |
| w17 | 12 | -0.020046 | 183.983 |
| w18 | 11 | 0.140191 | 54.072 |
| w19 | 10 | 0.139718 | 34.88 |
| w20 | 8 | -0.001455 | 9.237 |
| w21 | 8 | -0.090067 | 59.601 |
| w22 | 5 | 0.035007 | 1.325 |
| w23 | 13 | 0.100704 | 33.54 |
| w24 | 11 | -0.082334 | -34.642 |

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
| w1 | 16 | -0.115006 | 0.267 |
| w2 | 10 | 0.008225 | -4.041 |
| w3 | 9 | -0.005838 | -40.151 |
| w4 | 12 | 0.099039 | -20.096 |
| w5 | 13 | -0.093874 | -48.766 |
| w6 | 9 | 0.083764 | 38.371 |
| w7 | 16 | 0.171105 | -6.166 |
| w8 | 12 | 0.120325 | 31.787 |
| w9 | 15 | -0.160929 | -36.141 |
| w10 | 20 | 0.158323 | 63.381 |
| w11 | 7 | -0.094012 | 41.731 |
| w12 | 16 | 0.026027 | 67.838 |
| w13 | 4 | 0.051115 | -3.327 |
| w14 | 17 | -0.055381 | -25.32 |
| w15 | 13 | 0.044198 | 7.936 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.104447 | 24.987 |
| w18 | 6 | 0.103434 | 13.001 |
| w19 | 0 | None | 0.0 |
| w20 | 11 | -0.002708 | -2.606 |
| w21 | 12 | -0.083604 | 30.175 |
| w22 | 4 | 0.037724 | -6.801 |
| w23 | 10 | 0.049934 | 13.198 |
| w24 | 8 | 0.061518 | 187.167 |

