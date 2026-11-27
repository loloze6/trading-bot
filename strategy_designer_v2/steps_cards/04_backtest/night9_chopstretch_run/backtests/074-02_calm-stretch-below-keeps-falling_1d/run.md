# Backtest of 074-02_calm-stretch-below-keeps-falling_1d

- Plan: `../../../../03_test_plan/night9_chopstretch_run/plans/074-02_calm-stretch-below-keeps-falling_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | -0.056888 | 3.248 |
| w2 | 20 | 0.096082 | 52.252 |
| w3 | 20 | 0.086681 | 2.29 |
| w4 | 19 | -0.014526 | -39.134 |
| w5 | 34 | -0.120128 | -15.728 |
| w6 | 8 | 0.040385 | -6.852 |
| w7 | 43 | -0.000439 | 2.995 |
| w8 | 14 | -0.046056 | -12.33 |
| w9 | 30 | -0.164048 | -24.756 |
| w10 | 18 | -0.048881 | -14.702 |
| w11 | 7 | 0.040183 | -5.499 |
| w12 | 30 | 0.000239 | 5.03 |
| w13 | 12 | -0.023902 | -6.48 |
| w14 | 24 | 0.150883 | 62.006 |
| w15 | 2 | -0.074749 | -0.078 |
| w16 | 13 | 0.028261 | 4.139 |
| w17 | 7 | 0.163182 | -2.354 |
| w18 | 0 | -0.007903 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 13 | 0.067186 | 2.487 |
| w21 | 14 | -0.007841 | -20.235 |
| w22 | 18 | -0.066365 | -0.298 |
| w23 | 23 | -0.071428 | -9.939 |
| w24 | 21 | 0.007269 | -7.892 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | 0.020249 | 18.916 |
| w2 | 8 | 0.120927 | 32.762 |
| w3 | 16 | 0.035173 | -9.184 |
| w4 | 13 | -0.039151 | -23.342 |
| w5 | 40 | -0.059302 | -1.064 |
| w6 | 23 | -0.033479 | -23.256 |
| w7 | 35 | -0.017503 | 28.699 |
| w8 | 13 | -0.064279 | -13.257 |
| w9 | 33 | -0.032399 | -2.102 |
| w10 | 12 | -0.061935 | -16.134 |
| w11 | 3 | -0.100648 | -13.721 |
| w12 | 19 | -0.116791 | -3.339 |
| w13 | 13 | 0.185908 | 32.7 |
| w14 | 9 | 0.163384 | 45.894 |
| w15 | 15 | 0.013698 | -4.544 |
| w16 | 2 | -0.05899 | -2.979 |
| w17 | 6 | -0.034004 | -6.224 |
| w18 | 5 | -0.071311 | -4.717 |
| w19 | 0 | None | 0.0 |
| w20 | 11 | 0.085691 | -0.432 |
| w21 | 19 | -0.112437 | -35.261 |
| w22 | 12 | -0.081293 | 18.331 |
| w23 | 16 | -0.043212 | -20.009 |
| w24 | 20 | -0.008369 | -0.045 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | -0.11868 | -2.823 |
| w2 | 12 | 0.002849 | 14.105 |
| w3 | 23 | -0.017985 | -12.657 |
| w4 | 19 | 0.06505 | 3.25 |
| w5 | 23 | 0.087413 | 17.096 |
| w6 | 31 | -0.072795 | -26.748 |
| w7 | 48 | 0.003075 | 31.731 |
| w8 | 0 | -0.049752 | 0.0 |
| w9 | 43 | -0.045445 | 10.1 |
| w10 | 23 | -0.082008 | -26.718 |
| w11 | 3 | -0.090956 | -9.126 |
| w12 | 13 | -0.081471 | -3.527 |
| w13 | 22 | -0.023556 | 8.142 |
| w14 | 22 | 0.09019 | 36.891 |
| w15 | 20 | 0.147652 | 11.008 |
| w16 | 6 | -0.096402 | -5.087 |
| w17 | 6 | -0.175862 | -7.043 |
| w18 | 12 | 0.004453 | -2.988 |
| w19 | 8 | -0.115006 | -28.028 |
| w20 | 16 | 0.030743 | 8.188 |
| w21 | 15 | -0.028434 | -18.922 |
| w22 | 4 | 0.10669 | 3.172 |
| w23 | 20 | -0.068736 | -7.402 |
| w24 | 14 | -0.085084 | -15.525 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.112851 | -12.653 |
| w2 | 9 | -0.106416 | 14.344 |
| w3 | 25 | -0.12194 | -15.448 |
| w4 | 21 | -0.109817 | -12.874 |
| w5 | 39 | -0.035325 | 19.003 |
| w6 | 16 | -0.086188 | -14.675 |
| w7 | 48 | 0.010343 | 18.311 |
| w8 | 15 | -0.074288 | -11.231 |
| w9 | 37 | 0.011728 | 23.042 |
| w10 | 15 | -0.135548 | -14.822 |
| w11 | 2 | -0.03779 | -5.695 |
| w12 | 14 | -0.065713 | 18.155 |
| w14 | 19 | 0.128324 | 54.22 |
| w15 | 14 | 0.021393 | 1.278 |
| w16 | 2 | -0.111649 | -6.868 |
| w17 | 7 | -0.068389 | -6.557 |
| w18 | 3 | -0.037125 | -8.283 |
| w19 | 3 | 0.136904 | 9.121 |
| w20 | 11 | -0.02528 | -9.908 |
| w21 | 23 | 0.047494 | -11.669 |
| w22 | 8 | 0.035029 | -10.072 |
| w23 | 12 | 0.11352 | 33.304 |
| w24 | 2 | -0.015103 | -1.577 |

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
| w1 | 33 | 0.059114 | 26.285 |
| w2 | 6 | -0.011641 | 34.979 |
| w3 | 0 | -0.031238 | 0.0 |
| w4 | 0 | -0.093292 | 0.0 |
| w5 | 13 | 0.036208 | -61.979 |
| w6 | 17 | -0.088004 | -12.065 |
| w8 | 30 | -0.115944 | -22.933 |
| w9 | 36 | 0.026705 | 3.945 |
| w10 | 22 | 0.002543 | -6.563 |
| w11 | 0 | None | 0.0 |
| w12 | 35 | -0.051295 | -6.57 |
| w14 | 20 | 0.046883 | -21.963 |
| w15 | 28 | 0.045169 | -10.654 |
| w16 | 2 | -0.023942 | -4.255 |
| w17 | 17 | -0.009617 | -14.239 |
| w18 | 14 | -0.005834 | -6.239 |
| w19 | 10 | -0.072682 | -3.905 |
| w20 | 26 | 0.035669 | -30.423 |
| w21 | 12 | 0.021749 | -28.757 |
| w22 | 0 | -0.109593 | 0.0 |
| w23 | 33 | -0.076872 | -17.877 |
| w24 | 31 | -0.111068 | 5.65 |

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
| w1 | 29 | 0.092919 | 3.885 |
| w2 | 14 | -0.085316 | -8.397 |
| w3 | 33 | -0.018933 | 22.793 |
| w4 | 25 | -0.063112 | -7.4 |
| w5 | 38 | 0.050079 | 37.981 |
| w6 | 24 | -0.093232 | -22.693 |
| w7 | 40 | -0.104606 | -10.538 |
| w8 | 22 | 0.034424 | -3.127 |
| w9 | 22 | 0.009422 | 4.479 |
| w10 | 19 | -0.123982 | -15.15 |
| w11 | 5 | -0.046995 | -10.955 |
| w12 | 6 | 0.039244 | -8.273 |
| w13 | 15 | 0.092258 | 14.753 |
| w14 | 27 | 0.076742 | 11.23 |
| w15 | 21 | 0.028267 | 0.485 |
| w16 | 0 | None | 0.0 |
| w17 | 10 | -0.031599 | -10.498 |
| w18 | 7 | -0.03997 | -6.193 |
| w19 | 0 | None | 0.0 |
| w20 | 9 | -0.042602 | -13.687 |
| w21 | 14 | -0.068002 | -22.789 |
| w22 | 3 | -0.136683 | -2.326 |
| w23 | 24 | -0.054801 | -7.036 |
| w24 | 0 | None | 0.0 |

