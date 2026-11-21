# Backtest of 021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer_1d

- Plan: `../../../../03_test_plan/night3_ichimoku_run/plans/021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.031919 | -8.65 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.026227 | -16.51 |
| w4 | 3 | 0.183276 | 68.974 |
| w5 | 2 | -0.012151 | -1.583 |
| w6 | 2 | -0.093854 | 41.119 |
| w7 | 2 | 0.258022 | -9.506 |
| w8 | 2 | 0.004509 | 3.482 |
| w9 | 0 | None | 0.0 |
| w10 | 1 | 0.019459 | 37.984 |
| w11 | 1 | None | -0.02 |
| w12 | 0 | None | 0.0 |
| w13 | 3 | -0.086846 | 2.114 |
| w14 | 2 | 0.045823 | -18.75 |
| w15 | 2 | -0.077425 | -4.935 |
| w16 | 4 | -0.019589 | 11.384 |
| w17 | 1 | 0.041255 | 68.823 |
| w18 | 2 | -0.033973 | 5.563 |
| w19 | 2 | -0.03109 | 27.61 |
| w20 | 5 | -0.013754 | -11.429 |
| w21 | 1 | 0.018461 | 8.162 |
| w22 | 3 | -0.095474 | -15.862 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | -0.003053 | -14.569 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.063655 | -6.066 |
| w2 | 2 | 0.001307 | -1.664 |
| w3 | 1 | -0.019937 | -11.076 |
| w4 | 3 | 0.122185 | 50.249 |
| w5 | 2 | -0.042673 | -5.093 |
| w6 | 3 | -0.124218 | 30.128 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.050895 | 11.941 |
| w9 | 1 | -0.062083 | -14.935 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.034337 | 11.692 |
| w13 | 1 | -0.178588 | -2.467 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 4 | 0.002911 | 25.975 |
| w17 | 2 | -0.032755 | 26.648 |
| w18 | 4 | 0.053855 | 14.777 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | 0.055894 | -18.309 |
| w21 | 4 | 0.131441 | 54.128 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.120412 | 3.911 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.00027 | -12.618 |
| w2 | 2 | -0.069534 | -4.802 |
| w3 | 7 | 0.08354 | 5.978 |
| w4 | 2 | -0.00473 | -2.104 |
| w5 | 4 | -0.031149 | -5.525 |
| w6 | 2 | -0.034949 | 5.042 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.064737 | 24.797 |
| w9 | 0 | None | 0.0 |
| w10 | 6 | -0.056464 | 35.907 |
| w11 | 2 | 0.002585 | 15.536 |
| w12 | 2 | -0.086306 | -0.527 |
| w13 | 2 | 0.04115 | -4.978 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.079924 | 14.354 |
| w16 | 2 | -0.056801 | 25.688 |
| w17 | 2 | 0.102592 | 28.646 |
| w18 | 2 | -0.008778 | 1.94 |
| w19 | 3 | -0.016323 | 34.716 |
| w20 | 1 | None | -0.069 |
| w21 | 3 | 0.036946 | 11.307 |
| w22 | 4 | 0.080465 | -4.77 |
| w23 | 2 | 0.019993 | 3.099 |
| w24 | 3 | 0.076887 | -18.894 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.100954 | -15.611 |
| w2 | 2 | 0.010454 | -3.169 |
| w3 | 3 | -0.038102 | -9.248 |
| w4 | 3 | -0.017991 | -2.604 |
| w5 | 2 | 0.227274 | 1.833 |
| w6 | 2 | 0.11391 | 6.144 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.019711 | 2.259 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.022843 | 14.313 |
| w12 | 2 | -0.088633 | -21.092 |
| w14 | 2 | 0.029583 | -7.622 |
| w15 | 2 | -0.029801 | 16.345 |
| w16 | 4 | -0.015288 | 19.705 |
| w17 | 2 | -0.026099 | 13.151 |
| w18 | 2 | 0.046335 | 7.941 |
| w19 | 2 | -0.041062 | -8.955 |
| w20 | 4 | 0.018964 | 18.778 |
| w21 | 2 | -0.045234 | 19.199 |
| w22 | 2 | 0.008404 | 19.55 |
| w23 | 1 | -0.082705 | -17.998 |
| w24 | 4 | -0.013504 | 6.98 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=481. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 21 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.035765 | -16.22 |
| w2 | 0 | -0.041414 | 0.0 |
| w3 | 0 | -0.10274 | 0.0 |
| w4 | 0 | -0.192366 | 0.0 |
| w5 | 0 | 0.012558 | 0.0 |
| w6 | 3 | -0.035346 | 11.972 |
| w8 | 2 | -0.083755 | -8.171 |
| w9 | 2 | -0.080404 | -9.855 |
| w10 | 3 | 0.020536 | 23.539 |
| w11 | 6 | -0.026645 | 48.377 |
| w12 | 3 | -0.01259 | -24.998 |
| w15 | 2 | 0.240155 | -6.27 |
| w16 | 2 | -0.005417 | 2.313 |
| w17 | 1 | 0.009283 | -2.532 |
| w18 | 2 | -0.056127 | 26.796 |
| w19 | 2 | -0.043235 | 1.137 |
| w20 | 3 | -0.01645 | 4.979 |
| w21 | 3 | 0.070215 | 211.086 |
| w22 | 1 | -0.31663 | -3.929 |
| w23 | 3 | 0.114757 | 25.723 |
| w24 | 3 | -0.141238 | -29.19 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=481. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=481. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 470 warm-up bars -- required_bars=481. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.106036 | 6.868 |
| w2 | 1 | -0.018687 | -9.401 |
| w3 | 1 | -0.029387 | -11.454 |
| w4 | 5 | 0.068179 | -11.117 |
| w5 | 2 | -0.083629 | -1.913 |
| w6 | 4 | -0.015789 | 11.908 |
| w7 | 2 | 0.221574 | -11.906 |
| w8 | 2 | -0.017336 | 11.561 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.015115 | 5.253 |
| w11 | 4 | 0.184504 | 55.523 |
| w12 | 2 | 0.052503 | 48.492 |
| w14 | 2 | -0.011498 | -63.055 |
| w15 | 2 | -0.057429 | 12.801 |
| w16 | 2 | 0.015583 | 29.64 |
| w17 | 2 | -0.079221 | -4.386 |
| w18 | 2 | -0.03322 | 3.373 |
| w19 | 2 | -0.019806 | -0.287 |
| w20 | 3 | 0.047045 | -0.715 |
| w21 | 2 | -0.086164 | 4.874 |
| w22 | 1 | -0.047379 | -3.655 |
| w23 | 5 | -0.029844 | 4.585 |
| w24 | 6 | -0.013741 | 203.895 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=481. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

