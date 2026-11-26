# Backtest of 062-02_choppy-calm-below-high-falls_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/062-02_choppy-calm-below-high-falls_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.000958 | 12.006 |
| w2 | 10 | -0.0121 | 25.103 |
| w3 | 23 | 0.062939 | 17.896 |
| w4 | 2 | -0.051089 | -5.632 |
| w5 | 40 | -0.053734 | 3.087 |
| w6 | 16 | 0.063425 | -9.295 |
| w7 | 36 | 0.11366 | 35.522 |
| w8 | 24 | -0.077065 | -21.115 |
| w9 | 16 | 0.229728 | 29.451 |
| w10 | 19 | -0.028787 | -15.35 |
| w11 | 3 | 0.053421 | 0.883 |
| w12 | 1 | 0.114173 | 9.646 |
| w13 | 2 | -0.068882 | -3.587 |
| w14 | 21 | 0.047583 | 29.131 |
| w15 | 0 | None | 0.0 |
| w16 | 8 | 0.099275 | 34.211 |
| w17 | 13 | -0.004589 | -22.729 |
| w18 | 2 | 0.000277 | -6.695 |
| w19 | 0 | None | 0.0 |
| w20 | 12 | 0.139704 | 22.51 |
| w21 | 15 | 0.010588 | -17.281 |
| w22 | 28 | 0.017345 | 5.636 |
| w23 | 24 | -0.097665 | -20.501 |
| w24 | 22 | 0.006677 | 5.798 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.059582 | 2.529 |
| w2 | 5 | 0.19072 | 33.81 |
| w3 | 12 | 0.075908 | 12.304 |
| w4 | 17 | -0.193317 | -31.044 |
| w5 | 54 | -0.011936 | 12.931 |
| w6 | 7 | 0.017188 | -4.284 |
| w7 | 9 | -0.055043 | 6.153 |
| w8 | 12 | 0.095693 | 1.903 |
| w9 | 23 | 0.286 | 26.679 |
| w10 | 7 | -0.008486 | -21.779 |
| w11 | 0 | None | 0.0 |
| w12 | 7 | -0.014893 | -1.604 |
| w13 | 1 | 0.057662 | 2.103 |
| w14 | 7 | 0.101667 | 16.228 |
| w15 | 3 | 0.098339 | 2.498 |
| w16 | 4 | -0.041002 | -12.311 |
| w17 | 7 | -0.002997 | -10.078 |
| w18 | 2 | -0.11682 | -10.022 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | 0.101405 | 14.4 |
| w21 | 13 | 0.014908 | -14.163 |
| w22 | 4 | -0.031367 | -4.216 |
| w23 | 2 | -0.005399 | -2.457 |
| w24 | 6 | 0.109884 | -0.994 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.015581 | 20.19 |
| w2 | 18 | -0.092517 | 5.588 |
| w3 | 21 | -0.033727 | -30.424 |
| w4 | 13 | 0.114832 | -5.365 |
| w5 | 24 | 0.113676 | 24.379 |
| w6 | 31 | -0.154495 | -36.462 |
| w7 | 14 | -0.022957 | 14.669 |
| w8 | 2 | -0.00421 | -1.795 |
| w9 | 5 | -0.065652 | -1.397 |
| w10 | 26 | 0.011226 | -18.575 |
| w11 | 0 | None | 0.0 |
| w12 | 16 | -0.128325 | -20.916 |
| w13 | 2 | -0.038038 | -2.495 |
| w14 | 14 | 0.031409 | 13.598 |
| w15 | 2 | 0.214259 | -8.5 |
| w16 | 6 | 0.016855 | 2.962 |
| w17 | 8 | 0.043533 | -8.122 |
| w18 | 8 | -0.066233 | -8.467 |
| w19 | 12 | 0.02472 | -5.506 |
| w20 | 14 | -0.010815 | 10.614 |
| w21 | 18 | 0.043437 | -4.842 |
| w22 | 0 | None | 0.0 |
| w23 | 24 | -0.056267 | -10.318 |
| w24 | 12 | 0.044083 | 19.764 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.080085 | 19.726 |
| w2 | 2 | -0.11738 | -4.673 |
| w3 | 29 | -0.005787 | 6.02 |
| w4 | 34 | -0.036801 | -20.745 |
| w5 | 47 | -0.073841 | -0.163 |
| w6 | 23 | -0.036895 | -21.035 |
| w7 | 12 | 0.073537 | 16.629 |
| w8 | 15 | -0.128687 | -13.6 |
| w9 | 14 | 0.043214 | 29.818 |
| w10 | 17 | -0.020278 | -13.474 |
| w11 | 0 | None | 0.0 |
| w12 | 28 | -0.127577 | 3.62 |
| w14 | 14 | -0.029358 | -4.04 |
| w15 | 0 | None | 0.0 |
| w16 | 4 | -0.048217 | -1.562 |
| w17 | 2 | -0.133098 | -8.068 |
| w18 | 8 | -0.091693 | -12.92 |
| w19 | 1 | 0.064124 | 19.446 |
| w20 | 9 | 0.193435 | 9.039 |
| w21 | 33 | 0.096116 | 5.474 |
| w22 | 19 | 0.128572 | -8.813 |
| w23 | 15 | 0.052164 | 30.627 |
| w24 | 10 | 0.046333 | -1.51 |

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
| w1 | 22 | -0.053125 | 8.298 |
| w2 | 0 | -0.052737 | 0.0 |
| w3 | 0 | -0.165999 | 0.0 |
| w4 | 0 | -0.176341 | 0.0 |
| w5 | 15 | -0.016731 | 7.394 |
| w6 | 9 | -0.069055 | -24.472 |
| w8 | 35 | 0.019572 | -12.515 |
| w9 | 14 | 0.044842 | 26.13 |
| w10 | 30 | 0.067609 | -8.455 |
| w11 | 0 | None | 0.0 |
| w12 | 28 | -0.060081 | 21.91 |
| w14 | 1 | 0.123197 | 13.963 |
| w15 | 8 | -0.090317 | -35.085 |
| w16 | 1 | None | -0.047 |
| w17 | 12 | -0.022147 | -13.033 |
| w18 | 2 | -0.150991 | -5.467 |
| w19 | 10 | -0.058653 | -0.601 |
| w20 | 13 | -0.002798 | 0.407 |
| w21 | 20 | 0.125377 | -1.266 |
| w22 | 2 | 0.035794 | 0.44 |
| w23 | 35 | -0.056477 | -19.14 |
| w24 | 11 | 0.093444 | 6.522 |

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
| w1 | 7 | 0.043296 | 9.701 |
| w2 | 7 | -0.018198 | 9.955 |
| w3 | 16 | -0.086209 | -1.65 |
| w4 | 28 | -0.148008 | -17.345 |
| w5 | 22 | 0.085897 | 22.576 |
| w6 | 19 | -0.116352 | -36.703 |
| w7 | 2 | -0.095152 | -10.092 |
| w8 | 13 | -0.123123 | -17.804 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | 0.117826 | -0.034 |
| w11 | 0 | None | 0.0 |
| w12 | 9 | -0.012887 | -6.941 |
| w13 | 0 | None | 0.0 |
| w14 | 5 | 0.064668 | 36.081 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 11 | -0.109864 | -30.396 |
| w18 | 8 | -0.034521 | -11.22 |
| w19 | 0 | None | 0.0 |
| w20 | 9 | -0.050706 | 9.745 |
| w21 | 12 | -0.063437 | -6.473 |
| w22 | 2 | 0.042239 | -1.882 |
| w23 | 16 | -0.141638 | -6.23 |
| w24 | 5 | -0.018083 | -17.418 |

