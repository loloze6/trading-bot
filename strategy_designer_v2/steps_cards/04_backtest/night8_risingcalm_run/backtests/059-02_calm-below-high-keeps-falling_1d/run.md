# Backtest of 059-02_calm-below-high-keeps-falling_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/059-02_calm-below-high-keeps-falling_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 42 | -0.018825 | 4.114 |
| w2 | 32 | 0.086404 | 58.168 |
| w3 | 37 | 0.12058 | 17.119 |
| w4 | 29 | 0.058297 | -27.795 |
| w5 | 62 | -0.028596 | 1.372 |
| w6 | 16 | 0.100463 | -6.329 |
| w7 | 49 | 0.08675 | 19.085 |
| w8 | 29 | -0.062065 | -19.129 |
| w9 | 45 | -0.130042 | -24.351 |
| w10 | 39 | 0.00721 | -17.902 |
| w11 | 13 | 0.092005 | 5.639 |
| w12 | 35 | 0.148221 | 28.767 |
| w13 | 14 | -0.013038 | -1.222 |
| w14 | 29 | 0.106874 | 76.142 |
| w15 | 9 | -0.208087 | -23.098 |
| w16 | 28 | 0.051453 | -4.868 |
| w17 | 33 | 0.085168 | -29.585 |
| w18 | 20 | -0.136026 | -13.252 |
| w19 | 8 | -0.056972 | -13.739 |
| w20 | 14 | 0.052872 | 9.546 |
| w21 | 26 | 0.071044 | -18.909 |
| w22 | 31 | -0.083587 | -18.381 |
| w23 | 42 | 0.036532 | -10.458 |
| w24 | 24 | 0.035689 | 13.229 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 43 | -0.00581 | 13.587 |
| w2 | 9 | 0.170684 | 45.289 |
| w3 | 31 | 0.115744 | 9.068 |
| w4 | 52 | -0.073955 | -36.987 |
| w5 | 53 | -0.086966 | -3.715 |
| w6 | 35 | 0.006848 | -13.759 |
| w7 | 61 | -0.03454 | 30.693 |
| w8 | 40 | -0.108776 | -24.012 |
| w9 | 41 | -0.019424 | -0.137 |
| w10 | 45 | -0.074086 | -38.706 |
| w11 | 17 | 0.008488 | -18.769 |
| w12 | 46 | 0.019573 | -0.831 |
| w13 | 20 | 0.170698 | 30.624 |
| w14 | 12 | 0.210486 | 51.9 |
| w15 | 41 | -0.02536 | -14.824 |
| w16 | 17 | -0.093329 | -16.046 |
| w17 | 27 | -0.095327 | -26.966 |
| w18 | 16 | -0.135181 | -15.962 |
| w19 | 14 | -0.161007 | -13.52 |
| w20 | 11 | 0.046203 | 4.482 |
| w21 | 20 | -0.03136 | -23.058 |
| w22 | 13 | -0.036266 | -1.159 |
| w23 | 27 | 0.119916 | -16.604 |
| w24 | 29 | 0.058434 | 12.573 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 53 | 0.016253 | 21.608 |
| w2 | 26 | -0.006904 | 20.327 |
| w3 | 47 | 0.063212 | -14.262 |
| w4 | 41 | 0.01063 | -11.772 |
| w5 | 28 | 0.073473 | 28.695 |
| w6 | 55 | -0.000647 | -16.647 |
| w7 | 51 | 0.032263 | 46.13 |
| w8 | 17 | -0.119472 | -20.131 |
| w9 | 55 | 0.011296 | 19.032 |
| w10 | 61 | -0.078025 | -25.924 |
| w11 | 8 | -0.097486 | -15.435 |
| w12 | 34 | 0.013512 | -9.992 |
| w13 | 34 | -0.013393 | 15.293 |
| w14 | 30 | 0.133896 | 44.66 |
| w15 | 30 | 0.132948 | 31.539 |
| w16 | 30 | -0.032757 | -10.869 |
| w17 | 23 | -0.045051 | -23.993 |
| w18 | 24 | -0.089824 | -14.312 |
| w19 | 19 | 0.016616 | -10.924 |
| w20 | 29 | 0.016181 | 10.934 |
| w21 | 28 | 0.019846 | -5.691 |
| w22 | 3 | 0.124184 | 9.451 |
| w23 | 46 | -0.04605 | -21.831 |
| w24 | 34 | -0.100119 | -5.628 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.061915 | -6.626 |
| w2 | 15 | -0.068928 | -3.701 |
| w3 | 48 | -0.071431 | -14.121 |
| w4 | 53 | -0.106913 | -27.466 |
| w5 | 67 | 0.07228 | 13.28 |
| w6 | 56 | -0.07708 | -32.614 |
| w7 | 46 | 0.049412 | 27.675 |
| w8 | 45 | -0.166491 | -35.259 |
| w9 | 55 | -0.014239 | 18.495 |
| w10 | 64 | -0.250027 | -49.738 |
| w11 | 8 | -0.080935 | -20.302 |
| w12 | 58 | -0.056419 | -2.636 |
| w14 | 29 | 0.099545 | 60.528 |
| w15 | 25 | -0.014924 | -21.976 |
| w16 | 19 | 0.019428 | -8.954 |
| w17 | 34 | -0.092434 | -25.898 |
| w18 | 21 | -0.099236 | -18.322 |
| w19 | 1 | 0.11799 | 19.446 |
| w20 | 23 | -0.037895 | -26.188 |
| w21 | 33 | 0.033866 | -4.472 |
| w22 | 18 | 0.063916 | -4.834 |
| w23 | 30 | 0.09373 | 15.767 |
| w24 | 9 | 0.013517 | 0.175 |

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
| w1 | 47 | 0.093301 | 37.773 |
| w2 | 7 | -0.057303 | 18.436 |
| w3 | 0 | -0.009935 | 0.0 |
| w4 | 0 | -0.145218 | 0.0 |
| w5 | 18 | -0.058316 | -63.496 |
| w6 | 30 | 0.016853 | -11.904 |
| w8 | 54 | -0.229401 | -14.95 |
| w9 | 45 | 0.111201 | 41.884 |
| w10 | 53 | 0.034607 | -14.378 |
| w11 | 0 | None | 0.0 |
| w12 | 54 | 0.047567 | 33.032 |
| w14 | 29 | 0.087556 | -13.141 |
| w15 | 39 | 0.074565 | -1.144 |
| w16 | 9 | -0.087167 | -8.689 |
| w17 | 25 | -0.005394 | -54.945 |
| w18 | 28 | -0.099534 | -21.516 |
| w19 | 29 | -0.064382 | -10.963 |
| w20 | 37 | 0.035299 | 1.519 |
| w21 | 24 | 0.092464 | -2.713 |
| w22 | 8 | 0.035912 | 5.229 |
| w23 | 52 | 0.085683 | -1.981 |
| w24 | 46 | -0.093298 | 18.553 |

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
| w1 | 37 | 0.130883 | 16.754 |
| w2 | 16 | -0.027844 | 1.152 |
| w3 | 53 | 0.038273 | 14.634 |
| w4 | 50 | -0.06244 | -14.755 |
| w5 | 35 | 0.063681 | 39.785 |
| w6 | 56 | -0.057849 | -25.651 |
| w7 | 52 | -0.063457 | -6.752 |
| w8 | 55 | -0.034078 | -9.13 |
| w9 | 27 | 0.067879 | 13.744 |
| w10 | 51 | -0.247846 | -46.617 |
| w11 | 11 | -0.024972 | -15.766 |
| w12 | 32 | -0.025133 | -32.942 |
| w13 | 21 | 0.055745 | 13.492 |
| w14 | 34 | 0.119829 | 42.954 |
| w15 | 36 | 0.003713 | 1.77 |
| w16 | 0 | None | 0.0 |
| w17 | 33 | -0.080019 | -15.275 |
| w18 | 18 | -0.08401 | -11.487 |
| w19 | 0 | None | 0.0 |
| w20 | 14 | -0.013267 | -7.76 |
| w21 | 23 | -0.039797 | -19.586 |
| w22 | 5 | 0.028477 | 2.56 |
| w23 | 45 | -0.107061 | -26.122 |
| w24 | 12 | -0.039416 | -23.076 |

