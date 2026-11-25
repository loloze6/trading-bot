# Backtest of 045-01_agitated-wide-low-close-rebound_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/045-01_agitated-wide-low-close-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.004545 | -3.379 |
| w2 | 51 | 0.022567 | -12.763 |
| w3 | 40 | 0.213147 | 21.355 |
| w4 | 23 | 0.078158 | 13.659 |
| w5 | 0 | None | 0.0 |
| w6 | 46 | 0.238366 | 72.66 |
| w7 | 0 | None | 0.0 |
| w8 | 28 | -0.049139 | -1.618 |
| w9 | 26 | 0.006204 | -3.729 |
| w10 | 32 | -0.016487 | 6.309 |
| w11 | 70 | -0.012195 | 20.484 |
| w12 | 33 | 0.159732 | 17.874 |
| w13 | 64 | -0.001504 | -4.179 |
| w14 | 35 | 0.120714 | 2.85 |
| w15 | 74 | -0.131931 | -0.489 |
| w16 | 45 | 0.092022 | 8.811 |
| w17 | 47 | 0.038772 | 23.511 |
| w18 | 73 | 0.02821 | -4.623 |
| w19 | 77 | -0.012656 | 10.226 |
| w20 | 71 | 0.117165 | 12.772 |
| w21 | 37 | 0.063423 | 27.955 |
| w22 | 48 | 0.163276 | 19.152 |
| w23 | 3 | -0.018945 | 0.002 |
| w24 | 52 | 0.015801 | -12.216 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.121694 | -13.716 |
| w2 | 87 | 0.071055 | -10.989 |
| w3 | 41 | 0.272933 | 29.697 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 40 | 0.051384 | 14.52 |
| w7 | 0 | None | 0.0 |
| w8 | 27 | 0.021607 | 3.065 |
| w9 | 20 | 0.05945 | 3.412 |
| w10 | 37 | 0.028633 | 17.92 |
| w11 | 71 | 0.064442 | 55.076 |
| w12 | 19 | 0.06415 | 6.489 |
| w13 | 47 | -0.013952 | -2.862 |
| w14 | 63 | 0.208452 | 18.624 |
| w15 | 45 | 0.032221 | 3.74 |
| w16 | 63 | -0.050317 | -13.169 |
| w17 | 50 | 0.010501 | 9.132 |
| w18 | 67 | 0.014321 | 8.684 |
| w19 | 68 | -0.137076 | -15.982 |
| w20 | 80 | 0.117903 | 1.706 |
| w21 | 57 | 0.052079 | 20.176 |
| w22 | 67 | 0.111528 | -7.824 |
| w23 | 40 | 0.081717 | 33.979 |
| w24 | 38 | 0.028868 | -5.547 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 49 | 0.026689 | -9.868 |
| w3 | 34 | 0.144846 | 20.269 |
| w4 | 26 | 0.02535 | 2.33 |
| w5 | 49 | 0.070219 | 1.949 |
| w6 | 4 | 0.163573 | 7.709 |
| w7 | 0 | None | 0.0 |
| w8 | 80 | 0.077858 | 34.173 |
| w9 | 0 | None | 0.0 |
| w10 | 17 | 0.041671 | 4.312 |
| w11 | 84 | -0.127966 | -0.57 |
| w12 | 36 | -0.067078 | -10.404 |
| w13 | 41 | 0.000798 | -4.334 |
| w14 | 42 | 0.121522 | 4.146 |
| w15 | 52 | 0.104498 | 10.688 |
| w16 | 39 | 0.039641 | -1.282 |
| w17 | 64 | 0.041236 | 18.516 |
| w18 | 58 | 0.088659 | 8.607 |
| w19 | 61 | 0.097614 | 23.878 |
| w20 | 56 | 0.120074 | 4.304 |
| w21 | 65 | -0.027843 | 10.463 |
| w22 | 89 | 0.011749 | -4.457 |
| w23 | 19 | 0.071255 | 7.421 |
| w24 | 40 | -0.05949 | -12.101 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | -0.081386 | -17.946 |
| w2 | 51 | -0.052551 | -13.523 |
| w3 | 24 | 0.109585 | 9.517 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 21 | 0.026098 | 2.623 |
| w7 | 0 | None | 0.0 |
| w8 | 17 | 0.00044 | 0.058 |
| w9 | 4 | 0.00128 | -1.032 |
| w10 | 9 | 0.081016 | 6.571 |
| w11 | 72 | 0.083355 | 53.507 |
| w12 | 25 | 0.011794 | -3.388 |
| w14 | 48 | 0.097042 | -1.292 |
| w15 | 48 | -0.00755 | -1.585 |
| w16 | 51 | 0.015771 | -3.372 |
| w17 | 46 | -0.067573 | -7.81 |
| w18 | 68 | 0.178351 | 23.476 |
| w19 | 87 | 0.234881 | 18.271 |
| w20 | 64 | 0.228796 | 44.992 |
| w21 | 40 | 0.035476 | 2.875 |
| w22 | 63 | 0.047372 | 15.933 |
| w23 | 51 | -0.154981 | -20.903 |
| w24 | 74 | -0.079589 | 3.14 |

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
| w1 | 9 | 0.0066 | -1.955 |
| w2 | 23 | -0.062327 | -16.353 |
| w3 | 0 | 0.075177 | 0.0 |
| w4 | 0 | -0.004531 | 0.0 |
| w5 | 40 | -0.092526 | -4.471 |
| w6 | 30 | -0.028206 | -1.223 |
| w8 | 6 | 0.061169 | 1.776 |
| w9 | 24 | 0.046953 | 1.198 |
| w10 | 15 | 0.027523 | 3.558 |
| w11 | 91 | 0.026842 | 61.888 |
| w12 | 4 | 0.002139 | -0.471 |
| w14 | 32 | 0.152117 | 21.591 |
| w15 | 37 | 0.092295 | 8.822 |
| w16 | 76 | 0.00191 | -1.739 |
| w17 | 48 | 0.05001 | 15.122 |
| w18 | 49 | 0.080396 | 4.739 |
| w19 | 53 | -0.056981 | -12.608 |
| w20 | 48 | 0.016995 | 10.504 |
| w21 | 58 | 0.062658 | 73.227 |
| w22 | 87 | 0.005213 | -1.757 |
| w23 | 14 | 0.086192 | 9.442 |
| w24 | 24 | 0.022062 | -2.932 |

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
| w1 | 29 | 0.219709 | 27.692 |
| w2 | 50 | -0.012697 | -12.224 |
| w3 | 20 | 0.236892 | 14.465 |
| w4 | 12 | -0.001536 | -0.151 |
| w5 | 34 | 0.158642 | 16.157 |
| w6 | 16 | 0.028466 | 2.436 |
| w7 | 11 | -0.06397 | -6.627 |
| w8 | 16 | 0.082382 | 2.833 |
| w9 | 38 | 0.068822 | -0.595 |
| w10 | 35 | -0.133514 | -12.131 |
| w11 | 73 | -0.02336 | 31.677 |
| w12 | 51 | 0.027345 | 4.5 |
| w13 | 52 | 0.050069 | 3.757 |
| w14 | 38 | 0.115286 | 4.746 |
| w15 | 46 | 0.043422 | 0.249 |
| w16 | 88 | 0.04053 | 39.739 |
| w17 | 58 | -0.058041 | -18.999 |
| w18 | 64 | 0.157177 | 24.954 |
| w19 | 91 | 0.143731 | 6.598 |
| w20 | 69 | -0.065423 | -1.302 |
| w21 | 69 | -0.081586 | 4.678 |
| w22 | 86 | -0.04365 | -18.781 |
| w23 | 25 | -0.093569 | -9.124 |
| w24 | 73 | 0.039421 | 70.796 |

