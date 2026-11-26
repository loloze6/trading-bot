# Backtest of 041-01_agitated-scaled-rise-next-day-continues_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/041-01_agitated-scaled-rise-next-day-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.014167 | 0.215 |
| w2 | 23 | -0.035849 | -11.863 |
| w3 | 18 | -0.073905 | -8.833 |
| w4 | 14 | 0.112078 | 16.052 |
| w5 | 0 | None | 0.0 |
| w6 | 35 | -0.041239 | 6.94 |
| w7 | 0 | None | 0.0 |
| w8 | 18 | -0.121931 | -3.922 |
| w9 | 11 | 0.143875 | 9.72 |
| w10 | 16 | -0.079238 | -5.191 |
| w11 | 44 | 0.046969 | 29.4 |
| w12 | 21 | 0.131555 | 14.625 |
| w13 | 36 | -0.07918 | -11.907 |
| w14 | 18 | -0.167375 | -21.669 |
| w15 | 54 | -0.087706 | -0.914 |
| w16 | 25 | -0.086879 | -10.967 |
| w17 | 30 | 0.016654 | 15.706 |
| w18 | 30 | -0.110795 | -15.567 |
| w19 | 49 | -0.118225 | -9.515 |
| w20 | 36 | -0.093684 | -12.843 |
| w21 | 25 | -0.051962 | 0.199 |
| w22 | 26 | -0.148234 | -18.463 |
| w23 | 3 | 0.029119 | 0.494 |
| w24 | 26 | 0.025082 | -2.875 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.017494 | -3.281 |
| w2 | 42 | 0.002398 | -10.751 |
| w3 | 23 | -0.116858 | -11.128 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 22 | -0.12868 | -9.678 |
| w7 | 0 | None | 0.0 |
| w8 | 13 | -0.090477 | -3.648 |
| w9 | 9 | -0.093544 | -7.871 |
| w10 | 17 | -0.102658 | -4.433 |
| w11 | 43 | 0.081752 | 48.945 |
| w12 | 14 | 0.087532 | 6.114 |
| w13 | 27 | -0.021586 | -1.829 |
| w14 | 33 | -0.007567 | -10.961 |
| w15 | 24 | -0.063887 | -6.129 |
| w16 | 32 | -0.171805 | -18.719 |
| w17 | 31 | -0.050389 | -0.853 |
| w18 | 39 | -0.198196 | -25.744 |
| w19 | 38 | -0.105263 | -10.762 |
| w20 | 40 | -0.070071 | -13.568 |
| w21 | 38 | 0.014338 | 9.599 |
| w22 | 39 | -0.21099 | -33.233 |
| w23 | 15 | -0.035218 | 2.19 |
| w24 | 20 | 0.061761 | 0.948 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 31 | -0.21454 | -26.675 |
| w3 | 15 | 0.056043 | 3.933 |
| w4 | 13 | 0.062511 | 4.559 |
| w5 | 26 | 0.050344 | 5.999 |
| w6 | 4 | 0.095833 | 5.243 |
| w7 | 0 | None | 0.0 |
| w8 | 37 | -0.083688 | -1.402 |
| w9 | 0 | None | 0.0 |
| w10 | 11 | 0.012768 | 2.315 |
| w11 | 46 | 0.019417 | 10.606 |
| w12 | 20 | 0.012111 | -2.081 |
| w13 | 23 | -0.128639 | -10.386 |
| w14 | 19 | 0.028776 | -1.647 |
| w15 | 29 | 0.05486 | 4.8 |
| w16 | 20 | -0.114873 | -9.692 |
| w17 | 40 | 0.063706 | 15.405 |
| w18 | 26 | -0.161198 | -20.32 |
| w19 | 36 | -0.198158 | -21.027 |
| w20 | 31 | -0.077696 | -13.402 |
| w21 | 35 | -0.104829 | -12.577 |
| w22 | 53 | 0.037639 | -1.85 |
| w23 | 7 | -0.061949 | -3.233 |
| w24 | 23 | 0.028632 | -1.888 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | -0.095042 | -9.571 |
| w2 | 31 | -0.129696 | -20.609 |
| w3 | 13 | 0.01008 | -0.449 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 13 | 0.123108 | 10.096 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | -0.132403 | -4.113 |
| w9 | 1 | -0.08913 | -0.533 |
| w10 | 6 | -0.170287 | -8.655 |
| w11 | 38 | -0.059024 | 4.883 |
| w12 | 12 | 0.046299 | 1.534 |
| w14 | 18 | -0.03357 | -8.192 |
| w15 | 25 | -0.19187 | -21.242 |
| w16 | 30 | -0.084715 | -12.469 |
| w17 | 31 | -0.165178 | -15.63 |
| w18 | 35 | -0.143658 | -12.31 |
| w19 | 49 | -0.071942 | -25.506 |
| w20 | 45 | -0.071769 | -6.61 |
| w21 | 28 | -0.309435 | -34.194 |
| w22 | 39 | 0.019465 | 7.69 |
| w23 | 22 | 0.046981 | 4.216 |
| w24 | 41 | -0.042102 | -1.155 |

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
| w1 | 5 | -0.090112 | -5.762 |
| w2 | 1 | -0.113146 | -11.026 |
| w3 | 0 | 0.008332 | 0.0 |
| w4 | 0 | -0.150492 | 0.0 |
| w5 | 12 | -0.098085 | -5.44 |
| w6 | 17 | -0.078584 | -5.244 |
| w8 | 2 | -0.011817 | -0.414 |
| w9 | 12 | -0.08589 | -10.212 |
| w10 | 8 | -0.073057 | -3.844 |
| w11 | 54 | 0.119666 | 62.864 |
| w12 | 1 | 0.083744 | 0.422 |
| w14 | 20 | 0.172005 | 12.389 |
| w15 | 17 | -0.015398 | -3.071 |
| w16 | 38 | -0.201357 | -23.305 |
| w17 | 26 | -0.032108 | -6.168 |
| w18 | 25 | -0.171717 | -12.864 |
| w19 | 23 | -0.124799 | -12.997 |
| w20 | 28 | 0.203733 | 33.98 |
| w21 | 33 | 0.314488 | 91.254 |
| w22 | 48 | 0.007245 | 0.435 |
| w23 | 6 | 0.021088 | 1.407 |
| w24 | 14 | 0.024374 | -1.615 |

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
| w1 | 14 | 0.014949 | 0.289 |
| w2 | 26 | -0.109505 | -14.022 |
| w3 | 13 | 0.143282 | 8.351 |
| w4 | 6 | -0.11005 | -5.098 |
| w5 | 16 | 0.049781 | 1.792 |
| w6 | 6 | 0.050624 | 2.077 |
| w7 | 4 | -0.047542 | -2.007 |
| w8 | 7 | -0.126349 | -2.328 |
| w9 | 17 | -0.092269 | -13.45 |
| w10 | 18 | -0.130868 | -8.598 |
| w11 | 44 | 0.006913 | 22.769 |
| w12 | 25 | 0.167522 | 19.007 |
| w13 | 25 | -0.028141 | -5.047 |
| w14 | 13 | -0.032957 | -5.253 |
| w15 | 17 | -0.060901 | -8.643 |
| w16 | 54 | 0.035914 | 34.188 |
| w17 | 29 | -0.037489 | -8.309 |
| w18 | 31 | -0.217405 | -24.942 |
| w19 | 48 | 0.080608 | 6.443 |
| w20 | 30 | 0.101252 | 16.684 |
| w21 | 35 | -0.008981 | 10.134 |
| w22 | 50 | -0.010283 | -9.04 |
| w23 | 13 | 0.091921 | 6.534 |
| w24 | 53 | 0.091305 | 68.379 |

