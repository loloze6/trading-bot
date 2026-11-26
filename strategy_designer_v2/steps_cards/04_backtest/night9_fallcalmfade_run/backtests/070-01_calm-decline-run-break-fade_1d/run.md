# Backtest of 070-01_calm-decline-run-break-fade_1d

- Plan: `../../../../03_test_plan/night9_fallcalmfade_run/plans/070-01_calm-decline-run-break-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.149052 | -11.398 |
| w2 | 7 | 0.035226 | 3.086 |
| w3 | 11 | -0.037643 | -2.191 |
| w4 | 2 | 0.014142 | -0.179 |
| w5 | 5 | 0.018509 | 0.681 |
| w6 | 4 | 0.00395 | -1.806 |
| w7 | 15 | 0.082969 | 5.887 |
| w8 | 3 | 0.024361 | 0.258 |
| w9 | 16 | 0.009462 | 1.426 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 7 | -0.037987 | -2.456 |
| w13 | 8 | 0.098465 | 4.913 |
| w14 | 6 | 0.160647 | 22.37 |
| w15 | 0 | None | 0.0 |
| w16 | 3 | 0.017493 | 0.32 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 1 | -0.075154 | -0.688 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.013746 | 0.331 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.018747 | 1.651 |
| w2 | 0 | None | 0.0 |
| w3 | 10 | -0.018574 | -0.922 |
| w4 | 2 | -0.00908 | -0.353 |
| w5 | 4 | -0.117592 | -3.201 |
| w6 | 8 | 0.006045 | -2.787 |
| w7 | 20 | 0.165365 | 16.951 |
| w8 | 0 | None | 0.0 |
| w9 | 15 | 0.026701 | 2.907 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.020562 | 0.712 |
| w13 | 14 | 0.002167 | -1.43 |
| w14 | 6 | 0.07284 | 8.826 |
| w15 | 6 | 0.031394 | 1.168 |
| w16 | 4 | 0.056579 | 2.707 |
| w17 | 3 | -0.073486 | -4.998 |
| w18 | 1 | -0.011453 | -0.463 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 1 | -0.057165 | -0.494 |
| w22 | 5 | -0.075969 | -2.909 |
| w23 | 0 | None | 0.0 |
| w24 | 11 | 0.046686 | 3.831 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.028767 | 2.045 |
| w2 | 2 | 0.0223 | 0.54 |
| w3 | 6 | 0.075256 | 3.209 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 11 | 0.111159 | 3.177 |
| w7 | 29 | 0.103823 | 15.163 |
| w8 | 0 | None | 0.0 |
| w9 | 32 | -0.030188 | -2.688 |
| w10 | 4 | -0.065634 | -1.015 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | -0.004094 | -0.296 |
| w13 | 15 | -0.062321 | -5.29 |
| w14 | 11 | 0.151963 | 15.913 |
| w15 | 5 | 0.002152 | -0.298 |
| w16 | 7 | 0.005032 | 0.334 |
| w17 | 5 | -0.005552 | -2.696 |
| w18 | 3 | -0.019211 | -0.894 |
| w19 | 0 | None | 0.0 |
| w20 | 8 | -0.023933 | -1.494 |
| w21 | 1 | -0.023316 | -0.949 |
| w22 | 1 | -0.027119 | -0.253 |
| w23 | 2 | 0.027049 | -0.04 |
| w24 | 6 | 0.024998 | 1.293 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.036057 | 1.716 |
| w2 | 7 | 0.042138 | 1.659 |
| w3 | 5 | -0.034096 | -2.317 |
| w4 | 6 | -0.264904 | -11.891 |
| w5 | 4 | -0.11096 | -4.775 |
| w6 | 3 | -0.016894 | -1.795 |
| w7 | 31 | 0.24576 | 24.773 |
| w8 | 4 | 0.077326 | 0.733 |
| w9 | 24 | -0.058986 | -3.725 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 8 | -0.118389 | -6.194 |
| w14 | 7 | 0.015481 | 1.59 |
| w15 | 4 | 0.011648 | -0.059 |
| w16 | 4 | -0.036424 | -1.826 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | -0.007367 | -0.213 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.067367 | 1.36 |
| w21 | 2 | 0.01407 | 0.154 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | 0.040886 | 0.974 |
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
| w1 | 14 | 0.017018 | 1.878 |
| w2 | 3 | -0.113297 | 1.572 |
| w3 | 0 | 0.007425 | 0.0 |
| w4 | 0 | 0.069603 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 8 | -0.000744 | -1.494 |
| w8 | 15 | 0.069982 | 2.518 |
| w9 | 16 | 0.040635 | 3.024 |
| w10 | 4 | 0.038688 | 0.286 |
| w11 | 0 | None | 0.0 |
| w12 | 12 | -0.03692 | -1.207 |
| w14 | 13 | 0.010148 | -2.966 |
| w15 | 10 | -0.042063 | -3.604 |
| w16 | 3 | -0.052714 | -2.39 |
| w17 | 5 | -0.014744 | -3.157 |
| w18 | 8 | 0.057144 | 2.203 |
| w19 | 11 | 0.041211 | 2.819 |
| w20 | 11 | 0.103021 | 7.335 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | -0.097322 | -0.71 |
| w23 | 1 | 0.010489 | 0.029 |
| w24 | 15 | -0.081045 | -5.093 |

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
| w1 | 16 | -0.044491 | -4.563 |
| w2 | 6 | -0.025282 | -1.091 |
| w3 | 17 | 0.074822 | 8.102 |
| w4 | 11 | -0.038668 | -3.411 |
| w5 | 10 | 0.064479 | 6.741 |
| w6 | 9 | -0.041577 | -4.947 |
| w7 | 22 | 0.030373 | 2.894 |
| w8 | 12 | -0.004072 | -1.754 |
| w9 | 15 | 0.010465 | 2.195 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.028359 | -1.257 |
| w13 | 13 | 0.000624 | -0.191 |
| w14 | 15 | 0.016651 | 4.897 |
| w15 | 6 | 0.068177 | 2.147 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | -0.01218 | -1.131 |
| w18 | 2 | -0.022006 | -0.778 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | -0.004976 | -1.798 |
| w21 | 2 | -0.10477 | -8.906 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | -0.066613 | -5.966 |
| w24 | 0 | None | 0.0 |

