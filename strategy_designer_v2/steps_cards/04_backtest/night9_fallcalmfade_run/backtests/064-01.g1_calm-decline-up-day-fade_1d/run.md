# Backtest of 064-01.g1_calm-decline-up-day-fade_1d

- Plan: `../../../../03_test_plan/night9_fallcalmfade_run/plans/064-01.g1_calm-decline-up-day-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.078803 | -3.924 |
| w2 | 11 | -0.070713 | -14.492 |
| w3 | 17 | -0.01074 | -7.235 |
| w4 | 4 | 0.032049 | -2.095 |
| w5 | 8 | -0.055235 | -3.22 |
| w6 | 6 | 0.001273 | 1.01 |
| w7 | 24 | -0.086518 | -16.018 |
| w8 | 4 | 0.053163 | 0.178 |
| w9 | 23 | 0.01059 | 8.728 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 8 | 0.024658 | -1.369 |
| w13 | 17 | 0.01613 | 1.165 |
| w14 | 11 | 0.025052 | 15.09 |
| w15 | 0 | None | 0.0 |
| w16 | 4 | -0.055481 | -9.862 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.075154 | -0.856 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.032868 | 0.946 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.054836 | -12.817 |
| w2 | 0 | None | 0.0 |
| w3 | 11 | -0.028086 | -10.115 |
| w4 | 5 | 0.040009 | -5.285 |
| w5 | 9 | 0.013975 | 6.233 |
| w6 | 16 | -0.03259 | -13.06 |
| w7 | 35 | -0.002166 | 21.033 |
| w8 | 0 | None | 0.0 |
| w9 | 26 | 0.001227 | -4.958 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.020562 | 0.394 |
| w13 | 24 | 0.018114 | -9.836 |
| w14 | 9 | 0.110491 | 16.246 |
| w15 | 8 | 0.022898 | 16.113 |
| w16 | 7 | 0.041555 | -13.997 |
| w17 | 6 | -0.097653 | -3.27 |
| w18 | 4 | -0.023089 | -7.24 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | -0.037382 | -9.05 |
| w22 | 7 | 0.049379 | 10.826 |
| w23 | 0 | None | 0.0 |
| w24 | 16 | -0.040018 | 8.587 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 36 | 0.011981 | -21.8 |
| w2 | 5 | 0.043965 | -4.901 |
| w3 | 8 | 0.049479 | 5.069 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | -0.115725 | 0.0 |
| w6 | 16 | 0.153503 | 10.024 |
| w7 | 39 | 0.050034 | 23.148 |
| w8 | 0 | None | 0.0 |
| w9 | 44 | 0.046959 | 11.468 |
| w10 | 7 | 0.033902 | -0.071 |
| w11 | 0 | None | 0.0 |
| w12 | 7 | -0.001511 | 0.577 |
| w13 | 22 | 0.03173 | 0.079 |
| w14 | 18 | 0.094766 | 18.149 |
| w15 | 9 | 0.021528 | 6.629 |
| w16 | 15 | 0.010377 | -18.249 |
| w17 | 10 | -0.032681 | -16.516 |
| w18 | 13 | -0.074961 | -13.702 |
| w19 | 3 | -0.035427 | -1.563 |
| w20 | 12 | 0.026248 | -1.452 |
| w21 | 5 | -0.043466 | -1.631 |
| w22 | 2 | -0.003288 | 8.403 |
| w23 | 6 | -0.060404 | -16.491 |
| w24 | 10 | 0.008599 | 1.969 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.09172 | -17.902 |
| w2 | 10 | -0.006555 | -6.2 |
| w3 | 10 | 0.011421 | -1.794 |
| w4 | 10 | -0.210814 | -15.289 |
| w5 | 8 | -0.040678 | -3.286 |
| w6 | 7 | 0.01728 | -4.837 |
| w7 | 39 | 0.019633 | 0.707 |
| w8 | 2 | 0.11193 | 0.976 |
| w9 | 40 | -0.056103 | 17.292 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 16 | -0.024835 | -9.692 |
| w14 | 14 | 0.088485 | 13.086 |
| w15 | 6 | 0.002917 | 2.171 |
| w16 | 6 | -0.064225 | -25.582 |
| w17 | 0 | None | 0.0 |
| w18 | 6 | -0.074768 | -10.213 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | 0.060284 | -2.433 |
| w21 | 2 | -0.080395 | -11.455 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | 0.079188 | 2.349 |
| w24 | 0 | None | 0.0 |

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
| w1 | 21 | -0.11916 | -22.481 |
| w2 | 4 | 0.025805 | 8.699 |
| w3 | 0 | 0.027062 | 0.0 |
| w4 | 0 | 0.054212 | 0.0 |
| w5 | 0 | -0.027775 | 0.0 |
| w6 | 11 | 0.041289 | -5.126 |
| w8 | 20 | 0.201849 | 14.116 |
| w9 | 22 | -0.048251 | -2.11 |
| w10 | 7 | 0.064442 | -17.246 |
| w11 | 0 | None | 0.0 |
| w12 | 23 | -0.128349 | -10.311 |
| w14 | 20 | 0.016334 | -25.922 |
| w15 | 14 | -0.028694 | 6.923 |
| w16 | 8 | -0.074098 | -13.765 |
| w17 | 11 | -0.018399 | -6.275 |
| w18 | 13 | -0.116975 | -15.115 |
| w19 | 18 | -0.018797 | -18.262 |
| w20 | 12 | 0.11575 | 5.206 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | -0.097322 | 0.0 |
| w23 | 1 | 0.010489 | 0.688 |
| w24 | 28 | -0.029424 | 10.33 |

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
| w1 | 29 | -0.129203 | -18.941 |
| w2 | 17 | -0.1256 | -20.781 |
| w3 | 28 | 0.037482 | 14.293 |
| w4 | 22 | 0.04874 | -3.761 |
| w5 | 16 | -0.002528 | 16.023 |
| w6 | 21 | -0.038754 | -13.664 |
| w7 | 33 | 0.055866 | -9.878 |
| w8 | 16 | -0.002426 | -0.331 |
| w9 | 27 | -0.034552 | -12.868 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | -0.038476 | -4.468 |
| w13 | 20 | -0.04054 | -4.962 |
| w14 | 25 | -0.036414 | 3.053 |
| w15 | 10 | 0.043842 | 18.545 |
| w16 | 0 | None | 0.0 |
| w17 | 17 | -0.05249 | -1.505 |
| w18 | 14 | -0.057924 | -13.854 |
| w19 | 0 | None | 0.0 |
| w20 | 9 | -0.05324 | -9.343 |
| w21 | 5 | -0.105339 | -9.094 |
| w22 | 0 | None | 0.0 |
| w23 | 9 | -0.007954 | 2.513 |
| w24 | 0 | None | 0.0 |

