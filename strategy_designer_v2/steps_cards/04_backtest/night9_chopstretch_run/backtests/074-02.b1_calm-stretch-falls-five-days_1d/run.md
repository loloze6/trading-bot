# Backtest of 074-02.b1_calm-stretch-falls-five-days_1d

- Plan: `../../../../03_test_plan/night9_chopstretch_run/plans/074-02.b1_calm-stretch-falls-five-days_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 43 | -0.056888 | -4.143 |
| w2 | 20 | 0.096082 | 48.59 |
| w3 | 26 | 0.086681 | 9.14 |
| w4 | 16 | -0.014526 | -17.905 |
| w5 | 43 | -0.120128 | -13.57 |
| w6 | 8 | 0.040385 | -6.037 |
| w7 | 49 | -0.000439 | 4.753 |
| w8 | 14 | -0.046056 | -8.995 |
| w9 | 37 | -0.164048 | -33.18 |
| w10 | 23 | -0.048881 | -7.302 |
| w11 | 5 | 0.040183 | -1.28 |
| w12 | 37 | 0.000239 | -4.55 |
| w13 | 14 | -0.023902 | -2.302 |
| w14 | 28 | 0.150883 | 56.159 |
| w15 | 2 | -0.074749 | 0.079 |
| w16 | 11 | 0.028261 | 3.293 |
| w17 | 9 | 0.163182 | 0.629 |
| w18 | 0 | -0.007903 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 13 | 0.067186 | 11.391 |
| w21 | 14 | -0.007841 | -12.11 |
| w22 | 22 | -0.066365 | -13.584 |
| w23 | 31 | -0.071428 | -9.545 |
| w24 | 23 | 0.007269 | 7.096 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | 0.020249 | 13.682 |
| w2 | 9 | 0.120927 | 26.073 |
| w3 | 20 | 0.035173 | -0.163 |
| w4 | 15 | -0.039151 | -13.467 |
| w5 | 42 | -0.059302 | -0.952 |
| w6 | 31 | -0.033479 | -15.12 |
| w7 | 50 | -0.017503 | 21.053 |
| w8 | 13 | -0.064279 | -10.179 |
| w9 | 36 | -0.032399 | -5.095 |
| w10 | 17 | -0.061935 | -8.889 |
| w11 | 3 | -0.100648 | -7.636 |
| w12 | 26 | -0.116791 | -6.839 |
| w13 | 13 | 0.185908 | 39.254 |
| w14 | 12 | 0.163384 | 31.375 |
| w15 | 21 | 0.013698 | 1.299 |
| w16 | 2 | -0.05899 | -2.497 |
| w17 | 6 | -0.034004 | -5.773 |
| w18 | 5 | -0.071311 | -2.756 |
| w19 | 0 | None | 0.0 |
| w20 | 16 | 0.085691 | 3.745 |
| w21 | 18 | -0.112437 | -27.162 |
| w22 | 16 | -0.081293 | 0.964 |
| w23 | 17 | -0.043212 | -10.584 |
| w24 | 27 | -0.008369 | 2.514 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 51 | -0.11868 | -8.681 |
| w2 | 15 | 0.002849 | 8.706 |
| w3 | 31 | -0.017985 | -9.286 |
| w4 | 21 | 0.06505 | 3.435 |
| w5 | 22 | 0.087413 | 22.064 |
| w6 | 35 | -0.072795 | -22.978 |
| w7 | 51 | 0.003075 | 29.778 |
| w8 | 0 | -0.049752 | 0.0 |
| w9 | 47 | -0.045445 | 5.619 |
| w10 | 36 | -0.082008 | -19.675 |
| w11 | 4 | -0.090956 | -7.467 |
| w12 | 12 | -0.081471 | -2.982 |
| w13 | 25 | -0.023556 | 8.915 |
| w14 | 25 | 0.09019 | 35.413 |
| w15 | 26 | 0.147652 | 19.118 |
| w16 | 7 | -0.096402 | -6.557 |
| w17 | 6 | -0.175862 | -8.086 |
| w18 | 12 | 0.004453 | -1.928 |
| w19 | 8 | -0.115006 | -21.721 |
| w20 | 17 | 0.030743 | 13.699 |
| w21 | 18 | -0.028434 | -15.988 |
| w22 | 4 | 0.10669 | 9.623 |
| w23 | 22 | -0.068736 | -13.834 |
| w24 | 17 | -0.085084 | -8.704 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.112851 | -10.984 |
| w2 | 13 | -0.106416 | -10.225 |
| w3 | 40 | -0.12194 | -16.061 |
| w4 | 31 | -0.109817 | -15.955 |
| w5 | 64 | -0.035325 | 5.001 |
| w6 | 16 | -0.086188 | -11.843 |
| w7 | 56 | 0.010343 | 7.453 |
| w8 | 17 | -0.074288 | -7.399 |
| w9 | 45 | 0.011728 | 18.742 |
| w10 | 21 | -0.135548 | -13.361 |
| w11 | 2 | -0.03779 | -2.945 |
| w12 | 39 | -0.065713 | -4.885 |
| w14 | 21 | 0.128324 | 53.246 |
| w15 | 16 | 0.021393 | 3.281 |
| w16 | 2 | -0.111649 | -7.227 |
| w17 | 12 | -0.068389 | -1.087 |
| w18 | 3 | -0.037125 | -4.354 |
| w19 | 3 | 0.136904 | 11.046 |
| w20 | 12 | -0.02528 | -10.145 |
| w21 | 22 | 0.047494 | -4.39 |
| w22 | 8 | 0.035029 | -6.324 |
| w23 | 12 | 0.11352 | 32.979 |
| w24 | 2 | -0.015103 | -2.309 |

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
| w1 | 36 | 0.059114 | 21.87 |
| w2 | 7 | -0.011641 | 18.57 |
| w3 | 0 | -0.031238 | 0.0 |
| w4 | 0 | -0.093292 | 0.0 |
| w5 | 17 | 0.036208 | -5.429 |
| w6 | 20 | -0.088004 | -11.645 |
| w8 | 32 | -0.115944 | -16.839 |
| w9 | 42 | 0.026705 | 17.847 |
| w10 | 31 | 0.002543 | -6.665 |
| w11 | 0 | None | 0.0 |
| w12 | 42 | -0.051295 | 0.292 |
| w14 | 25 | 0.046883 | -19.978 |
| w15 | 40 | 0.045169 | 8.311 |
| w16 | 2 | -0.023942 | -4.089 |
| w17 | 18 | -0.009617 | -7.937 |
| w18 | 13 | -0.005834 | -0.786 |
| w19 | 13 | -0.072682 | -11.169 |
| w20 | 31 | 0.035669 | 4.029 |
| w21 | 10 | 0.021749 | -8.696 |
| w22 | 0 | -0.109593 | 0.0 |
| w23 | 41 | -0.076872 | -19.516 |
| w24 | 47 | -0.111068 | 13.949 |

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
| w1 | 32 | 0.092919 | 13.682 |
| w2 | 13 | -0.085316 | -15.191 |
| w3 | 48 | -0.018933 | 10.734 |
| w4 | 36 | -0.063112 | -5.762 |
| w5 | 39 | 0.050079 | 28.124 |
| w6 | 30 | -0.093232 | -22.505 |
| w7 | 41 | -0.104606 | -18.518 |
| w8 | 24 | 0.034424 | 1.337 |
| w9 | 24 | 0.009422 | -1.976 |
| w10 | 21 | -0.123982 | -12.033 |
| w11 | 5 | -0.046995 | -5.758 |
| w12 | 6 | 0.039244 | -4.467 |
| w13 | 14 | 0.092258 | 15.757 |
| w14 | 27 | 0.076742 | 12.892 |
| w15 | 25 | 0.028267 | 13.511 |
| w16 | 0 | None | 0.0 |
| w17 | 16 | -0.031599 | -1.968 |
| w18 | 6 | -0.03997 | -2.833 |
| w19 | 0 | None | 0.0 |
| w20 | 11 | -0.042602 | -6.614 |
| w21 | 12 | -0.068002 | -9.131 |
| w22 | 3 | -0.136683 | -2.326 |
| w23 | 30 | -0.054801 | -8.813 |
| w24 | 0 | None | 0.0 |

