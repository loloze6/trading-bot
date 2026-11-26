# Backtest of 038-01_calm-scaled-weekly-rise-continues_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/038-01_calm-scaled-weekly-rise-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.019472 | -4.897 |
| w2 | 17 | -0.020394 | -10.135 |
| w3 | 22 | -0.017922 | -27.867 |
| w4 | 24 | 0.082152 | 66.272 |
| w5 | 28 | -0.021598 | -19.393 |
| w6 | 20 | 0.082951 | 25.775 |
| w7 | 30 | 0.129862 | 2.302 |
| w8 | 25 | 0.08331 | 40.858 |
| w9 | 19 | -0.096503 | -14.854 |
| w10 | 27 | 0.098459 | 23.637 |
| w11 | 11 | -0.083868 | -8.237 |
| w12 | 28 | -0.304099 | -33.002 |
| w13 | 12 | 0.006085 | 2.86 |
| w14 | 26 | -0.01799 | -17.878 |
| w15 | 2 | 0.19574 | 58.739 |
| w16 | 28 | 0.033051 | 7.282 |
| w17 | 31 | -0.035551 | 35.955 |
| w18 | 18 | 0.068214 | 11.699 |
| w19 | 7 | 0.164014 | 34.865 |
| w20 | 6 | 0.150816 | 5.454 |
| w21 | 29 | -0.003404 | 21.941 |
| w22 | 13 | -0.022324 | -9.053 |
| w23 | 39 | 0.012966 | 6.704 |
| w24 | 18 | 0.087308 | 7.279 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | 0.116476 | 1.93 |
| w2 | 1 | -0.10274 | -4.498 |
| w3 | 25 | 0.022524 | -15.469 |
| w4 | 41 | 0.037043 | 29.324 |
| w5 | 27 | -0.165775 | -31.218 |
| w6 | 21 | 0.077364 | 29.254 |
| w7 | 22 | 0.006246 | -17.872 |
| w8 | 22 | 0.021535 | 8.161 |
| w9 | 22 | 0.016041 | 3.739 |
| w10 | 25 | 0.141522 | 68.56 |
| w11 | 12 | -0.05818 | 2.427 |
| w12 | 31 | -0.168241 | -5.537 |
| w13 | 18 | 0.070144 | 12.226 |
| w14 | 11 | 0.001777 | -13.904 |
| w15 | 23 | 0.182429 | 46.614 |
| w16 | 16 | 0.061406 | 66.304 |
| w17 | 22 | 0.015629 | 20.824 |
| w18 | 15 | 0.08701 | 30.366 |
| w19 | 13 | 0.215455 | 69.471 |
| w20 | 7 | 0.171571 | 3.113 |
| w21 | 10 | -0.043496 | -3.955 |
| w22 | 6 | -0.189681 | -20.165 |
| w23 | 27 | 0.042507 | 53.664 |
| w24 | 20 | 0.023116 | -5.971 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | 0.016675 | -8.126 |
| w2 | 16 | -0.060524 | -18.904 |
| w3 | 27 | -0.130202 | -16.11 |
| w4 | 34 | -0.058826 | -1.506 |
| w5 | 10 | 0.025944 | -5.158 |
| w6 | 40 | -0.045856 | 1.597 |
| w7 | 28 | -0.005627 | -20.588 |
| w8 | 13 | 0.059969 | 24.169 |
| w9 | 31 | -0.030427 | -9.714 |
| w10 | 30 | 0.04101 | 32.927 |
| w11 | 7 | 0.064097 | 12.499 |
| w12 | 23 | -0.010736 | 4.66 |
| w13 | 18 | 0.005157 | -0.406 |
| w14 | 17 | -0.026764 | -21.508 |
| w15 | 13 | -0.027708 | 2.689 |
| w16 | 26 | 0.041125 | 25.724 |
| w17 | 15 | -0.054642 | 3.93 |
| w18 | 20 | 0.066255 | 16.351 |
| w19 | 13 | 0.06454 | 6.437 |
| w20 | 12 | -0.110818 | -28.612 |
| w21 | 20 | -0.019422 | -5.245 |
| w22 | 0 | None | 0.0 |
| w23 | 28 | 0.060857 | 36.451 |
| w24 | 16 | -0.04389 | -13.931 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.175195 | -15.021 |
| w2 | 17 | -0.023758 | -1.767 |
| w3 | 38 | -0.152942 | -23.219 |
| w4 | 38 | -0.01053 | -0.535 |
| w5 | 22 | 0.177157 | 11.748 |
| w6 | 37 | -0.019681 | 12.572 |
| w7 | 22 | -0.023628 | -12.039 |
| w8 | 27 | -0.003952 | 10.772 |
| w9 | 33 | -0.03804 | -15.846 |
| w10 | 41 | -0.001743 | 32.749 |
| w11 | 8 | 0.038463 | 21.95 |
| w12 | 25 | -0.149727 | -24.0 |
| w14 | 13 | -0.010086 | -7.274 |
| w15 | 19 | 0.134564 | 16.846 |
| w16 | 21 | 0.028442 | 34.771 |
| w17 | 24 | -0.027769 | 20.962 |
| w18 | 17 | 0.035973 | 8.145 |
| w19 | 0 | None | 0.0 |
| w20 | 8 | -0.042034 | 10.991 |
| w21 | 19 | 0.088386 | 3.164 |
| w22 | 20 | 0.050701 | 24.632 |
| w23 | 15 | 0.095208 | 18.884 |
| w24 | 11 | -0.047038 | 3.55 |

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
| w1 | 26 | 0.085878 | 2.248 |
| w2 | 0 | 0.031794 | 0.0 |
| w3 | 0 | -0.11937 | 0.0 |
| w4 | 0 | -0.053931 | 0.0 |
| w5 | 4 | -0.004466 | -9.938 |
| w6 | 24 | 0.089155 | 40.761 |
| w8 | 23 | -0.010486 | 3.858 |
| w9 | 21 | -0.113075 | -17.048 |
| w10 | 26 | 0.182243 | 54.094 |
| w11 | 0 | None | 0.0 |
| w12 | 27 | -0.062827 | -8.452 |
| w14 | 12 | 0.158479 | 55.172 |
| w15 | 27 | 0.145551 | 19.18 |
| w16 | 14 | 0.03154 | 12.462 |
| w17 | 25 | 0.145642 | 94.624 |
| w18 | 12 | 0.159366 | 39.592 |
| w19 | 14 | 0.027046 | 2.549 |
| w20 | 14 | -0.068989 | -14.107 |
| w21 | 18 | 0.01829 | 29.322 |
| w22 | 5 | -0.013603 | -5.364 |
| w23 | 23 | 0.137683 | 49.441 |
| w24 | 27 | -0.091006 | -18.498 |

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
| w1 | 17 | 0.053545 | -5.328 |
| w2 | 13 | -0.008782 | -1.919 |
| w3 | 18 | -0.071508 | -14.54 |
| w4 | 31 | -0.1167 | -18.762 |
| w5 | 17 | -0.141668 | -20.937 |
| w6 | 51 | -0.043996 | -0.588 |
| w7 | 26 | -0.043521 | -12.086 |
| w8 | 31 | 0.104649 | 25.769 |
| w9 | 21 | -0.031812 | -8.129 |
| w10 | 24 | 0.064358 | 41.028 |
| w11 | 10 | 0.024458 | 17.435 |
| w12 | 25 | -0.130519 | -23.79 |
| w13 | 10 | 0.092641 | 11.325 |
| w14 | 15 | 0.0509 | -8.872 |
| w15 | 22 | 0.050671 | 19.868 |
| w16 | 0 | None | 0.0 |
| w17 | 19 | -0.010726 | 3.718 |
| w18 | 22 | 0.067608 | 14.086 |
| w19 | 0 | None | 0.0 |
| w20 | 12 | -0.018783 | 2.82 |
| w21 | 9 | -0.048975 | -3.177 |
| w22 | 5 | -0.000678 | 2.062 |
| w23 | 25 | -0.064981 | -1.533 |
| w24 | 9 | -0.06948 | 44.202 |

