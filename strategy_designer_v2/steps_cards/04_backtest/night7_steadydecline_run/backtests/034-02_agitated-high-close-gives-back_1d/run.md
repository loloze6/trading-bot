# Backtest of 034-02_agitated-high-close-gives-back_1d

- Plan: `../../../../03_test_plan/night7_steadydecline_run/plans/034-02_agitated-high-close-gives-back_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | -0.070264 | -5.76 |
| w2 | 57 | -0.048373 | 6.3 |
| w3 | 45 | 0.079652 | 16.325 |
| w4 | 26 | -0.137407 | -25.44 |
| w5 | 0 | None | 0.0 |
| w6 | 54 | 0.093789 | -18.332 |
| w7 | 0 | None | 0.0 |
| w8 | 28 | 0.124674 | 2.054 |
| w9 | 26 | 0.032867 | 6.59 |
| w10 | 31 | 0.042556 | -1.5 |
| w11 | 74 | -0.089843 | -35.971 |
| w12 | 30 | -0.194989 | -25.518 |
| w13 | 73 | 0.081984 | 12.825 |
| w14 | 39 | 0.106904 | 22.715 |
| w15 | 91 | 0.132789 | -16.589 |
| w16 | 48 | 0.163097 | 34.469 |
| w17 | 43 | -0.074238 | -32.197 |
| w18 | 75 | 0.124521 | 24.059 |
| w19 | 84 | 0.193316 | -3.254 |
| w20 | 80 | 0.081214 | 9.899 |
| w21 | 40 | 0.036749 | -12.473 |
| w22 | 52 | 0.147011 | 22.519 |
| w23 | 4 | -0.06427 | -2.2 |
| w24 | 48 | 0.023264 | 10.927 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.056825 | 6.841 |
| w2 | 92 | -0.144422 | -8.904 |
| w3 | 42 | 0.086516 | 14.422 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 41 | 0.125863 | 4.738 |
| w7 | 0 | None | 0.0 |
| w8 | 32 | 0.116786 | 6.794 |
| w9 | 24 | 0.071528 | 8.956 |
| w10 | 33 | 0.147311 | 3.288 |
| w11 | 71 | -0.011201 | -41.239 |
| w12 | 21 | -0.105293 | -10.071 |
| w13 | 49 | -0.064559 | -11.028 |
| w14 | 62 | -0.053074 | 0.99 |
| w15 | 45 | 0.104686 | 8.421 |
| w16 | 64 | 0.159798 | 14.416 |
| w17 | 55 | 0.148603 | 4.662 |
| w18 | 64 | 0.075836 | -1.338 |
| w19 | 78 | 0.154284 | 4.294 |
| w20 | 79 | 0.078399 | 23.285 |
| w21 | 64 | -0.007025 | -20.662 |
| w22 | 80 | 0.12739 | 45.632 |
| w23 | 39 | 0.04121 | -12.313 |
| w24 | 38 | -0.113572 | -8.459 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 58 | 0.035176 | 16.197 |
| w3 | 39 | -0.045322 | -12.242 |
| w4 | 23 | -0.068424 | -13.526 |
| w5 | 53 | -0.063551 | -14.279 |
| w6 | 5 | -0.142118 | -7.38 |
| w7 | 0 | None | 0.0 |
| w8 | 78 | 0.168654 | -9.471 |
| w9 | 0 | None | 0.0 |
| w10 | 16 | 0.007246 | -4.721 |
| w11 | 88 | 0.056762 | -20.829 |
| w12 | 38 | 0.066102 | 8.372 |
| w13 | 50 | 0.008376 | -3.184 |
| w14 | 44 | -0.021421 | 0.806 |
| w15 | 57 | -0.096565 | -15.485 |
| w16 | 46 | 0.18647 | 21.542 |
| w17 | 67 | 0.008465 | -24.721 |
| w18 | 61 | 0.102655 | 18.457 |
| w19 | 64 | 0.186032 | 14.308 |
| w20 | 61 | -0.015794 | 1.479 |
| w21 | 68 | 0.035092 | -23.663 |
| w22 | 90 | -0.02187 | -4.556 |
| w23 | 19 | 0.070011 | 4.146 |
| w24 | 47 | -0.081611 | -7.66 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 55 | 0.001321 | -4.18 |
| w2 | 61 | 0.100346 | 19.126 |
| w3 | 23 | -0.026396 | -5.702 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 22 | -0.02497 | -9.118 |
| w7 | 0 | None | 0.0 |
| w8 | 18 | 0.105333 | 3.586 |
| w9 | 2 | 0.021599 | 1.166 |
| w10 | 10 | 0.135204 | 7.348 |
| w11 | 79 | 0.10396 | -30.668 |
| w12 | 24 | -0.058107 | -6.44 |
| w14 | 44 | 0.057768 | 15.596 |
| w15 | 58 | 0.189062 | 24.425 |
| w16 | 60 | 0.142791 | 14.624 |
| w17 | 49 | 0.120464 | 2.139 |
| w18 | 69 | 0.207843 | 41.785 |
| w19 | 93 | 0.110819 | 34.336 |
| w20 | 65 | 0.055677 | -14.207 |
| w21 | 47 | 0.123735 | 9.913 |
| w22 | 61 | 0.019439 | -13.828 |
| w23 | 49 | -0.018002 | -11.124 |
| w24 | 75 | -0.10457 | -39.747 |

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
| w1 | 11 | 0.051613 | 4.615 |
| w2 | 25 | 0.125455 | 24.242 |
| w3 | 0 | 0.004354 | 0.0 |
| w4 | 0 | 0.123359 | 0.0 |
| w5 | 39 | 0.050529 | -1.543 |
| w6 | 31 | 0.053036 | -4.324 |
| w8 | 8 | -0.006812 | -0.283 |
| w9 | 20 | -0.026704 | -0.566 |
| w10 | 17 | 0.043463 | -0.179 |
| w11 | 91 | -0.007067 | -49.386 |
| w12 | 4 | -0.001419 | 0.023 |
| w14 | 39 | 0.00949 | -1.599 |
| w15 | 36 | 0.042422 | 4.909 |
| w16 | 79 | 0.18182 | 19.311 |
| w17 | 61 | 0.109858 | 10.243 |
| w18 | 58 | 0.207996 | 23.557 |
| w19 | 59 | 0.073664 | 9.67 |
| w20 | 49 | -0.174856 | -38.92 |
| w21 | 66 | -0.153207 | -54.861 |
| w22 | 88 | 0.007493 | -13.26 |
| w23 | 15 | -0.02213 | -4.209 |
| w24 | 24 | -0.058293 | -3.446 |

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
| w1 | 27 | 0.040298 | 4.999 |
| w2 | 56 | 0.117201 | 26.69 |
| w3 | 23 | -0.109529 | -11.817 |
| w4 | 14 | 0.029823 | 1.327 |
| w5 | 33 | -0.067058 | -6.799 |
| w6 | 15 | 0.148002 | 8.011 |
| w7 | 12 | 0.06572 | 5.596 |
| w8 | 16 | 0.190575 | 8.445 |
| w9 | 43 | 0.019012 | 7.594 |
| w10 | 35 | 0.152357 | 8.686 |
| w11 | 76 | 0.046754 | -35.323 |
| w12 | 53 | -0.02091 | -15.839 |
| w13 | 54 | 0.056767 | 10.863 |
| w14 | 32 | 0.075219 | 16.07 |
| w15 | 42 | 0.094456 | 11.399 |
| w16 | 99 | -0.005967 | -39.275 |
| w17 | 62 | 0.117489 | 17.837 |
| w18 | 62 | 0.202567 | 35.719 |
| w19 | 97 | -0.011525 | -0.717 |
| w20 | 65 | -0.140981 | -35.671 |
| w21 | 78 | -0.024173 | -33.732 |
| w22 | 94 | -0.103715 | -11.914 |
| w23 | 23 | -0.002428 | -3.8 |
| w24 | 80 | -0.172367 | -69.201 |

