# Backtest of 040-02_agitated-daily-rise-next-day-giveback_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/040-02_agitated-daily-rise-next-day-giveback_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.018472 | -2.154 |
| w2 | 25 | 0.052322 | 13.654 |
| w3 | 20 | 0.062877 | 6.471 |
| w4 | 16 | -0.098102 | -18.157 |
| w5 | 0 | None | 0.0 |
| w6 | 35 | 0.039483 | -14.148 |
| w7 | 0 | None | 0.0 |
| w8 | 18 | 0.104925 | 2.805 |
| w9 | 14 | -0.10652 | -7.699 |
| w10 | 16 | 0.102413 | 5.05 |
| w11 | 46 | -0.034832 | -27.061 |
| w12 | 21 | -0.146838 | -18.163 |
| w13 | 34 | 0.076547 | 11.709 |
| w14 | 20 | 0.177674 | 31.642 |
| w15 | 55 | 0.083722 | -6.171 |
| w16 | 25 | 0.090416 | 11.192 |
| w17 | 33 | -0.034984 | -22.067 |
| w18 | 30 | 0.122921 | 16.589 |
| w19 | 49 | 0.111275 | 1.514 |
| w20 | 37 | 0.105647 | 11.374 |
| w21 | 25 | 0.078701 | -1.482 |
| w22 | 26 | 0.143879 | 17.191 |
| w23 | 3 | -0.029161 | -0.614 |
| w24 | 27 | -0.018408 | -0.139 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.02111 | 2.309 |
| w2 | 43 | -0.006267 | 7.297 |
| w3 | 25 | 0.079324 | 8.108 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 22 | 0.118809 | 7.357 |
| w7 | 0 | None | 0.0 |
| w8 | 13 | 0.088352 | 3.307 |
| w9 | 11 | 0.096058 | 8.241 |
| w10 | 18 | 0.132355 | 5.205 |
| w11 | 43 | -0.088385 | -40.928 |
| w12 | 14 | -0.088515 | -7.106 |
| w13 | 27 | 0.00791 | -2.275 |
| w14 | 33 | 0.006593 | 7.428 |
| w15 | 24 | 0.060043 | 4.658 |
| w16 | 34 | 0.165964 | 18.763 |
| w17 | 34 | 0.052118 | -1.956 |
| w18 | 35 | 0.225962 | 34.451 |
| w19 | 39 | 0.10578 | 7.045 |
| w20 | 40 | 0.073334 | 12.231 |
| w21 | 40 | 0.005519 | -11.874 |
| w22 | 38 | 0.225212 | 43.921 |
| w23 | 16 | 0.041201 | -5.373 |
| w24 | 23 | -0.052835 | -3.392 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 32 | 0.228688 | 36.635 |
| w3 | 17 | -0.030287 | -6.167 |
| w4 | 13 | -0.078409 | -9.992 |
| w5 | 26 | -0.031565 | -10.951 |
| w6 | 4 | -0.094477 | -5.697 |
| w7 | 0 | None | 0.0 |
| w8 | 37 | 0.082003 | -4.211 |
| w9 | 0 | None | 0.0 |
| w10 | 10 | -0.005529 | -4.617 |
| w11 | 47 | -0.021968 | -17.054 |
| w12 | 23 | -0.012497 | -3.846 |
| w13 | 23 | 0.134314 | 10.601 |
| w14 | 20 | -0.045857 | -6.634 |
| w15 | 29 | -0.053593 | -9.261 |
| w16 | 20 | 0.117196 | 8.729 |
| w17 | 41 | -0.06652 | -23.892 |
| w18 | 25 | 0.202153 | 25.978 |
| w19 | 38 | 0.199681 | 20.341 |
| w20 | 32 | 0.06174 | 7.955 |
| w21 | 39 | 0.11472 | -0.248 |
| w22 | 49 | -0.029416 | -4.819 |
| w23 | 7 | 0.067165 | 2.365 |
| w24 | 24 | -0.029295 | -3.058 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.096329 | 6.852 |
| w2 | 32 | 0.109527 | 14.907 |
| w3 | 13 | -0.01517 | -3.046 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 14 | -0.12107 | -15.754 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.123616 | 3.565 |
| w9 | 1 | 0.089224 | 0.499 |
| w10 | 6 | 0.188063 | 10.663 |
| w11 | 39 | 0.072029 | -16.201 |
| w12 | 13 | -0.043008 | -3.756 |
| w14 | 19 | 0.061447 | 8.15 |
| w15 | 25 | 0.178378 | 19.765 |
| w16 | 28 | 0.112627 | 6.619 |
| w17 | 32 | 0.175606 | 11.949 |
| w18 | 34 | 0.14594 | 13.295 |
| w19 | 54 | 0.028995 | 8.532 |
| w20 | 45 | 0.085083 | -4.741 |
| w21 | 30 | 0.261907 | 28.073 |
| w22 | 38 | -0.011009 | -15.231 |
| w23 | 25 | -0.027989 | -13.113 |
| w24 | 41 | 0.041194 | -12.556 |

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
| w1 | 5 | 0.098596 | 6.918 |
| w2 | 1 | 0.129312 | 13.563 |
| w3 | 0 | 0.000814 | 0.0 |
| w4 | 0 | 0.13822 | 0.0 |
| w5 | 15 | 0.093758 | 4.435 |
| w6 | 16 | 0.141647 | 7.649 |
| w8 | 2 | 0.010756 | 0.25 |
| w9 | 12 | 0.076102 | 8.56 |
| w10 | 8 | 0.068616 | 2.447 |
| w11 | 50 | -0.116238 | -45.39 |
| w12 | 1 | -0.083744 | -0.554 |
| w14 | 21 | -0.129701 | -13.194 |
| w15 | 20 | -0.001141 | -2.703 |
| w16 | 38 | 0.193021 | 25.442 |
| w17 | 26 | 0.040242 | 5.235 |
| w18 | 23 | 0.167234 | 10.886 |
| w19 | 26 | 0.119373 | 13.627 |
| w20 | 32 | -0.218626 | -39.109 |
| w21 | 34 | -0.335126 | -62.248 |
| w22 | 48 | 0.022733 | -2.648 |
| w23 | 6 | -0.019763 | -2.713 |
| w24 | 14 | -0.02135 | -1.005 |

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
| w1 | 16 | -0.012972 | -2.022 |
| w2 | 25 | 0.105128 | 11.329 |
| w3 | 14 | -0.155035 | -12.777 |
| w4 | 6 | 0.102548 | 4.009 |
| w5 | 20 | -0.065647 | -7.285 |
| w6 | 6 | -0.053057 | -4.741 |
| w7 | 4 | 0.046959 | 1.984 |
| w8 | 7 | 0.113041 | 1.69 |
| w9 | 17 | 0.096404 | 13.548 |
| w10 | 19 | 0.112373 | 4.815 |
| w11 | 48 | -0.002542 | -27.187 |
| w12 | 26 | -0.140883 | -23.944 |
| w13 | 24 | 0.046134 | 5.664 |
| w14 | 16 | 0.066157 | 6.054 |
| w15 | 18 | 0.065996 | 6.249 |
| w16 | 53 | -0.044883 | -37.074 |
| w17 | 31 | 0.042735 | 5.594 |
| w18 | 30 | 0.278497 | 35.749 |
| w19 | 50 | -0.070313 | -14.688 |
| w20 | 33 | -0.087671 | -22.557 |
| w21 | 36 | 0.006893 | -18.206 |
| w22 | 48 | 0.009352 | 3.14 |
| w23 | 13 | -0.086493 | -7.781 |
| w24 | 53 | -0.101641 | -50.44 |

