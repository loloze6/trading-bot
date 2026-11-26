# Backtest of 061-01.d2_rising-calm-up-day-continuation_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/061-01.d2_rising-calm-up-day-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.022166 | -3.333 |
| w2 | 0 | -0.001974 | 0.0 |
| w3 | 1 | -0.053688 | -8.013 |
| w4 | 25 | 0.010686 | 37.123 |
| w5 | 18 | -0.152953 | -28.389 |
| w6 | 5 | 0.06998 | 29.088 |
| w7 | 8 | -0.020822 | -11.524 |
| w8 | 8 | 0.140651 | 45.871 |
| w9 | 0 | -0.008497 | 0.0 |
| w10 | 18 | -0.20528 | 12.388 |
| w11 | 6 | -0.04732 | -5.986 |
| w12 | 21 | -0.110055 | -22.333 |
| w13 | 0 | None | 0.0 |
| w14 | 3 | -0.061579 | -10.149 |
| w15 | 7 | 0.159779 | 49.13 |
| w16 | 15 | -0.058114 | -23.028 |
| w17 | 15 | -0.064867 | 45.247 |
| w18 | 13 | 0.043933 | 9.529 |
| w19 | 7 | 0.192384 | 40.973 |
| w20 | 0 | None | 0.0 |
| w21 | 19 | 0.216395 | 46.242 |
| w22 | 9 | -0.069384 | -0.885 |
| w23 | 45 | -0.130169 | 0.662 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.020698 | -9.67 |
| w2 | 3 | -0.12997 | -31.424 |
| w3 | 2 | 0.059716 | -3.124 |
| w4 | 40 | 0.068093 | 26.02 |
| w5 | 7 | -0.215357 | -20.041 |
| w6 | 8 | -0.023012 | 12.804 |
| w7 | 7 | -0.032951 | -8.757 |
| w8 | 17 | -0.139835 | 18.468 |
| w9 | 3 | -0.082091 | -4.3 |
| w10 | 27 | 0.068712 | 97.024 |
| w11 | 9 | -0.014491 | 25.795 |
| w12 | 24 | -0.065421 | -4.795 |
| w13 | 1 | -0.041138 | -16.138 |
| w14 | 1 | 0.004237 | -6.2 |
| w15 | 15 | 0.072964 | 60.797 |
| w16 | 9 | 0.030044 | 35.986 |
| w17 | 4 | 0.099755 | 42.085 |
| w18 | 8 | -0.056157 | 5.532 |
| w19 | 12 | 0.089905 | 77.96 |
| w20 | 6 | -0.002461 | -15.742 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | -0.171812 | -4.131 |
| w23 | 23 | 0.089538 | 76.255 |
| w24 | 3 | -0.011472 | -12.87 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.073567 | -10.164 |
| w2 | 4 | 0.018186 | -2.796 |
| w3 | 12 | 0.07433 | -33.439 |
| w4 | 24 | -0.013193 | 1.681 |
| w5 | 5 | -0.045038 | -4.521 |
| w6 | 20 | -0.124954 | -25.657 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | -0.022825 | 14.359 |
| w9 | 0 | None | 0.0 |
| w10 | 16 | -0.13529 | 30.423 |
| w11 | 8 | 0.044803 | 16.766 |
| w12 | 20 | 0.044907 | -12.773 |
| w13 | 3 | -0.03742 | -5.597 |
| w14 | 0 | None | 0.0 |
| w15 | 12 | 0.14275 | 0.341 |
| w16 | 13 | -0.054795 | -3.365 |
| w17 | 3 | -0.005533 | 11.007 |
| w18 | 4 | -0.00662 | -2.764 |
| w19 | 2 | 0.104732 | 1.43 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | 0.003369 | -1.526 |
| w22 | 0 | None | 0.0 |
| w23 | 22 | -0.023646 | -13.037 |
| w24 | 4 | -0.036499 | -2.008 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.057606 | 5.671 |
| w2 | 7 | 0.032701 | -7.584 |
| w3 | 6 | -0.119123 | -7.775 |
| w4 | 8 | 0.000527 | 12.598 |
| w5 | 12 | -0.057969 | -17.362 |
| w6 | 17 | -0.138953 | 4.714 |
| w7 | 0 | None | 0.0 |
| w8 | 25 | 0.001136 | 29.465 |
| w9 | 0 | None | 0.0 |
| w10 | 28 | -0.081175 | 20.827 |
| w11 | 4 | -0.036124 | 39.392 |
| w12 | 7 | -0.084494 | -13.591 |
| w14 | 8 | 0.003302 | -2.131 |
| w15 | 12 | 0.183896 | 33.538 |
| w16 | 11 | -0.055338 | 18.305 |
| w17 | 21 | -0.100102 | 14.397 |
| w18 | 8 | -0.010765 | 0.488 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | -0.049022 | 8.026 |
| w21 | 10 | 0.244457 | 22.621 |
| w22 | 2 | -0.087743 | -6.114 |
| w23 | 11 | 0.280709 | 46.357 |
| w24 | 4 | -0.08812 | -8.826 |

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
| w1 | 7 | -0.05763 | -9.316 |
| w2 | 0 | -0.025463 | 0.0 |
| w3 | 0 | -0.056852 | 0.0 |
| w4 | 0 | -0.138844 | 0.0 |
| w5 | 3 | -0.010199 | 41.708 |
| w6 | 14 | 0.033757 | 10.185 |
| w8 | 7 | -0.137813 | -10.778 |
| w9 | 6 | -0.122562 | -7.775 |
| w10 | 14 | 0.067695 | 55.453 |
| w11 | 0 | None | 0.0 |
| w12 | 18 | -0.064987 | -18.112 |
| w14 | 12 | 0.018316 | -6.142 |
| w15 | 10 | 0.020933 | -7.581 |
| w16 | 6 | 0.079122 | 0.361 |
| w17 | 6 | 0.210314 | 163.291 |
| w18 | 8 | 0.049101 | 7.433 |
| w19 | 2 | -0.210484 | -5.856 |
| w20 | 0 | None | 0.0 |
| w21 | 5 | 0.152119 | 131.937 |
| w22 | 1 | -0.031635 | -14.375 |
| w23 | 19 | 0.072832 | 6.386 |
| w24 | 5 | 0.030975 | 5.161 |

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
| w1 | 8 | -0.075371 | -15.911 |
| w2 | 2 | -0.08743 | -9.0 |
| w3 | 2 | 0.021634 | -4.164 |
| w4 | 13 | 0.033358 | -13.084 |
| w5 | 3 | -0.028347 | -20.578 |
| w6 | 18 | -0.142343 | -2.379 |
| w7 | 5 | 0.068819 | -5.863 |
| w8 | 10 | 0.104209 | 18.691 |
| w9 | 0 | None | 0.0 |
| w10 | 26 | 0.017695 | 64.841 |
| w11 | 13 | 0.095886 | 34.753 |
| w12 | 12 | 0.013697 | -24.693 |
| w13 | 0 | None | 0.0 |
| w14 | 3 | -0.056664 | -16.805 |
| w15 | 17 | 0.043905 | 8.668 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | -0.062301 | 0.494 |
| w18 | 6 | -0.062588 | -8.137 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | 0.149442 | 13.739 |
| w22 | 3 | -0.076009 | -12.796 |
| w23 | 15 | 0.127446 | 20.179 |
| w24 | 5 | -0.07564 | 50.898 |

