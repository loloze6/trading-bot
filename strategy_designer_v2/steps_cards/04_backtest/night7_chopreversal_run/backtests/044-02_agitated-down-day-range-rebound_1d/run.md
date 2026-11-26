# Backtest of 044-02_agitated-down-day-range-rebound_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/044-02_agitated-down-day-range-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.01785 | -2.683 |
| w2 | 29 | 0.081552 | -0.23 |
| w3 | 24 | 0.245727 | 21.401 |
| w4 | 11 | 0.123532 | 10.483 |
| w5 | 0 | None | 0.0 |
| w6 | 24 | 0.228383 | 34.702 |
| w7 | 0 | None | 0.0 |
| w8 | 16 | 0.044516 | 3.576 |
| w9 | 15 | -0.022022 | -5.048 |
| w10 | 13 | 0.038054 | 7.138 |
| w11 | 35 | 0.005176 | 8.451 |
| w12 | 15 | 0.09418 | 7.86 |
| w13 | 36 | 0.032755 | 0.819 |
| w14 | 17 | 0.205347 | 17.15 |
| w15 | 40 | -0.097889 | -3.765 |
| w16 | 22 | 0.188767 | 14.999 |
| w17 | 20 | 0.04164 | 11.895 |
| w18 | 37 | 0.16603 | 18.287 |
| w19 | 42 | 0.038753 | 8.258 |
| w20 | 42 | 0.134848 | 12.497 |
| w21 | 20 | 0.130711 | 19.024 |
| w22 | 24 | 0.150198 | 14.546 |
| w23 | 2 | -0.026356 | -0.251 |
| w24 | 34 | 0.017041 | -6.991 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.139217 | -11.008 |
| w2 | 43 | 0.074978 | -3.673 |
| w3 | 25 | 0.320801 | 28.075 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 19 | 0.114982 | 14.9 |
| w7 | 0 | None | 0.0 |
| w8 | 16 | 0.089925 | 5.714 |
| w9 | 12 | 0.064124 | 2.558 |
| w10 | 14 | 0.022039 | 5.845 |
| w11 | 36 | 0.027289 | 17.559 |
| w12 | 9 | 0.089502 | 5.225 |
| w13 | 20 | -0.068522 | -7.472 |
| w14 | 37 | 0.260521 | 30.605 |
| w15 | 20 | 0.034152 | 3.081 |
| w16 | 34 | 0.040414 | -0.067 |
| w17 | 26 | -0.018707 | -1.837 |
| w18 | 32 | 0.132914 | 21.291 |
| w19 | 39 | -0.052725 | -5.303 |
| w20 | 40 | 0.072434 | -1.454 |
| w21 | 34 | 0.087548 | 15.472 |
| w22 | 46 | 0.107789 | -1.251 |
| w23 | 18 | 0.146635 | 26.901 |
| w24 | 24 | 0.018588 | -3.882 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 29 | 0.145996 | 10.221 |
| w3 | 18 | 0.226681 | 23.323 |
| w4 | 9 | 0.121661 | 6.758 |
| w5 | 25 | 0.004335 | -4.871 |
| w6 | 1 | 0.066606 | 1.769 |
| w7 | 0 | None | 0.0 |
| w8 | 38 | 0.025489 | 11.005 |
| w9 | 0 | None | 0.0 |
| w10 | 10 | 0.027824 | 2.102 |
| w11 | 40 | -0.219434 | -18.431 |
| w12 | 20 | -0.015578 | -3.733 |
| w13 | 22 | 0.0619 | 4.291 |
| w14 | 25 | 0.144403 | 7.867 |
| w15 | 31 | 0.13023 | 10.01 |
| w16 | 29 | 0.108123 | 4.202 |
| w17 | 31 | 0.090493 | 17.377 |
| w18 | 27 | 0.174063 | 17.524 |
| w19 | 35 | 0.099238 | 18.283 |
| w20 | 26 | 0.04813 | -2.627 |
| w21 | 33 | 0.033097 | 10.149 |
| w22 | 49 | -0.060445 | -8.742 |
| w23 | 13 | 0.120198 | 8.797 |
| w24 | 23 | -0.008941 | -4.001 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.039735 | -7.999 |
| w2 | 26 | -0.086707 | -14.013 |
| w3 | 11 | 0.129114 | 8.17 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 9 | 0.026259 | 1.08 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | 0.025351 | 0.761 |
| w9 | 2 | 0.034546 | 0.547 |
| w10 | 5 | 0.082622 | 4.568 |
| w11 | 35 | -0.00202 | 18.447 |
| w12 | 12 | -0.003901 | -3.016 |
| w14 | 26 | 0.170695 | 9.996 |
| w15 | 28 | -0.03389 | -4.556 |
| w16 | 32 | 0.040016 | -3.034 |
| w17 | 23 | -0.015603 | -1.851 |
| w18 | 32 | 0.271164 | 32.294 |
| w19 | 49 | 0.202505 | 18.513 |
| w20 | 28 | 0.23093 | 31.221 |
| w21 | 19 | 0.088606 | 11.587 |
| w22 | 28 | 0.044273 | 7.289 |
| w23 | 22 | -0.116048 | -12.668 |
| w24 | 39 | 0.011421 | 9.855 |

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
| w1 | 5 | 0.062416 | 0.834 |
| w2 | 0 | -0.055904 | 0.0 |
| w3 | 0 | 0.189077 | 0.0 |
| w4 | 0 | 0.08224 | 0.0 |
| w5 | 25 | -0.003355 | 2.348 |
| w6 | 19 | 0.054869 | 6.821 |
| w8 | 5 | 0.052926 | 1.307 |
| w9 | 11 | 0.014474 | -0.689 |
| w10 | 8 | 0.148189 | 9.934 |
| w11 | 42 | 0.039862 | 31.108 |
| w12 | 4 | -0.018985 | -1.213 |
| w14 | 17 | 0.053766 | 3.088 |
| w15 | 19 | -0.009356 | -3.504 |
| w16 | 45 | 0.0644 | 1.97 |
| w17 | 32 | 0.138564 | 23.386 |
| w18 | 26 | 0.14031 | 9.036 |
| w19 | 33 | 0.010774 | -1.579 |
| w20 | 26 | 0.004706 | 2.535 |
| w21 | 30 | -0.035231 | 19.751 |
| w22 | 43 | 0.018817 | 0.643 |
| w23 | 7 | 0.070792 | 3.944 |
| w24 | 10 | 0.042145 | 0.063 |

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
| w1 | 13 | 0.15503 | 9.29 |
| w2 | 35 | 0.120124 | 4.993 |
| w3 | 11 | 0.247023 | 13.293 |
| w4 | 6 | 0.003298 | -0.014 |
| w5 | 17 | 0.074083 | 3.989 |
| w6 | 9 | 0.040026 | 2.627 |
| w7 | 9 | -0.034739 | -2.014 |
| w8 | 8 | 0.172 | 4.541 |
| w9 | 24 | 0.133459 | 7.843 |
| w10 | 20 | -0.064258 | -2.814 |
| w11 | 37 | -0.070503 | 4.02 |
| w12 | 28 | 0.002516 | 1.083 |
| w13 | 24 | 0.131024 | 6.224 |
| w14 | 20 | 0.145788 | 7.401 |
| w15 | 30 | 0.113767 | 8.106 |
| w16 | 45 | 0.061824 | 17.291 |
| w17 | 32 | -0.01 | -7.332 |
| w18 | 35 | 0.256938 | 30.904 |
| w19 | 50 | 0.076707 | -3.66 |
| w20 | 42 | 0.054138 | 14.037 |
| w21 | 39 | -0.04367 | 1.187 |
| w22 | 43 | -0.00305 | -7.47 |
| w23 | 13 | -0.083539 | -5.349 |
| w24 | 31 | -0.021261 | 13.268 |

